# app.py
# AI Transformation Command Center
# A portfolio project demonstrating AI transformation leadership capabilities
# Built for: Senior AI Transformation Manager role — Financial Services context
#
# HOW TO RUN:
#   1. Open this folder in VS Code
#   2. In the terminal run: pip install -r requirements.txt  (first time only)
#   3. Then run: streamlit run app.py
#   4. Dashboard opens automatically at http://localhost:8501

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from fpdf import FPDF
import io
from datetime import datetime

# Import all mock data functions from data.py
from data import (
    get_readiness_data,
    get_adoption_data,
    get_roi_data,
    get_trend_data,
    get_health_flags,
    get_summary_kpis,
)

# ── Page Configuration ────────────────────────────────────────────────────────
# This must be the first Streamlit command in the script
st.set_page_config(
    page_title="AI Transformation Command Center",
    page_icon="⚡",
    layout="wide",                  # Use full browser width
    initial_sidebar_state="expanded",
)

# ── Custom CSS Styling ────────────────────────────────────────────────────────
# Injects CSS to give the dashboard a polished, professional look
st.markdown("""
<style>
    /* Main background */
    .stApp { background-color: #0f1117; color: #e0e0e0; }

    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background-color: #1a1d27;
        border-right: 1px solid #2e3250;
    }

    /* KPI metric cards */
    div[data-testid="metric-container"] {
        background-color: #1a1d27;
        border: 1px solid #2e3250;
        border-radius: 10px;
        padding: 16px;
    }

    /* Section headers */
    .section-header {
        font-size: 1.1rem;
        font-weight: 600;
        color: #7c83fd;
        border-bottom: 1px solid #2e3250;
        padding-bottom: 8px;
        margin-bottom: 16px;
        letter-spacing: 0.05em;
        text-transform: uppercase;
    }

    /* Risk badge colors */
    .risk-high   { color: #ff4b4b; font-weight: 600; }
    .risk-medium { color: #ffa500; font-weight: 600; }
    .risk-watch  { color: #f0c040; font-weight: 600; }

    /* Page title */
    .main-title {
        font-size: 1.8rem;
        font-weight: 700;
        color: #ffffff;
        letter-spacing: -0.01em;
    }

    .main-subtitle {
        font-size: 0.95rem;
        color: #8b8fa8;
        margin-top: -8px;
    }
</style>
""", unsafe_allow_html=True)

# ── Load All Data ─────────────────────────────────────────────────────────────
# Load once at the top — Streamlit re-runs the whole script on interaction,
# so keeping data loading at the top keeps everything in sync.
readiness_df = get_readiness_data()
adoption_df  = get_adoption_data()
roi_df       = get_roi_data()
trend_df     = get_trend_data()
health_df    = get_health_flags(adoption_df)
kpis         = get_summary_kpis(adoption_df, roi_df)

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## ⚡ Command Center")
    st.markdown("---")

    # Navigation — controls which section is shown in the main area
    page = st.radio(
        "Navigate",
        options=[
            "Executive Summary",
            "AI Readiness",
            "Tool Adoption",
            "ROI & Efficiency",
            "Adoption Health",
            "Export Report",
        ],
        label_visibility="collapsed",
    )

    st.markdown("---")

    # Business line filter — applies to relevant charts
    st.markdown("**Filter by Business Line**")
    all_lines = readiness_df["Business Line"].tolist()
    selected_lines = st.multiselect(
        "Business Lines",
        options=all_lines,
        default=all_lines,
        label_visibility="collapsed",
    )

    st.markdown("---")
    st.markdown(
        "<small style='color:#555'>Financial Services · AI Transformation<br>"
        f"Last updated: {datetime.now().strftime('%b %d, %Y')}</small>",
        unsafe_allow_html=True,
    )

# ── Filter data based on sidebar selection ────────────────────────────────────
# All DataFrames filtered to the selected business lines
r_df = readiness_df[readiness_df["Business Line"].isin(selected_lines)]
a_df = adoption_df[adoption_df["Business Line"].isin(selected_lines)]
roi  = roi_df[roi_df["Business Line"].isin(selected_lines)]
t_df = trend_df[trend_df["Business Line"].isin(selected_lines)]

