from oplab import Client
import os
from oplab_robot.robot import Robot
from search.bull_put_credit_search import bull_put_credit_search

# Main
c = Client()
email = os.getenv("EMAIL")
password = os.getenv("PASSWORD")
userdata = c.login(email, password)
trading_accounts = c.domain.get_trading_accounts()
default_portfolio_id = c.domain.get_default_portfolio_id()

# Get the 30 down trend stocks
high_trends = c.market.get_ranking_trend(limit_to=30, sort='desc')
# For each down trend stock, get the call spread
puts_to_operate = []
for asset in high_trends:
    put_spread_list = bull_put_credit_search(c, asset['symbol'], atm_distance=0, risk_limit=10, min_days=5, max_days=30, probability_above=60, debug = True)
    if put_spread_list is not None:
        print("%s found %d put spread to operate" %(asset['symbol'], len(put_spread_list)))
        puts_to_operate.extend(put_spread_list)

        for put_spread in put_spread_list:
                amount = 300
                spread = -1*amount*put_spread.Risk() / 4
                name = "BullPutCredit({:.2f}".format(float(spread)) +")" +put_spread.sellput['symbol'] + "-" + put_spread.buyput['symbol']
                positions = [
                    {
                        'symbol': put_spread.sellput['symbol'],
                        'target_amount': amount,
                        'side': 'SELL',
                    }, {
                        'symbol': put_spread.buyput['symbol'],
                        'target_amount': amount,
                        'side': 'BUY',
                    }
                ]
                robot = Robot(trading_accounts[0]['id'],
                            default_portfolio_id,
                            'performance',
                            spread,
                            name,
                            put_spread.underlying,
                            positions,
                            "2022-17-02")
                robot.send(c, dry_run = False)


