import os
from oplab import Client
import json

c = Client()
email = os.getenv("EMAIL", default="amaral.alexandre@gmail.com")
password = os.getenv("PASSWORD", default="ale")
userdata = c.login(email, password)
print("userdata", userdata)
trading_accounts = c.domain.get_trading_accounts()
print("trading accounts:", json.dumps(trading_accounts, indent=4, sort_keys=True))
robot = {
    'trading_account_id': trading_accounts[0]['id'],
    'debug': 2,
    'mode': 'performance',
    'spread': 100,
    'strategy': {
        'name': 'strategy_test',
        'underlying': 'LREN4',
        },
    'positions': [
        {
            'symbol': 'LRENA280',
            'target_amount': -100
        },
        {
            'symbol': 'LRENA285',
            'target_amount': 100
        }
    ]
}
default_portfolio_id = c.domain.get_default_portfolio_id()
data = c.domain.create_robot(default_portfolio_id, robot, dry_run=False)
# pretty print
print(json.dumps(data, indent=4, sort_keys=True))

