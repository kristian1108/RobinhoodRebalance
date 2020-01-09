from flask import Flask, request, redirect
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

@app.route('/')
def hello():
	return "<h1 style='color:blue'>Hello There!</h1>"

@app.route('/sms', methods=['GET', 'POST'])
def sms_reply():
	resp = MessagingResponse()
	resp.message("Hola")

	return str(resp)

if __name__ == "__main__":
	app.run(host="0.0.0.0")



