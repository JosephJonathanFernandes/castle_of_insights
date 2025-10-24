from bokeh.io import curdoc
from bokeh.models import ColumnDataSource, Select, HoverTool
from bokeh.layouts import column, row
from bokeh.plotting import figure
import pandas as pd
import numpy as np
from data_loader import load_data
import warnings
from bokeh.util.warnings import BokehDeprecationWarning

# silence specific Bokeh deprecation warnings for older glyph methods
warnings.filterwarnings("ignore", category=BokehDeprecationWarning)

df = load_data()
source = ColumnDataSource(df)

department_options = ["All"] + sorted(df['Department'].dropna().unique().tolist()) if 'Department' in df.columns else ["All"]
department_select = Select(title="Department", value="All", options=department_options)

# small color map for Work_Rating if available
color_map = {}
if 'Work_Rating' in df.columns:
    uniq = sorted([str(x) for x in df['Work_Rating'].dropna().unique()])
    palette = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd"]
    for i, k in enumerate(uniq):
        color_map[k] = palette[i % len(palette)]
    # add a color column for plotting
    df['_rating_color'] = df['Work_Rating'].astype(str).map(color_map)
    source = ColumnDataSource(df)

# Salary vs Output
p1 = figure(title="Salary vs Output", x_axis_label="Salary", y_axis_label="Output (Estimated)", tools="pan,wheel_zoom,box_zoom,reset")
p1.scatter(x="Salary", y="output_est", source=source, marker='circle', size=8, color='_rating_color' if '_rating_color' in df.columns else 'navy', alpha=0.6)
p1.add_tools(HoverTool(tooltips=[("Salary", "@Salary"), ("Output", "@output_est"), ("Rating", "@Work_Rating")]))

# Tenure vs Output
p2 = figure(title="Tenure vs Output", x_axis_label="Tenure", y_axis_label="Output (Estimated)", tools="pan,wheel_zoom,box_zoom,reset")
p2.scatter(x="Tenure", y="output_est", source=source, marker='triangle', size=8, color='_rating_color' if '_rating_color' in df.columns else 'green', alpha=0.6)
p2.add_tools(HoverTool(tooltips=[("Tenure", "@Tenure"), ("Output", "@output_est"), ("Rating", "@Work_Rating")]))

def update(attr, old, new):
    if department_select.value == "All":
        new_df = df
    else:
        new_df = df[df["Department"] == department_select.value]
    # update color mapping column if needed
    if 'Work_Rating' in new_df.columns:
        new_df = new_df.copy()
        new_df['_rating_color'] = new_df['Work_Rating'].astype(str).map(color_map)
    # copy data into existing CDS safely
    source.data = dict(ColumnDataSource(new_df).data)

department_select.on_change("value", update)

# Add a simple linear fit for Salary vs Output if both columns exist
fit_source = None
if 'Salary' in df.columns and 'output_est' in df.columns and df[['Salary','output_est']].dropna().shape[0] > 2:
    xs = df['Salary'].dropna()
    ys = df.loc[xs.index, 'output_est'].dropna()
    # align indices
    common = df[['Salary', 'output_est']].dropna()
    coeffs = np.polyfit(common['Salary'], common['output_est'], 1)
    xline = np.linspace(common['Salary'].min(), common['Salary'].max(), 50)
    yline = np.polyval(coeffs, xline)
    p1.line(xline, yline, line_color='red', line_width=2, alpha=0.7)


layout = column(department_select, row(p1, p2))
curdoc().add_root(layout)
curdoc().title = "Castle of Insights (Bokeh)"
