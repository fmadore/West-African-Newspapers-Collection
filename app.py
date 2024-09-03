import json
import pandas as pd
import plotly.express as px
from shiny import App, ui, render
from shinywidgets import output_widget, render_widget

# Embed data as JSON string
data_json = '''[
  {
    "Institute or newspaper name": "National Library of Benin",
    "Country": "Benin",
    "City": "Porto-Novo",
    "Type": "Archives",
    "Inception": "1975"
  },
  {
    "Institute or newspaper name": "Le Héraut",
    "Country": "Benin",
    "City": "Abomey-Calavi",
    "Type": "Newspaper",
    "Inception": "1988"
  },
  {
    "Institute or newspaper name": "National Archives of Benin",
    "Country": "Benin",
    "City": "Porto-Novo",
    "Type": "Archives",
    "Inception": "1914"
  },
  {
    "Institute or newspaper name": "Fraternité",
    "Country": "Benin",
    "City": "Cotonou",
    "Type": "Newspaper",
    "Inception": "1999"
  },
  {
    "Institute or newspaper name": "Matin Libre",
    "Country": "Benin",
    "City": "Cotonou",
    "Type": "Newspaper",
    "Inception": "2014"
  },
  {
    "Institute or newspaper name": "La Croix du Bénin",
    "Country": "Benin",
    "City": "Cotonou",
    "Type": "Newspaper",
    "Inception": "1946"
  },
  {
    "Institute or newspaper name": "Le Matinal",
    "Country": "Benin",
    "City": "Cotonou",
    "Type": "Newspaper",
    "Inception": "1997"
  },
  {
    "Institute or newspaper name": "Civic Academy for Africa's Future",
    "Country": "Benin",
    "City": "Abomey-Calavi",
    "Type": "Education",
    "Inception": "2019"
  },
  {
    "Institute or newspaper name": "La Nation/Ehuzu/Daho-Express",
    "Country": "Benin",
    "City": "Cotonou",
    "Type": "Newspaper",
    "Inception": "1969"
  },
  {
    "Institute or newspaper name": "LASDEL Parakou",
    "Country": "Benin",
    "City": "Parakou",
    "Type": "Education",
    "Inception": null
  },
  {
    "Institute or newspaper name": "Agence Nationale de la Presse de Côte d'Ivoire",
    "Country": "Côte d'Ivoire",
    "City": "Abidjan",
    "Type": "Organisation",
    "Inception": null
  },
  {
    "Institute or newspaper name": "Archives Nationales de Côte d'Ivoire",
    "Country": "Côte d'Ivoire",
    "City": "Abidjan",
    "Type": "Archives",
    "Inception": null
  },
  {
    "Institute or newspaper name": "Le Temps",
    "Country": "Côte d'Ivoire",
    "City": "Abidjan",
    "Type": "Newspaper",
    "Inception": null
  },
  {
    "Institute or newspaper name": "Centre de Recherche et d'Action pour la Paix",
    "Country": "Côte d'Ivoire",
    "City": "Abidjan",
    "Type": "Library",
    "Inception": null
  },
  {
    "Institute or newspaper name": "Le Jour Plus / Le Jour",
    "Country": "Côte d'Ivoire",
    "City": "Abidjan",
    "Type": "Newspaper",
    "Inception": "1994"
  },
  {
    "Institute or newspaper name": "Le Patriote",
    "Country": "Côte d'Ivoire",
    "City": "Abidjan",
    "Type": "Newspaper",
    "Inception": "1991"
  },
  {
    "Institute or newspaper name": "L'inter",
    "Country": "Côte d'Ivoire",
    "City": "Abidjan",
    "Type": "Newspaper",
    "Inception": "1998"
  },
  {
    "Institute or newspaper name": "Soir Info",
    "Country": "Côte d'Ivoire",
    "City": "Abidjan",
    "Type": "Newspaper",
    "Inception": null
  },
  {
    "Institute or newspaper name": "Notre Voie/La Voie/Le Nouvel Horizon",
    "Country": "Côte d'Ivoire",
    "City": "Abidjan",
    "Type": "Newspaper",
    "Inception": "1991"
  },
  {
    "Institute or newspaper name": "Fraternité Matin",
    "Country": "Côte d'Ivoire",
    "City": "Abidjan",
    "Type": "Newspaper",
    "Inception": "1964"
  },
  {
    "Institute or newspaper name": "Groupement des Éditeurs de Presse de Côte d'Ivoire",
    "Country": "Côte d'Ivoire",
    "City": "Abidjan",
    "Type": "Organisation",
    "Inception": null
  },
  {
    "Institute or newspaper name": "Balme Library",
    "Country": "Ghana",
    "City": "Accra",
    "Type": "Library",
    "Inception": null
  },
  {
    "Institute or newspaper name": "Daily Graphic",
    "Country": "Ghana",
    "City": "Accra",
    "Type": "Newspaper",
    "Inception": "1950"
  },
  {
    "Institute or newspaper name": "The Mirror",
    "Country": "Ghana",
    "City": "Accra",
    "Type": "Newspaper",
    "Inception": null
  },
  {
    "Institute or newspaper name": "The Spectator",
    "Country": "Ghana",
    "City": "Accra",
    "Type": "Newspaper",
    "Inception": null
  },
  {
    "Institute or newspaper name": "Daily Guide",
    "Country": "Ghana",
    "City": "Accra",
    "Type": "Newspaper",
    "Inception": "1984"
  },
  {
    "Institute or newspaper name": "The Ghanaian Times",
    "Country": "Ghana",
    "City": "Accra",
    "Type": "Newspaper",
    "Inception": "1957"
  },
  {
    "Institute or newspaper name": "The Ghanaian Observer",
    "Country": "Ghana",
    "City": "Accra",
    "Type": "Newspaper",
    "Inception": "2006"
  },
  {
    "Institute or newspaper name": "Ghana Library Authority",
    "Country": "Ghana",
    "City": "Accra",
    "Type": "Archives",
    "Inception": null
  },
  {
    "Institute or newspaper name": "Bibliothèque et Archives nationales du Togo",
    "Country": "Togo",
    "City": "Lomé",
    "Type": "Archives",
    "Inception": null
  },
  {
    "Institute or newspaper name": "Université de Lomé",
    "Country": "Togo",
    "City": "Lomé",
    "Type": "Education",
    "Inception": null
  },
  {
    "Institute or newspaper name": "L'Alternative",
    "Country": "Togo",
    "City": "Lomé",
    "Type": "Newspaper",
    "Inception": "2008"
  },
  {
    "Institute or newspaper name": "Liberté",
    "Country": "Togo",
    "City": "Lomé",
    "Type": "Newspaper",
    "Inception": "2005"
  },
  {
    "Institute or newspaper name": "La Dépêche",
    "Country": "Togo",
    "City": "Lomé",
    "Type": "Newspaper",
    "Inception": "1993"
  }
]'''

