import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import pandas as pd

df = pd.read_csv("Titanic-Dataset.csv")

app = dash.Dash(__name__)
server = app.server  # Required for Render deployment

app.layout = html.Div(style={"fontFamily": "Arial", "padding": "20px", "backgroundColor": "#f9f9f9"}, children=[

    html.H1("🚢 Titanic Data Dashboard", style={"textAlign": "center", "color": "#2c3e50"}),

    # --- Filters ---
    html.Div(style={"display": "flex", "gap": "40px", "marginBottom": "30px", "justifyContent": "center"}, children=[

        html.Div([
            html.Label("Passenger Class:", style={"fontWeight": "bold"}),
            dcc.Dropdown(
                id="class-dropdown",
                options=[{"label": f"Class {i}", "value": i} for i in sorted(df["Pclass"].unique())],
                value=None,
                placeholder="All Classes",
                clearable=True,
                style={"width": "200px"}
            )
        ]),

        html.Div([
            html.Label("Age Range:", style={"fontWeight": "bold"}),
            dcc.RangeSlider(
                id="age-slider",
                min=0, max=80, step=5,
                marks={i: str(i) for i in range(0, 81, 10)},
                value=[0, 80],
                tooltip={"placement": "bottom"}
            )
        ], style={"width": "400px"}),

    ]),

    # --- Charts ---
    html.Div(style={"display": "flex", "gap": "20px"}, children=[
        dcc.Graph(id="survival-bar", style={"flex": "1"}),
        dcc.Graph(id="age-histogram", style={"flex": "1"}),
    ]),

])


@app.callback(
    Output("survival-bar", "figure"),
    Output("age-histogram", "figure"),
    Input("class-dropdown", "value"),
    Input("age-slider", "value"),
)
def update_charts(selected_class, age_range):
    filtered = df[(df["Age"] >= age_range[0]) & (df["Age"] <= age_range[1])]
    if selected_class:
        filtered = filtered[filtered["Pclass"] == selected_class]

    # Chart 1: Survival rate by gender
    survival = filtered.groupby(["Sex", "Survived"]).size().reset_index(name="Count")
    survival["Survived"] = survival["Survived"].map({0: "Did Not Survive", 1: "Survived"})
    fig1 = px.bar(
        survival, x="Sex", y="Count", color="Survived", barmode="group",
        title="Survival Count by Gender",
        color_discrete_map={"Survived": "#2ecc71", "Did Not Survive": "#e74c3c"},
        template="plotly_white"
    )

    # Chart 2: Age distribution by survival
    filtered2 = filtered.copy()
    filtered2["Survived"] = filtered2["Survived"].map({0: "Did Not Survive", 1: "Survived"})
    fig2 = px.histogram(
        filtered2, x="Age", color="Survived", nbins=20, barmode="overlay",
        title="Age Distribution by Survival",
        color_discrete_map={"Survived": "#2ecc71", "Did Not Survive": "#e74c3c"},
        template="plotly_white", opacity=0.7
    )

    return fig1, fig2


if __name__ == "__main__":
    app.run(debug=True)
    