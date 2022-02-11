from strategies.call_credit_spread import CallCreditLock
from oplab import Client
import instrument.options_helper as options_helper

# 3 - Trava no credito
# 3.1 - Venda de calls (trava de baixa com calls)
#           Como funciona?
#               Vende call de strike mais proximo (acima) do valor do ativo.
#               Compra call de strike mais longe (mais acima ainda )
#           Quando?
#               Ativo em queda
#           Lucro?
#               Premio recebido pela venda menos premio pago pela compra
#           Risco?
#               Diferença entre o strike da opcao de menor strike e de maior strike
#           Examplo real:
#              B3AS3 = R$54.89
#              Vende  B3SAC595(strike 58.19) por 0.72
#              Compra B3SAC602(strike 59.69) por 0.63
#              Lucro = premio recebido - premio pago = 0.72 - 0.63 = 0.09
#              Risco = strike comprado - strike vendido = 59.69 - 58.19 = 1.50
#              Caso ideal: lucro maior que risco
#              Caso aceitavel:
#                usar opcoes muito OTM que tenham mais de 90% de proabilidade de virar pó,
#                e utilizar a combinação com melhor relacao lucro/risco

# Search
def bear_call_credit_search(client: Client, underlying_asset = None, atm_distance = 5, risk_limit = 50, min_days = 0, max_days=90, probability_below = 92, debug = False):
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
            if opt_buy['days_to_maturity'] == opt_sell['days_to_maturity']:
                call_spread_strategy = CallCreditLock(opt_sell, opt_buy, underlying_asset)
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
    call_spread_list_accepted = []
    for call_spread in call_spread_list:
        above,below = call_spread.AboveBelowProbability(underlying_asset_data["close"], underlying_asset_data['iv_1y_max'])
        if below > probability_below:
            call_spread_list_accepted.append(call_spread)
    call_spread_list = call_spread_list_accepted

    # Print each profitable call spread
    if debug:
        for call_spread in call_spread_list:
            print(call_spread)

    return call_spread_list