# Load the data from JSON string
data = pd.DataFrame(json.loads(data_json))

# Clean and prepare the data
data['Inception'] = pd.to_datetime(data['Inception'], format='%Y', errors='coerce')

# Add GPS coordinates to the dataset
city_coordinates = {
    'Abomey-Calavi': [6.448611, 2.355556],
    'Cotonou': [6.366667, 2.416667],
    'Porto-Novo': [6.483333, 2.616667],
    'Lomé': [6.131944, 1.222778],
    'Abidjan': [5.336389, -4.026667],
    'Accra': [5.533333, -0.216667],
    'Parakou': [9.3369, 2.6323]  # Added Parakou coordinates
}

data['Latitude'] = data['City'].map(lambda x: city_coordinates.get(x, [None])[0])
data['Longitude'] = data['City'].map(lambda x: city_coordinates.get(x, [None])[1])

app_ui = ui.page_sidebar(
    ui.sidebar(
        ui.input_select("filter_type", "Filter by Type", choices=["All"] + list(data['Type'].unique())),
        ui.input_select("filter_country", "Filter by Country", choices=["All"] + list(data['Country'].unique())),
    ),
    ui.h1("WANA Partners Dashboard"),
    ui.h2("Partners by Type and Country"),
    output_widget("type_chart"),
    ui.h2("Partner Distribution"),
    output_widget("map"),
    ui.h2("Timeline"),
    output_widget("timeline"),
)

def server(input, output, session):
    @output
    @render_widget
    def map():
        filtered_data = data
        if input.filter_type() != "All":
            filtered_data = filtered_data[filtered_data['Type'] == input.filter_type()]
        if input.filter_country() != "All":
            filtered_data = filtered_data[filtered_data['Country'] == input.filter_country()]
        
        # Count partners per country for choropleth
        country_counts = filtered_data['Country'].value_counts().reset_index()
        country_counts.columns = ['Country', 'Count']
        
        # Create choropleth map
        fig = px.choropleth(country_counts, 
                            locations="Country", 
                            color="Count",
                            hover_name="Country", 
                            color_continuous_scale=px.colors.sequential.Viridis,
                            projection="natural earth")
        
        # Add point overlays for cities
        fig.add_scattergeo(
            lon=filtered_data['Longitude'],
            lat=filtered_data['Latitude'],
            text=filtered_data['Institute or newspaper name'],
            mode='markers',
            marker=dict(size=8, color='red', opacity=0.7),
            hoverinfo='text'
        )
        
        fig.update_geos(
            visible=False,
            resolution=50,
            showcountries=True,
            countrycolor="darkgray",
            showcoastlines=True,
            coastlinecolor="darkgray",
            fitbounds="locations"
        )
        
        fig.update_layout(height=600, margin={"r":0,"t":0,"l":0,"b":0})
        
        return fig

    @output
    @render_widget
    def type_chart():
        filtered_data = data
        if input.filter_country() != "All":
            filtered_data = filtered_data[filtered_data['Country'] == input.filter_country()]
        
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
        filtered_data = data
        if input.filter_type() != "All":
            filtered_data = filtered_data[filtered_data['Type'] == input.filter_type()]
        if input.filter_country() != "All":
            filtered_data = filtered_data[filtered_data['Country'] == input.filter_country()]
        
        fig = px.timeline(filtered_data, 
                          x_start="Inception", 
                          y="Institute or newspaper name",
                          color="Type",
                          hover_data=["Country", "City"])
        return fig

app = App(app_ui, server)