from secret_settings import *
import requests
import time
import sys

telegram_host = 'https://api.telegram.org/bot'
telegram_retrieve_path = '/getUpdates'
telegram_send_path = '/sendMessage'


def build_telegram_url(action='send'):
    if action == 'send':
        return telegram_host + TELEGRAM_BOT_TOKEN + telegram_send_path
    elif action == 'retrieve':
        return telegram_host + TELEGRAM_BOT_TOKEN + telegram_retrieve_path


def send_message(text='Default', to=TELEGRAM_CHAT_ID):
    url = build_telegram_url()
    requests.post(url=url, params={'chat_id': to, 'text': text})


def send_greeting(which='self'):
    if which == 'self':
        send_message(SELF_GREETING)


def wait_for_message(max_age=3):
    response = None

    while not response:
        message = get_most_recent_message_from_user(TELEGRAM_USERNAME)
        try:
            message_text = message['message']['text']
            timestamp = message['message']['date']
            assert time.time() - timestamp < max_age
            if message_text.strip().lower() == 'not now':
                send_message('Terminating the trading session. Will retry later.')
                sys.exit(0)
        except KeyError:
            send_message('Something is wrong with the message keys. Terminating now and will retry later.')
            sys.exit(1)
        except AssertionError:
            response = None
        time.sleep(0.1)

    return message_text


def get_trading_confirmation():
    send_message('Would you like to proceed with the trades? (y/n)')
    confirmation = wait_for_message()
    affirmative = ['yes', 'y', 'ye', 'yah', 'yeah', 'sure', 'go for it', 'proceed']
    if confirmation.strip().lower() in affirmative:
        return True
    return False


def send_actions(actions):
    action_message = 'The following trades are proposed:\n'
    for sec, action in actions.items():
        action = round(float(action),2)
        if action > 0:
            action_string = f'+${action}'
        elif action < 0:
            action_string = f'-${action}'
        else:
            action_string = 'No Change'

        action_message += f'{sec}: {action_string}\n'
    send_message(action_message)


def filter_messages_by_username(username, messages):
    filtered_messages = []
    for message in messages:
        if message['message']['from'].get('username', '-1') == username:
            filtered_messages.append(message)
    return filtered_messages


def get_most_recent_message_from_user(username):
    messages = requests.get(build_telegram_url(action='retrieve')).json()
    filtered_messages = filter_messages_by_username(username, messages['result'])
    return filtered_messages[-1]


def get_auth_token(login_email=LOGIN_EMAIL, retry_message=None, max_token_age=2):
    if retry_message:
        send_message(retry_message)
    else:
        send_message(f"Attempting to login to {login_email}. Please send the auth token or reply 'not now' to terminate.")

    return wait_for_message()





