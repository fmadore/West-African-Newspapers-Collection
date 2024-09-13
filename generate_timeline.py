import json
import pandas as pd
import plotly.graph_objs as go
from plotly.subplots import make_subplots
from pathlib import Path
import plotly.io as pio

# Set the correct path to the data file
current_dir = Path(__file__).parent
data_path = current_dir / "myapp" / "data.json"

# Load data from JSON file
try:
    with open(data_path, "r", encoding="utf-8") as file:
        data = pd.read_json(file)
except FileNotFoundError:
    print(f"Error: The file 'data.json' was not found in the directory: {data_path}")
    print("Please make sure the file exists and the path is correct.")
    exit(1)

# Filter for newspapers only
newspaper_data = data[data['Type'] == 'Newspaper'].copy()

# Convert Inception to year string
newspaper_data['Inception'] = pd.to_datetime(newspaper_data['Inception'], format='%Y', errors='coerce').dt.strftime('%Y')

# Handle Closure date, convert to year string
newspaper_data['Closure date'] = pd.to_datetime(newspaper_data['Closure date'], format='%Y', errors='coerce').dt.strftime('%Y')
newspaper_data['Closure date'] = newspaper_data['Closure date'].fillna('2024')

# Sort the data by Country and then by Inception date in descending order
newspaper_data = newspaper_data.sort_values(['Country', 'Inception'], ascending=[True, False])

# Create the timeline
fig = go.Figure()

for country in newspaper_data['Country'].unique():
    country_data = newspaper_data[newspaper_data['Country'] == country]
    fig.add_trace(go.Bar(
        x=[country_data['Closure date'], country_data['Inception']],
        y=country_data['Institute or newspaper name'],
        orientation='h',
        name=country,
        hovertemplate='<b>%{y}</b><br>Inception: %{customdata[0]}<br>Closure: %{customdata[1]}<br>Country: %{customdata[2]}<br>City: %{customdata[3]}<br>Classification: %{customdata[4]}',
        customdata=country_data[['Inception', 'Closure date', 'Country', 'City', 'Classification']].values,
        marker=dict(
            pattern=dict(
                shape=[
                    "/" if classification == 'Partially/fully digitised' else ""
                    for classification in country_data['Classification']
                ],
                size=4,
                solidity=0.9,
            )
        )
    ))

# Customize the layout
fig.update_layout(
    barmode='overlay',
    xaxis_title="Years of Publication",
    yaxis_title="Newspaper Name",
    height=2000,  # Increased height for better visibility
    width=1500,   # Increased width
    legend_title="Country",
    title="Newspaper Timeline",
    font=dict(size=12),
)

# Reverse the y-axis to have the oldest newspapers at the top
fig.update_yaxes(autorange="reversed")

# Add a legend for Classification
fig.add_trace(go.Bar(
    x=[None], y=[None],
    marker_color='rgba(0,0,0,0)',
    name='Not digitized',
    legendgroup='classification',
    legendgrouptitle_text="Status",
    showlegend=True
))
fig.add_trace(go.Bar(
    x=[None], y=[None],
    marker_color='rgba(0,0,0,0)',
    marker_pattern_shape="/",
    name='Partially/fully digitised',
    legendgroup='classification',
    legendgrouptitle_text="Status",
    showlegend=True
))

# Save the figure as an HTML file
output_file = current_dir / "newspaper_timeline.html"
pio.write_html(fig, file=str(output_file), auto_open=True)

print(f"Timeline graph has been saved as '{output_file}'")
print("The HTML file should open automatically in your default web browser.")
print("You can use your browser's print function (usually Ctrl+P or Cmd+P) to save it as a PDF or image.")