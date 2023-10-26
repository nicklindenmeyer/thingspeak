import requests
import pandas as pd
import streamlit as st

def get_data_from_thingspeak(channel_id, read_key):
    endpoint = f"https://api.thingspeak.com/channels/{channel_id}/feeds.json"
    params = {
        "api_key": read_key,
        "results": 8000
    }
    response = requests.get(endpoint, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()

data = get_data_from_thingspeak('2302302', 'A5W7L8EBQ74NJ3YH')

df = pd.DataFrame(data['feeds'])

print(df)

df