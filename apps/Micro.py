from dash import dcc, html, Input, Output, dash_table
import polars as pl
import pandas as pd
import os, csv, sys
from app import app

layout = html.Div([
    
    html.H1('MICRO COMPARISON', style={'textAlign': 'center'}),

    html.Br(),

    html.H4('ASN Presence', style={'textAlign': 'center'}),

    html.Br(),

    html.Div(className='row', children=[
        html.Div(className='col-3', children=[
            dcc.Input(id="input1",
                        type = "text",
                        placeholder="Enter ASN",
                        debounce=True),
        ]),
        html.Div(className='col-9', id="year_list", children=[
        ])
    ]),

    html.Br(),
    html.Br(),
    
    html.Div(className='row', children=[
        html.Div(className='row', children=[
            html.Div(className='col-6', children=[
                dcc.Dropdown(
                    id='dropdown_1',
                    options=[{'label': str(i), 'value': str(i)} for i in range(1998, 2023)],
                    value="1998"
                    )
            ]),
            html.Div(className='col-6', children=[
                dcc.Dropdown(
                    id='dropdown_2',
                    options=[{'label': str(i), 'value': str(i)} for i in range(1998, 2023)], 
                    value="2022"
                    )
            ])
        ])
    ]),
    
    html.Br(),

    html.Div(className='row justify-content-center', children=[
        dcc.Dropdown(
                id = 'dropdown_3',
                options=[], 
                style={'margin':'auto'},
                value=3356
                )
    ],style={'width':'20%', 'display':'inline-block', 'display':'flex', 'margin-left':'39%', 'align-items':'center', 'justify-content':'center'}),

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    html.Br(),
    html.Br(),

    html.H3(f'Centrality Scores', style={'textAlign': 'center'}),
    html.Div(className='row', children=[
        html.Div(className='column', style={'width': '100%'}, id='centrality_scores', children=[
        ])
    ]),

    html.Br(),
    html.Br(),

    html.H3('Relationship Statistics', style={'textAlign': 'center'}),
    html.Div(className='row', children=[
        html.Div(className='column', style={'width': '100%'}, id='relationship_statistics', children=[
        ])
    ]),

    html.Br(),
    html.Br(),

    html.Div([
        html.Div(className='row', children=[
            html.H3('Providers', style={'textAlign': 'center'}),
        ]),
        html.Div(className='row', children=[
            html.Div(className='column', style={'width': '50%'}, id="prov_1", children=[
            ]),
            html.Div(className='column', style={'width': '50%'}, id="prov_2", children=[
            ])
        ])
    ]),
    
    html.Div(className='row', children=[
        html.Div(className='column', style={'width': '50%'}, id='provider_rels_year_1', children=[
        ]),
        html.Div(className='column', style={'width': '50%'}, id='provider_rels_year_2', children=[
        ])
    ]),

    html.Br(),
    html.Br(),

    html.Div([
        html.Div(className='row', children=[
            html.H3('Customers', style={'textAlign': 'center'}),
        ]),
        html.Div(className='row', children=[
            html.Div(className='column', style={'width': '50%'}, id="cust_1", children=[
            ]),
            html.Div(className='column', style={'width': '50%'}, id="cust_2", children=[
            ])
        ])
    ]),
    
    html.Div(className='row', children=[
        html.Div(className='column', style={'width': '50%'}, id='customer_rels_year_1', children=[
            ]),
        html.Div(className='column', style={'width': '50%'}, id='customer_rels_year_2', children=[
            ])
    ]),

    html.Br(),
    html.Br(),

    html.Div([
        html.Div(className='row', children=[
            html.H3('Peers', style={'textAlign': 'center'}),
        ]),
        html.Div(className='row', children=[
            html.Div(className='column', style={'width': '50%'}, id="peer_1", children=[
            ]),
            html.Div(className='column', style={'width': '50%'}, id="peer_2", children=[
            ])
        ])
    ]),

    html.Div(className='row', children=[
    html.Div(className='column', style={'width': '50%'}, id='peer_rels_year_1', children=[
        ]),
    html.Div(className='column', style={'width': '50%'}, id='peer_rels_year_2', children=[
        ])
    ]),

    html.Br(),
    html.Br(),

],style={'max-width': '1200px', 'margin': 'auto'})


