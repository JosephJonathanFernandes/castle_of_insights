import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
from data_loader import load_data
import pkgutil
import importlib.util

# Compatibility shim for environments missing pkgutil.find_loader
if not hasattr(pkgutil, "find_loader"):
    def _find_loader(name):
        spec = importlib.util.find_spec(name)
        return spec.loader if spec is not None else None
    pkgutil.find_loader = _find_loader


df = load_data()

app = dash.Dash(__name__)


def _summary_cards(df):
    total = len(df)
    avg_tenure = df["Tenure"].dropna().mean() if "Tenure" in df.columns else None
    avg_output = df["output_est"].dropna().mean() if "output_est" in df.columns else None
    return html.Div([
        html.Div([html.H4("Headcount"), html.P(f"{total}")], style={"padding": "8px", "flex": "1", "border": "1px solid #ddd", "textAlign": "center"}),
        html.Div([html.H4("Avg Tenure"), html.P(f"{avg_tenure:.1f} yrs" if avg_tenure is not None else "N/A")], style={"padding": "8px", "flex": "1", "border": "1px solid #ddd", "textAlign": "center"}),
        html.Div([html.H4("Avg Output"), html.P(f"{avg_output:.1f}" if avg_output is not None else "N/A")], style={"padding": "8px", "flex": "1", "border": "1px solid #ddd", "textAlign": "center"}),
    ], style={"display": "flex", "gap": "8px", "marginBottom": "12px"})


app.layout = html.Div([
    html.H2("Castle of Insights Dashboard (Dash + Plotly)"),
    _summary_cards(df),

    # filters row
    html.Div([
        html.Div([
            html.Label("Department"),
            dcc.Dropdown(
                id='dept-filter',
                options=[{'label': d, 'value': d} for d in sorted(df['Department'].dropna().unique())] if 'Department' in df.columns else [],
                value=[],
                multi=True
            )
        ], style={"flex":1}),
        html.Div([
            html.Label("Tenure Group"),
            dcc.Dropdown(
                id='tenure-filter',
                options=[{'label': t, 'value': t} for t in df['TenureGroup'].cat.categories] if 'TenureGroup' in df.columns and hasattr(df['TenureGroup'], 'cat') else [],
                value=[],
                multi=True
            )
        ], style={"flex":1}),
        html.Div([
            html.Label("Company Origin"),
            dcc.Dropdown(
                id='company-filter',
                options=[{'label': c, 'value': c} for c in sorted(df['Company_Origin'].dropna().unique())] if 'Company_Origin' in df.columns else [],
                value=[],
                multi=True
            )
        ], style={"flex":1}),
    ], style={"display":"flex", "gap":"10px", "marginBottom":"20px"}),

    # charts
    dcc.Graph(id='company-pie'),
    dcc.Graph(id='rating-bar'),
    dcc.Graph(id='tenure-bar'),

    html.Hr(),
    html.H4("Bokeh interactive view"),
    html.Iframe(src="http://localhost:5006/bokeh_dashboard", width="100%", height="620")
])


@app.callback(
    [Output('company-pie', 'figure'),
     Output('rating-bar', 'figure'),
     Output('tenure-bar', 'figure')],
    [Input('dept-filter', 'value'), Input('tenure-filter', 'value'), Input('company-filter', 'value')]
)
def update_graphs(selected_depts, selected_tenures, selected_companies):
    dff = df.copy()
    if selected_depts:
        dff = dff[dff['Department'].isin(selected_depts)]
    if selected_tenures:
        dff = dff[dff['TenureGroup'].isin(selected_tenures)]
    if selected_companies:
        dff = dff[dff['Company_Origin'].isin(selected_companies)]

    # safe fig creation
    fig1 = px.pie(dff, names='Company_Origin', title='Company Split') if 'Company_Origin' in dff.columns else {}
    fig2 = px.histogram(dff, x='Work_Rating', color='Work_Rating', title='Performance Distribution') if 'Work_Rating' in dff.columns else {}
    fig3 = px.histogram(dff, x='TenureGroup', color='Work_Rating', title='Tenure Experience Distribution') if 'TenureGroup' in dff.columns else {}

    # small layout tweak
    try:
        fig3.update_layout(bargap=0.2)
    except Exception:
        pass

    return fig1, fig2, fig3


if __name__ == '__main__':
    # Run without Dash dev tools which call pkgutil.find_loader and may
    # trigger compatibility issues in some environments. Disable dev tools
    # explicitly to be safe during local runs.
    app.run(debug=False, dev_tools_ui=False, dev_tools_props_check=False)
