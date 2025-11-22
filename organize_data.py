import pandas as pd
import ast


def organize_data(file_path="data/flights_cache.csv"):
    df = pd.read_csv(file_path)

    dictionary_cols = ['departure', 'arrival', 'airline']

    for col in dictionary_cols:
        if col in df.columns:
            df[col] = df[col].apply(lambda x: ast.literal_eval(x) if pd.notna(x) else {})

    # Extract fields from nested dicts
    df['departure_airport'] = df['departure'].apply(lambda x: x.get('airport', 'Unknown'))
    df['arrival_airport'] = df['arrival'].apply(lambda x: x.get('airport', 'Unknown'))
    df['departure_delay'] = df['departure'].apply(lambda x: x.get('delay', 0) or 0)
    df['arrival_delay'] = df['arrival'].apply(lambda x: x.get('delay', 0) or 0)
    df['total_delay'] = df['departure_delay'] + df['arrival_delay']
    df['airline_name'] = df['airline'].apply(lambda x: x.get('name', 'Unknown'))
    df['departure_scheduled'] = df['departure'].apply(lambda x: x.get('scheduled', pd.NaT))
    df['arrival_scheduled'] = df['arrival'].apply(lambda x: x.get('scheduled', pd.NaT))

    df['departure_scheduled'] = pd.to_datetime(df['departure_scheduled'], errors='coerce')
    df['arrival_scheduled'] = pd.to_datetime(df['arrival_scheduled'], errors='coerce')

    # Convert datetime columns
    for col in ['departure_scheduled', 'arrival_scheduled']:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors='coerce')

    # Drop rows with missing essential data
    df = df.dropna(subset=['departure_airport', 'arrival_airport'])

    df.columns = [col.replace('.', '_') for col in df.columns]

    return df


if __name__ == "__main__":
    df = organize_data()
    df.to_csv("data/flights_organized.csv", index=False)
    print("Data organized and saved to flights_organized.csv")