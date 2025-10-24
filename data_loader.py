import os
import pandas as pd


def _find_col(df, candidates):
    """Return the first matching column name in df for case-insensitive candidates, or None."""
    cols = list(df.columns)
    for cand in candidates:
        for c in cols:
            if c and c.lower() == cand.lower():
                return c
    return None


def load_data():
    """Load available dataset.

    Priority:
    - cleaned_castle_of_insights.csv (project root)
    - department_retained_summary.csv
    - optimization_analysis.xlsx (sheet 'Retained_Employees' if present)

    The loader normalizes column names (strip + replace spaces with underscores)
    and creates commonly-used derived columns such as `TenureGroup` and
    canonical names like `output_est`, `Company_Origin`, `Work_Rating`, `Salary`.
    """
    base = os.path.dirname(__file__)
    candidates = [
        os.path.join(base, "cleaned_castle_of_insights.csv"),
        os.path.join(base, "department_retained_summary.csv"),
        os.path.join(base, "optimization_analysis.xlsx"),
    ]

    df = None
    for path in candidates:
        if os.path.exists(path):
            try:
                if path.lower().endswith('.csv'):
                    df = pd.read_csv(path)
                else:
                    # try sheet name commonly used in this repo; fall back to first sheet
                    try:
                        df = pd.read_excel(path, sheet_name="Retained_Employees")
                    except Exception:
                        df = pd.read_excel(path)
                break
            except Exception:
                # try next candidate if read fails
                df = None
                continue

    if df is None:
        raise FileNotFoundError(
            "No input data found. Please add 'cleaned_castle_of_insights.csv', 'department_retained_summary.csv' or 'optimization_analysis.xlsx' to the project root."
        )

    # normalize columns: strip and replace spaces with underscores
    df.columns = [str(c).strip().replace(" ", "_") for c in df.columns]

    # canonicalize some columns used by dashboards
    # Tenure
    tenure_col = _find_col(df, ["Tenure", "Tenure_Years", "Tenure (Years)"])
    if tenure_col and tenure_col != "Tenure":
        df.rename(columns={tenure_col: "Tenure"}, inplace=True)

    if "Tenure" in df.columns:
        df["Tenure"] = pd.to_numeric(df["Tenure"], errors="coerce")
        # bins: <5, 5-15, 15+
        df["TenureGroup"] = pd.cut(df["Tenure"], bins=[-1, 5, 15, 1e9], labels=["<5 years", "5-15 years", "15+ years"]) 

    # output estimate
    out_col = _find_col(df, ["output_est", "Output_Estimated", "Estimated_Output", "Output"])
    if out_col and out_col != "output_est":
        df.rename(columns={out_col: "output_est"}, inplace=True)

    # company origin
    comp_col = _find_col(df, ["Company_Origin", "Company", "Employer"])
    if comp_col and comp_col != "Company_Origin":
        df.rename(columns={comp_col: "Company_Origin"}, inplace=True)

    # work rating
    rating_col = _find_col(df, ["Work_Rating", "Rating", "Performance_Rating", "Performance"])
    if rating_col and rating_col != "Work_Rating":
        df.rename(columns={rating_col: "Work_Rating"}, inplace=True)

    # salary
    sal_col = _find_col(df, ["Salary", "Annual_Salary", "Base_Salary"])
    if sal_col and sal_col != "Salary":
        df.rename(columns={sal_col: "Salary"}, inplace=True)

    # department
    dept_col = _find_col(df, ["Department", "Dept"])
    if dept_col and dept_col != "Department":
        df.rename(columns={dept_col: "Department"}, inplace=True)

    return df

