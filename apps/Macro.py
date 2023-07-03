from dash import dcc, html, Input, Output, dash_table
import plotly.graph_objs as go
import polars as pl
import pandas as pd
from app import app

layout = html.Div([
    
    html.H1('MACRO COMPARISON', style={'textAlign': 'center'}),

    html.Br(),
    
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
    ]),

    html.Br(),

    html.H3('Degree Distribution', style={'textAlign': 'center'}),
    # Row 3: Degree distribution graph
    html.Div(className='row', children=[
        html.Div(className='col-12', children=[
            dcc.Graph(id = 'degree_distribution',
                figure=go.Figure(
                    data=[],
                ))
        ])
    ]),

    # Rows 4 & 5: Centrality graphs
    html.H3('Centrality Histograms', style={'textAlign': 'center'}),
    #Row 4: Centrality graphs (Degree & Betweenness)
    html.Div(className='row', children=[
        #Degree Centrality
        html.Div(className='col-3', style={'width': '50%'}, children=[
            dcc.Graph(id='degree_centrality',
                figure=go.Figure(
                    data=[]
                ))
        ]),
        #Betweenness Centrality
        html.Div(className='column', style={'width': '50%'}, children=[
            dcc.Graph(id='betweenness_centrality',
                figure=go.Figure(
                    data=[]
            ))
        ]),
    ]),    

    html.Br(),
    html.Br(),

    #Row 5 Centrality graphs (Closeness & Eigenvector)
    html.Div(className='row', children=[
        #Closeness Centrality
        html.Div(className='column', style={'width': '50%'}, children=[
            dcc.Graph(id='closeness_centrality',
                figure=go.Figure(
                    data=[]
                ))
        ]),
        #Eigenvector Centrality
        html.Div(className='column', style={'width': '50%'}, children=[
            dcc.Graph(id='eigenvector_centrality',
                figure=go.Figure(
                    data=[]
            ))
        ])    
    ]),

    html.Br(),
    html.Br(),

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    html.H3('Network Size', style={'textAlign': 'center'}),
    html.Div(className='row', children=[
        html.Div(className='column', style={'width': '100%'}, id = 'network_size', children=[
        ])
    ]),

    html.Br(),
    html.Br(),

    html.H3('Centrality Averages', style={'textAlign': 'center'}),
    html.Div(className='row', children=[
        html.Div(className='column', style={'width': '100%'}, id = 'centrality_avg', children=[
        ])
    ]),

    html.Br(),
    html.Br(),

    html.H3('Network Robustness', style={'textAlign': 'center'}),
    html.Div(className='row', children=[
        html.Div(className='column', style={'width': '100%'}, id = 'network_robustness', children=[
        ])
    ]),

    html.Br(),
    html.Br(),
    
    html.H3('Network Distance', style={'textAlign': 'center'}),
    html.Div(className='row', children=[
    html.Div(className='column', style={'width': '100%'}, id = 'network_distance', children=[
        ])
    ]),

    html.Br(),
    html.Br(),

    html.H3('Highest Average Centrality Nodes', style={'textAlign': 'center'}),
    html.Div(className='row', children=[
    html.Div(className='column', style={'width': '100%'}, id = 'avg_node', children=[
        ])
    ]),

    html.Br(),
    html.Br(),


],style={'max-width': '1200px', 'margin': 'auto'})

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#CSV TO DATAFRAME

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

macro_df = pl.read_csv("Datasets/MacroFinal.csv")
degree_dist_df = pl.read_csv("Datasets/DegreeDistFinal.csv")

def read_csv(input_year_1, input_year_2):
    i = pl.read_csv(f"Datasets/MicroYears/{input_year_1}_micro.csv")
    j = pl.read_csv(f"Datasets/MicroYears/{input_year_2}_micro.csv")

    return i, j

