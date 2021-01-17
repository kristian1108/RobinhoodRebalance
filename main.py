#!./venv/bin/python

import rebalance_utils as re
import outreach_utils as out
import argparse
import api_utils as api
import json

parser = argparse.ArgumentParser(description='Control execution of main.py')

parser.add_argument('--method', metavar='method', type=str, help='The method you wish to call.')

args = parser.parse_args()

if args.method == 'get_actions':
    actions = re.get_actions()
    save_json = []

    for security, action in actions.items():
        save_json.append(
            {
                'security': security,
                'action': action
            }
        )

    out.send_actions(actions)

    with open('next_actions.json', 'w+') as file:
        json.dump(save_json, file)


if args.method == 'self_greeting':
    out.send_greeting(which='self')

elif args.method == 'actions':
    out.send_actions_alert()

elif args.method == 'print':
    acct = api.TradingSession()
    acct.print_portfolio_info()
    print(re.get_actions())

"""

actions = re.get_actions()

out.send_actions_alert(actions, to=MY_NUMBER)
confirmations = api.TradingSession.rebalance(actions)

out.send_order_notifications(confirmations, to=MY_NUMBER)

"""






