import os
from oplab import Client
import json

c = Client()
email = os.getenv("EMAIL")
password = os.getenv("PASSWORD")
userdata = c.login(email, password)

print("API url:", c.market.url())

data = c.market.get_stock('BOVA11')
print("PETR4 quote:")
# pretty print
print(json.dumps(data, indent=4, sort_keys=True))

