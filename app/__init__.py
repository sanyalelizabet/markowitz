# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go

from app.core import Portfolio

TICKERS = ['AAPL', 'AMZN', 'FB']
portfolio = Portfolio(['AAPL', 'AMZN', 'FB'])
df = portfolio.get_cum_returns()

app = dash.Dash(__name__)

colors = {'background': '#333', 'text': '#7FDBFF'}

app.layout = html.Div(
    style={'backgroundColor': colors['background']},
    children=[
        html.H1(
            children='Markowitz Portfolio Optimization',
            style={
                'textAlign': 'center',
                'color': colors['text']
            }),
        html.Div(
            children='Visualize portfolio allocations \
            for different risk levels',
            style={
                'textAlign': 'center',
                'color': colors['text']
            }),
        dcc.Graph(
            id='asset-prices',
            figure={
                'data': [
                    go.Scatter(
                        y=df[asset].values,
                        x=df[asset].index,
                        name=asset
                    ) for asset in df.columns
                ],
                'layout': {
                    'plot_bgcolor': colors['background'],
                    'paper_bgcolor': colors['background'],
                    'font': {
                        'color': colors['text']
                    }
                }
            })
    ])
