#!./venv/bin/python

import rebalance_utils as re
import outreach_utils as out
import argparse
import api_utils as api
import json
import os
import logging as log
import time

log.basicConfig(filename='trading_log.log', level=log.INFO, format='%(asctime)s %(levelname)s: %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')


def save_actions():
    proposed_actions = re.get_actions()
    save_json = []

    for security, action in proposed_actions.items():
        save_json.append(
            {
                'security': security,
                'action': action
            }
        )

    out.send_actions(proposed_actions)

    with open('next_actions.json', 'w+') as file:
        json.dump(save_json, file)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Control execution of main.py')
    parser.add_argument('--execute', action='store_true', help='Run the trading algorithm to rebalance.')
    parser.add_argument('--cancel', action='store_true', help='Cancel all existing orders.')
    args = parser.parse_args()

    if args.cancel:
        out.send_message('Cancelling all orders.')
        api.TradingSession.close_open_orders()

    if args.execute:
        out.send_greeting(which='self')
        save_actions()
        time.sleep(5)

        with open('next_actions.json', 'r') as file:
            actions = json.load(file)

        if out.get_trading_confirmation():
            log.info('Sending orders.')
            out.send_greeting('Sending orders now...')
            confirmations = api.TradingSession.execute_trades(actions)

        os.remove('next_actions.json')