def read_edge_csv(input_year_1, input_year_2):
    
    l = pl.read_csv(f"Datasets/EdgeLists/output_{input_year_1}_E.csv")
    p = pl.read_csv(f"Datasets/EdgeLists/output_{input_year_2}_E.csv")

    return l, p


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#GRAPH DATA

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def generate_degree_distribution_data(input_year_1, input_year_2):
    """
    Function to generate degree distribution DataFrame to be read by Plotly Scatter Graph
    Arguments:
        INT input_year_1: year of the first dropdown
        INT input_year_2: year of the second dropdown
    Returns:
        DataFrame df: Polars Dataframe with the two selecteed years indexed from 1 to the final degree count
    """
    year_1 = degree_dist_df.select(str(input_year_1)).to_series()
    year_2 = degree_dist_df.select(str(input_year_2)).to_series() #Places the two years degree distribution into Series

    df = pl.DataFrame({str(input_year_1): year_1, str(input_year_2): year_2}) #Series are then placed into a DataFrame
    df = df.with_columns(pl.Series("count", range(1, len(df) + 1))) #Indexing column for distribution points
        
    return df

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def generate_degree_centrality_data(input_year_1, input_year_2):
    """
    Function to generate degree centrality data from a given year's csv set.
    Arguments:
        INT input_year_1: year of first dropdown
        INT input_year_2: year of second dropdown
    Returns:
        LIST: year_1_plot: list of the first year's degree centrality histogram values in a series
        LIST: year_2_plot: list of the second year's degree centrality histogram values in a series
    """
    i, j = read_csv(input_year_1, input_year_2) #Makes i and j DataFrame instances of the two selected Micro-CSVs

    bin=[0.00001, 0.00002, 0.00003, 0.0001, 0.001, 0.01, 0.02, 1] #Bin ranges specifically allocated to segregate the different degree values
    d_hist1 = i.select('Degree-C').to_series().hist(bins=bin,bin_count=12) #Performs a histogram upon the degree centralities of the first selected year with the bins above
    d_hist2 = j.select('Degree-C').to_series().hist(bins=bin,bin_count=12) #Performs a histogram upon the degree centralities of the second selected year with the bins above

    dhc_1 = list(d_hist1["Degree-C_count"]) #Takes the count from the first year histogram object and exports it to a list
    dhc_2 = list(d_hist2["Degree-C_count"]) #Takes the count from the second year histogram object and exports it to a list

    col1 = pl.Series("col1", dhc_1 + dhc_2) #Combines the years data

    degree_c_year_col = pl.Series("year", [input_year_1]*len(dhc_1) + [input_year_2]*len(dhc_2)) #For the values in dhc_1 and dhc_2, create a series to match them to the specific year

    df = pl.DataFrame({"year": degree_c_year_col, "node_count": col1}) #This Dataframe was created for ease of use for any future development

    year_1_plot = df.filter(pl.col('year') == input_year_1)['node_count'].to_list()
    year_2_plot = df.filter(pl.col('year') == input_year_2)['node_count'].to_list() #Convert the chosen year to a list

    return year_1_plot, year_2_plot


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def generate_betweenness_centrality_data(input_year_1, input_year_2):
    """
    Function to generate betweenness centrality data from a given year's csv set.
    Arguments:
        INT input_year_1: year of first dropdown
        INT input_year_2: year of second dropdown
    Returns:
        LIST: year_1_plot: list of the first year's betweenness centrality histogram values in a series
        LIST: year_2_plot: list of the second year's betweenness centrality histogram values in a series
    """
    i, j = read_csv(input_year_1, input_year_2)  
    
    bin=[0, 0.00000001, 0.0000001, 0.000001, 0.00001, 0.0001, 0.001, 0.01, 0.02, 1] #Bin ranges specifically allocated to segregate the different betweenness values
    b_hist1 = i.select('Betweenness-C').to_series().hist(bins=bin,bin_count=10)
    b_hist2 = j.select('Betweenness-C').to_series().hist(bins=bin,bin_count=10)

    bhc_1 = list(b_hist1["Betweenness-C_count"])
    bhc_2 = list(b_hist2["Betweenness-C_count"])

    col1 = pl.Series("col1", bhc_1 + bhc_2)
    
    betweenness_c_year_col = pl.Series("year", [input_year_1]*len(bhc_1) + [input_year_2]*len(bhc_2))

    df = pl.DataFrame({"year": betweenness_c_year_col, "node_count": col1})
    
    year_1_plot = df.filter(pl.col('year') == input_year_1)['node_count'].to_list()
    year_2_plot = df.filter(pl.col('year') == input_year_2)['node_count'].to_list()
    
    return year_1_plot, year_2_plot

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def generate_closeness_centrality_data(input_year_1, input_year_2):
    """
    Function to generate closeness centrality data from a given year's csv set.
    Arguments:
        INT input_year_1: year of first dropdown
        INT input_year_2: year of second dropdown
    Returns:
        LIST: year_1_plot: list of the first year's closeness centrality histogram values in a series
        LIST: year_2_plot: list of the second year's closeness centrality histogram values in a series
    """
    
    i, j = read_csv(input_year_1, input_year_2)

    bin=[0.2, 0.22, 0.23, 0.24, 0.25, 0.26, 0.27, 0.28, 0.3, 0.4, 0.5] #Bin ranges specifically allocated to segregate the different closeness values
    c_hist1 = i.select('Closeness-C').to_series().hist(bins=bin,bin_count=11)
    c_hist2 = j.select('Closeness-C').to_series().hist(bins=bin,bin_count=11)

    chc_1 = list(c_hist1["Closeness-C_count"])
    chc_2 = list(c_hist2["Closeness-C_count"])

    col1 = pl.Series("col1", chc_1 + chc_2)

    closeness_c_year_col = pl.Series("year", [input_year_1]*len(chc_1) + [input_year_2]*len(chc_2))

    df = pl.DataFrame({"year": closeness_c_year_col, "node_count": col1})

    year_1_plot = df.filter(pl.col('year') == input_year_1)['node_count'].to_list()
    year_2_plot = df.filter(pl.col('year') == input_year_2)['node_count'].to_list() 

    return year_1_plot, year_2_plot

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def generate_eigenvector_centrality_data(input_year_1, input_year_2):
    """
    Function to generate eigenvector centrality data from a given year's csv set.
    Arguments:
        INT input_year_1: year of first dropdown
        INT input_year_2: year of second dropdown
    Returns:
        LIST: year_1_plot: list of the first year's eigenvector centrality histogram values in a series
        LIST: year_2_plot: list of the second year's eigenvector centrality histogram values in a series
    """

    i, j = read_csv(input_year_1, input_year_2) 

    bin=[0, 0.00000001, 0.0000001, 0.000001, 0.00001, 0.0001, 0.001, 0.01, 0.02, 1] #Bin ranges specifically allocated to segregate the different Eigenvector values
    e_hist1 = i.select('Eigenvector-C').to_series().hist(bins=bin,bin_count=10)
    e_hist2 = j.select('Eigenvector-C').to_series().hist(bins=bin,bin_count=10)

    ehc_1 = list(e_hist1["Eigenvector-C_count"])
    ehc_2 = list(e_hist2["Eigenvector-C_count"])

    col1 = pl.Series("col1", ehc_1 + ehc_2)

    eigenvector_c_year_col = pl.Series("year", [input_year_1]*len(ehc_1) + [input_year_2]*len(ehc_2))

    df = pl.DataFrame({"year": eigenvector_c_year_col, "node_count": col1})

    year_1_plot = df.filter(pl.col('year') == input_year_1)['node_count'].to_list()
    year_2_plot = df.filter(pl.col('year') == input_year_2)['node_count'].to_list()


    return year_1_plot, year_2_plot

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#TABLE DATA

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def generate_network_size(input_year_1, input_year_2):
    """
    Function for generating network size table data
    Arguments:
        INT input_year_1: year of first dropdown
        INT input_year_2: year of second dropdown
    Returns:
        DataFrame DF: Contains single float/int data of each selected year relevant to Network Size comparison E.G Vertex & Edge Count
    """
    
    i, j = read_csv(input_year_1, input_year_2) #need to count the unique values of each tier
    l, p = read_edge_csv(input_year_1, input_year_2) #Both edge lists

    #Filter the Macro_DF by selected years and return a DF with the vertex and edge counts
    node_edge_df = macro_df.filter((pl.col('Year') == int(input_year_1)) | (pl.col('Year') == int(input_year_2))).select(["Vertex-C", "Edge-C"]) 
    vertex_c = list(node_edge_df.select("Vertex-C").to_series()) 
    edge_c = list(node_edge_df.select("Edge-C").to_series()) #Create series with the vertex and edge count

    ratio_df_1 = l.select('REL').to_series().value_counts() 
    ratio_values_1 = list(ratio_df_1["counts"]) #Selecting the relationship column for year 1 as a list

    ratio_df_2 = p.select('REL').to_series().value_counts()
    ratio_values_2 = list(ratio_df_2["counts"]) #Selecting the relationship column for year 2 as a list

    tier1_year1_c = i.select('tier').to_series().to_list().count(1) #Counts number of Tier 1s
    tier1_year2_c = j.select('tier').to_series().to_list().count(1)

    tier2_year1_c = i.select('tier').to_series().to_list().count(2) #Counts number of Tier 2s
    tier2_year2_c = j.select('tier').to_series().to_list().count(2)

    tier3_year1_c = i.select('tier').to_series().to_list().count(3) #Counts number of Tier 3s
    tier3_year2_c = j.select('tier').to_series().to_list().count(3)
    
    tier1_v = tier1_year1_c, tier1_year2_c
    tier2_v = tier2_year1_c, tier2_year2_c
    tier3_v = tier3_year1_c, tier3_year2_c

    p2p_v = ratio_values_1[0], ratio_values_2[0] #Peer to peer edges
    p2c_v = ratio_values_1[1], ratio_values_2[1] #Provider to customer edges

    network_size_df = pl.DataFrame({
        "Year": [input_year_1, input_year_2],
        "Vertex Count": vertex_c,
        "Edge Count": edge_c,
        "Provider-Customer": p2c_v,
        "Peer-Peer": p2p_v,
        "Tier1 Count": tier1_v,
        "Tier2 Count": tier2_v,
        "Tier3 Count": tier3_v
    })

    return network_size_df

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    """
    Function for generating centrality averages table data
    """
   
