import os
from oplab import Client
from oplab_robot.robot import Robot
from search.bear_call_credit_search import bear_call_credit_search

# Main
c = Client()
email = os.getenv("EMAIL")
password = os.getenv("PASSWORD")
userdata = c.login(email, password)
trading_accounts = c.domain.get_trading_accounts()
default_portfolio_id = c.domain.get_default_portfolio_id()

# Configuration
amount_to_operate = 300
atm_distance_in_percentage = 5 # 5%
risk_limit_in_percentage = 10 # 10%
min_days = 10
max_days = 30
probability_below = 80 #80%
debug = True # printout each strategy
expire_date = "2022-17-02"
maximum_robot_number = 1000

# Get the 30 down trend stocks
down_trends = c.market.get_ranking_trend(limit_to=30, sort='asc')

# For each down trend stock, get the call spread
robot_counter = 0
calls_to_operate = []
for asset in down_trends:
    call_spread_list = bear_call_credit_search(c, asset['symbol'], atm_distance_in_percentage,
                                                risk_limit_in_percentage,
                                                min_days, max_days, probability_below, debug)
    if call_spread_list is not None:
        print("%s found %d calls spread to operate" %(asset['symbol'], len(call_spread_list)))
        calls_to_operate.extend(call_spread_list)
        for call_spread in reversed(call_spread_list):
                spread = -1*amount_to_operate*call_spread.Risk() * 2 / 3
                name = "BearCallCredit({:.2f}".format(float(spread)) +")" +call_spread.sellcall['symbol'] + "-" + call_spread.buycall['symbol']
                positions = [
                    {
                        'symbol': call_spread.sellcall['symbol'],
                        'target_amount': amount_to_operate,
                        'side': 'SELL',
                    }, {
                        'symbol': call_spread.buycall['symbol'],
                        'target_amount': amount_to_operate,
                        'side': 'BUY',
                    }
                ]
                robot = Robot(trading_accounts[0]['id'],
                            default_portfolio_id,
                            'performance',
                            spread,
                            name,
                            call_spread.underlying,
                            positions,
                            expire_date)
                robot.send(c, dry_run = False)
                robot_counter += 1
                print("Robot %d created" % robot_counter)
                if robot_counter >= maximum_robot_number:
                    quit()
