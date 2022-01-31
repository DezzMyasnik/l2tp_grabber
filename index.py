from dash import dcc, html
#import dash_html_components as html
from dash.dependencies import Input, Output

from app import app
from apps import app1, app2, app3

menu_li = [html.Li(className='menu-children', children=[dcc.Link('К перехвату сообщений', href='/apps/app1')]),
           html.Li(className='menu-children', children=[dcc.Link('К статистике СМС сообщений', href='/apps/app2')]),
           html.Li(className='menu-children', children=[dcc.Link('Доступность оборудования', href='/apps/app3')]),
           #html.Li(className='menu-children', children=[dcc.Link('К управлению ботом', href='/apps/app4')]),
           #html.Li(className='menu-children', children=[dcc.Link('К настройкам', href='/apps/app5')])
           ]

app.layout = html.Div(children=[
    dcc.Location(id='url', refresh=False),

    html.Footer(id='menu',
                children=[html.Ul(className='main-menu',
                            children=menu_li
                                      )
                              ]
                    ),

    html.Div(id='page-content'),
    ])


@app.callback(Output('page-content', 'children'),
              Input('url', 'pathname'))
def display_page(pathname):
    if pathname == '/apps/app1':
        app.layout
        return app1.layout
    elif pathname == '/apps/app2':
        return app2.layout
    elif pathname == '/apps/app3':
        return app3.layout
    #elif pathname == '/apps/app4':
    #    return app4.layout
    #elif pathname == '/apps/app5':
    #    return app5.layout
    elif pathname == '/':
       return app1.layout
    else:
        return '404'

if __name__ == '__main__':
    app.run_server(host='127.0.0.1',debug=True, port=8050)