from twilio.rest import Client
from secret_settings import *

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
    if cl:
        send_message(text=client_greeting, to=CLIENT_NUMBER)
    else:
        send_message(text=other_greeting, to=MY_NUMBER)


def send_actions_alert(actions, to=MY_NUMBER):
    message = 'The following trades are now being placed: '

    for sec, action in actions.items():
        message += sec+': '+str(action)+' '

    return send_message(message, to=to)


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
