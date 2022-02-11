import os
from oplab import Client
import json

c = Client()
email = os.getenv("EMAIL")
password = os.getenv("PASSWORD")
userdata = c.login(email, password)
data = c.market.get_ranking_down_trend(limit_to=3)
# pretty print
print(json.dumps(data, indent=4, sort_keys=True))

