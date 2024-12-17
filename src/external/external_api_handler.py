import requests

class ExternalAPIHandler:
    def fetch_data(self, url: str, params: dict = None):
        response = requests.get(url, params=params)
        if response.status_code != 200:
            raise Exception(f"API request failed: {response.status_code}")
        return response.json()
