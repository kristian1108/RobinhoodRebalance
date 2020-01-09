import robin_stocks as r
import time
from secret_settings import *


class TradingSession:

    def __init__(self):
        login = r.login(LOGIN_EMAIL, LOGIN_PASSWORD, expiresIn=10, by_sms=False)
        self.holdings = r.build_holdings()
        self.securities = []
        self.prices = {}
        self.shares = {}
        self.profile = r.profiles.load_portfolio_profile()
        self.acct = r.profiles.load_account_profile()

    def get_portfolio_info(self):
        if not self.securities:
            for sec, info in self.holdings.items():
                self.securities.append(sec)
                self.prices[sec] = info['price']
                self.shares[sec] = info['quantity']

        buying_power = float(self.acct['portfolio_cash'])
        total_aum = float(self.profile['market_value'])

        return self.securities, self.prices, total_aum, buying_power, self.shares


    @staticmethod
    def close_open_orders():
        return r.orders.cancel_all_open_orders()

    @staticmethod
    def rebalance(actions):
        confirmations = {}

        for sec, action in actions.items():
            if action > 0:
                print('Buying ' + str(action) + ' share(s) of ' + sec)
                confirmations[sec] = r.orders.order_buy_market(sec, action, timeInForce='gfd')
            elif action < 0:
                print('Selling ' + str(abs(action)) + ' share(s) of ' + sec)
                confirmations[sec] = r.orders.order_sell_market(sec, abs(action), timeInForce='gfd')
                time.sleep(10)
            else:
                pass

        return confirmations







