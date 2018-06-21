import dash_html_components as html
from utils import StaticUrlPath


def Footer():
    footer = html.Div([
        html.Div([
            html.Div([html.Img(src=StaticUrlPath('txrx_logo.png'), height='101', width='81')])
        ], className='two columns'),
        html.Div([
            html.Div([html.Img(src=StaticUrlPath('quiddity_logo.png'), height='101', width='275')])
        ], className='five columns'),
        html.Div([
            html.Div([html.Img(src=StaticUrlPath('january_advisors_logo.png'), height='101', width='101')])
        ], className='two columns'),
        html.Div([
            html.Div([html.Img(src=StaticUrlPath('att_foundry_logo.png'), height='101', width='175')])
        ], className='three columns')
    ], className='row')
    return footer