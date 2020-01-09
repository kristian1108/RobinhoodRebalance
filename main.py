import rebalance_utils as re
import outreach_utils as out
import api_utils as api
import time
from secret_settings import *

out.send_greeting(cl=False)

actions = re.get_actions()

out.send_actions_alert(actions, to=MY_NUMBER)
confirmations = api.TradingSession.rebalance(actions)

out.send_order_notifications(confirmations, to=MY_NUMBER)








