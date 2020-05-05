import collections
import dash
import pandas as pd

from dash.dependencies import Output, Input
from dash.exceptions import PreventUpdate

import dash_html_components as html
import dash_core_components as dcc
import dash_table

app = dash.Dash(__name__)

df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminderDataFiveYear.csv')

countries = set(df['country'])


app.layout = html.Div([
    dcc.Store(id='memory-output'),
    dcc.Dropdown(id='memory-countries', options=[
        {'value': x, 'label': x} for x in countries
    ], multi=True, value=['Canada', 'United States']),
    dcc.Dropdown(id='memory-field', options=[
        {'value': 'lifeExp', 'label': 'Life expectancy'},
        {'value': 'gdpPercap', 'label': 'GDP per capita'},
    ], value='lifeExp'),
    html.Div([
        dash_table.DataTable(
            id='memory-table',
            columns=[{'name': i, 'id': i} for i in df.columns]
        ),
    ])
])


@app.callback(Output('memory-output', 'data'),
              [Input('memory-countries', 'value')])
def filter_countries(countries_selected):
    if not countries_selected:
        # Return all the rows on initial load/no country selected.
        return df.to_dict('records')

    filtered = df.query('country in @countries_selected')

    return filtered.to_dict('records')


@app.callback(Output('memory-table', 'data'),
              [Input('memory-output', 'data')])
def on_data_set_table(data):
    if data is None:
        raise PreventUpdate

    return data


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    dcc.Tabs(id='tabs-example', value='tab-1', children=[
        dcc.Tab(label='Tab one', value='tab-1'),
        dcc.Tab(label='Tab two', value='tab-2'),
    ]),
    html.Div(id='tabs-example-content')
])

@app.callback(Output('tabs-example-content', 'children'),
              [Input('tabs-example', 'value')])
def render_content(tab):
    if tab == 'tab-1':
        return html.Div([
            html.H3('Tab content 1')
        ])
    elif tab == 'tab-2':
        return html.Div([
            html.H3('Tab content 2')
        ])

if __name__ == '__main__':
    app.run_server(debug=True, threaded=True, port=10450)


"""# -*- coding: utf-8 -*-

# Загрузим необходимые пакеты
import dash
import dash_core_components as dcc
import dash_html_components as html
from get_data import download_file_from_google_drive


file_id = '11MyDo3_uwNfdm_c_-73MA1gjTrfESUAv'
destination = '/home/varykha/Documents/vhack/data/cpu_utilization.csv'
download_file_from_google_drive(file_id, destination)

#  Объяснение данных строк пока опускается, будет объяснено далее
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    html.H1(children='Hello Dash'),

    html.Div(children='''
        Dash: A web application framework for Python.
    '''),

    dcc.Graph(
        id='example-graph',
        figure={
            'data': [
                {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
                {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': u'Montréal'},
            ],
            'layout': {
                'title': 'Dash Data Visualization'
            }
        }
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)"""
