# Efficient frontier visualization

## Description

This tool plots efficient frontier for selected assets. Currently, User can choose assets from the S&P 500 constituents list. Algorithm will generate randomly weighted portfolios from the selected list of stocks. Expected return and standard deviation are being calculated for resulting portfolios based on historical prices for selected securities (downloaded from Quandl). Final values are visualized using plotly's Scatter chart.

## Technologies used

- Dash, Plotly
- Pandas
- Quandl python api
- Bulma
