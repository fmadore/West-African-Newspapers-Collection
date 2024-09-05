import json
import pandas as pd
import plotly.express as px
from shiny import App, ui, render
from shinywidgets import output_widget, render_widget
from pathlib import Path
import geopandas as gpd
import cartopy.io.shapereader as shpreader

# Load data from JSON file
data_path = Path(__file__).parent / "data.json"
with open(data_path, "r", encoding="utf-8") as file:
    data = pd.read_json(file)

# Clean and prepare the data
data['Inception'] = pd.to_datetime(data['Inception'], format='%Y', errors='coerce')

# Safely extract latitude and longitude
def extract_coordinate(coord, index):
    if isinstance(coord, list) and len(coord) > index:
        return coord[index]
    return None

data['Latitude'] = data['Coordinates'].apply(lambda x: extract_coordinate(x, 0))
data['Longitude'] = data['Coordinates'].apply(lambda x: extract_coordinate(x, 1))

# Prepare the JSON data for country colors
country_counts = data['Country'].value_counts().to_dict()
country_color_data = json.dumps(country_counts)

# Prepare unique values for dropdowns
unique_types = ["All"] + sorted(data['Type'].unique().tolist())
unique_countries = ["All"] + sorted(data['Country'].unique().tolist())
unique_cities = ["All"] + sorted(data['City'].unique().tolist())

# Load world map data
world = gpd.read_file(shpreader.natural_earth(resolution='110m', category='cultural', name='admin_0_countries'))
world = world.to_crs(epsg=4326)
world_geojson = json.loads(world.to_json())

app_ui = ui.page_sidebar(
    ui.sidebar(
        ui.input_select("filter_type", "Filter by Type", choices=unique_types),
        ui.input_select("filter_country", "Filter by Country", choices=unique_countries),
        ui.input_select("filter_city", "Filter by City", choices=unique_cities),
    ),
    ui.h1("WANA Partners Dashboard"),
    ui.navset_tab(
        ui.nav_panel("Overview", 
            ui.h2("Data Overview"),
            ui.output_data_frame("data_table")
        ),
        ui.nav_panel("Type", 
            ui.h2("Partners by Type and Country"),
            output_widget("type_chart")
        ),
        ui.nav_panel("Map", 
            ui.h2("Partner Distribution"),
            output_widget("map")
        ),
        ui.nav_panel("Newspaper Timeline", 
            ui.h2("Newspaper Timeline"),
            output_widget("timeline")
        ),
    )
)

