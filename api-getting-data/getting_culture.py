import requests 
import time
import hashlib
import os
import apikey
import pandas as pd
import pyeuropeana.apis as apis
import pyeuropeana.utils as utils
import json
europeana_api_key = apikey.load("EUROPEANA_API_KEY")
os.environ['EUROPEANA_API_KEY'] = europeana_api_key
def fetch_darth_vader_data():
    swapi_url = "https://swapi.dev/api/people/4/"
    
    try:
        response = requests.get(swapi_url)
        response.raise_for_status()
        darth_vader_data = response.json()
        print("Darth Vader Data:")
        print(darth_vader_data)
        return darth_vader_data
    except requests.exceptions.RequestException as e:
        print(f"Error fetching from SWAPI: {e}")
        return None


def search_europeana(query):
    try:
        result = apis.search(
            query='*',  # Searching for Darth Vader
            qf='(TYPE:IMAGE)',
            reusability='open AND permission',
            media=True,
            thumbnail=True,
            landingpage=True,
            colourpalette='#0000FF',
            theme='photography',
            sort='europeana_id',
            profile='rich',
            rows=1000,
        )

        if result and 'items' in result and isinstance(result['items'], list):
            dataframe = utils.search2df(result)

            if dataframe is not None and not dataframe.empty:
                print("\nRelated items from Europeana (as DataFrame):")
                print(dataframe.head()) 
                return dataframe
            else:
                print("No related items found in Europeana.")
                return None
        else:
            print("Invalid response structure from Europeana API.")
            return None

    except Exception as e:
        print(f"Error fetching from Europeana: {e}")
        return None

if __name__ == "__main__":
    darth_vader_data = fetch_darth_vader_data()

    europeana_dataframe = search_europeana('Darth Vader')

    if darth_vader_data is not None:
        swapi_df = pd.DataFrame([darth_vader_data])  
        swapi_df.to_csv('darth_vader_swapi_data.csv', index=False)
        print("SWAPI data saved to 'darth_vader_swapi_data.csv'.")
    
    if europeana_dataframe is not None:
        combined_data = {
            "Darth Vader Data": [darth_vader_data], 
            "Europeana Data": [europeana_dataframe.to_dict(orient='records')]
        }
        
        combined_df = pd.DataFrame(combined_data)

        combined_df.to_csv('darth_vader_europeana_data.csv', index=False)
        print("Data saved to 'darth_vader_europeana_data.csv'.")
    else:
        print("No Europeana data to save.")
