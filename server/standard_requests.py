from server.gmail_service import get_default_gmail_service
from time import time


def get_labeled_letters(service):
    gmail_users = service.users()
    messages = gmail_users.messages()
    list_of_messages = messages.list(userId="me", fields="messages/id").execute()
    print(list_of_messages)


def label_letter(): # функция для продакшена, не знаю, как работает => не знаю, как назвать
    ...


if __name__ == "__main__":
    service = get_default_gmail_service()
    train_data = get_labeled_letters(service)
