from flask import Flask, request, redirect
from twilio.twiml.messaging_response import MessagingResponse
from secret_settings import *
import outreach_utils as out
import os

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
                pid = os.fork()
                if pid == 0:
                    os.system('python main.py actions')


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
