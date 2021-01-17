import robin_stocks as r
import time
from secret_settings import *
import outreach_utils as out
import logging as log

log.basicConfig(filename='trading_log.log', level=log.INFO, format='%(asctime)s %(levelname)s: %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')


class TradingSession:

    def __init__(self):
        login = r.login(LOGIN_EMAIL, LOGIN_PASSWORD, expiresIn=10, by_sms=False)
        self.holdings = r.build_holdings()
        self.securities = []
        self.prices = {}
        self.equity = {}
        self.profile = r.profiles.load_portfolio_profile()
        self.acct = r.profiles.load_account_profile()

    def get_portfolio_info(self):
        if not self.securities:
            for sec, info in self.holdings.items():
                self.securities.append(sec)
                self.prices[sec] = info['price']
                self.equity[sec] = info['equity']

        buying_power = float(self.acct['portfolio_cash'])
        invested_value = float(self.profile['market_value'])

        return self.securities, self.prices, invested_value, buying_power, self.equity

    def print_portfolio_info(self):
        securities, prices, invested, buying, equity = self.get_portfolio_info()
        TradingSession.print_with_emphasis('SECURITIES')
        print(securities)
        TradingSession.print_with_emphasis('PRICES')
        print(prices)
        TradingSession.print_with_emphasis('TOTAL INVESTED VALUE')
        print(invested)
        TradingSession.print_with_emphasis('BUYING POWER')
        print(buying)
        TradingSession.print_with_emphasis('EQUITY')
        print(equity)

    @staticmethod
    def execute_trades(actions):
        confirmations = {}
        for trade in actions:
            security = trade['security']
            action = trade['action']
            if action > 0:
                print(f'Buying ${action} of {security}')
                confirmations[security] = r.orders.order_buy_fractional_by_price(security, action, timeInForce='gfd')
            elif action < 0:
                print(f'Selling ${abs(action)} of {security}')
                confirmations[security] = r.orders.order_sell_fractional_by_price(security, abs(action), timeInForce='gfd')
                time.sleep(10)
            else:
                pass

        confirmation_message = 'The following orders have been successfully sent:\n'
        for sym, confirmation in confirmations.items():
            try:
                confirmation_message += f"{sym}: {round(float(confirmation['quantity']),2)} shares @ ${round(float(confirmation['price']),2)} | Trigger {confirmation['trigger']} \n"
            except KeyError:
                confirmation_message += f'Something is wrong with {sym}'

        log.info('ORDERS SENT')
        log.info(confirmation_message)
        out.send_message(confirmation_message)

        return confirmations

    @staticmethod
    def print_with_emphasis(s):
        print(f'********** {s} **********')

    @staticmethod
    def close_open_orders():
        TradingSession()
        confirmations = r.orders.cancel_all_stock_orders()
        if confirmations:
            confirmation_message = 'All orders have been successfully cancelled with ids: \n'
            for confirmation in confirmations:
                confirmation_message += f"{confirmation['id']}\n\n"
        else:
            confirmation_message = 'No orders to cancel.'
        out.send_message(confirmation_message)
        return confirmations








