import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table_experiments as dt
import dash.dependencies
from dash.dependencies import Input, Output, State
import pandas as pd
import os

from components import Header, Footer
from utils import StaticUrlPath, StaticDataPath
from query import QuerySqlPID
from credentials.credentials import aahouston


# Generic app/deployment stuff
app = dash.Dash('AAIoT', static_folder='static')
server = app.server
if 'DYNO' in os.environ:
    app.scripts.append_script({
        'external_url': 'https://cdn.rawgit.com/chriddyp/ca0d8f02a1659981a0ea7f013a378bbd/raw/e79f3f789517deec58f41251f7dbb6bee72c44ab/plotly_ga.js'
    })


# Create controls
# TODO

# Load data - SQL database
def initialize():
    database = QuerySqlPID()
    DF_ALL = database.query_all()
    return DF_ALL


# Load data - sensor locations (hard-coded)
sensor_locations = [
                    {'DeviceIdStr': 'Device ID #1', 'DeviceIdNum': 1, 'latitude': 29.7507295, 'longitude': -95.3404711},
                    {'DeviceIdStr': 'Device ID #2', 'DeviceIdNum': 2, 'latitude': 29.761993, 'longitude': -95.366302}
]


# Create global chart template
layout = dict(
    autosize=True,
    height=500,
    font=dict(color='#CCCCCC'),
    titlefont=dict(color='#CCCCCC', size='14'),
    margin=dict(
        l=35,
        r=35,
        b=35,
        t=45
    ),
    hovermode="closest",
    plot_bgcolor="#191A1A",
    paper_bgcolor="#020202",
    legend=dict(font=dict(size=10), orientation='h'),
    title='Satellite Overview',
    mapbox=dict(
        accesstoken=aahouston.MAPBOX_API_TOKEN,
        style="dark",
        center=dict(
            lon=-78.05,
            lat=42.54
        ),
        zoom=7,
    )
)

# Create app template
app.layout = html.Div([
    html.Div([
        Header(),
    ], className='row'),
    html.Div([
        html.Div([
            dcc.Dropdown(
                id='sensor-dropdown',
                options=[
                    {'label': 'Device ID #1', 'value': 1},
                    {'label': 'Device ID #2', 'value': 2}
                ],
                value=1,
                placeholder="Please choose a sensor",
            ),
            # Create map graph
            html.Div([
                html.Div([
                    # TODO: Explanatory text/headings in this div
                ]),
                dcc.Graph(id='sensor-map')
            ]),
        ])
    ], className='row'),
    html.Div([
        html.Div([
            html.P('text1'),
        ], className='four columns'),
        html.Div([
            html.P('text2')
        ], className='four columns'),
        html.Div([
            html.P('text3')
        ], className='four columns')
    ], className='row'),
    Footer()
], className='ten columns offset-by-one')


@app.callback(Output('sensor-map', 'figure'),
              [Input('sensor-dropdown', 'value')])
def update_map_graph(value):
    zoom = 12.0
    lat_init = 29.761993
    lon_init = -95.366302
    traces = []
    trace = dict(
        type='scattermapbox',
        lat=lat_init,
        lon=lon_init,
        text='Sensor Locations',
        marker=dict(
            size=6,
            opacity=0.7,
        )
    )
    traces.append(trace)
    figure = dict(data=traces, layout=layout)
    return figure


# External CSS
external_css = ["https://cdnjs.cloudflare.com/ajax/libs/skeleton/2.0.4/skeleton.min.css",
                "//fonts.googleapis.com/css?family=Raleway:400,300,600",
                "//fonts.googleapis.com/css?family=Dosis:Medium",
                "https://cdn.rawgit.com/plotly/dash-app-stylesheets/62f0eb4f1fadbefea64b2404493079bf848974e8/dash-uber-ride-demo.css",
                "https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css"]
for css in external_css:
    app.css.append_css({"external_url": css})


@app.server.before_first_request
def load_all_data():
    global DF_ALL
    DF_ALL = initialize()


if __name__ == '__main__':
    app.server.run(debug=True)