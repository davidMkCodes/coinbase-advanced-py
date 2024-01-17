from json import dumps
from coinbase.rest import RESTClient

api_key = "organizations/580a132a-4496-40c8-bda9-024a5a70d29c/apiKeys/0724df8b-744d-49c3-a85a-34562364b121"
api_secret = "-----BEGIN EC PRIVATE KEY-----\nMHcCAQEEIBPTxO6CNbH0WmglA2ISiAmKp4P8snmBIi3gjiOd45IWoAoGCCqGSM49\nAwEHoUQDQgAEXsJkko1qK5ljuLcF6t1jci7TIJRtGH6YnkCKgXxPXL+ReOw9FfNM\nexdWhv3BXcwpr1tomazbgHo+sGRLmwp1Wg==\n-----END EC PRIVATE KEY-----\n"

client = RESTClient(api_key=api_key, api_secret=api_secret)

accounts = client.get_accounts()
print(dumps(accounts, indent=2))