def generate_avg_centrality(input_year_1, input_year_2):
    
    #Filters by the two selected years in the macro_df rows and returns the centrality columns
    centrality_avg_df = macro_df.filter((pl.col('Year') == int(input_year_1)) | (pl.col('Year') == int(input_year_2))).select(["Year", "Central-P Dominance", "Degree_C-A", "Betweenness-A", "Closeness-A", "Eigenvector-A"])
    
    return centrality_avg_df
    
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    """
    Function for generating network robustness table data
    """
   
def generate_network_robustness(input_year_1, input_year_2):
    
    #Filters by the two selected years in the macro_df rows and returns the columns relating to network robustness
    network_robustness_df = macro_df.filter((pl.col('Year') == int(input_year_1)) | (pl.col('Year') == int(input_year_2))).select(["Year", "G-Clustering", "Density", "K-Core", "Min-Cut"])
    
    return network_robustness_df
    
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  
def generate_network_distance(input_year_1, input_year_2):
    """
    Function for generating network distance table data
    Arguments:
        INT input_year_1: year of first dropdown
        INT input_year_2: year of second dropdown
    Returns:
        DataFrame DF: Contains single float/int data of each selected year relevant to Network Distance comparison E.G Diameter & Radius
    """
    
    #Filters by the two selected years in the macro_df rows and returns the columns relating to network distance
    network_distance_df = macro_df.filter((pl.col('Year') == int(input_year_1)) | (pl.col('Year') == int(input_year_2))).select(["Year", "Diameter", "Radius", "AvgPthLen", "Assortivity"])
    
    return network_distance_df

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    """
    Function for generating highest average node data
    """