def read_csv(input_year_1, input_year_2):
    i = pl.read_csv(f"Datasets/MicroYears/{input_year_1}_micro.csv")
    j = pl.read_csv(f"Datasets/MicroYears/{input_year_2}_micro.csv")

    return i, j

def read_edge_csv(input_year_1, input_year_2):
    
    l = pl.read_csv(f"Datasets/EdgeLists/output_{input_year_1}_E.csv")
    p = pl.read_csv(f"Datasets/EdgeLists/output_{input_year_2}_E.csv")

    return l, p

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#RELATIONSHIP QUERY FUNCTIONS

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def identify_asn_customers(input_year_1, input_year_2, chosen_node):

    """
    Function for finding ASN customers
    Arguments:
        INT input_year_1: year of first dropdown
        INT input_year_2: year of second dropdown
        INT chosen_node: the ASN the user has requested
    Returns:
        DataFrame asp_count_1: first year ASN customers
        DataFrame asp_count_2: second year ASN customers
    """
    
    l, p = read_edge_csv(input_year_1, input_year_2)

    #Find all customers of an AS
    #If the seleted ASN is in the ASP column and the REL == -1, then whats left are the ASes Customers
    asp_count_1 = l.filter((pl.col('ASP') == chosen_node) & (pl.col('REL') == -1)) 
    asp_count_2 = p.filter((pl.col('ASP') == chosen_node) & (pl.col('REL') == -1)) 

    return asp_count_1, asp_count_2

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    """
    Function for finding ASN providers
    """

def identify_asn_providers(input_year_1, input_year_2, chosen_node):
    
    l, p = read_edge_csv(input_year_1, input_year_2)

    asc_count_1 = l.filter((pl.col('ASC') == chosen_node) & (pl.col('REL') == -1)) #If the seleted AS is in the ASC column and the REL == -1, then whats left are the ASes Providers
    asc_count_2 = p.filter((pl.col('ASC') == chosen_node) & (pl.col('REL') == -1))

    return asc_count_1, asc_count_2

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    """
    Function for finding ASN peers
    """

def identify_asn_peers(input_year_1, input_year_2, chosen_node):
    
    l, p = read_edge_csv(input_year_1, input_year_2)

    peer_count_1 = l.filter((pl.col('ASP') == chosen_node) & (pl.col('REL') == 0) | (pl.col('ASC') == chosen_node) & (pl.col('REL') == 0)) #If the AS is in either ASP or ASC and the REL == 0 than these are peers
    peer_count_2 = p.filter((pl.col('ASP') == chosen_node) & (pl.col('REL') == 0) | (pl.col('ASC') == chosen_node) & (pl.col('REL') == 0))

    return peer_count_1, peer_count_2

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#TABLE DATA

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    """
    Function for generating ASN centrality table data
    """

def generate_nodal_centrality(input_year_1, input_year_2, chosen_node):
    
    i, j = read_csv(input_year_1, input_year_2)

    centrality_1 = i.filter(pl.col('ASN') == chosen_node).select(["Degree-C", "Betweenness-C", "Closeness-C", "Eigenvector-C"]) #Select the specific Centrality scores of an AS
    centrality_2 = j.filter(pl.col('ASN') == chosen_node).select(["Degree-C", "Betweenness-C", "Closeness-C", "Eigenvector-C"])

    combined_centrality = pl.concat([centrality_1, centrality_2], how="vertical") #Stack both years to cread a single DF
    id_df = pl.DataFrame({"Year": [input_year_1, input_year_2], "ASN": [chosen_node, chosen_node]}) #Add ASN for clarity
    nodal_centrality_df = pl.concat([id_df, combined_centrality],how="horizontal")

    return nodal_centrality_df

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    """
    Function for generating ASN relationship statistics table data
    """

