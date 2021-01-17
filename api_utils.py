import robin_stocks as r
import time
from secret_settings import *


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
    def print_with_emphasis(s):
        print(f'********** {s} **********')

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