def generate_avg_node_score(input_year_1, input_year_2):

    i, j = read_csv(input_year_1, input_year_2) #Micro CSVs

    data_val1 = i.drop('ASN', 'tier').mean(axis=1) #Produces a DF with the average of all the centrality rows
    #Average in remaining data_val1 is then appended to the new DF with just the ASN. No join is needed since the data is in the same order
    avg_node_df_year1 = i.drop(['Degree-C', 'Betweenness-C', 'Closeness-C', 'Eigenvector-C', 'tier']).with_columns(data_val1.alias('Average')).sort('Average', descending=True).rename({
        "ASN": f"ASN-{input_year_1}", #rename columns to feature selected year
        "Average": f"Average-{input_year_1}",
    }).head(50) #Only the top 50 are then delivered

    data_val2 = j.drop('ASN', 'tier').mean(axis=1) 
    avg_node_df_year2 = j.drop(['Degree-C', 'Betweenness-C', 'Closeness-C', 'Eigenvector-C', 'tier']).with_columns(data_val2.alias('Average')).sort('Average', descending=True).rename({
        "ASN": f"ASN-{input_year_2}",
        "Average": f"Average-{input_year_2}",
    }).head(50)

    avg_node_df = pl.concat(
        [
            avg_node_df_year1, #Concat the two years
            avg_node_df_year2
        ],
        how="horizontal")

    return avg_node_df


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#GRAPH CALLBACKS

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