def generate_nodal_statistics(input_year_1, input_year_2, chosen_node):

    i, j = read_csv(input_year_1, input_year_2)

    tier_status_1 = i.filter(pl.col('ASN') == chosen_node).select(["tier"]).to_series().to_list() #Select Tier of AS
    tier_status_2 = j.filter(pl.col('ASN') == chosen_node).select(["tier"]).to_series().to_list()

    asp_count_1, asp_count_2 = identify_asn_providers(input_year_1, input_year_2, chosen_node) #Retrieve Providers
    asc_count_1, asc_count_2 = identify_asn_customers(input_year_1, input_year_2, chosen_node) #Retrieve Customers
    peer_count_1, peer_count_2 = identify_asn_peers(input_year_1, input_year_2, chosen_node)   #Retrieve Peers

    asc_1 = asc_count_1.drop("ASC", "REL").to_series().to_list().count(chosen_node) #Count how many times the AS is recorded to get total number of Customers
    asc_2 = asc_count_2.drop("ASC", "REL").to_series().to_list().count(chosen_node)

    asp_1 = asp_count_1.drop("ASP", "REL").to_series().to_list().count(chosen_node) #Count how many times the AS is recorded to get total number of Providers
    asp_2 = asp_count_2.drop("ASP", "REL").to_series().to_list().count(chosen_node)

    peer_1 = peer_count_1.drop("ASP", "ASC").to_series().to_list().count(0) #Count Peer connections
    peer_2 = peer_count_2.drop("ASP", "ASC").to_series().to_list().count(0)

    #merge results
    asps = asp_1, asp_2
    ascs = asc_1, asc_2
    peers = peer_1, peer_2
    tiers = tier_status_1[0], tier_status_2[0]

    relationship_statistics_df = pl.DataFrame({
        "Year": [input_year_1, input_year_2],
        "ASN": [chosen_node, chosen_node],
        "Providers Count": asps,
        "Customer Count": ascs,
        "Peer Count": peers,
        "Tier": tiers
    })

    return relationship_statistics_df

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    """
    Function for generating providers list table year 1 data
    """

def generate_providers_list_year_1(input_year_1, input_year_2, chosen_node):

    asp_count_1, asp_count_2 = identify_asn_providers(input_year_1, input_year_2, chosen_node)
    asp_count_2 = None #reclaim waisted memory

    asn_providers_year_1_df = asp_count_1.drop("ASC", "REL") #All providers of year 1

    n_rows, n_cols = asn_providers_year_1_df.shape
    if n_rows < 10:
        df_fill = pl.DataFrame({
            "ASP": [0] * (10 - n_rows) #if there is less than 10 rows, fill with 0s to keep table shape
        })
        asn_providers_year_1_df = pl.concat([asn_providers_year_1_df, df_fill], how="vertical")
   
    return asn_providers_year_1_df

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    """
    Function for generating providers list table year 2 data
    """

def generate_providers_list_year_2(input_year_1, input_year_2, chosen_node):

    asp_count_1, asp_count_2 = identify_asn_providers(input_year_1, input_year_2, chosen_node)
    asp_count_1 = None

    asn_providers_year_2_df = asp_count_2.drop("ASC", "REL") #All providers of year 2

    n_rows, n_cols = asn_providers_year_2_df.shape
    if n_rows < 10:
        df_fill = pl.DataFrame({
            "ASP": [0] * (10 - n_rows)
        })
        asn_providers_year_2_df = pl.concat([asn_providers_year_2_df, df_fill], how="vertical")
   
    return asn_providers_year_2_df
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    """
    Function for generating customers list table year 1 data
    """

def generate_customers_list_year_1(input_year_1, input_year_2, chosen_node):

    asc_count_1, asc_count_2 = identify_asn_customers(input_year_1, input_year_2, chosen_node)
    asc_count_2 = None

    asn_customers_year_1_df = asc_count_1.drop("ASP", "REL") #All customers of year 1

    n_rows, n_cols = asn_customers_year_1_df.shape
    if n_rows < 10:
        df_fill = pl.DataFrame({
            "ASC": [0] * (10 - n_rows)
        })
        asn_customers_year_1_df = pl.concat([asn_customers_year_1_df, df_fill], how="vertical")
   
    return asn_customers_year_1_df
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    """
    Function for generating customers list table year 2 data
    """

def generate_customers_list_year_2(input_year_1, input_year_2, chosen_node):
    
    asc_count_1, asc_count_2 = identify_asn_customers(input_year_1, input_year_2, chosen_node)
    asc_count_1 = None

    asn_customers_year_2_df = asc_count_2.drop("ASP", "REL") #All customers of year 2

    n_rows, n_cols = asn_customers_year_2_df.shape
    if n_rows < 10:
        df_fill = pl.DataFrame({
            "ASC": [0] * (10 - n_rows)
        })
        asn_customers_year_2_df = pl.concat([asn_customers_year_2_df, df_fill], how="vertical")
   
    return asn_customers_year_2_df
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    """
    Function for generating peer list table year 1 data
    """

