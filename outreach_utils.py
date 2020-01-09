from twilio.rest import Client
from secret_settings import *
import time
import rebalance_utils as re

account_sid = TWIL_ACCT_SID
auth_token = TWIL_AUTH_TOKEN

client = Client(account_sid, auth_token)


def send_message(text='Default', to=CLIENT_NUMBER):
    message = client.messages.create(
        body=text,
        from_=TWILIO_NUMBER,
        to=to
    )

    return message.sid


def send_greeting(cl=True):

    with open("last_greeting.txt", "w") as file:
        seconds = time.time()
        file.write(str(seconds) + "\n")
        file.close()

    if cl:
        send_message(text=client_greeting, to=CLIENT_NUMBER)
    else:
        send_message(text=other_greeting, to=MY_NUMBER)


def send_actions_alert(num=MY_NUMBER):
    message = 'The following trades are now being placed: '

    actions = re.get_actions()

    for sec, action in actions.items():
        message += sec+': '+str(action)+' '

    send_message(message, to=num)

    return actions


def send_order_notifications(confirmations, to=MY_NUMBER):
    success = []
    failure = []
    order_ids = []

    for sec, result in confirmations.items():
        try:
            order_ids.append(result['id'])
            success.append(sec)
        except KeyError:
            failure.append(sec)

    message = 'These securities were successfully ordered: ' + str(success)
    a = send_message(message, to=to)
    message = 'These securities failed: ' + str(failure)
    b = send_message(message, to=to)

    return a, b


def send_waiting_token(to=MY_NUMBER):
    send_message('Waiting for token. Please go to https://bit.ly/2N9FTyH to send it.', to=to)
    time.sleep(30)
    send_message('Now fetching token.', to=to)


def get_task(body):
    query = client.preview.understand.assistants(TWIL_ASSISTANT) \
        .queries.create(language='en-US', query=body)

    task = query.results.get('task')

    return task


def check_recency():

    try:
        with open('last_greeting.txt', 'r') as file:
            last = float(file.read())
    except FileNotFoundError:
        return False

    now = time.time()

    if now-last > 120:
        return False
    else:
        return True


def send_confirmation():
    send_message("Great! Now proceeding.")


def send_token_conf(status):
    if status:
        send_message("Token successfully received!")
    else:
        send_message("Something broke.")



