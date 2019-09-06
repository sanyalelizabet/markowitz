# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input, State
import plotly.graph_objs as go

from app.portfolio import Portfolio
from app.data import get_tickers_dict

app = dash.Dash(__name__)
portfolio = Portfolio()

colors = {'background': '#333', 'text': '#7FDBFF'}

app.layout = html.Div([
    html.H1('Markowitz Portfolio Optimization'),
    html.Label('Select assets for portfolio'),
    dcc.Dropdown(
        id='selected',
        options=get_tickers_dict(),
        multi=True,
    ),
    html.Button('Get chart', id='button'),
    dcc.Graph(id='returns-chart')
])


@app.callback(
    Output('returns-chart', 'figure'), 
    [Input('button', 'n_clicks')],
    [State('selected', 'value')],
)
def generate_returns_chart(n_clicks, value):
    assets = value or []
    portfolio.assets = assets
    df = portfolio.get_cum_returns()
    return {
        'data': [
            go.Scatter(y=df[asset].values, x=df[asset].index, name=asset)
            for asset in assets
        ],
    }
