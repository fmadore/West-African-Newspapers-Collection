import json
import pandas as pd
import plotly.express as px
from shiny import App, ui, render
from shinywidgets import output_widget, render_widget
import io

# Load data from JSON file
data_url = "https://raw.githubusercontent.com/yourusername/yourrepository/main/data.json"
data = pd.read_json(data_url)

# ... (rest of your data preparation code remains the same)

# ... (your app_ui and server functions remain the same)

# Instead of running the app directly, create it and make it available globally
app = App(app_ui, server)