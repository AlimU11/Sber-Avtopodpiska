import dash_bootstrap_components as dbc
from dash import Dash, dcc, html
from layout import layout

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = layout


if __name__ == '__main__':
    app.run_server(
        debug=True,
        host='127.0.0.1',
        port=8080,
    )  # TODO: remove debug, change host and port
