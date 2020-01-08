import api_utils as api
from random import randint
from secret_settings import *


def compute_total_cost(pr, lt_actions, bond_actions):
    total_cost = 0.0

    for sec, action in bond_actions.items():
        total_cost += float(pr[sec]) * action

    for sec, action in lt_actions.items():
        total_cost += float(pr[sec]) * action

    return total_cost


def get_actions():

    ts = api.TradingSession()

    portfolio = ts.get_portfolio_info()
    current_securities = portfolio[0]
    prices = portfolio[1]
    total_aum = portfolio[2]
    buying_power = portfolio[3]
    shares_owned = portfolio[4]

    BOND_VALUE = total_aum - LT_VALUE
    INTENT_SECURITIES = BOND_SECURITIES + LT_SECURITIES

    anomalies = [sec for sec in current_securities if sec not in INTENT_SECURITIES]

    if anomalies:
        print('Your invested securities and your intended securities do not match.')
        print('You own ' + str(anomalies) + ', not listed your intended securities.')

    balanced_bond_shares = {}
    balanced_lt_shares = {}

    bond_action_needed = {}
    lt_action_needed = {}

    for sec, alloc in BOND_ALLOCATIONS.items():
        dollar_alloc = alloc*BOND_VALUE
        shares = int(dollar_alloc/float(prices[sec]))+1
        balanced_bond_shares[sec] = shares

    for sec, alloc in LT_ALLOCATIONS.items():
        dollar_alloc = alloc*LT_VALUE
        shares = int(dollar_alloc / float(prices[sec]))+1
        balanced_lt_shares[sec] = shares

    for sec in BOND_SECURITIES:
        bond_action_needed[sec] = int(balanced_bond_shares[sec] - float(shares_owned[sec]))

    for sec in LT_SECURITIES:
        lt_action_needed[sec] = int(balanced_lt_shares[sec] - float(shares_owned[sec]))

    total_act_cost = compute_total_cost(prices, lt_action_needed, bond_action_needed)

    while total_act_cost > buying_power-TRADING_BUFFER:
        num_sec = len(INTENT_SECURITIES)
        decrease = INTENT_SECURITIES[randint(0, num_sec-1)]

        lt = False
        bond = False

        if decrease in LT_SECURITIES:
            lt = True
        else:
            bond = True

        if lt and lt_action_needed[decrease] > 0:
            lt_action_needed[decrease] -= 1
        elif bond and bond_action_needed[decrease] > 0:
            bond_action_needed[decrease] -= 1
        else:
            pass

        total_act_cost = compute_total_cost(prices, lt_action_needed, bond_action_needed)

    agg_actions = {}

    for sec, action in lt_action_needed.items():
        try:
            agg_actions[sec] += action
        except KeyError:
            agg_actions[sec] = action
    for sec, action in bond_action_needed.items():
        try:
            agg_actions[sec] += action
        except KeyError:
            agg_actions[sec] = action

    agg_actions = {k: v for k, v in sorted(agg_actions.items(), key=lambda item: item[1])}

    return agg_actions




