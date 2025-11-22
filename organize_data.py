import pandas as pd


def organize_data(file_path="data/flights_cache.csv"):
    df = pd.read_csv(file_path)

    datetime_cols = ["departure.scheduled", "arrival.scheduled"]

    for col in datetime_cols:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors='coerce')
        else:
            df[col] = pd.NaT

    depart_delay = 'departure.delay'
    arrival_delay = 'arrival.delay'

    if 'depart_delay' in df.columns and 'arrival_delay' in df.columns:
        df['total_delay'] = df['depart_delay'].fillna(0) + df['arrival_delay'].fillna(0)
    else:
        df['total_delay'] = None

    essential_cols = ['departure.airport', 'arrival.airport']
    for col in essential_cols:
        if col not in df.columns:
            df[col] = None


    df = df.dropna(subset=essential_cols)

    df = df.dropna(subset=["departure.scheduled", "arrival.scheduled"])

    df.columns = [col.replace('.', '_') for col in df.columns]

    return df


if __name__ == "__main__":
    df = organize_data()
    df.to_csv("data/flights_organized.csv", index=False)
    print("Data organized and saved to flights_organized.csv")