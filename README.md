# Castle of Insights — Dash + Bokeh Dashboards

This repository contains two interactive dashboards to explore the Castle of Insights dataset:

- `app_dash.py` — main Plotly Dash application with summary KPIs, filters, and interactive charts.
- `bokeh_dashboard.py` — Bokeh server app with detailed scatter plots and interactive widgets (embedded in the Dash app via an iframe).

Overview
--------
The code loads data using `data_loader.py`. The loader looks for, in order:

1. `cleaned_castle_of_insights.csv`
2. `department_retained_summary.csv`
3. `optimization_analysis.xlsx` (sheet `Retained_Employees` or first sheet)

It normalizes column names and creates derived fields like `TenureGroup` which the dashboards use.

Prerequisites
-------------
- Python 3.10+ (or the version you use for the project)
- Recommended: create a virtual environment

Install
-------
From the project root (PowerShell):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Run the apps
------------
Open two terminals (PowerShell):

1) Start the Bokeh server (so Dash can embed it):

```powershell
bokeh serve --show bokeh_dashboard.py --port 5006
```

2) Start the Dash app:

```powershell
python app_dash.py
```

Dash will be available at http://127.0.0.1:8050 and includes an iframe to the Bokeh app at http://localhost:5006/bokeh_dashboard.

Files of interest
-----------------
- `data_loader.py` — robust loader and normalizer for CSV/Excel sources.
- `app_dash.py` — Dash app (filters, summary cards, Plotly charts).
- `bokeh_dashboard.py` — Bokeh server app (scatter plots, hover, color mapping, regression line).
- `cleaned_castle_of_insights.csv` / `department_retained_summary.csv` — sample data files (if present in repo).

Development notes
-----------------
- The Dash app expects the Bokeh server to run on port 5006 for embedding. You can remove the iframe if you prefer to run them separately.
- I suppressed a few Bokeh deprecation warnings to keep imports quiet; if you prefer to remove suppression I can update the code to use the newest API patterns.

If you have a PDF or design spec
------------------------------
You mentioned a PDF earlier — if you upload it I will adapt the dashboard layout, chart selection, and exact KPI definitions to match it.

Contributing
------------
- Create a branch for changes, add tests if you change loader logic, and open a PR with a short description.

License
-------
Add your project license here if you have one. If not, let me know which license you prefer and I can add it.

Contact / Next steps
--------------------
Tell me if you want:

- the dashboards to match a provided PDF (upload it),
- export/download features for filtered datasets, or
- additional charts (churn, performance vs salary, time series).

I'll implement whichever you prefer next.
