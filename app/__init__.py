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
    html.Div([
        html.Div([
            dcc.Dropdown(
                id='selected',
                options=get_tickers_dict(),
                multi=True,
                placeholder='Select assets for portfolio',
            )
        ], style = {'width': '60%', 'display': 'table-cell'}),
        html.Div([
            html.Button('Run optimization', id='button'),
        ], style = {'width': '40%', 'display': 'table-cell'}),
    ], style = {'width': '100%', 'height': '50px', 'display': 'table'}),
    html.Div([
        html.Div([
            dcc.Graph(id='frontier'),
        ]),
        html.Div([
            dcc.Graph(id='returns-chart'),
        ]),
    ], style={'columnCount': 2})
])


@app.callback(
    [Output('frontier', 'figure'), Output('returns-chart', 'figure')],
    [Input('button', 'n_clicks')],
    [State('selected', 'value')],
)
def generate_returns_chart(n_clicks, value):
    if not value:
        return {}, {}
    assets = value
    portfolio.assets = assets
    df = portfolio.cum_returns
    means, stds = portfolio.generate_random_portfolios(500)
    frontier_graph = {
        'data': [
            go.Scatter(y=means, x=stds, mode='markers', marker_size=5)
        ],
        'layout': {
            'title': 'Efficient frontier'
        }
    }
    returns_graph = {
        'data': [
            go.Scatter(y=df[asset].values, x=df[asset].index, name=asset)
            for asset in assets
        ],
        'layout': {
            'title': 'Returns',
            'font': {
                'color': '#fff',
            }
        }
    }
    return frontier_graph, returns_graph
