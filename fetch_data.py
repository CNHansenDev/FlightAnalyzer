import requests
import pandas as pd

API_KEY = "e1ad387cd0d84ae7190fca2e88f996ea"
BASE_URL = "http://api.aviationstack.com/v1/flights"

def fetch_flights(params):
    params['access_key'] = API_KEY
    response = requests.get(BASE_URL, params=params)
    data = response.json()['data']
    df = pd.DataFrame(data)
    return df

if __name__ == "__main__":
    params = {"limit": 100}  # Example: fetch 100 flights
    df = fetch_flights(params)
    df.to_csv("data/flights_cache.csv", index=False)
    print("Data fetched and saved to flights_cache.csv")