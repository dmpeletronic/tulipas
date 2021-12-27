import os
from oplab import Client

import asyncio
import json
import websockets

c = Client()
email = os.getenv("EMAIL", default="dmpeletronic@gmail.com")
password = os.getenv("PASSWORD", default="daiana10!")

print("API url:", c.domain.url())
print("email:", email)
print("password:", password)
userdata = c.login(email, password)
print("User data:", userdata)

def on_tick(df, message):
    print("Tick: ", message)

def on_order(df, message):
    print("Order: ", message)

def on_robot(df, message):
    print("Robot: ", message)

def on_system(df, message):
    print("System: ", message)

c.start_datafeed(['PETR4','VALE3', 'PETRA249'], tick_callback=on_tick, order_callback=on_order, robot_callback=on_robot, system_callback=on_system)

