import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd


APP_ID = 'portal_dash'
URL_BASE = '/dashboard/'
MIN_HEIGHT = 200


def dashboard(server):
    app = dash.Dash(
        server=server,
        url_base_pathname=URL_BASE,
        suppress_callback_exceptions=True,
        # external_stylesheets=[
        #     '/static/css/main.scss.css'
        # ]
    )

    df = pd.DataFrame({
        'Reagent': ['Acetonitrile', 'Acetone', 'Sodium Chloride', 'Acetic Acid', 'DMEM'],
        'Amount': [2, 1, 1, 1, 0],
        'Status': ['Open', 'Open', 'Open', 'Unopened', 'Expired']
    })

    fig = px.bar(df, x='Reagent', y='Amount', color='Status', barmode='group')

    app.layout = html.Div([
        html.H1('Welcome', className='title'),
        dcc.Graph(
            id='reagent-status',
            figure=fig
        )
    ])

    @app.callback(
        Output(component_id=f'{APP_ID}_my_output', component_property='children'),
        [Input(component_id=f'{APP_ID}_my_input', component_property='value')]
    )
    def update_output_div(input_value):
        return 'Output: {}'.format(input_value)

    return server


if __name__ == '__main__':
    from flask import Flask, render_template

    app = Flask(__name__)

    # inject Dash
    app = dashboard(app)

    @app.route(URL_BASE+'debug')
    def dash_app():
        return render_template('dashapps/dash_app_debug.html',
                               dash_url=URL_BASE,
                               min_height=MIN_HEIGHT)

    app_port = 5001
    print(f'http://localhost:{app_port}{URL_BASE}/debug')
    app.run(debug=True, port=app_port)