import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import plotly.graph_objs as go
import pandas as pd
import numpy as np


color_discrete_sequence = px.colors.qualitative.Set1

df = pd.read_csv('data/migration_mq.csv') #Medium quality data
df['timestamp'] = pd.to_datetime(df['timestamp'])
df['year'] = df['timestamp'].dt.year

app = dash.Dash(__name__)

#Initial empty map plot
initial_fig = px.scatter_geo()
initial_fig.update_geos(
    projection_type="equirectangular",
    visible=False, resolution=50,
    showcountries=True, countrycolor="#bfbfbf"
)
initial_fig.update_layout(
    height=800,
    margin={"r":0,"t":0,"l":0,"b":0}
)

app.layout = html.Div([
    dcc.RangeSlider(
        id='year-slider',
        min=df['year'].min(),
        max=df['year'].max(),
        value=[df['year'].min(), df['year'].max()],
        marks={str(year): str(year) for year in df['year'].unique()},
        step=None
    ),
    dcc.Dropdown(
        id='individual-dropdown',
        multi=True
    ),
    html.Div([
        dcc.Slider(
            id='timestamp-slider',
            min=0,
            max=52,  
            value=52,
            marks={i: f'Week {i+1}' for i in range(0, 53, 2)},  #Label every other week for readability
            step=1
        )
    ], id='timestamp-slider-container', style={'display': 'block'}),
    dcc.Graph(id='map-plot', figure=initial_fig, style={'height': '600px', 'width': '100%'}),
])

@app.callback(
    Output('individual-dropdown', 'options'),
    Input('year-slider', 'value'))
def set_individual_options(selected_years):
    #Filter based on selected years and create a set of unique 'id_year' values
    filtered_df = df[df['year'].between(*selected_years)]
    return [{'label': id_year, 'value': id_year} for id_year in np.sort(filtered_df['id_year'].unique())]

@app.callback(
    Output('map-plot', 'figure'),
    [Input('individual-dropdown', 'value'),
     Input('timestamp-slider', 'value')],
    prevent_initial_call=True)

def update_map(selected_id_years, selected_week):
    if not selected_id_years:
        #Plot the empty map if no individuals are selected
        return initial_fig

    #Convert week number to the corresponding date range within the year
    year_start = pd.to_datetime(f'{selected_id_years[0].split("_")[1]}-01-01')
    week_end = year_start + pd.to_timedelta(selected_week * 7, 'd')

    #Get all data up to the end of the selected week
    dff = df[(df['id_year'].isin(selected_id_years)) & (df['timestamp'] < week_end)]

    #Get last point for each 'id_year' to show as current location
    last_points = dff.sort_values('timestamp').groupby('id_year').last().reset_index()

    #Create a color map for the selected id_years
    unique_id_years = dff['id_year'].unique()
    colors = px.colors.qualitative.Plotly[:len(unique_id_years)]
    color_map = dict(zip(unique_id_years, colors))

    fig = go.Figure()

    #Plot lines for each id_year
    for id_year in unique_id_years:
        id_year_df = dff[dff['id_year'] == id_year]
        fig.add_trace(
            go.Scattergeo(
                lon=id_year_df['location-long'],
                lat=id_year_df['location-lat'],
                mode='lines',
                line=dict(width=2, color=color_map[id_year]),
                name=id_year
            )
        )

        #Get the last location for the current id_year
        last_location = last_points[last_points['id_year'] == id_year]
        fig.add_trace(
            go.Scattergeo(
                lon=last_location['location-long'],
                lat=last_location['location-lat'],
                mode='markers',
                marker=dict(size=8, color=color_map[id_year]),
                name=id_year,
                showlegend=False
            )
        )

    fig.update_geos(
        projection_type="equirectangular",
        visible=False, resolution=50,
        showcountries=True, countrycolor="#bfbfbf"
    )
    fig.update_layout(
        height=800,
        margin={"r":0,"t":0,"l":0,"b":0},
        legend_title_text='ID + Year',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.05,
            xanchor="center",
            x=0.5
        )
    )

    return fig



if __name__ == '__main__':
    app.run_server(debug=True)