def server(input, output, session):
    @output
    @render.data_frame
    def data_table():
        filtered_data = data
        if input.filter_type() != "All":
            filtered_data = filtered_data[filtered_data['Type'] == input.filter_type()]
        if input.filter_country() != "All":
            filtered_data = filtered_data[filtered_data['Country'] == input.filter_country()]
        if input.filter_city() != "All":
            filtered_data = filtered_data[filtered_data['City'] == input.filter_city()]
        
        columns_to_display = ['Institute or newspaper name', 'Country', 'City', 'Type', 'Inception', 'Closure date']
        display_data = filtered_data[columns_to_display].copy()
        
        display_data['Inception'] = display_data['Inception'].dt.strftime('%Y')
        display_data['Closure date'] = pd.to_datetime(display_data['Closure date'], errors='coerce').dt.strftime('%Y')
        display_data = display_data.rename(columns={'Institute or newspaper name': 'Name'})
        display_data = display_data.sort_values('Name')
        
        return render.DataGrid(display_data, filters=True, height="100%")

    @output
    @render_widget
    def map():
        filtered_data = data
        if input.filter_type() != "All":
            filtered_data = filtered_data[filtered_data['Type'] == input.filter_type()]
        if input.filter_country() != "All":
            filtered_data = filtered_data[filtered_data['Country'] == input.filter_country()]
        if input.filter_city() != "All":
            filtered_data = filtered_data[filtered_data['City'] == input.filter_city()]
        
        # Count partners per country
        country_counts = filtered_data['Country'].value_counts().reset_index()
        country_counts.columns = ['Country', 'Count']

        fig = px.choropleth(country_counts, 
                            geojson=world_geojson, 
                            locations='Country', 
                            color='Count',
                            color_continuous_scale="Viridis",
                            range_color=(0, country_counts['Count'].max()),
                            labels={'Count':'Number of Partners'},
                            hover_name='Country',
                            hover_data={'Count': True, 'Country': False},
                            featureidkey="properties.NAME")

        fig.update_geos(showcountries=True, countrycolor="Black", countrywidth=0.5,
                        showcoastlines=True, coastlinecolor="Black", coastlinewidth=0.5)

        # Calculate the center of the data points
        center_lat = filtered_data['Latitude'].mean()
        center_lon = filtered_data['Longitude'].mean()

        fig.update_layout(
            title_text='Partner Distribution by Country',
            geo=dict(
                showframe=False,
                projection_type='natural earth',
                center=dict(lat=center_lat, lon=center_lon),
                # Adjust the zoom level as needed
                projection_scale=2
            ),
            height=600,
            margin={"r":0,"t":40,"l":0,"b":0}
        )

        # Add scatter plot for individual partners
        scatter_data = px.scatter_geo(filtered_data,
                                      lat='Latitude',
                                      lon='Longitude',
                                      hover_name='Institute or newspaper name',
                                      color='Type')

        for trace in scatter_data.data:
            fig.add_trace(trace)

        # Adjust legend position
        fig.update_layout(
            legend=dict(
                yanchor="top",
                y=0.99,
                xanchor="left",
                x=0.01,
                bgcolor="rgba(255, 255, 255, 0.5)"
            )
        )

        # Simplify hover information for both choropleth and scatter plots
        fig.update_traces(
            hovertemplate='%{hovertext}<br>Count: %{z}',
            selector=dict(type='choropleth')
        )
        fig.update_traces(
            hovertemplate='%{hovertext}',
            selector=dict(type='scattergeo')
        )

        return fig

    @output
    @render_widget
    def type_chart():
        filtered_data = data
        if input.filter_country() != "All":
            filtered_data = filtered_data[filtered_data['Country'] == input.filter_country()]
        if input.filter_city() != "All":
            filtered_data = filtered_data[filtered_data['City'] == input.filter_city()]
        
        type_country_counts = filtered_data.groupby(['Type', 'Country']).size().reset_index(name='Count')
        
        fig = px.bar(type_country_counts, 
                     x='Type', 
                     y='Count', 
                     color='Country', 
                     title='Partners by Type and Country',
                     labels={'Count': 'Number of Partners'},
                     hover_data=['Country', 'Count'])
        
        fig.update_layout(barmode='stack')
        return fig

    @output
    @render_widget
    def timeline():
        # Filter for newspapers only
        newspaper_data = data[data['Type'] == 'Newspaper'].copy()
        
        # Convert Inception to year string
        newspaper_data['Inception'] = pd.to_datetime(newspaper_data['Inception'], format='%Y', errors='coerce').dt.strftime('%Y')
        
        # Handle Closure date, convert to year string
        newspaper_data['Closure date'] = pd.to_datetime(newspaper_data['Closure date'], format='%Y', errors='coerce').dt.strftime('%Y')
        newspaper_data['Closure date'] = newspaper_data['Closure date'].fillna('2024')
        
        # Apply filters
        if input.filter_country() != "All":
            newspaper_data = newspaper_data[newspaper_data['Country'] == input.filter_country()]
        if input.filter_city() != "All":
            newspaper_data = newspaper_data[newspaper_data['City'] == input.filter_city()]
        
        # Sort the data by Country and then by Inception date in descending order
        newspaper_data = newspaper_data.sort_values(['Country', 'Inception'], ascending=[True, False])
        
        # Create the timeline
        fig = px.timeline(newspaper_data, 
                          x_start="Inception", 
                          x_end="Closure date",
                          y="Institute or newspaper name",
                          color="Country",
                          hover_data=["Country", "City"])
        
        # Customize the layout
        fig.update_layout(
            title="Newspaper Timeline",
            xaxis_title="Year",
            yaxis_title="Newspaper Name",
            height=600
        )
        
        # Update traces to show the newspaper name in the hover text
        fig.update_traces(hovertemplate='<b>%{y}</b><br>Inception: %{x}<br>Closure: %{x_end}<br>Country: %{customdata[0]}<br>City: %{customdata[1]}')
        
        # Reverse the y-axis to have the oldest newspapers at the top
        fig.update_yaxes(autorange="reversed")
        
        return fig

app = App(app_ui, server)