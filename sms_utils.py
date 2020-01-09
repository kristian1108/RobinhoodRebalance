from flask import Flask, request, redirect
from twilio.twiml.messaging_response import MessagingResponse
from secret_settings import *
import outreach_utils as out
from threading import Thread
import api_utils as api
import os
import time

app = Flask(__name__)


@app.route('/')
def hello():
    return "<h1 style='color:blue'>Hello There!</h1>"


@app.route('/sms', methods=['GET', 'POST'])
def sms_reply():
    body = request.values.get('Body', None)
    sender = request.values.get('From', None)
    resp = MessagingResponse()

    if sender != MY_NUMBER and sender != CLIENT_NUMBER:
        resp.message("Request refused. Have a nice day.")

    else:
        task = out.get_task(body)

        if task == 'proceed':

            if out.check_recency():
                resp.message("Great! Now proceeding.")
                for i in range(1, 100):
                    a = 6+9

                #th = Thread(target=out.send_actions_alert())
                #th.start()

            else:
                resp.message('Your trading session is not active right now.')


        """
        if task == 'approval':
            if out.check_recency():
                resp.message('Ok, now executing.')

                with open("actions.txt", "w") as file:
                    actions = file.read()

                os.remove('actions.txt')

                confirmations = api.TradingSession.rebalance(actions)
                out.send_order_notifications(confirmations, to=MY_NUMBER)

            else:
                resp.message('Your trading session is not active right now.')
        """

    return str(resp)


if __name__ == "__main__":
    app.run(host="0.0.0.0")
