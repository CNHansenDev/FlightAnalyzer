import pandas as pd
import ast

# Load organized flights
flights_df = pd.read_csv("data/flights_organized.csv")

# Parse nested dicts
for col in ['departure', 'arrival']:
    if flights_df[col].dtype == 'object':
        flights_df[col] = flights_df[col].apply(lambda x: ast.literal_eval(x) if pd.notna(x) else {})

# Extract IATA codes
flights_df['dep_iata'] = flights_df['departure'].apply(lambda x: x.get('iata', None))
flights_df['arr_iata'] = flights_df['arrival'].apply(lambda x: x.get('iata', None))

# Load airport coordinates
airports_df = pd.read_csv("data/airports.dat", header=None,
                          names=["Airport_ID","Name","City","Country","IATA","ICAO","Latitude","Longitude","Altitude","Timezone","DST","Tz_database","Type","Source"])

# Merge departure coordinates using IATA
flights_df = flights_df.merge(
    airports_df[['IATA','Latitude','Longitude']],
    left_on='dep_iata', right_on='IATA', how='left'
).rename(columns={"Latitude":"dep_lat", "Longitude":"dep_lon"})

# Merge arrival coordinates using IATA
flights_df = flights_df.merge(
    airports_df[['IATA','Latitude','Longitude']],
    left_on='arr_iata', right_on='IATA', how='left'
).rename(columns={"Latitude":"arr_lat", "Longitude":"arr_lon"})

# Drop extra IATA columns from merge
flights_df = flights_df.drop(columns=['IATA_x','IATA_y'])

# Save merged CSV
flights_df.to_csv("data/flights_with_coords.csv", index=False)
print("Merged flight data saved with coordinates.")