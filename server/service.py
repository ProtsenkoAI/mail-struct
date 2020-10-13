# TODO: make class to operate conveniently with scopes and pathes

import os.path
import pickle
import socket
from googleapiclient.discovery import build

from server.settings import default_scopes, default_user_token_path, default_service_creds_path
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow


def get_service():
    """Gets token and returns service for it."""
    creds = get_token()
    service = build_service(creds)

    return service


def get_token():
    if check_token_ready():
        token_creds = load_token()
    else:
        token_creds = create_token()

    return token_creds


def build_service(token_creds):
    socket.setdefaulttimeout(1000)  # fixing problem with socket.timeout during build
    service = build('gmail', 'v1', credentials=token_creds)
    return service


def check_token_ready():
    if os.path.isfile(default_user_token_path):
        token = load_token()
        token_refreshable = not token.expired or token.expred and token.refresh_token
        if token.valid and token_refreshable:
            return True

    else:
        return False


def load_token():
    with open(default_user_token_path) as token_file:
        token_creds = pickle.load(token_file)

    if token_creds.expired and token_creds.refresh_token:
        token_creds.refresh(Request())

    return token_creds


def create_token(save=True):
    flow = InstalledAppFlow.from_client_secrets_file(default_service_creds_path, default_scopes)
    token_creds = flow.run_local_server(port=0)

    if save:
        save_token(token_creds)

    return token_creds


def save_token(token_creds):
    with open(default_user_token_path, "wb") as token_file:
        pickle.dump(token_creds, token_file)


if __name__ == "__main__":
    service = get_service()
    print(service)