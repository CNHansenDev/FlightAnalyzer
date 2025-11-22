import pandas as pd


def analyze_flights(file_path="data/flights_organized.csv"):
    df = pd.read_csv(file_path)
    print(df.head(5))
    print(df.columns.tolist())

    # Top 10 delayed airports
    top_airports = df.groupby('departure_airport')['total_delay'].mean().sort_values(ascending=False).head(10)

    # Average delay by day of week
    df['day_of_week'] = pd.to_datetime(df['departure_scheduled']).dt.day_name()
    daily_delays = df.groupby('day_of_week')['total_delay'].mean()

    top_airlines = df['airline_name'].value_counts().head(10)

    busiest_airports = df['departure_airport'].value_counts().head(10)

    df['route'] = df['departure_airport'] + '_' + df['arrival_airport']
    popular_routes = df['route'].value_counts().head(10)

    df['flight_date'] = pd.to_datetime(df['departure_scheduled']).dt.date
    flights_per_day = df.groupby('flight_date').size()

    return top_airports, daily_delays, top_airlines, busiest_airports, popular_routes, flights_per_day


if __name__ == "__main__":
    top_airports, daily_delays, top_airlines, busiest_airports, popular_routes, flights_per_day = analyze_flights()

    print("Top 10 delayed airports:\n", top_airports)
    print("\nAverage delays by day:\n", daily_delays)
    print("\nTop 10 airlines by number of flights:\n", top_airlines)
    print("\nTop 10 busiest departure airports:\n", busiest_airports)
    print("\nTop 10 most common routes:\n", popular_routes)
    print("\nFlights per day:\n", flights_per_day)