# RobinhoodTrader
This package is designed to automate rebalancing trades in Robinhood. It was built with the robin_stocks api wrapper, which can be found at http://www.robin-stocks.com/en/latest/.

## Setup
Ensure you have a Python 3 virtual environment set up and activated before running. To install dependencies, run:
```
pip install -r requirements.txt
```

## Secret Settings
You must have a `secret_settings.py` file in the project directory to run the program. This file must contain values for the following variables:

```
CLIENT_NUMBER = If you are managing for third party, you can send SMS notifications to them. Example: '+11234567899'
MY_NUMBER = Send SMS notifications to yourself. Example: '+11234567899'
TWILIO_NUMBER = The Twilio number that messages should originate from. Example: '+11234567899'

BOND_SECURITIES = List of bonds that you would like to own. Example: ['BND', 'TLT']
LT_SECURITIES = List of other assets. Example: ['VOO', 'AAPL']

BOND_ALLOCATIONS = Dictionary of asset and percentage. Percentagese must add up to 1. Example: {'BND':0.75, 'BNDX':0.25}
LT_ALLOCATIONS = Dictionary of asset and percentage. Percentagese must add up to 1. Example: {'VOO':0.75, 'AAPL':0.25}

LT_VALUE = Nominal portfolio value of your LT securities in dollars. Example:100000
TRADING_BUFFER = Won't place trades that lead to having less than this amount of cash left over. Example:100

LOGIN_EMAIL = Robinhood email to login. Example: 'me@gmail.com'
LOGIN_PASSWORD = Robinhood password. Example: 'password'

TWIL_ACCT_SID = Twilio account SID. Example: 'AB2343BE'
TWIL_AUTH_TOKEN = Twilion auth token. Example: '23424234223sdfas'

client_greeting = Initial message to client. Example: 'Hello, Amy.'
other_greeting = Initial message to other. Example: 'Hello.'
```

## Run
Running the main program will first send out a greeting to you client. Then, it will compute the trades that must be executed
in order to achieve a portfolio of `BOND_SECURITIES + LT_SECURITIES` at the desired level of allocations. Your client will 
be notified of the planned trades. The trades will then be sent to Robinhood as 'good for day' market orders, with sell
orders occurring first for the sake of cash flow. Finally, notifications will be sent indicating which trades were successful
and which failed for any reason. 

To run:
```
python main.py
```
