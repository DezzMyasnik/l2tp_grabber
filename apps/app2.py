
from dash import  dcc, html
from dash import dash_table as dt
import init_db
import dash
from dash.dependencies import Output, Input
import plotly
from app import app
import plotly.express as px
#import dash_table as dt

import pandas as pd


with init_db.db_session:
    #frome_phones = list(init_db.distinct(o.From_phone_num for o in init_db.SMS_text))
    df = pd.read_sql('Select To_phone_num,count(*) from SMS_text group by To_phone_num order by count(*) DESC', init_db.db.get_connection())
    #count=df.shape[0]
#stat = df[''].value_counts()
#br =  [{'label': i, 'value': i} for i in frome_phones]
#PAGE_SIZE = 20
layout = html.Div(children=[
    html.Div(id='app-2-display-value'),
    html.H1(children='Статистика входящих СМС сообщений'),
    html.Div(id='dd-output-container_2'),
    dt.DataTable(id='table_of_phones',
                 columns=[{"name": i, "id": i} for i in df.columns],
                 # fill_width=True,
                 style_cell={
                     # 'whiteSpace': 'normal',
                     # 'height': 'auto',
                     'textAlign': 'left',
                 },
                 style_table={
                     'width': '450px',
                     'position': 'relative',
                     'left': '35%'
                 },
                 style_header={
                     'backgroundColor': 'rgb(230, 230, 230)',
                     'fontWeight': 'bold'
                 },
                 # page_current=0,
                 #data=df,
                 ),
    dcc.Interval(
            id='interval-component_2',
            interval=5 * 1000,  # in milliseconds
            n_intervals=0
        )
    #html.Button('Add Row', id='editing-rows-button', n_clicks=0),

])

@app.callback(
    Output('table_of_phones', 'data'),
    Input('interval-component_2', 'n_intervals')
)
def update_table(n): #filter
    with init_db.db_session:
        df = pd.read_sql('Select To_phone_num,count(*) from SMS_text group by To_phone_num order by count(*) DESC',
                         init_db.db.get_connection())

    #page_size = pp_size
    return df.to_dict('records')