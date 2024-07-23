import streamlit as st
import pandas as pd
import geopandas as gpd
import folium
from streamlit_folium import st_folium

# Load Data
@st.cache_data
def load_data():
    data = pd.read_csv('benthos_data.csv')
    return data

# Convert DataFrame to GeoDataFrame
def convert_to_geodataframe(df):
    gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.Longitude, df.Latitude))
    return gdf

# Initialize Streamlit app
st.title('Benthos Species Mapping')

# Load data
data = load_data()

# Drop rows with any NaN values
data = data.dropna()

# Convert to GeoDataFrame
gdf = convert_to_geodataframe(data)

# Sidebar Filters
st.sidebar.header('Filter Data')
selected_watershed = st.sidebar.multiselect('Select Watershed', data['Watershed'].unique())
selected_year = st.sidebar.multiselect('Select Year', data['Year'].unique())
selected_phylum = st.sidebar.multiselect('Select Phylum', data['Phylum'].unique())

# Apply filters
filtered_data = data.copy()
if selected_watershed:
    filtered_data = filtered_data[filtered_data['Watershed'].isin(selected_watershed)]
if selected_year:
    filtered_data = filtered_data[filtered_data['Year'].isin(selected_year)]
if selected_phylum:
    filtered_data = filtered_data[filtered_data['Phylum'].isin(selected_phylum)]

# Convert filtered DataFrame to GeoDataFrame
filtered_gdf = convert_to_geodataframe(filtered_data)

# Create map
m = folium.Map(location=[filtered_data['Latitude'].mean(), filtered_data['Longitude'].mean()], zoom_start=5)
for _, row in filtered_gdf.iterrows():
    folium.Marker(location=[row['Latitude'], row['Longitude']],
                  popup=f"Site: {row['Site Name']}<br>Common Name: {row['Common Name']}<br>Total Count: {row['Total Count']}<br>Date Collected: {row['Collection Date']}").add_to(m)

# Display map
st_folium(m, width=700, height=500)

# Show filtered data table
st.header('Filtered Data')
st.write(filtered_data)
