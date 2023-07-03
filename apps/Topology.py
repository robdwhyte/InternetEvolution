from dash import dcc, html, Input, Output, ctx
import dash_bootstrap_components as dbc
import sys
from app import app

layout = html.Div([
    
    html.H1('TOPOLOGY RENDERING', style={'textAlign': 'center'}),

    html.Br(),

    html.Div(className='row', children=[
        dcc.Dropdown(
            id='dropdown_1',
            options=[{'label': str(i), 'value': str(i)} for i in range(1998, 2023)],
            value="1998",
            style={'align-items':'center', 'justify-content':'center'}
            )
    ]),

    html.Br(),
    html.Br(),

    html.Div(className="row", children=[
        dcc.RadioItems([
            "Radial-Tree Layout",
            "SFDP Layout"
            ], 
            "Radial-Tree Layout", 
            inline=True, 
            id="layout_option",
            style={'margin-left':'39%', 'align-items':'center', 'justify-content':'center'},
            inputStyle={"margin-right":"10px", "margin-left":"10px"})
    ]),
    
    html.Br(),
    html.Br(),

    html.Div(className='row', id="topology", children=[
    ],style = {'align-items':'center', 'justify-content':'center'}),

    html.Br(),
    html.Br(),

    html.Div(className="row", children=[
        dbc.Button("Download Image", id="download_button", className="d-grid gap-2 col-6 mx-auto"),
        dcc.Download(id="download_image")
    ]),

    html.Br(),
    html.Br()

],style={'max-width': '1200px', 'margin': 'auto'})

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""
    Function for returning the chosen years topology
"""
@app.callback(Output(component_id="topology", component_property="children"),
             Input(component_id="dropdown_1", component_property="value"),
             Input(component_id="layout_option", component_property="value"))

def select_images(dropdown_1, layout_option):

    if layout_option == "Radial-Tree Layout": #Radio item value
        layout_directory = "Radial_Layout"
        layout_format = "_radial.svg"
    else:
        layout_directory = "SFDP_Layout"
        layout_format = "_sfdp.svg"

    return html.Img(id="topology_render",
                    src = app.get_asset_url(f"{layout_directory}/{dropdown_1}{layout_format}"), #Dash uses asset folder for Images
                    style = {"width":"1200px", "height":"1200px"},  
                    alt=f"Topology of {dropdown_1} in {layout_option}"
                    )

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""
    Function to download the present image
"""

@app.callback(Output(component_id="download_image", component_property="data"),
              Input(component_id="download_button", component_property="n_clicks"),
              Input(component_id="topology_render", component_property="src"),
              prevent_initial_call = True,)
def download_image(n_clicks, data):

    if "download_button" == ctx.triggered_id: #If the button is clicked, download the image
        return dcc.send_file((sys.path[0] + data))