@app.callback(Output(component_id='degree_distribution', component_property='figure'),
              Input(component_id='dropdown_1', component_property='value'),
              Input(component_id='dropdown_2', component_property='value'))

def degree_distribution_update(dropdown_1, dropdown_2):
    """
    Function to update the degree distribution graph
    Arguments: Dropdown values
    Returns: plotly graph object of degree distribution
    """
    df = generate_degree_distribution_data(dropdown_1, dropdown_2)

    degree_distribution_fig = go.Figure()

    #First selected year
    degree_distribution_fig.add_trace(go.Scatter(
    name = dropdown_1,
    x=df["count"],
    y=df[dropdown_1],
    mode='markers',
    line = dict(color = '#FF0000')
    ))

    #Second selected year
    degree_distribution_fig.add_trace(go.Scatter(
    name = dropdown_2,
    x=df["count"],
    y=df[dropdown_2],
    mode='markers',
    line = dict(color = '#0000FF')
    ))

    degree_distribution_fig.update_layout(
        xaxis_title = "Degree(k)",
        yaxis_title = "P(k)",
        legend= {'itemsizing': 'constant'})

    degree_distribution_fig.update_xaxes(type="log") #Puts the x axis into a log for condensed data
    degree_distribution_fig.update_xaxes(minor=dict(ticks="inside", ticklen=6, showgrid=True))
    degree_distribution_fig.update_traces(
    mode='markers+lines',
    marker=dict(size=7),
    line=dict(width=3),
    showlegend=True)
    
    return degree_distribution_fig

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

@app.callback(Output(component_id='degree_centrality', component_property='figure'),
              Input(component_id='dropdown_1', component_property='value'),
              Input(component_id='dropdown_2', component_property='value'))

