from flask import Flask, request, redirect
from twilio.twiml.messaging_response import MessagingResponse
from secret_settings import *
from outreach_utils import client

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
        query = client.preview.understand.assistants(TWI_ASSISTANT) \
            .queries.create(language='en-US', query=body)

        task = query.results.get('task')

        resp.message(task)

    return str(resp)


if __name__ == "__main__":
    app.run(host="0.0.0.0")