def generate_peer_list_year_1(input_year_1, input_year_2, chosen_node):
    
    peer_count_1, peer_count_2 = identify_asn_peers(input_year_1, input_year_2, chosen_node)
    peer_count_2 = None

    asn_peers_year_1_df = peer_count_1.drop("REL") #All peers of year 1

    n_rows, n_cols = asn_peers_year_1_df.shape
    if n_rows < 10:
        df_fill = pl.DataFrame({
            "ASP": [0] * (10 - n_rows),
            "ASC": [0] * (10 - n_rows)
        })
        asn_peers_year_1_df = pl.concat([asn_peers_year_1_df, df_fill], how="vertical")
   
    return asn_peers_year_1_df
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    """
    Function for generating peer list table year 2 data
    """

def generate_peer_list_year_2(input_year_1, input_year_2, chosen_node):
    
    peer_count_1, peer_count_2 = identify_asn_peers(input_year_1, input_year_2, chosen_node)
    peer_count_1 = None

    asn_peers_year_2_df = peer_count_2.drop("REL") #All peers of year 2

    n_rows, n_cols = asn_peers_year_2_df.shape
    if n_rows < 10:
        df_fill = pl.DataFrame({
            "ASP": [0] * (10 - n_rows),
            "ASC": [0] * (10 - n_rows)
        })
        asn_peers_year_2_df = pl.concat([asn_peers_year_2_df, df_fill], how="vertical")
   
    return asn_peers_year_2_df
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#TABLE CALLBACKS

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    """
    Callback for generating available ASNs present in both years for dropdown_3
    """

@app.callback(Output(component_id='dropdown_3', component_property='options'),
              Input(component_id='dropdown_1', component_property='value'),
              Input(component_id='dropdown_2', component_property='value'))

def available_asns_list(dropdown_1, dropdown_2):

    i, j = read_csv(dropdown_1, dropdown_2) #Utilises the Micro CSV's since all ASNs are listed in a single column for indexing

    nodes_year_1 = i.select('ASN').unique().to_series().to_list() 
    nodes_year_2 = j.select('ASN').unique().to_series().to_list()

    common_nodes = list(set(nodes_year_1).intersection(nodes_year_2)) #Selecting the common nodes from each year and providing them as the options for dropdown_3

    return common_nodes

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    """
    Callback for displaying available ASNs present in all years
    """

@app.callback(Output(component_id='year_list', component_property='children'),
              Input(component_id='input1', component_property='value'))

def available_asns_year_list(input1):

    value = str(input1)   #Value to search for ASN
    files_with_value = [] #List to store names of files containing the value

    for filename in os.listdir(sys.path[0] + f"/Datasets/EdgeLists/"): #Scans the Edge List directory
        if filename.endswith('.csv'):
            with open(os.path.join(sys.path[0] + f"/Datasets/EdgeLists/{filename}"), newline='') as csvfile: #Open files
                reader = csv.reader(csvfile)
                for row in reader: 
                    if value in row: #If the ASN is found in any row of the Edge list
                        year = filename.split('_')[1]
                        files_with_value.append(f"{year}, ") #Append it to the list
                        break
    
    return html.P(sorted(files_with_value)) #Return the list as a paragraph element

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    """
    Function for updating ASN centrality table data
    """
@app.callback(Output(component_id='centrality_scores', component_property='children'),
              Input(component_id='dropdown_1', component_property='value'),
              Input(component_id='dropdown_2', component_property='value'),
              Input(component_id='dropdown_3', component_property='value'))

def update_asn_centrality_table(dropdown_1, dropdown_2, chosen_node):
    
    #Some headers are changed for readability
    nodal_centrality_df = generate_nodal_centrality(dropdown_1, dropdown_2, chosen_node).to_pandas().rename(columns={"Degree-C": "Degree Centrality", "Betweenness-C": "Betweenness Centrality", "Closeness-C": "Closeness Centrality", "Eigenvector-C": "Eigenvector Centrality"})
    data = nodal_centrality_df.to_dict("records")
    columns =  [{"name": i, "id": i,} for i in (nodal_centrality_df.columns)]

    return dash_table.DataTable(data=data, columns=columns, page_current=0, page_size=10, style_cell_conditional=[
        {'if': {'column_id': 'Year'},
         'width': '6%', 'textAlign': 'left'},
        {'if': {'column_id': 'ASN'},
         'width': '6%', 'textAlign': 'left'}])

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 
    """
    Function for updating ASN relationship statistics table data
    """