def degree_centrality_update(dropdown_1, dropdown_2):
    """
    Function to update the degree centrality graph
    Arguments: Dropdown values
    Returns: plotly graph object of degree centrality
    """

    year_1_plot, year_2_plot = generate_degree_centrality_data(dropdown_1, dropdown_2)
    
    x = [1,2,3,4,5,6,7,8,9]

    degree_c_fig = go.Figure(data=[go.Bar(
        name = dropdown_1,
        x = x,
        y = year_1_plot,
        text=year_1_plot,
        textposition='auto'
        ),
        
    go.Bar(
        name = dropdown_2,
        x = x,
        y = year_2_plot,
        text= year_2_plot,
        textposition='auto'
        )])
    
    degree_c_fig.update_layout(
        barmode='stack',
        bargap=0,
        bargroupgap=0.1,
        title='Distribution of Degree Centrality',
        title_x=0.5,
        xaxis_tickfont_size=12,
        yaxis=dict(
            title='Frequency',
            titlefont_size=16,
            tickfont_size=14,
        ),
        xaxis = dict(
            title='Discretisation',
            tickmode = 'array',
            tickvals = x,
            #Specific Bins to Degree Centrality: 0.00001, 0.00002, 0.00003, 0.0001, 0.0001, 0.001, 0.01, 0.02
            ticktext = ['0 - 0.00001', '0.00001 - 0.00002', '0.00002 - 0.00003', '0.00003 - 0.0001', '0.0001 - 0.001', '0.001 - 0.01', '0.01 - 0.02', '0.02 - 1', '1 - inf']
        ),
        legend_x= 1,
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="right",
            bgcolor='rgba(255, 255, 255, 0)',
            bordercolor='rgba(255, 255, 255, 0)'
        )
    )

    return degree_c_fig

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

@app.callback(Output(component_id='betweenness_centrality', component_property='figure'),
              Input(component_id='dropdown_1', component_property='value'),
              Input(component_id='dropdown_2', component_property='value'))

def betweenness_centrality_update(dropdown_1, dropdown_2):
    """
    Function to update the betweenness centrality graph
    Arguments: Dropdown values
    Returns: plotly graph object of betweenness centrality
    """
    year_1_plot, year_2_plot = generate_betweenness_centrality_data(dropdown_1, dropdown_2)

    x = [1,2,3,4,5,6,7,8,9,10,11]

    betweenness_c_fig = go.Figure(data=[
        go.Bar(
            name = dropdown_1,
            x = x,
            y = year_1_plot,
            text=year_1_plot,
            textposition='auto'
            ),
        
        go.Bar(
            name = dropdown_2,
            x = x,
            y = year_2_plot,
            text= year_2_plot,
            textposition='auto'
            )])
    
    betweenness_c_fig.update_layout(
        barmode='stack',
        bargap=0,
        bargroupgap=0.1,
        title='Distribution of Betweenness Centrality',
        title_x=0.5,
        xaxis_tickfont_size=12,
        yaxis=dict(
            title='Frequency',
            titlefont_size=16,
            tickfont_size=14,
        ),
        xaxis = dict(
            title='Discretisation',
            tickmode = 'array',
            tickvals = x,
            ticktext = ['0 - 1.0e-9', '1.0e-9 - 1.0e-8', '1.0e-8 - 1.0e-7', '1.0e-7 - 1.0e-6', '1.0e-6 - 0.00001', '0.00001 - 0.0001', '0.0001 - 0.001', '0.001 - 0.01', '0.01 - 0.02', '0.02 - 1', '1 - inf']
        ),
        legend_x= 1,
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="right",
            bgcolor='rgba(255, 255, 255, 0)',
            bordercolor='rgba(255, 255, 255, 0)'
        )
    )

    return betweenness_c_fig

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

@app.callback(Output(component_id='closeness_centrality', component_property='figure'),
              Input(component_id='dropdown_1', component_property='value'),
              Input(component_id='dropdown_2', component_property='value'))

