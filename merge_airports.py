import pandas as pd

# Load organized flights
flights_df = pd.read_csv("data/flights_organized.csv")

# Load airport coordinates
airports_df = pd.read_csv("data/airports.dat", header=None,
                          names=["Airport_ID","Name","City","Country","IATA","ICAO","Latitude","Longitude","Altitude","Timezone","DST","Tz_database","Type","Source"])

# Merge departure airport coordinates
flights_df = flights_df.merge(
    airports_df[['ICAO','Latitude','Longitude']],
    left_on='departure_airport', right_on='ICAO', how='left'
).rename(columns={"Latitude":"dep_lat", "Longitude":"dep_lon"})

# Merge arrival airport coordinates
flights_df = flights_df.merge(
    airports_df[['ICAO','Latitude','Longitude']],
    left_on='arrival_airport', right_on='ICAO', how='left'
).rename(columns={"Latitude":"arr_lat", "Longitude":"arr_lon"})

# Drop the extra ICAO columns created by merge
flights_df = flights_df.drop(columns=['ICAO_x', 'ICAO_y'])

# Save merged CSV
flights_df.to_csv("data/flights_with_coords.csv", index=False)
print("Merged flight data saved with coordinates.")