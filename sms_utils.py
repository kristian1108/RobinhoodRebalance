from flask import Flask, request, redirect
from twilio.twiml.messaging_response import MessagingResponse
from secret_settings import *
import outreach_utils as out
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
                resp.message("Ok let's go.")

    return str(resp)


if __name__ == "__main__":
    app.run(host="0.0.0.0")
