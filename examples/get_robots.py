import os
from oplab import Client
import json

c = Client()
email = os.getenv("EMAIL", default="amaral.alexandre@gmail.com")
password = os.getenv("PASSWORD", default="ale")
userdata = c.login(email, password)
print("userdata", userdata)
default_portfolio_id = c.domain.get_default_portfolio_id()
data = c.domain.get_robots(default_portfolio_id)
# pretty print
print(json.dumps(data, indent=4, sort_keys=True))

