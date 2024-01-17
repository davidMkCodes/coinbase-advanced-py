from json import dumps
from coinbase.rest import RESTClient

api_key = ""
api_secret = ""

client = RESTClient(api_key=api_key, api_secret=api_secret)

accounts = client.get_accounts()
print(dumps(accounts, indent=2))
