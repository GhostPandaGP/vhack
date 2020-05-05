import dash
import pandas as pd
from dash.dependencies import Output, Input
from dash.exceptions import PreventUpdate
import dash_html_components as html
import dash_core_components as dcc
import dash_table
import plotly.graph_objs as go
from app.get_data import download_file_from_google_drive

import schedule
import time

# подкачка новых данных
file_id = '1-4LfMPoJYxvZzK3tRHo5YJpZWhMFzYdY'
destination = 'data/cpu_data.csv'
download_file_from_google_drive(file_id, destination)

# запуск приложения
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
# app = dash.Dash(__name__)

# выгрузка данных показателя
fig = go.Figure(data=[go.Scatter(x=[1, 2, 3], y=[4, 1, 2])])

# задание вкладок
app.layout = html.Div([
    dcc.Tabs(id='tabs-example', value='tab-3', children=[
        dcc.Tab(label='Ошибки у пользователей', value='tab-1',),
        dcc.Tab(label='Статистика по пользователям', value='tab-2'),
        dcc.Tab(label='Ошибки комутаторов', value='tab-3'),
        dcc.Tab(label='Информация о комутаторе', value='tab-4'),
    ]),
    html.Div(id='tabs-example-content')
])

# ---- #
# задание тела вкладки один
# извлечение данных
df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminderDataFiveYear.csv')
countries = set(df['country'])
a = html.Div([
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

# задание типа вкладки 3
def analys():
    df.columns = ['ind', 'time', 'cpu_utilization',  'temp_slot', 'load_plat', 'number_mac','temp_plat', 'comm']
    df['status'] = '0'

    for ind, row in df.iterrows():
        if (row.temp_slot > 60 and row.temp_slot < 80) or  (row.temp_plat > 60 and row.temp_plat < 80) or  (row.cpu_utilization > 0.65 and row.cpu_utilization < 0.8) or (row.load_plat > 0.65 and row.load_plat < 0.8):
            df.iloc[ind, 8] = 1

        elif (row.temp_slot >= 80) or (row.temp_plat >= 80) or (row.cpu_utilization >= 0.8) or (row.load_plat >= 0.8) or (row.number_mac >= 10000000):
            df.iloc[ind, 8] = 2

        else:
            df.iloc[ind, 8] = 0

df = pd.read_csv('data/cpu_data.csv')
analys()
df1 = df[['comm', 'status']]
df1 = df1[df1['status'].astype(int) != 0]
print(df1.head())
df_names = df['comm'].unique()
tab3_table = html.Div([
    dcc.Store(id='com-output'),
    dcc.Dropdown(id='com-name', options=[
        {'value': x, 'label': x} for x in df_names
    ], multi=True, ),
    html.Div([
        dash_table.DataTable(
            id='com-table',
            columns=[{'name': i, 'id': i} for i in df1.columns]
        )
    ])
])

@app.callback(Output('com-output', 'data'),
              [Input('com-name', 'value')])
def filter_countries(names_selected):
    if not names_selected:
        # Return all the rows on initial load/no country selected.
        return df1.to_dict('records')

    filtered = df1.query('name in @names_selected')

    return filtered.to_dict('records')

@app.callback(Output('com-table', 'data'),
              [Input('com-output', 'data')])
def on_data_set_table(data):
    if data is None:
        raise PreventUpdate

    return data

# задание типа вкладки 4
fig41 = go.Figure(
    data=[go.Scatter(x=df['time'], y=df['cpu_utilization'])],
    layout={
        "title": "CPU Utilization"
    }
)
fig42 = go.Figure(
    data=[go.Scatter(x=df['time'], y=df['load_plat'])],
    layout={
        "title": "Load plat"
    }
)
fig43 = go.Figure(
    data=[go.Scatter(x=df['time'], y=df['temp_slot'])],
    layout={
        "title": "Temp Slot"
    }
)
fig44 = go.Figure(
    data=[go.Scatter(x=df['time'], y=df['temp_plat'])],
    layout={
        "title": "Temp plat"
    }
)
fig45 = go.Figure(
    data=[go.Scatter(x=df['time'], y=df['number_mac'])],
    layout={
        "title": "Number mac"
    }
)
tab4 = html.Div([
    dcc.Graph(
        id='t4-graph1',
        figure=fig41,
    ),
    dcc.Graph(
        id='t4-graph2',
        figure=fig42,
    ),
    dcc.Graph(
        id='t4-graph3',
        figure=fig43,
    ),
    # html.Div(
    #     style='display: flex;',
    #     children=[
    #         html.Div(
    #             style='',
    #             children=[
    #                 dcc.Graph(
    #                     id='t4-graph3',
    #                     figure=fig43,
    #                 ),
    #             ]
    #         ),
    #     ]
    # ),
    dcc.Graph(
        id='t4-graph4',
        figure=fig44,
    ),
    dcc.Graph(
        id='t4-graph5',
        figure=fig45,
    ),
])

# переключение между вкладками
@app.callback(Output('tabs-example-content', 'children'),
              [Input('tabs-example', 'value')])
def render_content(tab):
    if tab == 'tab-1':
        return html.Div([
            a
        ])
    elif tab == 'tab-2':
        return html.Div([
            dcc.Graph(
                id='example-graph-2',
                figure=fig
            )
        ])
    elif tab == 'tab-3':
        return html.Div([
            tab3_table
        ])
    elif tab == 'tab-4':
        return html.Div([
            tab4,
        ])

if __name__ == '__main__':
    app.run_server(debug=False, threaded=True, port=10450)

    schedule.every(20).seconds.do(analys)
    while True:
        download_file_from_google_drive(file_id, destination)
        schedule.run_pending()
        time.sleep(1)

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
