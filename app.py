# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input, State
import plotly.graph_objs as go

from portfolio import Portfolio
from data import get_tickers_dict

app = dash.Dash(__name__)

portfolio = Portfolio()

app.layout = html.Div([
    html.H1(
        'Efficient frontier visualization dashboard',
        className='title has-text-centered',
    ),
    html.Div([
        html.Div([
            html.Div([
                html.Label(
                    'Asset universe',
                    className='label'
                ),
                dcc.Dropdown(
                    id='selected',
                    options=get_tickers_dict(),
                    multi=True,
                    placeholder='Select several assets',
                    className='control'
                ),
            ], className='field'),
            html.Div([
                html.Label(
                    'Number of scenarios',
                    className='label'
                ),
                dcc.Slider(
                    id='simulations',
                    min=100,
                    max=1000,
                    step=None,
                    marks={i: str(i) for i in range(100, 1001, 100)},
                    value=100,
                    className='control'
                ),
            ], className='field'),
            html.Div([
                html.Div([
                    html.Button(
                        'Generate',
                        id='button',
                        className='button is-primary')
                ], className='control'),
            ], className='field'),
        ], className='column'),
        html.Div([
            html.Div([
                dcc.Markdown('''
                    This application generates n portfolios with random weights
                    from a specified list of financial assets. For each
                    portfolio expected return and standard deviation are being
                    calculated and the resulting values are visualized on a
                    graph.

                    Historical adjusted close values are retrieved from Quandl.
                ''', className='message-body')
            ], className='message is-primary'),
        ], className='column'),
    ], className='columns'),
    dcc.Loading([
        html.Div(
            [
                html.Div(id='returns-chart', className="column"),
                html.Div(id='frontier-chart', className="column")
            ],
            className="columns"
        )
    ])
], className="container")


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
                    go.Scatter(
                        x=stds,
                        y=means,
                        mode='markers',
                        marker_size=5,
                        name='Random',
                    )
                ],
                'layout': {
                    'title': 'Generated portfolios',
                    'xaxis': {'title': 'Standard deviation (ann.)'},
                    'yaxis': {'title': 'Expected return (ann.)'},
                }
            })
    ]
    returns_graph = [
        dcc.Graph(
            figure={
                'data': [
                    go.Scatter(
                        x=df[asset].index,
                        y=df[asset].values,
                        name=asset
                    )
                    for asset in selected
                ],
                'layout': {
                    'title': 'Historical returns',
                    'xaxis': {'title': 'Date'},
                    'yaxis': {'title': 'Cumulative return (%)'},
                }
            })
    ]
    return frontier_graph, returns_graph


if __name__ == '__main__':
    app.run_server(debug=True)