def closeness_centrality_update(dropdown_1, dropdown_2):
    """
    Function to update the closeness centrality graph
    Arguments: Dropdown values
    Returns: plotly graph object of closeness centrality
    """
  
    year_1_plot, year_2_plot = generate_closeness_centrality_data(dropdown_1, dropdown_2)

    x = [1,2,3,4,5,6,7,8,9,10,11,12]
    
    closeness_c_fig = go.Figure(data=[go.Bar(
        name = dropdown_1,
        x = x,
        y = year_1_plot,
        text=year_1_plot,
        textposition='auto'
        ),
        
    go.Bar(
        name = dropdown_2,
        x = x,
        y = year_2_plot,
        text= year_2_plot,
        textposition='auto'
        )])
    
    closeness_c_fig.update_layout(
        barmode='stack',
        bargap=0,
        bargroupgap=0.1,
        title='Distribution of Closeness Centrality',
        title_x=0.5,
        xaxis_tickfont_size=12,
        yaxis=dict(
            title='Frequency',
            titlefont_size=16,
            tickfont_size=14,
        ),
        xaxis = dict(
            title='Discretisation',
            tickmode = 'array',
            tickvals = x,
            ticktext = ['0 - 0.2', '0.2 - 0.22', '0.22 - 0.23', '0.23 - 0.24', '0.24, - 0.25', '0.25 - 0.26', '0.26 - 0.27', '0.27 - 0.28', '0.28 - 0.3', '0.3 - 0.4', '0.4 - 0.5', '1 - inf']
        ),
        legend=dict(
            x=0,
            y=1.0,
            bgcolor='rgba(255, 255, 255, 0)',
            bordercolor='rgba(255, 255, 255, 0)'
        )
    )

    return closeness_c_fig

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

@app.callback(Output(component_id='eigenvector_centrality', component_property='figure'),
              Input(component_id='dropdown_1', component_property='value'),
              Input(component_id='dropdown_2', component_property='value'))

def eigenvector_centrality_update(dropdown_1, dropdown_2):
    """
    Function to update the eigenvector centrality graph
    Arguments: Dropdown values
    Returns: plotly graph object of eigenvector centrality
    """
    year_1_plot, year_2_plot = generate_eigenvector_centrality_data(dropdown_1, dropdown_2)
    
    x = [1,2,3,4,5,6,7,8,9,10,11]

    eigenvector_c_fig = go.Figure(data=[go.Bar(
        name = dropdown_1,
        x = x,
        y = year_1_plot,
        text=year_1_plot,
        textposition='auto'
        ),
        
    go.Bar(
        name = dropdown_2,
        x = x,
        y = year_2_plot,
        text= year_2_plot,
        textposition='auto'
        )])
    
    eigenvector_c_fig.update_layout(
        barmode='stack',
        bargap=0,
        bargroupgap=0.1,
        title='Distribution of Eigenvector Centrality',
        title_x=0.5,
        xaxis_tickfont_size=12,
        yaxis=dict(
            title='Frequency',
            titlefont_size=16,
            tickfont_size=14,
        ),
        xaxis = dict(
            title='Discretisation',
            tickmode = 'array',
            tickvals = x,
            ticktext = ['0 - 1.0e-9', '1.0e-9 - 1.0e-8', '1.0e-8 - 1.0e-7', '1.0e-7 - 1.0e-6', '1.0e-6 - 0.00001', '0.00001 - 0.0001', '0.0001 - 0.001', '0.001 - 0.01', '0.01 - 0.02', '0.02 - 1', '1 - inf']
        ),
        legend=dict(
            x=0,
            y=1.0,
            bgcolor='rgba(255, 255, 255, 0)',
            bordercolor='rgba(255, 255, 255, 0)'
        )
    )
    
    return eigenvector_c_fig

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#TABLE CALLBACKS

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
@app.callback(Output(component_id='network_size', component_property='children'),
              Input(component_id='dropdown_1', component_property='value'),
              Input(component_id='dropdown_2', component_property='value'))

