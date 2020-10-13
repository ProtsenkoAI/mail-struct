from pathlib import Path

default_scopes = ["https://www.googleapis.com/auth/gmail.labels",
                  "https://www.googleapis.com/auth/gmail.readonly"]

data_path = Path.cwd() / "google-cloud-data"

default_service_creds_path = data_path / "credentials.json"
default_user_token_path = data_path / "token.pickle"
