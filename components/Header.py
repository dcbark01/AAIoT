import dash_html_components as html
from utils import StaticUrlPath


def Header():
    logo = html.Div([
        html.Div([
            html.Img(src=StaticUrlPath('air_alliance_logo.png'), height='150', width='150')
        ], className='two columns padded'),
        html.Div([
            html.H2('Air Alliance Houston - IoT Sensor Network', style={'font-family': 'Dosis'})
        ])
    ])
    return logo