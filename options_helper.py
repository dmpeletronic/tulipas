import instrument
from oplab import Client
import json

def find_options(client: Client, underlying_symbol = None):
    ''' Client is the oplab client
        underlying_symbol ITUB4
    '''
    if client is None:
        return
    if underlying_symbol is None:
        return

    options = client.market.get_options_from_symbol(underlying_symbol)
    return options

def find_all_options(data, underlying_symbol, opttype):
    ''' Data: the list with all assets to analise
        related asset: ITUB4
        type: PUT or CALL
    '''
    internaldata = data
    internaldata = filter_list_by_asset(internaldata, underlying_symbol)
    internaldata = filter_option_list_by_type(internaldata, opttype)
    return internaldata

def filter_by_type(option_list, opttype):
    '''
        type: PUT or CALL
    '''
    output_data = []
    for opt in option_list:
        if opt['type'] == opttype:
            output_data.append(opt)
    return output_data


def filter_by_days_to_maturity(option_list, days_to_maturity, operator):
    output_data = []
    for opt in option_list:
        if operator == ">":
            if opt['days_to_maturity'] > days_to_maturity:
                output_data.append(opt)
        elif operator == "<":
            if opt['days_to_maturity'] < days_to_maturity:
                output_data.append(opt)
        elif operator == ">=":
            if opt['days_to_maturity'] >= days_to_maturity:
                output_data.append(opt)
        elif operator == "<=":
            if opt['days_to_maturity'] <= days_to_maturity:
                output_data.append(opt)
        elif operator == "=":
            if opt['days_to_maturity'] == days_to_maturity:
                output_data.append(opt)
    return output_data

def filter_list_by_description(input_data, description):
    output_data = []
    for d in input_data:
        if d.description == description:
            output_data.append(d)
    return output_data

def filter_by_bid_ask_available(option_list):
    output_data = []
    for opt in option_list:
        if opt['bid'] > 0 and opt['ask'] > 0:
            output_data.append(opt)
    return output_data

def filter_option_list_by_month(input_data, month):
    output_data = []
    for d in input_data:
        desired_month = d.description+month
        if desired_month in d.symbol:
            output_data.append(d)
    return output_data

def month_to_letter(opttype, month):
    switcher = {
        "January":   { 'Call': 'A', 'Put': 'M'},
        "February":  { 'Call': 'B', 'Put': 'N'},
        "March":     { 'Call': 'C', 'Put': 'O'},
        "April":     { 'Call': 'D', 'Put': 'P'},
        "May":       { 'Call': 'E', 'Put': 'Q'},
        "June":      { 'Call': 'F', 'Put': 'R'},
        "July":      { 'Call': 'G', 'Put': 'S'},
        "August":    { 'Call': 'H', 'Put': 'T'},
        "September": { 'Call': 'I', 'Put': 'U'},
        "October":   { 'Call': 'J', 'Put': 'V'},
        "November":  { 'Call': 'K', 'Put': 'W'},
        "December":  { 'Call': 'L', 'Put': 'X'},
    }
    return switcher[month][opttype]
