import os
from oplab import Client
import json

c = Client()
email = os.getenv("EMAIL", default="dmpeletronic@gmail.com")
password = os.getenv("PASSWORD", default="daiana10!")
#password = os.getenv("PASSWORD", default="123456")
userdata = c.login(email, password)

options = c.market.get_options_from_symbol('MGLU3')

subscribe_options = []
for option in options:
    if option["days_to_maturity"] <= 30:
        subscribe_options.append(option["symbol"])

print("Options:", subscribe_options)

def on_tick(df, message):
    print("Tick: ", message)

c.start_datafeed(subscribe_options, tick_callback=on_tick)

