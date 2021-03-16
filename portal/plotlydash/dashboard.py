import dash
# from dash.dependencies import Input, Output
# import dash_table
import dash_html_components as html


def init_dashboard(server):
    dash_app = dash.Dash(
        server=server,
        routes_pathname_prefix='/dashapp/',
        external_stylesheets=[
            '/static/css/main.scss.css'
        ]
    )

    dash_app.layout = html.Div(id='dash-container')

    return dash_app.server
