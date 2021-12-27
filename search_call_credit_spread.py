from call_credit_spread import CallCreditLock
import options_helper
from oplab import Client
import json
import os

# Search
def call_search(client: Client, underlying_asset = None, atm_distance = 5, risk_limit = 50):
    ''' Client is the oplab client
        underlying_asset ITUB4
        atm_distance in percentage 5%
        risk_limit in percentage 50%
    '''
    if client is None:
        return
    if underlying_asset is None:
        return
    underlying_asset_data = client.market.get_stock(underlying_asset)
    if underlying_asset_data['has_options'] == False:
        return
    # Get all options from an asset
    options = options_helper.find_options(client, underlying_asset)
    if len(options) == 0:
        return
    # Filter by type
    options = options_helper.filter_by_type(options, "CALL")
    # Filter by days to maturity
    options = options_helper.filter_by_days_to_maturity(options, 30, "<")
    # Filter only options with BID/ASK bigger then 0
    options = options_helper.filter_by_bid_ask_available(options)
    # Filter by liquidity
    #print("TODO: Filter by liquidity (bid/ask vol > 0)")
    # Filter only the options where strike are bigger than the asset last trade
    underlying_asset_data = client.market.get_stock(underlying_asset)
    if (underlying_asset_data is not None) and (underlying_asset_data['close'] is not None):
        # Calculate the atm_distance in value
        # close is the last trade price
        atm_distance_value = underlying_asset_data["close"] * (1.0 + atm_distance / 100.0)
    else:
        print("Error: %s['close'] is None" % underlying_asset)
        return
    # Filter options that can be sold above the atm_distance
    options_to_sell = []
    for opt in options:
        if opt["strike"] >= atm_distance_value:
            options_to_sell.append(opt)

    # Create possibles CallSpread to sell that will be profitable
    call_spread_list = []
    for opt_sell in options_to_sell:
        for opt_buy in options:
            call_spread_strategy = CallCreditLock(opt_sell, opt_buy)
            if call_spread_strategy.Profit() > 0.01:
                call_spread_list.append(call_spread_strategy)

    # Filter by profit limit
    profit_risk_min_ratio = risk_limit
    call_spread_list_accepted = []
    for call_spread in call_spread_list:
        ratio = call_spread.Ratio()
        if ratio > profit_risk_min_ratio:
            call_spread_list_accepted.append(call_spread)
    call_spread_list = call_spread_list_accepted

    # Filter by probability
    expire_probability_limit = 92 # 92%
    call_spread_list_accepted = []
    for call_spread in call_spread_list:
        above,below = 5,95
        if below > expire_probability_limit:
            call_spread_list_accepted.append(call_spread)
    call_spread_list = call_spread_list_accepted

    # Print each profitable call spread
    for call_spread in call_spread_list:
        print(call_spread)

    print("%s found %d calls spread to operate" %(underlying_asset, len(call_spread_list)))

# Main
c = Client()
email = os.getenv("EMAIL", default="dmpeletronic@gmail.com")
password = os.getenv("PASSWORD", default="daiana10!")
userdata = c.login(email, password)


# Get the 30 down trend stocks
down_trends = c.market.get_ranking_down_trend(limit_to=30)

for asset in down_trends:
    call_search(c, asset['symbol'], 5, 20)