# AI Transformation Command Center

A working prototype of the tool an AI Transformation Manager would use on day one. Built to answer the question every financial services executive is asking right now: "How is our AI transformation actually going?"
This dashboard gives a single source of truth across six business lines — scoring AI readiness before deployment, tracking adoption health after rollout, measuring operational ROI, and flagging at-risk implementations before they become failures. It closes with an automated executive PDF report designed for board-level communication.
Built with: Python · Pandas · Streamlit · Plotly · FPDF2
Demonstrates: AI transformation strategy · Change management thinking · Data-driven decision making · Executive reporting · Financial services domain expertise# AI Transformation Command Center

A portfolio project demonstrating AI transformation leadership capabilities
in a financial services context.

Built for: Senior AI Transformation Manager role
Stack: Python · Pandas · Streamlit · Plotly · FPDF2

---

## What this project demonstrates

- AI readiness scoring across business lines (4 dimensions)
- Tool adoption tracking with health monitoring
- ROI and operational efficiency metrics
- Automated PDF executive report generation
- Filtering and interactive dashboard controls

---

## Setup (one time only)

Make sure Python is installed, then open this folder in VS Code.

Open the terminal in VS Code (Terminal → New Terminal) and run:

```
pip install -r requirements.txt
```

This installs: streamlit, pandas, plotly, numpy, fpdf2

---

## Running the dashboard

Every time you want to run it:

```
streamlit run app.py
```

Your browser will open automatically at http://localhost:8501

To stop it: press Ctrl+C in the terminal

---

## Project structure

```
ai_transformation_command_center/
├── app.py              # Main dashboard — all pages and charts
├── data.py             # Mock data — all synthetic financial institution data
├── requirements.txt    # Python dependencies
└── README.md           # This file
```

---

## Navigating the dashboard

Use the left sidebar to move between pages:

| Page | What it shows |
|------|--------------|
| Executive Summary | Top KPIs and trend overview |
| AI Readiness | Radar chart + scores by dimension |
| Tool Adoption | Heatmap + satisfaction by tool |
| ROI & Efficiency | Before/after operational impact |
| Adoption Health | At-risk deployments flagged |
| Export Report | Generate and download a PDF |

---

## Notes

All data is synthetic and randomly generated for demonstration purposes.
No real client, employee, or institutional data is used.
