import json
import pandas as pd
import plotly.express as px
from shiny import App, ui, render
from shinywidgets import output_widget, render_widget
from pathlib import Path

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
        
        columns_to_display = ['Institute or newspaper name', 'Country', 'City', 'Type', 'Inception']
        display_data = filtered_data[columns_to_display].copy()
        
        display_data['Inception'] = display_data['Inception'].dt.strftime('%Y')
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
        
        fig = px.scatter_mapbox(filtered_data, 
                                lat="Latitude", 
                                lon="Longitude", 
                                hover_name="Institute or newspaper name",
                                color="Type",
                                zoom=4,
                                height=600)
        
        fig.update_layout(
            mapbox_style="open-street-map",
            mapbox=dict(
                center=dict(lat=filtered_data['Latitude'].mean(), lon=filtered_data['Longitude'].mean()),
            ),
            margin={"r":0,"t":0,"l":0,"b":0},
            hoverlabel=dict(bgcolor="white", font_size=12),
            legend=dict(
                yanchor="top",
                y=0.99,
                xanchor="left",
                x=0.01,
                bgcolor="rgba(255, 255, 255, 0.5)"
            )
        )
        
        fig.update_traces(hovertemplate='%{hovertext}')
        
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
        
        # Convert Inception to datetime if it's not already
        newspaper_data['Inception'] = pd.to_datetime(newspaper_data['Inception'], format='%Y', errors='coerce')
        
        # Add a 'Closure date' column, set to 2024 for all newspapers
        newspaper_data['Closure date'] = pd.to_datetime('2024-01-01')
        
        # Apply filters
        if input.filter_country() != "All":
            newspaper_data = newspaper_data[newspaper_data['Country'] == input.filter_country()]
        if input.filter_city() != "All":
            newspaper_data = newspaper_data[newspaper_data['City'] == input.filter_city()]
        
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
        fig.update_traces(hovertemplate='<b>%{y}</b><br>Inception: %{x}<br>Country: %{customdata[0]}<br>City: %{customdata[1]}')
        
        return fig

app = App(app_ui, server)