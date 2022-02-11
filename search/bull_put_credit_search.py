from strategies.put_credit_spread import PutCreditLock
from oplab import Client
import instrument.options_helper as options_helper

# Search
def bull_put_credit_search(client: Client, underlying_asset = None, atm_distance = 5, risk_limit = 50, min_days = 0, max_days=90, probability_above = 92, debug = False):
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
    options = options_helper.filter_by_type(options, "PUT")
    # Filter by days to maturity
    options = options_helper.filter_by_days_to_maturity(options, min_days, ">")
    options = options_helper.filter_by_days_to_maturity(options, max_days, "<")
    # Filter only options with BID/ASK bigger then 0
    options = options_helper.filter_by_bid_ask_available(options)
    # Filter by liquidity
    #print("TODO: Filter by liquidity (bid/ask vol > 0)")
    # Filter only the options where strike are bigger than the asset last trade
    underlying_asset_data = client.market.get_stock(underlying_asset)
    if (underlying_asset_data is not None) and (underlying_asset_data['close'] is not None):
        # Calculate the atm_distance in value
        # close is the last trade price
        atm_distance_value = underlying_asset_data["close"] * (1.0 - atm_distance / 100.0)
    else:
        print("Error: %s['close'] is None" % underlying_asset)
        return
    # Filter options that can be sold above the atm_distance
    options_to_sell = []
    for opt in options:
        if opt["strike"] <= atm_distance_value:
            options_to_sell.append(opt)

    # Create possibles CallSpread to sell that will be profitable
    put_spread_list = []
    for opt_sell in options_to_sell:
        for opt_buy in options:
            if opt_buy['days_to_maturity'] == opt_sell['days_to_maturity']:
                put_spread_strategy = PutCreditLock(opt_sell, opt_buy, underlying_asset)
                if put_spread_strategy.Profit() > 0.01:
                    put_spread_list.append(put_spread_strategy)

    # Filter by profit limit
    profit_risk_min_ratio = risk_limit
    put_spread_list_accepted = []
    for put_spread in put_spread_list:
        ratio = put_spread.Ratio()
        if ratio > profit_risk_min_ratio:
            put_spread_list_accepted.append(put_spread)
    put_spread_list = put_spread_list_accepted

    # Filter by probability
    put_spread_list_accepted = []
    for put_spread in put_spread_list:
        above,below = put_spread.AboveBelowProbability(underlying_asset_data["close"], underlying_asset_data['iv_1y_max'])
        if above > probability_above:
            put_spread_list_accepted.append(put_spread)
    put_spread_list = put_spread_list_accepted

    # Print each profitable call spread
    if debug:
        for put_spread in put_spread_list:
            print(put_spread)

    return put_spread_list



