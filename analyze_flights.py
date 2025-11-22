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

    return top_airports, daily_delays


if __name__ == "__main__":
    top_airports, daily_delays = analyze_flights()
    print("Top 10 delayed airports:\n", top_airports)
    print("\nAverage delays by day:\n", daily_delays)