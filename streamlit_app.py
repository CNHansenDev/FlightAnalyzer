import streamlit as st
import pandas as pd
from streamlit_folium import st_folium
import folium
import ast

from graph_flights import graph_flights


# -----------------------
# Load Data
# -----------------------
@st.cache_data
def load_flights():
    df = pd.read_csv("data/flights_with_coords.csv")

    # Cleanup numeric types
    for col in ['dep_lat','dep_lon','arr_lat','arr_lon']:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df = df.dropna(subset=['dep_lat','dep_lon','arr_lat','arr_lon'])
    return df

@st.cache_data
def load_summary(csv_path="data/flights_organized.csv"):
    # Load CSV
    df = pd.read_csv(csv_path)

    # Parse stringified dictionaries into actual dicts
    df['departure'] = df['departure'].apply(ast.literal_eval)
    df['arrival'] = df['arrival'].apply(ast.literal_eval)

    # Extract IATA codes for merging and mapping
    df['dep_iata'] = df['departure'].apply(lambda x: x.get('iata'))
    df['arr_iata'] = df['arrival'].apply(lambda x: x.get('iata'))

    # Extract full airport names if needed
    df['departure_airport_full'] = df['departure'].apply(lambda x: x.get('airport'))
    df['arrival_airport_full'] = df['arrival'].apply(lambda x: x.get('airport'))

    # Convert scheduled times to datetime
    df['departure_scheduled'] = pd.to_datetime(df['departure_scheduled'], errors='coerce')
    df['arrival_scheduled'] = pd.to_datetime(df['arrival_scheduled'], errors='coerce')

    # Day of week and flight date
    df['day_of_week'] = df['departure_scheduled'].dt.day_name()
    df['flight_date'] = df['departure_scheduled'].dt.date

    # Build route string
    df['route'] = df['dep_iata'] + " → " + df['arr_iata']

    return df

flights_map = load_flights()
flights_summary = load_summary()
print(flights_summary.columns)


# -----------------------
# Streamlit Layout
# -----------------------
st.title("✈️ Flight Dashboard")
st.write("Live flight data processed through AviationStack + Airport Merging + Route Visualization")



# -----------------------
# Sidebar Filters (cleaned)
# -----------------------

# Ensure all string columns are strings and fill missing values
flights_summary['airline_name'] = flights_summary['airline_name'].fillna("Unknown").astype(str)
flights_summary['departure_airport'] = flights_summary['departure_airport'].fillna("Unknown").astype(str)
flights_summary['arrival_airport'] = flights_summary['arrival_airport'].fillna("Unknown").astype(str)

# Multiple filters in sidebar
selected_airline = st.sidebar.multiselect(
    "Select Airline",
    sorted(flights_summary['airline_name'].unique())
)

selected_dep_airport = st.sidebar.multiselect(
    "Departure Airport",
    sorted(flights_summary['departure_airport'].unique())
)

selected_arr_airport = st.sidebar.multiselect(
    "Arrival Airport",
    sorted(flights_summary['arrival_airport'].unique())
)

# Time slider (departure hour)
time_range = st.sidebar.slider(
    "Departure Hour",
    0, 23, (0, 23)
)

# -----------------------
# Apply filters to dataframe
# -----------------------
filtered_summary = flights_summary.copy()

if selected_airline:
    filtered_summary = filtered_summary[filtered_summary['airline_name'].isin(selected_airline)]

if selected_dep_airport:
    filtered_summary = filtered_summary[filtered_summary['departure_airport'].isin(selected_dep_airport)]

if selected_arr_airport:
    filtered_summary = filtered_summary[filtered_summary['arrival_airport'].isin(selected_arr_airport)]

filtered_summary = filtered_summary[
    (filtered_summary['departure_scheduled'].dt.hour >= time_range[0]) &
    (filtered_summary['departure_scheduled'].dt.hour <= time_range[1])
]

filtered_summary = pd.merge(
    filtered_summary,
    flights_map[['dep_iata','arr_iata','dep_lat','dep_lon','arr_lat','arr_lon']],
    on=['dep_iata','arr_iata'],
    how='left'
)

filtered_summary = filtered_summary.dropna(subset=['dep_lat','dep_lon','arr_lat','arr_lon'])



tabs = st.tabs(["Overview", "Routes Map", "Airlines", "Airports", "Data Explorer"])
overview_tab, routes_tab, airlines_tab, airports_tab, data_tab = tabs

with overview_tab:
    st.subheader("KPIs")
    col1, col2, col3, col4, col5 = st.columns((1,1,1,3,3))

    num_flights = len(filtered_summary)

    # Check if the DataFrame is not empty
    if num_flights > 0:
        busiest_airport = filtered_summary['departure_airport'].mode()[0]
        most_common_route = filtered_summary['route'].mode()[0]
        avg_distance = round(filtered_summary['distance'].mean(),
                             2) if 'distance' in filtered_summary.columns else "N/A"
        airports_used = filtered_summary['departure_airport'].nunique()
    else:
        # Define default values for when no flights are filtered
        busiest_airport = "N/A"
        most_common_route = "N/A"
        avg_distance = "N/A"
        airports_used = 0

    col1.metric("Total Flights", num_flights)
    col2.metric("Airports Used", airports_used)
    col3.metric("Avg Distance (km)", avg_distance)
    col4.metric("Busiest Airport", busiest_airport)
    col5.metric("Most Common Route", most_common_route)

with routes_tab:
    st.subheader("Flight Route Map")

    if len(filtered_summary) > 0:
        # Only proceed with map creation if there are flights to display
        m = folium.Map(location=[filtered_summary['dep_lat'].mean(), filtered_summary['dep_lon'].mean()], zoom_start=3)

        route_counts = filtered_summary['route'].value_counts().to_dict()
        filtered_summary['route_count'] = filtered_summary['route'].map(route_counts)

        # Iterating over a potentially large DataFrame can be slow.
        # Consider using `apply` or vectorization for large datasets,
        # but the current loop is fine for prototyping.
        for _, row in filtered_summary.iterrows():
            folium.Marker([row['dep_lat'], row['dep_lon']], tooltip=f"Departure: {row['dep_iata']}").add_to(m)
            folium.Marker([row['arr_lat'], row['arr_lon']], tooltip=f"Arrival: {row['arr_iata']}").add_to(m)
            folium.PolyLine([[row['dep_lat'], row['dep_lon']], [row['arr_lat'], row['arr_lon']]],
                            weight=2 + row.get('route_count', 1), color='blue', opacity=0.6).add_to(m)

        st_folium(m, width=900, height=600)
    else:
        # Display a message if no flights are available for the map
        st.info("No flights match the current filter selection to display on the map.")

with airlines_tab:
    st.subheader("Flight Analytics")
    graph_flights(filtered_summary)

with data_tab:
    st.subheader("Data Explorer")
    st.dataframe(filtered_summary)

