from dash import dcc, html, Input, Output
from app import app
from apps import Macro, Micro, Topology

app.layout = html.Div([
    # Row 1: Navbar
    html.Nav(className='navbar navbar-expand-lg navbar-light bg-light', children=[
        
        html.A(className='navbar-brand', href='/apps/Macro', children='Logo'),
        
        html.Button(className='navbar-toggler', type='button',
                    **{'data-toggle': 'collapse', 'data-target': '#navbarNav', 'aria-controls': 'navbarNav',
                       'aria-expanded': 'false', 'aria-label': 'Toggle navigation'}, children=[
                html.Span(className='navbar-toggler-icon')
        ]),

        html.Div(className='collapse navbar-collapse', id='navbarNav', children=[
            html.Ul(className='navbar-nav', children=[
                html.Li(className='nav-item active', children=[
                    dcc.Link(className='nav-link', href='/apps/Macro', children='Macro')
                ]),
                html.Li(className='nav-item', children=[
                    dcc.Link(className='nav-link', href='/apps/Micro', children='Micro')
                ]),
                html.Li(className='nav-item', children=[
                    dcc.Link(className='nav-link', href='/apps/Topology', children='Topology')
                ]),
            ])
        ])
    ]),

    dcc.Location(id='url', refresh=False, pathname='apps/Macro'),
    html.Div(id='page_content', children=[]) #Children is the property that takes the output from the page callback
])

@app.callback(Output(component_id='page_content', component_property='children'),
              [Input(component_id='url', component_property='pathname')])

def display_page(pathname):
    #print(type(pathname))
    if pathname == '/apps/Macro':
        return Macro.layout
    if pathname == '/apps/Micro':
        return Micro.layout
    if pathname == '/apps/Topology':
        return Topology.layout
    else:
        return "404 Page Error"
    
if __name__ == '__main__':
    app.run_server(debug=True)