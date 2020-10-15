from pathlib import Path

default_scopes = ["https://www.googleapis.com/auth/gmail.labels",
                  "https://www.googleapis.com/auth/gmail.readonly"]

data_path = Path.cwd() / "google-cloud-data"

default_service_files_path = "./google-cloud-data/"
