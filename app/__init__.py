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

app.layout = html.Div([
    html.H1('Efficient frontier visualization'),
    dcc.Slider(
        id='simulations',
        min=50,
        max=500,
        step=None,
        marks={i: str(i) for i in range(50, 501, 50)},
        value=100,
    ),
    html.Div([
        html.Div([
            dcc.Dropdown(
                id='selected',
                options=get_tickers_dict(),
                multi=True,
                placeholder='Select assets for portfolio',
            )
        ], style={'width': '60%', 'display': 'table-cell'}),
        html.Div([
            html.Button('Run optimization', id='button'),
        ], style={'width': '40%', 'display': 'table-cell'}),
    ], style={
        'width': '100%',
        'height': '50px',
        'display': 'table'
    }),
    dcc.Loading([
        html.Div(
            [html.Div(id='returns-chart'), html.Div(id='frontier-chart')],
            style={'columnCount': 2}
        )
    ])
])


@app.callback(
    [
        Output('frontier-chart', 'children'),
        Output('returns-chart', 'children')
    ],
    [Input('button', 'n_clicks')],
    [State('selected', 'value'), State('simulations', 'value')],
)
def generate_returns_chart(n_clicks, selected, simulations):
    if not selected:
        return [], []
    portfolio.assets = selected
    df = portfolio.cum_returns
    means, stds = portfolio.generate_random_portfolios(simulations)
    frontier_graph = [
        dcc.Graph(
            figure={
                'data': [
                    go.Scatter(y=means, x=stds, mode='markers', marker_size=5)
                ],
                'layout': {
                    'title': 'Generated portfolios'
                }
            })
    ]
    returns_graph = [
        dcc.Graph(
            figure={
                'data': [
                    go.Scatter(
                        y=df[asset].values, x=df[asset].index, name=asset)
                    for asset in selected
                ],
                'layout': {
                    'title': 'Historical returns',
                }
            })
    ]
    return frontier_graph, returns_graph
