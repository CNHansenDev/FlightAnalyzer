import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def graph_flights(file_path="data/flights_organized.csv"):
    df = pd.read_csv(file_path)
    df['departure_scheduled'] = pd.to_datetime(df['departure_scheduled'], errors='coerce')
    df['day_of_week'] = df['departure_scheduled'].dt.day_name()
    df['flight_date'] = pd.to_datetime(df['departure_scheduled']).dt.date
    df['route'] = df['departure_airport'] + " → " + df['arrival_airport']

    # Top 10 delayed airports
    top_airports = df.groupby('departure_airport')['total_delay'].mean().sort_values(ascending=False).head(10)
    plt.figure(figsize=(10, 6))
    sns.barplot(x=top_airports.values, y=top_airports.index, color="red")
    plt.title("Top 10 Delayed Airports (Average Delay in Minutes)")
    plt.xlabel("Average Total Delay")
    plt.ylabel("Airport")
    plt.tight_layout()
    plt.show()

    # Average delays by day
    daily_delays = df.groupby('day_of_week')['total_delay'].mean()
    plt.figure(figsize=(8, 5))
    sns.barplot(x=daily_delays.index, y=daily_delays.values, color="blue")
    plt.title("Average Delay by Day of Week")
    plt.xlabel("Day of Week")
    plt.ylabel("Average Total Delay")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

    # Top 10 airlines by number of flights
    top_airlines = df['airline_name'].value_counts().head(10)
    plt.figure(figsize=(10, 6))
    sns.barplot(x=top_airlines.values, y=top_airlines.index, color="green")
    plt.title("Top 10 Airlines by Number of Flights")
    plt.xlabel("Number of Flights")
    plt.ylabel("Airline")
    plt.tight_layout()
    plt.show()

    # Top 10 busiest departure airports
    busiest_airports = df['departure_airport'].value_counts().head(10)
    plt.figure(figsize=(10, 6))
    sns.barplot(x=busiest_airports.values, y=busiest_airports.index, color="purple")
    plt.title("Top 10 Busiest Departure Airports")
    plt.xlabel("Number of Flights")
    plt.ylabel("Airport")
    plt.tight_layout()
    plt.show()

    # Top 10 most common routes
    popular_routes = df['route'].value_counts().head(10)
    plt.figure(figsize=(10, 6))
    sns.barplot(x=popular_routes.values, y=popular_routes.index, color="orange")
    plt.title("Top 10 Most Common Routes")
    plt.xlabel("Number of Flights")
    plt.ylabel("Route")
    plt.tight_layout()
    plt.show()

    # Flights per day
    flights_per_day = df.groupby('flight_date').size()
    plt.figure(figsize=(10, 5))
    sns.lineplot(x=flights_per_day.index, y=flights_per_day.values, marker='o')
    plt.title("Flights per Day")
    plt.xlabel("Date")
    plt.ylabel("Number of Flights")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    graph_flights()