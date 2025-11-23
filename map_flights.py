import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap

# Load flights with coordinates
df = pd.read_csv("data/flights_with_coords.csv")

# Clean up bad/missing coordinates
df = df.dropna(subset=['dep_lat', 'dep_lon', 'arr_lat', 'arr_lon'])

# Ensure numeric types (important!)
df["dep_lat"] = pd.to_numeric(df["dep_lat"], errors="coerce")
df["dep_lon"] = pd.to_numeric(df["dep_lon"], errors="coerce")
df["arr_lat"] = pd.to_numeric(df["arr_lat"], errors="coerce")
df["arr_lon"] = pd.to_numeric(df["arr_lon"], errors="coerce")

df = df.dropna(subset=['dep_lat', 'dep_lon', 'arr_lat', 'arr_lon'])

# Create world map
plt.figure(figsize=(16, 9))
m = Basemap(projection='mill', resolution='c')
m.drawcoastlines()
m.drawcountries()

# Plot each flight properly
for _, row in df.iterrows():
    # Convert lat/lon → map projection
    x1, y1 = m(row['dep_lon'], row['dep_lat'])
    x2, y2 = m(row['arr_lon'], row['arr_lat'])

    # Draw line
    m.plot([x1, x2], [y1, y2],
           color='blue', alpha=0.5, linewidth=0.7)

plt.title("Flight Routes")
plt.show()
