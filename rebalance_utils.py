import api_utils as api
from random import randint
from secret_settings import *
import logging as log

log.basicConfig(filename='trading_log.log', level=log.INFO, format='%(asctime)s %(levelname)s: %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')


def compute_total_cost(action_needed):
    total_cost = 0.0

    for sec, action in action_needed.items():
        total_cost += action

    return total_cost


def sync_target_and_current_securities(target_securities, current_equity):
    current_securities = set(current_equity.keys())
    for security in target_securities:
        if security not in current_securities:
            current_equity[security] = 0


def get_actions():
    log.info('')
    log.info('***RETRIEVING ACTIONS***')

    ts = api.TradingSession()

    securities, prices, invested_value, buying_power, current_equity = ts.get_portfolio_info()
    acct_value = invested_value + buying_power
    invested_value = acct_value*INVESTED_PORTION

    anomalies = [sec for sec in securities if sec not in SECURITIES]

    if anomalies:
        log.warning('Your invested securities and your intended securities do not match.')
        log.warning('You own ' + str(anomalies) + ', not listed your intended securities.')

    balanced_allocations = {}
    action_needed = {}

    for sec, alloc in ALLOCATIONS.items():
        balanced = invested_value*alloc
        balanced_allocations[sec] = balanced

    sync_target_and_current_securities(SECURITIES, current_equity)

    for sec in SECURITIES:
        action_needed[sec] = balanced_allocations[sec] - float(current_equity[sec])

    total_act_cost = compute_total_cost(action_needed)
    max_cost = buying_power-TRADING_BUFFER

    log.info(f'Total Trade Cost: {total_act_cost} | Max Allowed Cost : {max_cost} | Difference: {total_act_cost - max_cost}')

    reduce_trade_cost_by = total_act_cost-max_cost
    decrease_val = reduce_trade_cost_by / 3

    while total_act_cost > max_cost+0.05:
        num_sec = len(SECURITIES)

        decrease = SECURITIES[randint(0, num_sec - 1)]

        while float(current_equity[decrease]) <= decrease_val:
            decrease = SECURITIES[randint(0, num_sec-1)]

        log.info(f'Reducing the value of {decrease} by {decrease_val}')
        action_needed[decrease] -= decrease_val

        total_act_cost = compute_total_cost(action_needed)
        log.info(f'Total Trade Cost: {total_act_cost}')

    sorted_actions = {k: v for k, v in sorted(action_needed.items(), key=lambda item: item[1])}

    log.info(f'Total Account Value: {acct_value}')
    log.info(f'Total Invested Value: {invested_value}')
    log.info(f'Trading Buffer: {TRADING_BUFFER}')
    log.info(f'Buying Power: {buying_power}')
    log.info(f'Total Cost Of Trades: {sum(sorted_actions.values())}')
    log.info(f'Cash Left Over After Trades: {buying_power-sum(sorted_actions.values())}')

    log.info('***DONE RETRIEVING ACTIONS***')

    return sorted_actions




