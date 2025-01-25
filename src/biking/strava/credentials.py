import os


class Credentials:
    def __init__(self, params):
        self.client_id = params.auth.client_id
        self.client_secret = params.auth.client_secret
        self.app_auth_code = params.auth.app_code
        self.access_tokens_file = params.auth.access_tokens_file

        self.access_token = None
        self.refresh_token = None

    def load_access_tokens(self):
        file = self.access_tokens_file
        if not os.path.exists(file):
            return False

        self.access_token = None
        self.refresh_token = None

        with open(file, "r") as f:
            for line in f:
                line = line.strip()
                if "=" in line:
                    name, value = line.split("=", 1)
                    if name == "access_token":
                        self.access_token = value
                    elif name == "refresh_token":
                        self.refresh_token = value

        return self.access_token and self.refresh_token

    def store_access_tokens(self):
        file = self.access_tokens_file

        with open(file, "w") as f:
            f.write(f"access_token={self.access_token}\n")
            f.write(f"refresh_token={self.refresh_token}\n")
