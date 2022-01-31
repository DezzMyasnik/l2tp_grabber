import os
from collections import deque
from pythonping import ping
import dash
import dash_daq as daq
from dash import dcc,html
#import dash_html_components as html
import plotly
from dash.dependencies import Input, Output
import plotly.express as px
import datetime
import random
from app import app
import plotly.graph_objs as go
from metaphora_2012_bot import send_sate

import platform    # For getting the operating system name
import subprocess  # For executing a shell command

def ping_some(host):
    verbose = ping(host, count=1)
    #data = verbose.readlines()
    if verbose.packet_loss == 0.0:
        return True
    else:
        return False




#X = deque(maxlen=20)
#X.append(datetime.datetime.now())

#Y = deque(maxlen=20)
#Y.append(ping('192.168.1.201'))


#app = dash.Dash(__name__, update_title=None)  # remove "Updating..." from title
#app.layout = html.Div([dcc.Graph(id='graph', figure=figure), dcc.Interval(id="interval")])





layout = html.Div([
    html.P(children='Доступность оборудования'),
    #dcc.Graph(id="line-chart"),

    html.Div(children=[
    daq.Indicator(
        id ='indicator',
        label="192.168.1.201 - Метафора",
        color="red",
        #value=False,
        ),
    daq.Indicator(
        id ='indicator_2',
        label="192.168.1.23 - Bullet База",
        color="red",
        #value=False,
        ),
    daq.Indicator(
        id ='indicator_3',
        label="192.168.1.21 - Bullet - Высотка",
        color="red",
        #value=False,
        ),
    ]),
    dcc.Interval(
            id='interval-component',
            interval=5*1000, # in milliseconds
            n_intervals=0
        )
])

state_of_201=True
# Multiple components can update everytime interval gets fired.
@app.callback(
              Output('indicator','color'),
              Output('indicator','value'),
              Input('interval-component', 'n_intervals'))
def update_graph_live(n):
    if ping_some('192.168.1.201'):
        #send_sate("201 is On")
        return ('green',True)
    #send_sate("201 is Off")
    return ('red', False)

@app.callback(
              Output('indicator_2','color'),
              Output('indicator_2','value'),
              Input('interval-component', 'n_intervals'))
def update_graph_live(n):
    if ping_some('192.168.1.23'):
        return ('green',True)

    return ('red', False)

@app.callback(
              Output('indicator_3','color'),
              Output('indicator_3','value'),
              Input('interval-component', 'n_intervals'))
def update_graph_live(n):
    if ping_some('192.168.1.23'):
        return ('green',True)

    return ('red', False)