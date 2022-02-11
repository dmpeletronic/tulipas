import os
from oplab import Client
import json

c = Client()
email = os.getenv("EMAIL")
password = os.getenv("PASSWORD")
userdata = c.login(email, password)
print("userdata", userdata)
default_portfolio_id = c.domain.get_default_portfolio_id()
data = c.domain.get_robot(default_portfolio_id, 1864)
# pretty print
print(json.dumps(data, indent=4, sort_keys=True))

