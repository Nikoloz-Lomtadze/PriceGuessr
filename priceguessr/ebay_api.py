import requests
import base64
class EbayApi:
    def __init__(self,client_id,client_secret,environment = "sandbox"):
        self.client_id = client_id
        self.client_secret = client_secret
        self.environment = environment
        self.access_token = None
        if environment == "sandbox":
            self.base_url = "https://api.sandbox.ebay.com"
        else:
            self.base_url = "https://api.ebay.com"
    def get_access_token(self):
        credentials = f"{self.client_id}:{self.client_secret}"
        encoded_credentials = base64.b64encode(credentials.encode()).decode()
        url = f"{self.base_url}/identity/v1/oauth2/token"

        headers = {
            "Authorization": f"Basic {encoded_credentials}",
            "Content-Type": "application/x-www-form-urlencoded"
        }

        data = {
            "grant_type": "client_credentials",
            "scope": "https://api.ebay.com/oauth/api_scope"
        }
        response = requests.post(url, headers=headers, data=data)
        response.raise_for_status()

        token_data = response.json()
        self.access_token = token_data["access_token"]

        return self.access_token

    def search_items(self, keyword, limit=10):
        if self.access_token is None:
            self.get_access_token()

        url = f"{self.base_url}/buy/browse/v1/item_summary/search"

        headers = {
            "Authorization": f"Bearer {self.access_token}"
        }

        params = {
            "q": keyword,
            "limit": limit
        }

        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()

        data = response.json()
        return data.get("itemSummaries", [])