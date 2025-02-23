import requests
import pandas as pd
import json
import os

class BLSApiClient:
    BASE_URL = "https://api.bls.gov/publicAPI/v2/timeseries/data/"

    def __init__(self, api_key):
        self.api_key = api_key

    def fetch_laus_data(self, start_year, end_year, county_fips_list):
        """Fetch county-level LAUS data (unemployment) for specified counties."""
        # Build series IDs: LAUCN<state_fips><county_fips>000000003
        series_ids = [f"LAUCN{fips}0000000003" for fips in county_fips_list]

        # BLS API limits to 50 series per request; split into chunks
        chunk_size = 50
        all_data = []

        headers = {"Content-type": "application/json"}
        for i in range(0, len(series_ids), chunk_size):
            chunk = series_ids[i:i + chunk_size]
            payload = {
                "seriesid": chunk,
                "startyear": str(start_year),
                "endyear": str(end_year),
                "registrationkey": self.api_key
            }
            response = requests.post(self.BASE_URL, data=json.dumps(payload), headers=headers)

            if response.status_code != 200:
                print(f"API request failed for chunk {i//chunk_size + 1}: {response.status_code}")
                continue

            data = response.json()
            if data["status"] != "REQUEST_SUCCEEDED":
                print(f"Error in chunk {i//chunk_size + 1}: {data.get('message', 'Unknown error')}")
                continue

            all_data.extend(data["Results"]["series"])

        return self._process_data(all_data)

    def _process_data(self, series_data):
        """Process BLS JSON response into a DataFrame."""
        records = []
        for series in series_data:
            series_id = series["seriesID"]
            fips = series_id[5:10]  # Extract FIPS (e.g., "17031" from LAUCN170310000000003)

            # Handle cases where data might be empty
            if not series["data"]:
                print(f"No data returned for series {series_id}")
                continue

            for datapoint in series["data"]:
                year = int(datapoint["year"])
                period = datapoint["period"]  # e.g., "M12" for December
                value = float(datapoint["value"]) if datapoint["value"] != "-" else None

                records.append({
                    "fips": fips,
                    "year": year,
                    "month": int(period.replace("M", "")),
                    "unemployment_rate": value
                })

        df = pd.DataFrame(records)
        return df

if __name__ == "__main__":
    # Set BLS API key from environment variable
    api_key = os.getenv("BLS_API_KEY")
    if not api_key:
        raise ValueError("Please set the BLS_API_KEY environment variable.")

    # Load a county FIPS reference table (you’ll need to provide this) I used census.gov to extract this information
    try:
        fips_df = pd.read_csv("county_geoid.csv")
 
        county_fips_list = fips_df["GEOID"].tolist()
    except FileNotFoundError:
        print("Please download 'national_county.txt' from Census and place it in the working directory.")
        # Fallback: Use a small test list
        county_fips_list = ["17031", "17037", "06037"]  # Cook IL, DuPage IL, Los Angeles CA

    bls_client = BLSApiClient(api_key)

    # Fetch data for 2023-2024 (latest available as of Feb 22, 2025)
    start_year = 2024
    end_year = 2025
    bls_data = bls_client.fetch_laus_data(start_year, end_year, county_fips_list)

    # Filter for the most recent complete month
    if not bls_data.empty:
        latest_data = bls_data[
            (bls_data["year"] == bls_data["year"].max()) & 
            (bls_data["month"] == bls_data["month"].max())
        ][["fips", "unemployment_rate"]]

        # Handle missing values
        latest_data = latest_data.dropna()

        print("\nNational County-Level BLS Unemployment Data (Latest Month Sample):")
        print(latest_data.head())


