# ამ ფაილში არის კოდები რომლითაც ვქმნით აპი ტოკენს ვუკავშირდებით აპი-ს და ვითხოვთ მონაცემებს

import requests
import base64 # ვაქცევთ მონაცემებს ფორმატში რომელიც ჭირდება ebay-ს (დოკუმენტაცია)
class EbayApi:
    def __init__(self,client_id,client_secret,environment = "sandbox"): # ჩვენ არ ვიყენებთ სენდბოქს უბრალოდ თუ სენდბოხი იქნება გამოიყენბეს მის ლინკს
        self.client_id = client_id
        self.client_secret = client_secret # მონაცემები აპი-ს გარემოსი
        self.environment = environment
        self.access_token = None
        if environment == "sandbox":
            self.base_url = "https://api.sandbox.ebay.com"
        else:
            self.base_url = "https://api.ebay.com"
    def get_access_token(self): # ვიღებთ tokens 
        credentials = f"{self.client_id}:{self.client_secret}"
        encoded_credentials = base64.b64encode(credentials.encode()).decode() # აქცევს ჩვენს მონაცემს ბიტებათ შემდეგ base64 და შემდეგ ისევ ტექსტად
        url = f"{self.base_url}/identity/v1/oauth2/token"

        headers = {
            "Authorization": f"Basic {encoded_credentials}",
            "Content-Type": "application/x-www-form-urlencoded"
        }

        data = {
            "grant_type": "client_credentials",
            "scope": "https://api.ebay.com/oauth/api_scope"
        }
        response = requests.post(url, headers=headers, data=data) # ვაგზავნით რექუესთს
        response.raise_for_status() # ამოწმებს თუ რექუესთი კარგად შესრულდა თუ არა აბრუებს კოდს

        token_data = response.json()
        self.access_token = token_data["access_token"]

        return self.access_token

    def search_items(self, keyword, limit=10): # ამ ფუნქციით ვეძებთ 10 ნივთს
        if self.access_token is None:
            self.get_access_token() # ვამოწმებთ თუ გვაქვს თოქენი

        url = f"{self.base_url}/buy/browse/v1/item_summary/search"

        headers = {
            "Authorization": f"Bearer {self.access_token}"
        }

        params = { # პარამეტრები თუ რას ვეძებთ და რამდენს
            "q": keyword,
            "limit": limit
        }

        response = requests.get(url, headers=headers, params=params)  # ვითხოვთ ნივთებს
        response.raise_for_status()

        data = response.json()
        return data.get("itemSummaries", []) # ვიღებთ ლისტს სადაც ნივთების მონაცემებია დიქშინერებში