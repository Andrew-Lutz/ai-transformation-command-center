# data.py
# Mock data module for the AI Transformation Command Center
# Simulates a large financial institution's AI transformation metrics
# All data is synthetic and for portfolio/demonstration purposes only

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# ── Reproducible randomness ───────────────────────────────────────────────────
np.random.seed(42)

# ── Constants ─────────────────────────────────────────────────────────────────
BUSINESS_LINES = [
    "Retail Banking",
    "Wealth Management",
    "Commercial Lending",
    "Operations & Servicing",
    "Compliance & Risk",
    "Treasury Services",
]

AI_TOOLS = [
    "Client Resolution AI",
    "Document Processing Bot",
    "Fraud Detection Engine",
    "Compliance Screening AI",
    "Forecasting Assistant",
    "Onboarding Automation",
]

QUARTERS = ["Q1 2024", "Q2 2024", "Q3 2024", "Q4 2024", "Q1 2025"]


# ── AI Readiness Scores ───────────────────────────────────────────────────────
def get_readiness_data() -> pd.DataFrame:
    """
    Returns AI readiness scores per business line across four dimensions:
    - Data Quality    : how clean and structured the team's data is
    - Process Maturity: how well-documented and standardized workflows are
    - Change Appetite : willingness of staff to adopt new tools
    - Tech Infrastructure: existing systems' compatibility with AI tooling
    Each score is out of 100. Overall = average of all four.
    """
    data = {
        "Business Line": BUSINESS_LINES,
        "Data Quality": [82, 74, 68, 90, 77, 85],
        "Process Maturity": [78, 80, 65, 88, 85, 70],
        "Change Appetite": [72, 68, 60, 80, 65, 75],
        "Tech Infrastructure": [85, 70, 62, 92, 80, 78],
    }
    df = pd.DataFrame(data)
    df["Overall Score"] = df[
        ["Data Quality", "Process Maturity", "Change Appetite", "Tech Infrastructure"]
    ].mean(axis=1).round(1)

    # Readiness tier based on overall score
    df["Tier"] = pd.cut(
        df["Overall Score"],
        bins=[0, 60, 74, 84, 100],
        labels=["Not Ready", "Developing", "Ready", "Leading"],
    )
    return df


# ── AI Tool Adoption ──────────────────────────────────────────────────────────
def get_adoption_data() -> pd.DataFrame:
    """
    Returns adoption rates and active usage metrics per AI tool per business line.
    - Deployed     : whether the tool has been rolled out to that line (bool)
    - Adoption Rate: % of eligible staff actively using the tool
    - Weekly Uses  : average number of tool interactions per week
    - Satisfaction : staff-reported satisfaction score (1–5)
    """
    records = []
    for line in BUSINESS_LINES:
        for tool in AI_TOOLS:
            deployed = np.random.choice([True, False], p=[0.65, 0.35])
            adoption_rate = round(np.random.uniform(30, 95), 1) if deployed else 0.0
            weekly_uses = int(np.random.uniform(50, 800)) if deployed else 0
            satisfaction = round(np.random.uniform(3.0, 5.0), 1) if deployed else None
            records.append({
                "Business Line": line,
                "AI Tool": tool,
                "Deployed": deployed,
                "Adoption Rate (%)": adoption_rate,
                "Weekly Uses": weekly_uses,
                "Satisfaction (1-5)": satisfaction,
            })
    return pd.DataFrame(records)


# ── ROI & Efficiency Metrics ──────────────────────────────────────────────────
def get_roi_data() -> pd.DataFrame:
    """
    Returns before/after operational metrics per business line showing
    the measurable impact of AI tool adoption.
    - Handle Time Reduction (%): average case/task handle time improvement
    - Error Rate Reduction (%) : reduction in processing errors
    - Cost Savings ($K/month)  : estimated monthly cost savings
    - Capacity Freed (hrs/mo)  : staff hours freed for higher-value work
    """
    data = {
        "Business Line": BUSINESS_LINES,
        "Handle Time Reduction (%)": [28, 19, 15, 35, 22, 30],
        "Error Rate Reduction (%)": [40, 25, 18, 55, 48, 35],
        "Cost Savings ($K/month)": [120, 85, 60, 210, 95, 140],
        "Capacity Freed (hrs/mo)": [320, 180, 140, 450, 220, 310],
    }
    df = pd.DataFrame(data)
    df["Total ROI Score"] = (
        df["Handle Time Reduction (%)"] * 0.25
        + df["Error Rate Reduction (%)"] * 0.25
        + (df["Cost Savings ($K/month)"] / 210 * 100) * 0.25
        + (df["Capacity Freed (hrs/mo)"] / 450 * 100) * 0.25
    ).round(1)
    return df


# ── Adoption Trend Over Time ──────────────────────────────────────────────────
def get_trend_data() -> pd.DataFrame:
    """
    Returns quarterly adoption rate trends per business line.
    Shows trajectory — which lines are accelerating vs stalling.
    """
    records = []
    base_rates = {
        "Retail Banking": 40,
        "Wealth Management": 35,
        "Commercial Lending": 25,
        "Operations & Servicing": 55,
        "Compliance & Risk": 38,
        "Treasury Services": 45,
    }
    for quarter in QUARTERS:
        for line in BUSINESS_LINES:
            base = base_rates[line]
            idx = QUARTERS.index(quarter)
            # Simulates realistic ramp-up with some variance
            rate = min(95, base + (idx * np.random.uniform(6, 12)))
            records.append({
                "Quarter": quarter,
                "Business Line": line,
                "Adoption Rate (%)": round(rate, 1),
            })
    return pd.DataFrame(records)


# ── Adoption Health Flags ─────────────────────────────────────────────────────
def get_health_flags(adoption_df: pd.DataFrame) -> pd.DataFrame:
    """
    Identifies at-risk deployments where a tool is deployed but adoption
    is low — a key signal of change management failure or poor fit.
    Flags any deployed tool with adoption rate below 50%.
    """
    flags = adoption_df[
        (adoption_df["Deployed"] == True) & (adoption_df["Adoption Rate (%)"] < 50)
    ].copy()
    flags["Risk Level"] = pd.cut(
        flags["Adoption Rate (%)"],
        bins=[0, 30, 40, 50],
        labels=["High Risk", "Medium Risk", "Watch"],
    )
    return flags.reset_index(drop=True)


# ── Summary KPIs ──────────────────────────────────────────────────────────────
def get_summary_kpis(adoption_df: pd.DataFrame, roi_df: pd.DataFrame) -> dict:
    """
    Returns top-level KPIs for the executive summary view.
    """
    deployed = adoption_df[adoption_df["Deployed"] == True]
    return {
        "tools_deployed": int(adoption_df["Deployed"].sum()),
        "avg_adoption_rate": round(deployed["Adoption Rate (%)"].mean(), 1),
        "total_cost_savings": int(roi_df["Cost Savings ($K/month)"].sum()),
        "total_capacity_freed": int(roi_df["Capacity Freed (hrs/mo)"].sum()),
        "at_risk_deployments": int(
            ((adoption_df["Deployed"] == True) & (adoption_df["Adoption Rate (%)"] < 50)).sum()
        ),
        "avg_satisfaction": round(
            deployed["Satisfaction (1-5)"].dropna().mean(), 1
        ),
    }