@app.callback(Output(component_id='relationship_statistics', component_property='children'),
              Input(component_id='dropdown_1', component_property='value'),
              Input(component_id='dropdown_2', component_property='value'),
              Input(component_id='dropdown_3', component_property='value'))

def update_asn_relationship_statistics_table(dropdown_1, dropdown_2, chosen_node):
    
    relationship_statistics_df = generate_nodal_statistics(dropdown_1, dropdown_2, chosen_node).to_pandas()
    data = relationship_statistics_df.to_dict("records")
    columns =  [{"name": i, "id": i,} for i in (relationship_statistics_df.columns)]

    return dash_table.DataTable(data=data, columns=columns, page_current=0, page_size=10, style_cell_conditional=[
        {'if': {'column_id': 'Year'},
         'width': '6%', 'textAlign': 'left'},
        {'if': {'column_id': 'ASN'},
         'width': '6%', 'textAlign': 'left'}])

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 
    """
    Function for updating ASN provider list table 1 data
    """
@app.callback(Output(component_id='provider_rels_year_1', component_property='children'),
              Input(component_id='dropdown_1', component_property='value'),
              Input(component_id='dropdown_2', component_property='value'),
              Input(component_id='dropdown_3', component_property='value'))

def update_asn_provider_list_table_1(dropdown_1, dropdown_2, chosen_node):
    
    asn_providers_year_1_df = generate_providers_list_year_1(dropdown_1, dropdown_2, chosen_node).to_pandas().rename(columns={"ASP":"Providers"})
    data = asn_providers_year_1_df.to_dict("records")
    columns =  [{"name": i, "id": i,} for i in (asn_providers_year_1_df.columns)]

                                                                                          #Because the DataTable converts data to strings a placeholder is used to remind users how to make queries
    return dash_table.DataTable(data=data, columns=columns, page_current=0, page_size=10, filter_action="native", filter_options={"placeholder_text": "Search for ASN, wrap INT with \"\" "}, style_data_conditional=[
        {'if': {'filter_query': '{Providers} = "0"'}, #If there a zero values, make their cells text and background white
            'backgroundColor': 'white',
            'color': 'white'}])

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    """
    Function for updating ASN provider list table 2 data
    """
@app.callback(Output(component_id='provider_rels_year_2', component_property='children'),
              Input(component_id='dropdown_1', component_property='value'),
              Input(component_id='dropdown_2', component_property='value'),
              Input(component_id='dropdown_3', component_property='value'))

def update_asn_provider_list_table_2(dropdown_1, dropdown_2, chosen_node):
    
    asn_providers_year_2_df = generate_providers_list_year_2(dropdown_1, dropdown_2, chosen_node).to_pandas().rename(columns={"ASP":"Providers"})
    data = asn_providers_year_2_df.to_dict("records")
    columns =  [{"name": i, "id": i,} for i in (asn_providers_year_2_df.columns)]

    return dash_table.DataTable(data=data, columns=columns, page_current=0, page_size=10, filter_action="native", filter_options={"placeholder_text": "Search for ASN, wrap INT with \"\" "}, style_data_conditional=[
        {'if': {'filter_query': '{Providers} = "0"'},
            'backgroundColor': 'white',
            'color': 'white'}])

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    """
    Function for updating ASN customer list table 1 data
    """
@app.callback(Output(component_id='customer_rels_year_1', component_property='children'),
              Input(component_id='dropdown_1', component_property='value'),
              Input(component_id='dropdown_2', component_property='value'),
              Input(component_id='dropdown_3', component_property='value'))

def update_asn_customer_list_table_1(dropdown_1, dropdown_2, chosen_node):
    
    asn_customer_year_1_df = generate_customers_list_year_1(dropdown_1, dropdown_2, chosen_node).to_pandas().rename(columns={"ASC":"Customers"})
    data = asn_customer_year_1_df.to_dict("records")
    columns =  [{"name": i, "id": i,} for i in (asn_customer_year_1_df.columns)]

    return dash_table.DataTable(data=data, columns=columns, page_current=0, page_size=10, filter_action="native", filter_options={"placeholder_text": "Search for ASN, wrap INT with \"\" "}, style_data_conditional=[
        {'if': {'filter_query': '{Customers} = "0"'},
            'backgroundColor': 'white',
            'color': 'white'}])

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    """
    Function for updating ASN customer list table 2 data
    """
