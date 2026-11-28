import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import snowflake.connector
from pathlib import Path
from html import escape

# =====================================================
# ATMOSYNC | PREMIUM ANALYTICS DASHBOARD
# Preserves the existing CSV + Snowflake/dbt data flow.
# =====================================================

st.set_page_config(
    page_title="AtmoSync | Cold Chain Intelligence",
    page_icon="🌡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------- THEME --------------------
NAVY = "#172B4D"
BLUE = "#3979D8"
CYAN = "#36B9C7"
MUTED = "#718198"
GRID = "rgba(115, 137, 166, 0.16)"
TEMP_MIN, TEMP_MAX = 2.0, 8.0
HUM_MIN, HUM_MAX = 80.0, 95.0
VIB_MIN, VIB_MAX = 0.1, 0.8

css_path = Path(__file__).parent / "assets" / "style.css"
if css_path.exists():
    st.markdown(
        f"<style>{css_path.read_text(encoding='utf-8')}</style>",
        unsafe_allow_html=True
    )

# -------------------- REUSABLE UI --------------------
def section_heading(icon, title, subtitle=None):
    sub = f'<div class="section-subtitle">{escape(str(subtitle))}</div>' if subtitle else ""
    st.markdown(
        f"""<div class="section-heading">
          <div class="section-icon">{icon}</div>
          <div><div class="section-title">{escape(str(title))}</div>{sub}</div>
        </div>""",
        unsafe_allow_html=True
    )

def kpi_card(icon, label, value, note="", accent="blue"):
    st.markdown(
        f"""<div class="kpi-card accent-{accent}">
          <div class="kpi-head">
            <div class="kpi-icon">{icon}</div>
            <div class="kpi-label">{escape(str(label))}</div>
          </div>
          <div class="kpi-value">{escape(str(value))}</div>
          <div class="kpi-note">{escape(str(note))}</div>
        </div>""",
        unsafe_allow_html=True
    )

def hero(title, subtitle, description, eyebrow="COLD CHAIN INTELLIGENCE"):
    st.markdown(
        f"""<div class="hero">
          <div class="hero-orb orb-one"></div><div class="hero-orb orb-two"></div>
          <div class="hero-content">
            <div class="hero-topline">
              <span class="hero-eyebrow">{escape(eyebrow)}</span>
              <span class="hero-chip"><span class="live-dot"></span> PROTOTYPE ANALYTICS</span>
            </div>
            <h1>{escape(title)}</h1>
            <h3>{escape(subtitle)}</h3>
            <p>{escape(description)}</p>
          </div>
        </div>""",
        unsafe_allow_html=True
    )

def status_card(container_id, status, readings):
    if status == "CHECK REQUIRED":
        cls, icon, label = "status-warning", "⚠", "Attention required"
    elif status == "INVALID":
        cls, icon, label = "status-invalid", "!", "Invalid sensor data"
    else:
        cls, icon, label = "status-success", "✓", "Within configured limits"
    st.markdown(
        f"""<div class="container-card">
          <div class="container-card-top">
            <span class="container-label">CONTAINER</span>
            <span class="{cls}">{icon} {escape(status)}</span>
          </div>
          <div class="container-id">{escape(str(container_id))}</div>
          <div class="container-card-bottom">
            <span>{label}</span><strong>{int(readings)} readings</strong>
          </div>
        </div>""",
        unsafe_allow_html=True
    )

def chart_layout(fig, height=340):
    fig.update_layout(
        height=height,
        margin=dict(l=8, r=8, t=18, b=8),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, Segoe UI, sans-serif", color="#52657E", size=11),
        legend=dict(orientation="h", y=1.12, x=0, bgcolor="rgba(0,0,0,0)"),
        hoverlabel=dict(bgcolor="#172B4D", font_color="white"),
    )
    fig.update_xaxes(showgrid=False, linecolor=GRID, zeroline=False)
    fig.update_yaxes(showgrid=True, gridcolor=GRID, zeroline=False)
    return fig

# -------------------- DATA --------------------
def check_risk(row):
    issues = []
    if not TEMP_MIN <= row["temperature_c"] <= TEMP_MAX:
        issues.append("Temperature out of range")
    if not HUM_MIN <= row["humidity_percent"] <= HUM_MAX:
        issues.append("Humidity out of range")
    if not VIB_MIN <= row["vibration_mm_s"] <= VIB_MAX:
        issues.append("Vibration out of range")
    return ", ".join(issues) if issues else "Normal"

@st.cache_data(show_spinner=False)
def load_sensor_data(file_mtime):
    data_path = Path(__file__).resolve().parent.parent / "sensor_readings.csv"
    if not data_path.exists():
        return pd.DataFrame(), f"Sensor data file not found: {data_path}. Run main.py first."
    try:
        data = pd.read_csv(data_path)
        required = [
            "timestamp", "container_id", "temperature_c",
            "humidity_percent", "vibration_mm_s", "sensor_status"
        ]
        missing = [col for col in required if col not in data.columns]
        if missing:
            return pd.DataFrame(), "Sensor CSV is missing columns: " + ", ".join(missing)
        if data.empty:
            return pd.DataFrame(), "Sensor data file is empty."

        for col in ["temperature_c", "humidity_percent", "vibration_mm_s"]:
            data[col] = pd.to_numeric(data[col], errors="coerce")
        data["timestamp"] = pd.to_datetime(data["timestamp"], errors="coerce")
        data = data.dropna(subset=[
            "timestamp", "container_id", "temperature_c",
            "humidity_percent", "vibration_mm_s"
        ]).copy()
        if data.empty:
            return pd.DataFrame(), "No valid sensor readings are available."

        data["container_id"] = data["container_id"].astype(str)
        data["Risk Details"] = data.apply(check_risk, axis=1)
        data["Calculated Status"] = data["Risk Details"].map(
            lambda value: "CHECK REQUIRED" if value != "Normal" else "VALID"
        )
        return data, None
    except Exception as exc:
        return pd.DataFrame(), f"Unable to read sensor CSV: {exc}"

@st.cache_data(ttl=120, show_spinner=False)
def load_market_data():
    try:
        sf = st.secrets["snowflake"]
        params = {
            "account": sf["account"],
            "user": sf["user"],
            "password": sf["password"],
            "warehouse": sf["warehouse"],
            "database": sf.get("database", "ATMOSYNC_DB"),
            "schema": sf.get("schema", "ANALYTICS")
        }
        if sf.get("role"):
            params["role"] = sf["role"]
        conn = snowflake.connector.connect(**params)
        query = """
            SELECT CONTAINER_ID, RISK_LEVEL, AVG_TEMPERATURE, AVG_HUMIDITY,
                   CHECK_REQUIRED_COUNT, RECOMMENDED_MARKET, COMMODITY,
                   PRICE_PER_KG, DISTANCE_KM, RECOMMENDATION
            FROM ATMOSYNC_DB.ANALYTICS.SPOILAGE_ARBITRAGE
            ORDER BY CONTAINER_ID
        """
        try:
            result = conn.cursor().execute(query).fetch_pandas_all()
        finally:
            conn.close()
        return result, None
    except Exception as exc:
        return pd.DataFrame(), str(exc)

def safe_number(series):
    return pd.to_numeric(series, errors="coerce")

# -------------------- SIDEBAR --------------------
with st.sidebar:
    st.markdown(
        """<div class="sidebar-brand">
          <div class="brand-mark">A<span>°</span></div>
          <div><div class="brand-name">AtmoSync</div>
          <div class="brand-caption">COLD CHAIN INTELLIGENCE</div></div>
        </div>""",
        unsafe_allow_html=True
    )
    st.markdown('<div class="sidebar-kicker">WORKSPACE</div>', unsafe_allow_html=True)
    page = st.radio(
        "Navigation",
        ["Overview & Analytics", "Container Monitoring", "Market Intelligence"],
        format_func=lambda x: {
            "Overview & Analytics": "◫   Overview & Analytics",
            "Container Monitoring": "◉   Container Monitoring",
            "Market Intelligence": "↗   Market Intelligence"
        }[x],
        label_visibility="collapsed",
        key="dashboard_page"
    )
    st.markdown('<div class="sidebar-divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-kicker">SENSOR THRESHOLDS</div>', unsafe_allow_html=True)
    st.markdown(
        """<div class="threshold-row"><span>🌡 Temperature</span><strong>2–8 °C</strong></div>
        <div class="threshold-row"><span>💧 Humidity</span><strong>80–95%</strong></div>
        <div class="threshold-row"><span>〰 Vibration</span><strong>0.1–0.8 mm/s</strong></div>""",
        unsafe_allow_html=True
    )
    st.markdown('<div class="sidebar-divider"></div>', unsafe_allow_html=True)
    st.markdown(
        """<div class="sidebar-note"><span class="note-dot"></span>
        <div><strong>Prototype environment</strong><small>Illustrative monitoring thresholds and data</small></div></div>""",
        unsafe_allow_html=True
    )

# -------------------- APP HEADER --------------------
hero(
    "AtmoSync",
    "Smart Micro-Climate & Arbitrage Analytics",
    "A unified view of container conditions, cold-chain risk signals and potential market opportunities."
)

left, right = st.columns([5, 1])
with left:
    st.markdown('<div class="data-caption">DATA SOURCE &nbsp; / &nbsp; LOCAL SENSOR CSV + SNOWFLAKE ANALYTICS</div>', unsafe_allow_html=True)
with right:
    if st.button("↻  Refresh", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

sensor_path = Path(__file__).resolve().parent.parent / "sensor_readings.csv"
mtime = sensor_path.stat().st_mtime if sensor_path.exists() else 0
df, sensor_error = load_sensor_data(mtime)
if sensor_error:
    st.error(sensor_error)
    st.stop()

# -------------------- FILTERS --------------------
container_options = ["All Containers"] + sorted(df["container_id"].unique().tolist())
with st.sidebar:
    st.markdown('<div class="sidebar-kicker filter-kicker">FILTERS</div>', unsafe_allow_html=True)
    selected_container = st.selectbox("Container", container_options, key="container_filter")
    min_date = df["timestamp"].min().date()
    max_date = df["timestamp"].max().date()
    date_range = st.date_input(
        "Date range", value=(min_date, max_date),
        min_value=min_date, max_value=max_date, key="date_filter"
    )

filtered = df.copy()
if selected_container != "All Containers":
    filtered = filtered[filtered["container_id"] == selected_container]
if isinstance(date_range, (tuple, list)):
    if len(date_range) == 2:
        start_date, end_date = date_range
        filtered = filtered[filtered["timestamp"].dt.date.between(start_date, end_date)]
    elif len(date_range) == 1:
        filtered = filtered[filtered["timestamp"].dt.date == date_range[0]]
else:
    filtered = filtered[filtered["timestamp"].dt.date == date_range]

if filtered.empty:
    st.warning("No sensor readings match the selected container and date range.")
    st.stop()

# Market data is only queried on pages that display it.
market_df, market_error = (pd.DataFrame(), None)
if page in ["Overview & Analytics", "Market Intelligence"]:
    market_df, market_error = load_market_data()

# =====================================================
# PAGE 1: OVERVIEW
# =====================================================
if page == "Overview & Analytics":
    total_containers = filtered["container_id"].nunique()
    total_readings = len(filtered)
    avg_temp = filtered["temperature_c"].mean()
    alerts = int((filtered["Risk Details"] != "Normal").sum())
    normal = total_readings - alerts
    alert_rate = (alerts / total_readings * 100) if total_readings else 0

    section_heading("✦", "Operations overview", "A quick read of the selected sensor data")
    c1, c2, c3, c4 = st.columns(4)
    with c1: kpi_card("📦", "CONTAINERS", total_containers, "Unique containers in view", "blue")
    with c2: kpi_card("⌁", "SENSOR READINGS", f"{total_readings:,}", "Available sensor records", "cyan")
    with c3: kpi_card("🌡", "AVERAGE TEMPERATURE", f"{avg_temp:.2f} °C", "Across selected readings", "violet")
    with c4: kpi_card("⚠", "ALERT READINGS", f"{alerts:,}", f"{alert_rate:.1f}% of selected readings", "rose")

    section_heading("◉", "Container health", "Status calculated using configured prototype thresholds")
    groups = list(filtered.groupby("container_id"))
    cols = st.columns(min(max(len(groups), 1), 3))
    for i, (container_id, group) in enumerate(groups):
        status = "CHECK REQUIRED" if (group["Risk Details"] != "Normal").any() else "VALID"
        with cols[i % len(cols)]:
            status_card(container_id, status, len(group))

    section_heading("⌁", "Sensor performance", "Temperature and humidity patterns over time")
    chart_col, summary_col = st.columns([1.8, 1])
    with chart_col:
        trend = filtered.sort_values("timestamp")
        fig = px.line(
            trend, x="timestamp", y="temperature_c", color="container_id",
            markers=True, color_discrete_sequence=["#3979D8", "#36B9C7", "#8B78D6"]
        )
        fig.add_hrect(y0=TEMP_MIN, y1=TEMP_MAX, fillcolor="#36B9C7", opacity=0.08, line_width=0)
        fig.update_layout(yaxis_title="Temperature (°C)", xaxis_title="")
        st.plotly_chart(chart_layout(fig, 350), use_container_width=True)
    with summary_col:
        st.markdown('<div class="insight-panel"><div class="insight-kicker">CURRENT FILTER SUMMARY</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="insight-number">{normal:,}<span> / {total_readings:,}</span></div><div class="insight-label">readings within configured limits</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="progress-track"><div class="progress-fill" style="width:{100-alert_rate:.1f}%"></div></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="insight-foot"><span>Normal readings</span><strong>{100-alert_rate:.1f}%</strong></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="insight-foot"><span>Readings requiring attention</span><strong>{alerts:,}</strong></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    section_heading("⚑", "Risk analysis & alerts", "Sensor records outside the configured thresholds")
    alert_df = filtered[filtered["Risk Details"] != "Normal"].copy()
    if alert_df.empty:
        st.success("All displayed sensor readings are within configured limits.")
    else:
        st.warning(f"{len(alert_df)} reading(s) are outside one or more configured limits.")
        st.dataframe(
            alert_df[["timestamp", "container_id", "temperature_c", "humidity_percent",
                      "vibration_mm_s", "Risk Details", "Calculated Status"]],
            use_container_width=True, hide_index=True
        )

    section_heading("↗", "Market intelligence snapshot", "Summary returned by the Snowflake dbt analytics model")
    if market_error:
        st.info("Market snapshot is unavailable. Check the Snowflake connection and analytics table configuration.")
    elif market_df.empty:
        st.info("No market analytics rows were returned from Snowflake.")
    else:
        selected_market = market_df.copy()
        if selected_container != "All Containers":
            selected_market = selected_market[selected_market["CONTAINER_ID"].astype(str) == selected_container]
        if selected_market.empty:
            st.info("No market analytics rows for the selected container.")
        else:
            price = safe_number(selected_market["PRICE_PER_KG"]).mean()
            m1, m2, m3 = st.columns(3)
            with m1: kpi_card("▣", "DBT RESULT ROWS", len(selected_market), "Rows returned by analytics model", "blue")
            with m2: kpi_card("₹", "AVERAGE MOCK PRICE", f"₹{price:.2f}/kg" if pd.notna(price) else "—", "Illustrative market-price data", "violet")
            with m3: kpi_card("◎", "HIGH-RISK ROWS", int((selected_market["RISK_LEVEL"].astype(str).str.upper() == "HIGH").sum()), "Model risk labels", "rose")

# =====================================================
# PAGE 2: CONTAINER MONITORING
# =====================================================
elif page == "Container Monitoring":
    section_heading("◉", "Container monitoring", "Inspect sensor readings, patterns and threshold breaches")
    metric_labels = {
        "Temperature (°C)": "temperature_c",
        "Humidity (%)": "humidity_percent",
        "Vibration (mm/s)": "vibration_mm_s"
    }
    chosen_metric = st.selectbox("Sensor metric", list(metric_labels.keys()), key="metric_select")
    metric_col = metric_labels[chosen_metric]
    chart_df = filtered.sort_values("timestamp")

    section_heading("⌁", f"{chosen_metric} trend", "Interactive time-series view · hover to inspect readings")
    fig = px.line(
        chart_df, x="timestamp", y=metric_col, color="container_id",
        markers=True, color_discrete_sequence=["#3979D8", "#36B9C7", "#8B78D6"]
    )
    fig.update_layout(xaxis_title="", yaxis_title=chosen_metric)
    if metric_col == "temperature_c":
        fig.add_hrect(y0=TEMP_MIN, y1=TEMP_MAX, fillcolor="#36B9C7", opacity=0.08, line_width=0)
    elif metric_col == "humidity_percent":
        fig.add_hrect(y0=HUM_MIN, y1=HUM_MAX, fillcolor="#36B9C7", opacity=0.08, line_width=0)
    else:
        fig.add_hrect(y0=VIB_MIN, y1=VIB_MAX, fillcolor="#36B9C7", opacity=0.08, line_width=0)
    st.plotly_chart(chart_layout(fig, 390), use_container_width=True)

    section_heading("▤", "Sensor data explorer", "Search, sort and export the filtered records")
    search_text = st.text_input("Search records", placeholder="Search container, status or risk detail…")
    table_df = filtered.copy()
    if search_text:
        mask = table_df.astype(str).apply(
            lambda col: col.str.contains(search_text, case=False, na=False)
        ).any(axis=1)
        table_df = table_df[mask]
    sort_column = st.selectbox(
        "Sort by", ["timestamp", "container_id", "temperature_c",
                    "humidity_percent", "vibration_mm_s"], key="table_sort"
    )
    sort_ascending = st.toggle("Ascending order", value=False)
    table_df = table_df.sort_values(sort_column, ascending=sort_ascending)
    st.dataframe(table_df, use_container_width=True, hide_index=True)
    st.download_button(
        "⬇  Download sensor data (CSV)",
        data=table_df.to_csv(index=False).encode("utf-8"),
        file_name="atmosync_sensor_data.csv",
        mime="text/csv"
    )

    section_heading("⚑", "Threshold alerts", "Only readings that breach configured prototype limits")
    alert_df = filtered[filtered["Risk Details"] != "Normal"]
    if alert_df.empty:
        st.success("No alert readings in the current filter.")
    else:
        st.dataframe(alert_df, use_container_width=True, hide_index=True)

    section_heading("◫", "All sensor trends", "Compare the three sensor measurements")
    trend = filtered.sort_values("timestamp")
    t1, t2 = st.columns(2)
    with t1:
        fig_t = px.line(trend, x="timestamp", y="temperature_c", color="container_id",
                        color_discrete_sequence=["#3979D8", "#36B9C7"])
        fig_t.update_layout(xaxis_title="", yaxis_title="Temperature (°C)")
        st.plotly_chart(chart_layout(fig_t, 270), use_container_width=True)
    with t2:
        fig_h = px.line(trend, x="timestamp", y="humidity_percent", color="container_id",
                        color_discrete_sequence=["#8B78D6", "#36B9C7"])
        fig_h.update_layout(xaxis_title="", yaxis_title="Humidity (%)")
        st.plotly_chart(chart_layout(fig_h, 270), use_container_width=True)
    fig_v = px.line(trend, x="timestamp", y="vibration_mm_s", color="container_id",
                    color_discrete_sequence=["#D69A32", "#3979D8"])
    fig_v.update_layout(xaxis_title="", yaxis_title="Vibration (mm/s)")
    st.plotly_chart(chart_layout(fig_v, 270), use_container_width=True)

# =====================================================
# PAGE 3: MARKET INTELLIGENCE
# =====================================================
else:
    section_heading("↗", "Spoilage arbitrage & market analysis",
                    "Container risk labels and illustrative market recommendations from the dbt model")
    if market_error:
        st.error("Unable to connect to Snowflake or retrieve market analytics.")
        st.caption("Check local Snowflake credentials, warehouse and analytics table configuration.")
    elif market_df.empty:
        st.info("Snowflake returned no market analytics rows.")
    else:
        view_market = market_df.copy()
        if selected_container != "All Containers":
            view_market = view_market[view_market["CONTAINER_ID"].astype(str) == selected_container]
        if view_market.empty:
            st.info("No market recommendation is available for this container.")
        else:
            st.markdown('<div class="connection-strip"><span class="connection-dot"></span> SNOWFLAKE ANALYTICS RESULT RECEIVED</div>', unsafe_allow_html=True)
            high_risk = int((view_market["RISK_LEVEL"].astype(str).str.upper() == "HIGH").sum())
            avg_price = safe_number(view_market["PRICE_PER_KG"]).mean()
            a, b, c = st.columns(3)
            with a: kpi_card("▣", "ANALYTICS ROWS", len(view_market), "Rows in current result", "blue")
            with b: kpi_card("⚠", "HIGH-RISK ROWS", high_risk, "Based on dbt model labels", "rose")
            with c: kpi_card("₹", "AVERAGE MOCK PRICE", f"₹{avg_price:.2f}/kg" if pd.notna(avg_price) else "—", "Illustrative commodity price", "violet")

            section_heading("▤", "Market analysis table", "Results returned by the Snowflake dbt model")
            st.dataframe(view_market, use_container_width=True, hide_index=True)

            section_heading("₹", "Price comparison", "Illustrative mock market prices · not live market quotes")
            price_df = view_market.copy()
            price_df["PRICE_PER_KG"] = safe_number(price_df["PRICE_PER_KG"])
            fig = px.bar(
                price_df, x="CONTAINER_ID", y="PRICE_PER_KG",
                color="RISK_LEVEL", text="PRICE_PER_KG",
                color_discrete_map={"HIGH": "#D85B6A", "MEDIUM": "#D69A32", "LOW": "#27A27B"}
            )
            fig.update_traces(texttemplate="₹%{text:.2f}", textposition="outside", cliponaxis=False)
            fig.update_layout(xaxis_title="Container", yaxis_title="Price per kg")
            st.plotly_chart(chart_layout(fig, 340), use_container_width=True)

            section_heading("⌖", "Container recommendations", "Recommendation details returned by the analytics model")
            for _, row in view_market.iterrows():
                risk = str(row.get("RISK_LEVEL", "UNKNOWN")).upper()
                risk_class, risk_icon = (
                    ("risk-high", "⚠") if risk == "HIGH" else
                    ("risk-medium", "◈") if risk == "MEDIUM" else
                    ("risk-low", "✓") if risk == "LOW" else
                    ("risk-neutral", "•")
                )
                price = pd.to_numeric(pd.Series([row.get("PRICE_PER_KG")]), errors="coerce").iloc[0]
                distance = pd.to_numeric(pd.Series([row.get("DISTANCE_KM")]), errors="coerce").iloc[0]
                price_text = f"₹{price:.2f}/kg" if pd.notna(price) else "—"
                distance_text = f"{distance:.0f} km" if pd.notna(distance) else "—"
                st.markdown(
                    f"""<div class="recommendation-card {risk_class}">
                      <div class="recommendation-top">
                        <strong>{escape(str(row.get('CONTAINER_ID', '—')))}</strong>
                        <span>{risk_icon} &nbsp; {escape(risk)} RISK</span>
                      </div>
                      <div class="recommendation-details">
                        <div><small>RECOMMENDED MARKET</small><strong>{escape(str(row.get('RECOMMENDED_MARKET', '—')))}</strong></div>
                        <div><small>COMMODITY</small><strong>{escape(str(row.get('COMMODITY', '—')))}</strong></div>
                        <div><small>ILLUSTRATIVE PRICE</small><strong>{price_text}</strong></div>
                        <div><small>DISTANCE</small><strong>{distance_text}</strong></div>
                      </div>
                      <p>{escape(str(row.get('RECOMMENDATION', 'No recommendation text available.')))}</p>
                    </div>""",
                    unsafe_allow_html=True
                )
            st.caption(
                "Important: Market prices are illustrative mock data. Risk labels use configured "
                "prototype thresholds and are not scientifically validated spoilage predictions."
            )
            st.download_button(
                "⬇  Download market analysis (CSV)",
                data=view_market.to_csv(index=False).encode("utf-8"),
                file_name="atmosync_market_analysis.csv",
                mime="text/csv"
            )

# -------------------- FOOTER --------------------
st.markdown(
    """<div class="footer">
      <div class="footer-brand"><span class="footer-mark">A°</span> AtmoSync</div>
      <div class="footer-subtitle">SMART COLD CHAIN ANALYTICS</div>
      <div class="footer-line">Micro-climate monitoring &nbsp;·&nbsp; Data analytics &nbsp;·&nbsp; Market intelligence</div>
      <div class="footer-disclaimer">Prototype dashboard · Market values are illustrative where indicated</div>
    </div>""",
    unsafe_allow_html=True
)
