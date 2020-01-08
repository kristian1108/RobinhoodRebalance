import api_utils as api

if __name__ == "__main__":
    ts = api.TradingSession()
    api.TradingSession.close_open_orders()