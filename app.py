from datetime import datetime

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
from dash.dependencies import Input, Output

import models.models as md
from utils import day_to_range

app = dash.Dash(__name__)

server = app.server 

colors = {"background": "#ffffff", "text": "#111111"}

app.layout = html.Div(
    style={"backgroundColor": colors["background"]},
    children=[
        html.H1(
            children="Bars Dashboard",
            style={"textAlign": "center", "color": colors["text"]},
        ),
        dcc.Checklist(
            id="toggle-rangeslider",
            options=[{"label": "Include Rangeslider", "value": "slider"}],
            value=["slider"],
        ),
        dcc.Graph(id="graph"),
        html.Label("Stock:"),
        dcc.Dropdown(
            id="paper",
            options=[
                {"label": name.name, "value": name.ticker}
                for name in md.StocksNames.get_stock_names()
            ],
            value=md.StocksNames.get_first_ticker(),
        ),
        html.Label("Day:"),
        dcc.Dropdown(
            id="date",
            options=[
                {"label": date, "value": date}
                for date in md.StocksAggregates.get_days("AAPL")
            ],
            value=md.StocksAggregates.get_first_day(md.StocksNames.get_first_ticker()),
        ),
    ],
)


@app.callback(
    [Output("graph", "figure"), Output("date", "options")],
    [
        Input("toggle-rangeslider", "value"),
        Input(component_id="paper", component_property="value"),
        Input(component_id="date", component_property="value"),
    ],
)
def display_candlestick(toggle_rangeslider_value, paper_value, date_value):

    ctx = dash.callback_context

    if ctx.triggered:
        input_id = ctx.triggered[0]["prop_id"].split(".")[0]
    else:
        input_id = None

    days = md.StocksAggregates.get_days(paper_value)
    date = [{"label": date, "value": date} for date in days]
    if input_id == "date":
        from_, to = day_to_range(date_value)
    else:
        from_, to = day_to_range(days[0] if len(days) > 0 else "1999-01-01")
    data = md.StocksAggregates.get_stock_aggregates(paper_value, from_, to)
    fig = go.Figure(
        go.Candlestick(
            x=[df.timestamp for df in data],
            open=[df.open for df in data],
            high=[df.highest for df in data],
            low=[df.lowest for df in data],
            close=[df.close for df in data],
        )
    )
    fig.update_layout(xaxis_rangeslider_visible="slider" in toggle_rangeslider_value)

    return fig, date


if __name__ == "__main__":
    app.run_server(debug=True, host='0.0.0.0', port=8080) 
