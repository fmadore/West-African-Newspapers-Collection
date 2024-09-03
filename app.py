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

app_ui = ui.page_sidebar(
    ui.sidebar(
        ui.input_select("filter_type", "Filter by Type", choices=["All"] + list(data['Type'].unique())),
        ui.input_select("filter_country", "Filter by Country", choices=["All"] + list(data['Country'].unique())),
    ),
    ui.h1("WANA Partners Dashboard"),
    ui.h2("Partner Distribution"),
    output_widget("map"),
    ui.h2("Partners by Type"),
    output_widget("type_chart"),
    ui.h2("Partners by Country"),
    output_widget("country_chart"),
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
        
        fig = px.scatter_geo(filtered_data, 
                             locations="Country", 
                             color="Type", 
                             hover_name="Institute or newspaper name",
                             projection="natural earth")
        return fig

    @output
    @render_widget
    def type_chart():
        filtered_data = data
        if input.filter_country() != "All":
            filtered_data = filtered_data[filtered_data['Country'] == input.filter_country()]
        
        type_counts = filtered_data['Type'].value_counts().reset_index()
        type_counts.columns = ['Type', 'Count']
        
        fig = px.bar(type_counts, x='Type', y='Count', title='Partners by Type')
        return fig

    @output
    @render_widget
    def country_chart():
        filtered_data = data
        if input.filter_type() != "All":
            filtered_data = filtered_data[filtered_data['Type'] == input.filter_type()]
        
        country_counts = filtered_data['Country'].value_counts().reset_index()
        country_counts.columns = ['Country', 'Count']
        
        fig = px.bar(country_counts, x='Country', y='Count', title='Partners by Country')
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