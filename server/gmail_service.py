import os.path
import pickle
import socket
from pathlib import Path
from googleapiclient.discovery import build

from server.settings import default_scopes, default_service_files_path
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow


class GMailService:
    def __init__(self, files_path, scopes=None, force_reset=False, save_things=True):
        self.files_path = Path(files_path)

        self.service_creds_path = str(self.files_path / "credentials.json")
        self.token_path = str(self.files_path / "token.pickle")
        self.service_path = str(self.files_path / "service.pickle")

        self.scopes = scopes
        self.force_reset = force_reset
        self.save_things = save_things

        self._create()

    def _create(self):
        """Gets token and returns service for it."""
        creds = self._get_token()
        service = self._build_service(creds)

        return service

    def _get_token(self):
        if self._check_token_ready() and not self.force_reset:
            token_creds = self._load_token()
        else:
            token_creds = self._create_token()

        return token_creds

    def _check_token_ready(self, ):
        if os.path.isfile(self.token_path):
            token = self._load_token()
            token_refreshable = not token.expired or token.expred and token.refresh_token
            if token.valid and token_refreshable:
                return True

        else:
            return False

    def _load_token(self, ):
        token_creds = self._pickle_load(self.token_path)

        if token_creds.expired and token_creds.refresh_token:
            token_creds.refresh(Request())

        return token_creds

    def _create_token(self):
        assert self.scopes is not None, \
            "if new token is created, you should provide scopes for it in ServiceCreator init."

        flow = InstalledAppFlow.from_client_secrets_file(self.service_creds_path, self.scopes)
        token_creds = flow.run_local_server(port=0)

        if self.save_things:
            self._pickle_save(token_creds, self.token_path)

        return token_creds

    def _pickle_save(self, obj, path):
        with open(path, "wb") as file:
            pickle.dump(obj, file)

    def _pickle_load(self, path):
        with open(path, "rb") as file:
            obj = pickle.load(file)

        return obj

    def _build_service(self, token_creds):
        socket.setdefaulttimeout(1000)  # fixing problem with socket.timeout during build

        if os.path.isfile(self.service_path) and not self.force_reset:
            service = self._pickle_load(self.service_path)
        else:
            service = self._create_service(token_creds)

        return service

    def _create_service(self, token_creds):
        service = build('gmail', 'v1', credentials=token_creds)

        if self.save_things:
            self._pickle_save(service, self.service_path)

        return service


def get_default_gmail_service():
    default_service_creator = GMailService(default_service_files_path, default_scopes)
    return default_service_creator


if __name__ == "__main__":
    service = get_default_gmail_service()
    print(service)
    gmail_users = service.users()
    print(gmail_users)
    users_labels = gmail_users.labels()
    results = users_labels.list(userId='me').execute()

    labels = results.get('labels', [])

    if not labels:
        print('No labels found.')
    else:
        print('Labels:')
        for label in labels:
            print(label['name'])