@app.callback(Output(component_id='customer_rels_year_2', component_property='children'),
              Input(component_id='dropdown_1', component_property='value'),
              Input(component_id='dropdown_2', component_property='value'),
              Input(component_id='dropdown_3', component_property='value'))

def update_asn_customer_list_table_2(dropdown_1, dropdown_2, chosen_node):
    
    asn_customer_year_2_df = generate_customers_list_year_2(dropdown_1, dropdown_2, chosen_node).to_pandas().rename(columns={"ASC":"Customers"})
    data = asn_customer_year_2_df.to_dict("records")
    columns =  [{"name": i, "id": i,} for i in (asn_customer_year_2_df.columns)]

    return dash_table.DataTable(data=data, columns=columns, page_current=0, page_size=10, filter_action="native", filter_options={"placeholder_text": "Search for ASN, wrap INT with \"\" "}, style_data_conditional=[
        {'if': {'filter_query': '{Customers} = "0"'},
            'backgroundColor': 'white',
            'color': 'white'}])
        

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    """
    Function for updating ASN customer list table 1 data
    """
@app.callback(Output(component_id='peer_rels_year_1', component_property='children'),
              Input(component_id='dropdown_1', component_property='value'),
              Input(component_id='dropdown_2', component_property='value'),
              Input(component_id='dropdown_3', component_property='value'))

def update_asn_peer_list_table_1(dropdown_1, dropdown_2, chosen_node):
    
    asn_peers_year_1_df = generate_peer_list_year_1(dropdown_1, dropdown_2, chosen_node).to_pandas().rename(columns={"ASP": "AS1", "ASC": "AS2"})
    data = asn_peers_year_1_df.to_dict("records")
    columns =  [{"name": i, "id": i,} for i in (asn_peers_year_1_df.columns)]

    return dash_table.DataTable(data=data, columns=columns, page_current=0, page_size=10, filter_action="native", filter_options={"placeholder_text": "Search for ASN, wrap INT with \"\" "}, style_data_conditional=[
        {'if': {'filter_query': '{AS1} = "0"'},
            'backgroundColor': 'white',
            'color': 'white'},
        {'if': {'filter_query': '{AS2} = "0"'},
            'backgroundColor': 'white',
            'color': 'white'},
        ])
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    """
    Function for updating ASN customer list table 2 data
    """
@app.callback(Output(component_id='peer_rels_year_2', component_property='children'),
              Input(component_id='dropdown_1', component_property='value'),
              Input(component_id='dropdown_2', component_property='value'),
              Input(component_id='dropdown_3', component_property='value'))

def update_asn_peer_list_table_2(dropdown_1, dropdown_2, chosen_node):
    
    asn_peers_year_2_df = generate_peer_list_year_2(dropdown_1, dropdown_2, chosen_node).to_pandas().rename(columns={"ASP": "AS1", "ASC": "AS2"})
    data = asn_peers_year_2_df.to_dict("records")
    columns =  [{"name": i, "id": i,} for i in (asn_peers_year_2_df.columns)]

    return dash_table.DataTable(data=data, columns=columns, page_current=0, page_size=10, filter_action="native", filter_options={"placeholder_text": "Search for ASN, wrap INT with \"\" "}, style_data_conditional=[
        {'if': {'filter_query': '{AS1} = "0"'},
            'backgroundColor': 'white',
            'color': 'white'},
        {'if': {'filter_query': '{AS2} = "0"'},
            'backgroundColor': 'white',
            'color': 'white'},
        ])

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    """
        Function for displaying table titles
    """
@app.callback(Output(component_id="prov_1", component_property= "children"),
              Output(component_id="prov_2", component_property= "children"),
              Output(component_id="cust_1", component_property= "children"),
              Output(component_id="cust_2", component_property= "children"),
              Output(component_id="peer_1", component_property= "children"),
              Output(component_id="peer_2", component_property= "children"),
              Input(component_id='dropdown_1', component_property='value'),
              Input(component_id='dropdown_2', component_property='value'))

def update_table_titles(dropdown_1, dropdown_2):
    return html.H5(dropdown_1, style={'textAlign': 'center'}), html.H5(dropdown_2, style={'textAlign': 'center'}), html.H5(dropdown_1, style={'textAlign': 'center'}), html.H5(dropdown_2, style={'textAlign': 'center'}), html.H5(dropdown_1, style={'textAlign': 'center'}), html.H5(dropdown_2, style={'textAlign': 'center'})

