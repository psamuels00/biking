import requests


class Authentication:
    def __init__(self, params, credentials):
        self.params = params
        self.credentials = credentials

        if not credentials.load_access_tokens():
            self.exchange_tokens()

    def exchange_tokens(self, refresh=False):
        data = dict(
            client_id=self.credentials.client_id,
            client_secret=self.credentials.client_secret,
        )

        if not refresh:
            data["code"] = self.credentials.app_auth_code
            data["grant_type"] = "authorization_code"
        else:
            data["refresh_token"] = self.credentials.refresh_token
            data["grant_type"] = "refresh_token"

        response = requests.post(self.params.url.token, data=data)

        if response.status_code == 200:
            data = response.json()

            self.credentials.access_token = data["access_token"]
            self.credentials.refresh_token = data["refresh_token"]
            self.credentials.store_access_tokens()
        else:
            print(f"**** Error: {response.status_code}")
            print("**** Response:", response.text)

    def refresh_tokens(self):
        self.exchange_tokens(refresh=True)


