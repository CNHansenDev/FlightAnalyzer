import requests
import pandas as pd
import os

API_KEY = "e1ad387cd0d84ae7190fca2e88f996ea"
BASE_URL = "http://api.aviationstack.com/v1/flights"
OUTPUT_FILE = "data/flights_cache.csv"


def fetch_flights(params):
    params['access_key'] = API_KEY
    response = requests.get(BASE_URL, params=params)

    # Check request
    if response.status_code != 200:
        print(f"API request failed. Code: {response.status_code}")
        print(response.text)
        return None

    json_data = response.json()

    # Check API
    if "error" in json_data:
        print("API Error:", json_data["error"])
        return None

    data = json_data.get("data", [])

    if not data:
        print("No flight data.")
        return pd.DataFrame()

    df = pd.DataFrame(data)
    return df


if __name__ == "__main__":
    os.makedirs("data", exist_ok=True)
    params = {"limit": 100}
    df = fetch_flights(params)

    if df is not None and not df.empty:
        df.to_csv(OUTPUT_FILE, index=False)
        print(f"Data saved to {OUTPUT_FILE}")
    else:
        print("Data not saved.")