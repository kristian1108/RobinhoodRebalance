import rebalance_utils as re
import outreach_utils as out
import argparse

parser = argparse.ArgumentParser(description='Control execution of main.py')

parser.add_argument('Method', metavar='method', type=str, help='The method you wish to call.')

args = parser.parse_args()

if args.Method == 'greeting':
    out.send_greeting(cl=False)

elif args.Method == 'actions':
    actions = re.get_actions()
    out.send_actions_alert(actions)



"""

actions = re.get_actions()

out.send_actions_alert(actions, to=MY_NUMBER)
confirmations = api.TradingSession.rebalance(actions)

out.send_order_notifications(confirmations, to=MY_NUMBER)

"""