def network_size_update(dropdown_1, dropdown_2):

    network_size_df = generate_network_size(dropdown_1, dropdown_2).to_pandas() #All Polars DFs are converted to Pandas so .to_dict can convert the data into a way Dash can read it
    data=network_size_df.to_dict("records")
    columns =  [{"name": i, "id": i,} for i in (network_size_df.columns)]
    
    return dash_table.DataTable(data=data, columns=columns, style_cell_conditional=[
        {'if': {'column_id': 'Year'},
         'width': '10%', 'textAlign': 'left'}])
        
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

@app.callback(Output(component_id='centrality_avg', component_property='children'),
              Input(component_id='dropdown_1', component_property='value'),
              Input(component_id='dropdown_2', component_property='value'))

def centrality_avg_update(dropdown_1, dropdown_2):
    
    #Some header names are changed for readability
    centrality_avg_df = generate_avg_centrality(dropdown_1, dropdown_2).to_pandas().rename(columns={"Degree_C-A": "Degree", "Betweenness-A": "Betweenness", "Closeness-A": "Closeness", "Eigenvector-A": "Eigenvector"})
    data = centrality_avg_df.to_dict("records")
    columns =  [{"name": i, "id": i,} for i in (centrality_avg_df.columns)]
    
    return dash_table.DataTable(data=data, columns=columns, style_cell_conditional=[
        {'if': {'column_id': 'Year'},
         'width': '10%', 'textAlign': 'left'},
         {'if': {'column_id': 'Central-P Dominance'},
          'width': '22.5%'}])

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

@app.callback(Output(component_id='network_robustness', component_property='children'),
              Input(component_id='dropdown_1', component_property='value'),
              Input(component_id='dropdown_2', component_property='value'))

def network_robustness_update(dropdown_1, dropdown_2):
    
    network_robustness_df = generate_network_robustness(dropdown_1, dropdown_2).to_pandas().rename(columns={"G-Clustering": "Global Clustering Coefficient"})
    data = network_robustness_df.to_dict("records")
    columns =  [{"name": i, "id": i,} for i in (network_robustness_df.columns)]
    
    return dash_table.DataTable(data=data, columns=columns, style_cell_conditional=[
        {'if': {'column_id': 'Year'},
         'width': '10%', 'textAlign': 'left'},
        {'if': {'column_id': 'Global Clustering Coefficient'},
         'width': '30%'}])

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

@app.callback(Output(component_id='network_distance', component_property='children'),
              Input(component_id='dropdown_1', component_property='value'),
              Input(component_id='dropdown_2', component_property='value'))

def network_distance_update(dropdown_1, dropdown_2):
    
    network_distance_df = generate_network_distance(dropdown_1, dropdown_2).to_pandas().rename(columns={"AvgPthLen": "Average Shortest Path Length"})
    data=network_distance_df.to_dict("records")
    columns =  [{"name": i, "id": i,} for i in (network_distance_df.columns)]
    
    return dash_table.DataTable(data=data, columns=columns, style_cell_conditional=[
        {'if': {'column_id': 'Year'},
         'width': '10%', 'textAlign': 'left'},
         {'if': {'column_id': 'Average Shortest Path Length'},
          'width': '30%'}])

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

@app.callback(Output(component_id='avg_node', component_property='children'),
              Input(component_id='dropdown_1', component_property='value'),
              Input(component_id='dropdown_2', component_property='value'))

def avg_node_score_update(dropdown_1, dropdown_2):
    
    avg_node_df = generate_avg_node_score(dropdown_1, dropdown_2).to_pandas()
    data=avg_node_df.to_dict("records")
    columns =  [{"name": i, "id": i,} for i in (avg_node_df.columns)]
    
    return dash_table.DataTable(data=data, columns=columns, page_current=0, sort_action='native', page_size=5)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
