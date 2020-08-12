import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

app = dash.Dash(__name__)

# Import and clean data
df = pd.read_csv("Data/road_eqr_carbua.tsv")
year = [1987] + list(range(1989,2013))
year = year[::-1]
year = [str(item) for item in year]
df.columns = ['unit', 'vehicle', 'mot_nrg', 'geo/time'] + year

df = df.astype(str)
df['2012'].value_counts()
df['2012'] = df['2012'].replace([': '],0)
df['2011'] = df['2011'].replace([': '],0)
df['2010'] = df['2010'].replace([': '],0)

df["2012"] = pd.to_numeric(df["2012"])
df["2011"] = pd.to_numeric(df["2011"])
df['2010'] = pd.to_numeric(df["2010"])
df['Total'] = df['2012']+df['2011']+df['2010']

# App layout
app.layout = html.Div([
    
    html.H1("Dashboard for EV distribution in Europe", style={'text-align': 'center'}),

    dcc.Dropdown(id="slct_vhcl",
                 options=[
                     {"label": "car", "value": 'CAR'},
                     {"label": "bus", "value": 'BUS_TOT'},
                    ],
                 multi=False,
                 value='CAR',
                 style={'width': "40%"}
                 ),

    html.Div(id='output_container', children=[]),
    html.Br(),

    dcc.Graph(id='my_map', figure={})

])

# Connect the Plotly graphs with Dash Components
@app.callback(
    [Output(component_id='output_container', component_property='children'),
     Output(component_id='my_map', component_property='figure')],
    [Input(component_id='slct_vhcl', component_property='value')]
)
def update_graph(option_slctd):
    print(option_slctd)
    print(type(option_slctd))
    
    container = "The vehicle chosen by user was: {}".format(option_slctd)

    dff = df.copy()
    dff = dff[dff["vehicle"] == option_slctd]
    dff = dff[dff["mot-nrg"] == "ELC"]

    # Plotly Express
    fig = px.choropleth(
        data_frame=dff,
        locationmode='country names',
        locations='geo/time',
        color='Total',
        hover_data=['Total', 'geo/time'],
        color_continuous_scale=px.colors.sequential.YlOrRd,
        labels={'title': 'total no. of electric vehicles'},
        template='plotly_dark'
    )

    return container, fig


if __name__ == '__main__':
    app.run_server(debug=True)
