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

# Get the 30 down trend stocks
down_trends = c.market.get_ranking_trend(limit_to=30, sort='asc')
amount=100
robot_counter = 0
# For each down trend stock, get the call spread
calls_to_operate = []
for asset in down_trends:
    call_spread_list = bear_call_credit_search(c, asset['symbol'], atm_distance=5, risk_limit=10, min_days=10, max_days=30, probability_below=50, debug = True)
    if call_spread_list is not None:
        print("%s found %d calls spread to operate" %(asset['symbol'], len(call_spread_list)))
        calls_to_operate.extend(call_spread_list)
        for call_spread in reversed(call_spread_list):
                spread = -1*amount*call_spread.Risk() * 2 / 3
                name = "BearCallCredit({:.2f}".format(float(spread)) +")" +call_spread.sellcall['symbol'] + "-" + call_spread.buycall['symbol']
                positions = [
                    {
                        'symbol': call_spread.sellcall['symbol'],
                        'target_amount': amount,
                        'side': 'SELL',
                        'depth': 2
                    }, {
                        'symbol': call_spread.buycall['symbol'],
                        'target_amount': amount,
                        'side': 'BUY',
                        'depth': 2
                    }
                ]
                robot = Robot(trading_accounts[0]['id'],
                            default_portfolio_id,
                            'performance',
                            spread,
                            name,
                            call_spread.underlying,
                            positions,
                            "2022-17-02")
                robot.send(c, dry_run = False)
                robot_counter += 1
                print("Robot %d created" % robot_counter)
                if robot_counter >= 10:
                    quit()