# ══════════════════════════════════════════════════════════════════════════════
# PAGE: EXECUTIVE SUMMARY
# ══════════════════════════════════════════════════════════════════════════════
if page == "Executive Summary":

    st.markdown('<p class="main-title">AI Transformation Command Center</p>', unsafe_allow_html=True)
    st.markdown('<p class="main-subtitle">Enterprise AI Adoption · Performance Intelligence · Financial Services</p>', unsafe_allow_html=True)
    st.markdown("---")

    # ── Top KPI Row ───────────────────────────────────────────────────────────
    # st.metric() renders a clean KPI card with label, value, and optional delta
    col1, col2, col3, col4, col5, col6 = st.columns(6)

    with col1:
        st.metric(
            label="🛠 Tools Deployed",
            value=kpis["tools_deployed"],
            delta="Active rollouts",
        )
    with col2:
        st.metric(
            label="📈 Avg Adoption Rate",
            value=f"{kpis['avg_adoption_rate']}%",
            delta="+8% vs last quarter",
        )
    with col3:
        st.metric(
            label="💰 Monthly Savings",
            value=f"${kpis['total_cost_savings']}K",
            delta="Across all lines",
        )
    with col4:
        st.metric(
            label="⏱ Capacity Freed",
            value=f"{kpis['total_capacity_freed']} hrs",
            delta="Per month",
        )
    with col5:
        st.metric(
            label="⚠️ At-Risk Deployments",
            value=kpis["at_risk_deployments"],
            delta="Need attention",
            delta_color="inverse",   # Red when number is high
        )
    with col6:
        st.metric(
            label="⭐ Staff Satisfaction",
            value=f"{kpis['avg_satisfaction']}/5",
            delta="Average score",
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Charts Row ────────────────────────────────────────────────────────────
    col_left, col_right = st.columns(2)

    with col_left:
        st.markdown('<p class="section-header">Adoption Trend by Business Line</p>', unsafe_allow_html=True)

        # Line chart — shows quarterly adoption rate per business line
        fig_trend = px.line(
            t_df,
            x="Quarter",
            y="Adoption Rate (%)",
            color="Business Line",
            markers=True,
            template="plotly_dark",
            color_discrete_sequence=px.colors.qualitative.Bold,
        )
        fig_trend.update_layout(
            plot_bgcolor="#1a1d27",
            paper_bgcolor="#1a1d27",
            legend=dict(font=dict(size=10)),
            margin=dict(l=0, r=0, t=10, b=0),
        )
        # st.plotly_chart renders an interactive Plotly figure
        st.plotly_chart(fig_trend, use_container_width=True)

    with col_right:
        st.markdown('<p class="section-header">Overall Readiness by Business Line</p>', unsafe_allow_html=True)

        # Horizontal bar chart — shows overall readiness score per line
        fig_ready = px.bar(
            r_df.sort_values("Overall Score"),
            x="Overall Score",
            y="Business Line",
            orientation="h",
            color="Overall Score",
            color_continuous_scale="Blues",
            template="plotly_dark",
            text="Overall Score",
        )
        fig_ready.update_layout(
            plot_bgcolor="#1a1d27",
            paper_bgcolor="#1a1d27",
            coloraxis_showscale=False,
            margin=dict(l=0, r=0, t=10, b=0),
        )
        fig_ready.update_traces(textposition="outside")
        st.plotly_chart(fig_ready, use_container_width=True)

    # ── Cost Savings Summary ──────────────────────────────────────────────────
    st.markdown('<p class="section-header">Monthly Cost Savings & Capacity Freed</p>', unsafe_allow_html=True)

    col_a, col_b = st.columns(2)

    with col_a:
        fig_cost = px.bar(
            roi,
            x="Business Line",
            y="Cost Savings ($K/month)",
            color="Cost Savings ($K/month)",
            color_continuous_scale="Teal",
            template="plotly_dark",
            text="Cost Savings ($K/month)",
        )
        fig_cost.update_layout(
            plot_bgcolor="#1a1d27",
            paper_bgcolor="#1a1d27",
            coloraxis_showscale=False,
            margin=dict(l=0, r=0, t=10, b=0),
        )
        fig_cost.update_traces(texttemplate="$%{text}K", textposition="outside")
        st.plotly_chart(fig_cost, use_container_width=True)

    with col_b:
        fig_cap = px.bar(
            roi,
            x="Business Line",
            y="Capacity Freed (hrs/mo)",
            color="Capacity Freed (hrs/mo)",
            color_continuous_scale="Purples",
            template="plotly_dark",
            text="Capacity Freed (hrs/mo)",
        )
        fig_cap.update_layout(
            plot_bgcolor="#1a1d27",
            paper_bgcolor="#1a1d27",
            coloraxis_showscale=False,
            margin=dict(l=0, r=0, t=10, b=0),
        )
        fig_cap.update_traces(texttemplate="%{text} hrs", textposition="outside")
        st.plotly_chart(fig_cap, use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: AI READINESS
# ══════════════════════════════════════════════════════════════════════════════
elif page == "AI Readiness":

    st.markdown('<p class="main-title">AI Readiness Assessment</p>', unsafe_allow_html=True)
    st.markdown('<p class="main-subtitle">Scores across Data Quality · Process Maturity · Change Appetite · Tech Infrastructure</p>', unsafe_allow_html=True)
    st.markdown("---")

    col_left, col_right = st.columns([1.2, 1])

    with col_left:
        st.markdown('<p class="section-header">Readiness Scores by Dimension</p>', unsafe_allow_html=True)

        # Radar / spider chart — ideal for multi-dimension scoring
        categories = ["Data Quality", "Process Maturity", "Change Appetite", "Tech Infrastructure"]

        fig_radar = go.Figure()
        colors = px.colors.qualitative.Bold

        for i, row in r_df.iterrows():
            values = [row[c] for c in categories]
            values += values[:1]  # Close the radar shape
            fig_radar.add_trace(go.Scatterpolar(
                r=values,
                theta=categories + [categories[0]],
                fill="toself",
                name=row["Business Line"],
                line_color=colors[i % len(colors)],
                fillcolor=colors[i % len(colors)],
                opacity=0.3,
            ))

        fig_radar.update_layout(
            polar=dict(
                radialaxis=dict(visible=True, range=[0, 100], color="#555"),
                bgcolor="#1a1d27",
            ),
            paper_bgcolor="#1a1d27",
            plot_bgcolor="#1a1d27",
            legend=dict(font=dict(size=10, color="#ccc")),
            margin=dict(l=20, r=20, t=20, b=20),
            template="plotly_dark",
        )
        st.plotly_chart(fig_radar, use_container_width=True)

    with col_right:
        st.markdown('<p class="section-header">Readiness Tiers</p>', unsafe_allow_html=True)

        # Display the readiness table with tier labels
        display_cols = ["Business Line", "Overall Score", "Tier"]
        st.dataframe(
            r_df[display_cols].sort_values("Overall Score", ascending=False),
            use_container_width=True,
            hide_index=True,
        )

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<p class="section-header">Score Breakdown</p>', unsafe_allow_html=True)

        # Full detail table
        st.dataframe(
            r_df[["Business Line"] + categories + ["Overall Score"]].sort_values("Overall Score", ascending=False),
            use_container_width=True,
            hide_index=True,
        )

    # ── Insight callout ───────────────────────────────────────────────────────
    st.markdown("---")
    st.info(
        "💡 **Transformation Insight**: Business lines scoring below 70 in Change Appetite "
        "require a dedicated change management track before tool deployment — technical readiness "
        "alone does not predict successful adoption."
    )


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: TOOL ADOPTION
# ══════════════════════════════════════════════════════════════════════════════
elif page == "Tool Adoption":

    st.markdown('<p class="main-title">AI Tool Adoption Tracker</p>', unsafe_allow_html=True)
    st.markdown('<p class="main-subtitle">Deployment status · Adoption rates · Staff satisfaction by tool and business line</p>', unsafe_allow_html=True)
    st.markdown("---")

    # ── Filter by tool ────────────────────────────────────────────────────────
    all_tools = adoption_df["AI Tool"].unique().tolist()
    selected_tools = st.multiselect(
        "Filter by AI Tool",
        options=all_tools,
        default=all_tools,
    )

    # Apply both business line and tool filters
    filtered = a_df[a_df["AI Tool"].isin(selected_tools)]
    deployed_only = filtered[filtered["Deployed"] == True]

    col_left, col_right = st.columns(2)

    with col_left:
        st.markdown('<p class="section-header">Adoption Rate by Tool & Business Line</p>', unsafe_allow_html=True)

        # Heatmap — great for showing adoption rate across two dimensions
        pivot = deployed_only.pivot_table(
            index="Business Line",
            columns="AI Tool",
            values="Adoption Rate (%)",
            aggfunc="mean",
        ).fillna(0)

        fig_heat = px.imshow(
            pivot,
            color_continuous_scale="Blues",
            template="plotly_dark",
            text_auto=".0f",
            aspect="auto",
        )
        fig_heat.update_layout(
            paper_bgcolor="#1a1d27",
            plot_bgcolor="#1a1d27",
            margin=dict(l=0, r=0, t=10, b=0),
            coloraxis_colorbar=dict(title="Rate %"),
        )
        st.plotly_chart(fig_heat, use_container_width=True)

    with col_right:
        st.markdown('<p class="section-header">Staff Satisfaction by Tool</p>', unsafe_allow_html=True)

        # Average satisfaction score per tool — bar chart
        sat = (
            deployed_only.groupby("AI Tool")["Satisfaction (1-5)"]
            .mean()
            .reset_index()
            .sort_values("Satisfaction (1-5)", ascending=True)
        )

        fig_sat = px.bar(
            sat,
            x="Satisfaction (1-5)",
            y="AI Tool",
            orientation="h",
            color="Satisfaction (1-5)",
            color_continuous_scale="RdYlGn",
            range_color=[1, 5],
            template="plotly_dark",
            text=sat["Satisfaction (1-5)"].round(1),
        )
        fig_sat.update_layout(
            paper_bgcolor="#1a1d27",
            plot_bgcolor="#1a1d27",
            coloraxis_showscale=False,
            margin=dict(l=0, r=0, t=10, b=0),
        )
        fig_sat.update_traces(textposition="outside")
        st.plotly_chart(fig_sat, use_container_width=True)

    st.markdown('<p class="section-header">Full Adoption Detail</p>', unsafe_allow_html=True)
    st.dataframe(
        filtered.sort_values(["Business Line", "AI Tool"]),
        use_container_width=True,
        hide_index=True,
    )


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: ROI & EFFICIENCY
# ══════════════════════════════════════════════════════════════════════════════
elif page == "ROI & Efficiency":

    st.markdown('<p class="main-title">ROI & Operational Efficiency</p>', unsafe_allow_html=True)
    st.markdown('<p class="main-subtitle">Before/after impact of AI adoption across operational metrics</p>', unsafe_allow_html=True)
    st.markdown("---")

    # ── Summary metrics ───────────────────────────────────────────────────────
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Monthly Savings", f"${roi['Cost Savings ($K/month)'].sum()}K")
    with col2:
        st.metric("Avg Handle Time Reduction", f"{roi['Handle Time Reduction (%)'].mean():.1f}%")
    with col3:
        st.metric("Avg Error Rate Reduction", f"{roi['Error Rate Reduction (%)'].mean():.1f}%")
    with col4:
        st.metric("Total Capacity Freed", f"{roi['Capacity Freed (hrs/mo)'].sum()} hrs/mo")

    st.markdown("<br>", unsafe_allow_html=True)

    col_left, col_right = st.columns(2)

    with col_left:
        st.markdown('<p class="section-header">Handle Time & Error Rate Reduction</p>', unsafe_allow_html=True)

        # Grouped bar chart — shows two metrics side by side per business line
        fig_ops = go.Figure()
        fig_ops.add_trace(go.Bar(
            name="Handle Time Reduction (%)",
            x=roi["Business Line"],
            y=roi["Handle Time Reduction (%)"],
            marker_color="#7c83fd",
        ))
        fig_ops.add_trace(go.Bar(
            name="Error Rate Reduction (%)",
            x=roi["Business Line"],
            y=roi["Error Rate Reduction (%)"],
            marker_color="#4ecdc4",
        ))
        fig_ops.update_layout(
            barmode="group",
            template="plotly_dark",
            paper_bgcolor="#1a1d27",
            plot_bgcolor="#1a1d27",
            legend=dict(font=dict(size=10)),
            margin=dict(l=0, r=0, t=10, b=0),
        )
        st.plotly_chart(fig_ops, use_container_width=True)

    with col_right:
        st.markdown('<p class="section-header">ROI Score by Business Line</p>', unsafe_allow_html=True)

        # Scatter plot — ROI score vs cost savings, bubble size = capacity freed
        fig_scatter = px.scatter(
            roi,
            x="Cost Savings ($K/month)",
            y="Total ROI Score",
            size="Capacity Freed (hrs/mo)",
            color="Business Line",
            template="plotly_dark",
            hover_name="Business Line",
            size_max=40,
        )
        fig_scatter.update_layout(
            paper_bgcolor="#1a1d27",
            plot_bgcolor="#1a1d27",
            margin=dict(l=0, r=0, t=10, b=0),
        )
        st.plotly_chart(fig_scatter, use_container_width=True)

    st.markdown('<p class="section-header">Full ROI Data Table</p>', unsafe_allow_html=True)
    st.dataframe(roi.sort_values("Total ROI Score", ascending=False), use_container_width=True, hide_index=True)

    st.info(
        "💡 **Transformation Insight**: High capacity-freed figures indicate successful "
        "automation of repetitive tasks — this is the primary lever for reinvesting staff "
        "time into advisory and complex judgment work."
    )


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: ADOPTION HEALTH
# ══════════════════════════════════════════════════════════════════════════════
elif page == "Adoption Health":

    st.markdown('<p class="main-title">Adoption Health Monitor</p>', unsafe_allow_html=True)
    st.markdown('<p class="main-subtitle">Flagged deployments where tools are live but adoption is lagging</p>', unsafe_allow_html=True)
    st.markdown("---")

    # Filter health flags to selected business lines
    h_df = health_df[health_df["Business Line"].isin(selected_lines)]

    # ── Risk summary KPIs ─────────────────────────────────────────────────────
    high   = len(h_df[h_df["Risk Level"] == "High Risk"])
    medium = len(h_df[h_df["Risk Level"] == "Medium Risk"])
    watch  = len(h_df[h_df["Risk Level"] == "Watch"])

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total At-Risk", len(h_df))
    with col2:
        st.metric("🔴 High Risk", high, delta="Adoption < 30%", delta_color="inverse")
    with col3:
        st.metric("🟠 Medium Risk", medium, delta="Adoption 30–40%", delta_color="inverse")
    with col4:
        st.metric("🟡 Watch", watch, delta="Adoption 40–50%", delta_color="off")

    st.markdown("<br>", unsafe_allow_html=True)

    col_left, col_right = st.columns(2)

    with col_left:
        st.markdown('<p class="section-header">At-Risk Deployments by Business Line</p>', unsafe_allow_html=True)

        if not h_df.empty:
            risk_count = h_df.groupby(["Business Line", "Risk Level"]).size().reset_index(name="Count")
            fig_risk = px.bar(
                risk_count,
                x="Business Line",
                y="Count",
                color="Risk Level",
                color_discrete_map={
                    "High Risk": "#ff4b4b",
                    "Medium Risk": "#ffa500",
                    "Watch": "#f0c040",
                },
                template="plotly_dark",
                barmode="stack",
            )
            fig_risk.update_layout(
                paper_bgcolor="#1a1d27",
                plot_bgcolor="#1a1d27",
                margin=dict(l=0, r=0, t=10, b=0),
            )
            st.plotly_chart(fig_risk, use_container_width=True)
        else:
            st.success("✅ No at-risk deployments for selected business lines.")

    with col_right:
        st.markdown('<p class="section-header">Adoption Rate Distribution</p>', unsafe_allow_html=True)

        deployed_filtered = a_df[a_df["Deployed"] == True]
        fig_hist = px.histogram(
            deployed_filtered,
            x="Adoption Rate (%)",
            nbins=20,
            template="plotly_dark",
            color_discrete_sequence=["#7c83fd"],
        )
        fig_hist.add_vline(x=50, line_dash="dash", line_color="#ff4b4b", annotation_text="Risk threshold")
        fig_hist.update_layout(
            paper_bgcolor="#1a1d27",
            plot_bgcolor="#1a1d27",
            margin=dict(l=0, r=0, t=10, b=0),
        )
        st.plotly_chart(fig_hist, use_container_width=True)

    st.markdown('<p class="section-header">Flagged Deployments — Action Required</p>', unsafe_allow_html=True)

    if not h_df.empty:
        st.dataframe(
            h_df[["Business Line", "AI Tool", "Adoption Rate (%)", "Weekly Uses", "Risk Level"]]
            .sort_values("Adoption Rate (%)"),
            use_container_width=True,
            hide_index=True,
        )
    else:
        st.success("✅ All deployments are above the 50% adoption threshold.")

    st.info(
        "💡 **Transformation Insight**: Low adoption in a deployed tool is rarely a technology "
        "problem — it is almost always a change management, training, or workflow integration "
        "problem. Each flagged row represents an intervention opportunity."
    )


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: EXPORT REPORT
# ══════════════════════════════════════════════════════════════════════════════
elif page == "Export Report":

    st.markdown('<p class="main-title">Export Executive Report</p>', unsafe_allow_html=True)
    st.markdown('<p class="main-subtitle">Generate a PDF summary for leadership, stakeholders, or portfolio presentation</p>', unsafe_allow_html=True)
    st.markdown("---")

    st.markdown("### Report preview")

    # Show a summary of what will be in the report
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Sections included:**")
        st.markdown("- Executive KPI summary")
        st.markdown("- AI readiness scores by business line")
        st.markdown("- Tool adoption rates and satisfaction")
        st.markdown("- ROI and operational efficiency metrics")
        st.markdown("- At-risk deployment flags")
        st.markdown("- Transformation insights and recommendations")

    with col2:
        st.markdown("**Report details:**")
        st.markdown(f"- Generated: {datetime.now().strftime('%B %d, %Y')}")
        st.markdown(f"- Business lines included: {len(selected_lines)}")
        st.markdown(f"- Tools tracked: {len(adoption_df['AI Tool'].unique())}")
        st.markdown(f"- At-risk flags: {len(health_df)}")

    st.markdown("---")

    # ── PDF Generation ────────────────────────────────────────────────────────
    # FPDF2 builds the PDF programmatically — each method adds an element
    def generate_pdf() -> bytes:
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()

        # ── Cover section ──────────────────────────────────────────────────
        pdf.set_fill_color(15, 17, 23)
        pdf.rect(0, 0, 210, 50, "F")
        pdf.set_font("Helvetica", "B", 20)
        pdf.set_text_color(255, 255, 255)
        pdf.cell(0, 15, "", ln=True)
        pdf.cell(0, 10, "AI Transformation Command Center", ln=True, align="C")
        pdf.set_font("Helvetica", "", 11)
        pdf.set_text_color(180, 180, 200)
        pdf.cell(0, 8, "Executive Summary Report — Financial Services", ln=True, align="C")
        pdf.set_text_color(120, 120, 140)
        pdf.cell(0, 6, f"Generated: {datetime.now().strftime('%B %d, %Y')}", ln=True, align="C")
        pdf.ln(12)

        # ── Section helper ─────────────────────────────────────────────────
        def section(title: str):
            pdf.set_fill_color(30, 35, 60)
            pdf.set_font("Helvetica", "B", 12)
            pdf.set_text_color(124, 131, 253)
            pdf.cell(0, 8, title.upper(), ln=True, fill=True)
            pdf.set_text_color(50, 50, 50)
            pdf.ln(2)

        def row(label: str, value: str):
            pdf.set_font("Helvetica", "", 10)
            pdf.set_text_color(60, 60, 80)
            pdf.cell(80, 7, label)
            pdf.set_font("Helvetica", "B", 10)
            pdf.set_text_color(30, 30, 50)
            pdf.cell(0, 7, value, ln=True)

        # ── KPIs ───────────────────────────────────────────────────────────
        section("Executive KPIs")
        row("Tools Deployed:", str(kpis["tools_deployed"]))
        row("Average Adoption Rate:", f"{kpis['avg_adoption_rate']}%")
        row("Monthly Cost Savings:", f"${kpis['total_cost_savings']}K")
        row("Capacity Freed (hrs/month):", f"{kpis['total_capacity_freed']} hours")
        row("At-Risk Deployments:", str(kpis["at_risk_deployments"]))
        row("Average Staff Satisfaction:", f"{kpis['avg_satisfaction']} / 5.0")
        pdf.ln(6)

        # ── Readiness Scores ───────────────────────────────────────────────
        section("AI Readiness by Business Line")
        for _, row_data in readiness_df.sort_values("Overall Score", ascending=False).iterrows():
            row(row_data["Business Line"], f"Overall: {row_data['Overall Score']} — Tier: {row_data['Tier']}")
        pdf.ln(6)

        # ── ROI Summary ────────────────────────────────────────────────────
        section("ROI & Operational Efficiency")
        for _, row_data in roi_df.sort_values("Total ROI Score", ascending=False).iterrows():
            row(
                row_data["Business Line"],
                f"Savings: ${row_data['Cost Savings ($K/month)']}K/mo | "
                f"Handle Time: -{row_data['Handle Time Reduction (%)']}% | "
                f"Errors: -{row_data['Error Rate Reduction (%)']}%"
            )
        pdf.ln(6)

        # ── Health Flags ───────────────────────────────────────────────────
        section("At-Risk Deployments")
        if not health_df.empty:
            for _, row_data in health_df.iterrows():
                row(
                    f"{row_data['Business Line']} — {row_data['AI Tool']}",
                    f"Adoption: {row_data['Adoption Rate (%)']}% | Risk: {row_data['Risk Level']}"
                )
        else:
            pdf.set_font("Helvetica", "", 10)
            pdf.set_text_color(60, 60, 80)
            pdf.cell(0, 7, "No at-risk deployments identified.", ln=True)
        pdf.ln(6)

        # ── Recommendations ────────────────────────────────────────────────
        section("Transformation Insights")
        insights = [
            "Business lines below 70 in Change Appetite require a dedicated change management track.",
            "Low adoption in deployed tools signals a change management or training gap, not a technology failure.",
            "High capacity-freed metrics indicate successful automation — reinvest that time in advisory work.",
            "Prioritize readiness interventions in Commercial Lending before expanding tool deployment.",
        ]
        pdf.set_font("Helvetica", "", 10)
        pdf.set_text_color(60, 60, 80)
        for insight in insights:
            pdf.multi_cell(0, 6, f"• {insight}")
            pdf.ln(1)

        # Return as bytes for Streamlit download button
        return bytes(pdf.output())

    # ── Download button ───────────────────────────────────────────────────────
    # st.download_button streams the file to the user's browser
    if st.button("⚡ Generate PDF Report", type="primary"):
        with st.spinner("Building your report..."):
            pdf_bytes = generate_pdf()
        st.success("✅ Report ready!")
        st.download_button(
            label="📄 Download Executive Report (PDF)",
            data=pdf_bytes,
            file_name=f"AI_Transformation_Report_{datetime.now().strftime('%Y%m%d')}.pdf",
            mime="application/pdf",
        )

    st.markdown("---")
    st.info(
        "💡 **Portfolio tip**: Use this PDF export in interviews to show you can produce "
        "board-ready reporting automatically — not just build dashboards, but close the "
        "loop with executive deliverables."
    )
