import os
from oplab import Client
import json

c = Client()
email = os.getenv("EMAIL", default="dmpeletronic@gmail.com")
password = os.getenv("PASSWORD", default="daiana10!")
#password = os.getenv("PASSWORD", default="123456")
userdata = c.login(email, password)

print("API url:", c.market.url())

options = c.market.get_options_from_symbol('PETR4')
print("Options:")
# pretty print
print(json.dumps(options, indent=4, sort_keys=True))
print("Fount options:", len(options))

