import plotly.express as px
import json
import pandas as pd
import plotly.graph_objects as go


def convert_csv_to_json(csv_Africa_covid_data, csv_Europe_covid_data, json_Africa_output, json_Europe_output):
    # Read CSV files into pandas DataFrames
    df_Europe = pd.read_csv(csv_Europe_covid_data)

    # Convert DataFrames to JSON and save to new files
    df_Europe.to_json(json_Europe_output, orient='records', lines=True)

# Replace  'csv-Europe-covid-data.csv' to 'json-Europe-output.json' with your actual filenames
convert_csv_to_json('csv-Europe-covid-data.csv','json-Europe-output.json')



# this is a world data, filter out Europe

# Load the Europe JSON data
with open('json-Europe-output.json') as f:
    data_europe = pd.read_json(f, lines=True)

# Filter the data for Europe
europe_data_filtered = data_europe[data_europe['continent'] == 'Europe']

# Save the filtered data to a new JSON file
europe_data_filtered.to_json('json-Europe-Filtered.json', orient='records', lines=True)




# Open and load the JSON file
with open('json-Europe-Filtered.json', 'r') as file:
    data = [json.loads(line) for line in file]

# Convert the JSON data to a DataFrame
europe_filtered_data = pd.DataFrame(data)

# Select specific columns for Europe
europe_selected_columns = europe_filtered_data[
    ['iso_code', 'continent', 'location', 'date', 'total_cases', 'population',
     'total_vaccinations', 'people_vaccinated', 'people_fully_vaccinated',
     'total_vaccinations_per_hundred', 'people_vaccinated_per_hundred',
     'people_fully_vaccinated_per_hundred']
]

# Save the DataFrame to a new JSON file
europe_selected_columns.to_json('json-Europe-SelectedColumns.json', orient='records', lines=True)


# Load your Europe data
europe_df = pd.read_json('json-Europe-SelectedColumns.json', lines=True)

# Replace 'date', 'total_vaccinations', and 'location' with your actual column names
# Convert the 'date' column to datetime if it's not already
europe_df['date'] = pd.to_datetime(europe_df['date'])

# Extract year and month from the date
europe_df['year_month'] = europe_df['date'].dt.to_period('M').astype(str)  # Convert Period to string

# Group by location and year_month, aggregating total vaccinations
grouped_df = europe_df.groupby(['location', 'year_month'], as_index=False).agg({
    'iso_code': 'first',
    'continent': 'first',
    'date': 'first',
    'total_cases': 'sum',
    'population': 'first',
    'total_vaccinations': 'sum',
    'people_vaccinated': 'sum',
    'people_fully_vaccinated': 'sum',
    'total_vaccinations_per_hundred': 'sum',
    'people_vaccinated_per_hundred': 'sum',
    'people_fully_vaccinated_per_hundred': 'sum'
})

# Create a choropleth using Plotly Express based on total vaccinations
fig = px.choropleth(grouped_df,
                    locations='location',
                    locationmode='country names',
                    color='total_vaccinations',
                    hover_name='location',
                    hover_data=grouped_df.columns,
                    animation_frame='year_month',
                    color_continuous_scale='Viridis',
                    title="Total Vaccinations Choropleth Across Locations in Europe",
                    width=1200,
                    height=800,
                    projection='natural earth'
                    )

# Use Europe-specific projection and set the initial center and zoom
fig.update_geos(
    projection_type="natural earth",
    center=dict(lon=10, lat=50),
    scope="europe",
)


# Show the plot
fig.show()





















