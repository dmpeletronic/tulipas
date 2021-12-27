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
datafeed_url = userdata['endpoints'][0]
print("Datafeed url:", datafeed_url)
datafeed_token = userdata['datafeed-access-token']
print("Datafeed token", datafeed_token)

class Datafeed:
    def __init__(self, url, token, ticks, tick_callback = None, order_callback = None, robot_callback = None, system_callback = None):
        self.url = url
        self.token = token
        self.running = False
        self.tick_callback = tick_callback
        self.order_callback = order_callback
        self.robot_callback = robot_callback
        self.system_callback = system_callback
        self.subscribe_ticks = ticks

    def start(self):
        try:
            self.running = True
            self.loop = asyncio.get_event_loop()
            self.loop.create_task(self.__receiver())
            self.loop.run_forever()
        except Exception:
            self.loop.close()

    def stop(self):
        self.running = False
        self.loop.stop()

    async def subscribe(self, subscription_type = 'tick', symbols = None):
        subscriptions = {
            'access-token': self.token,
            'type': subscription_type
        }
        if symbols is not None:
            subscriptions['subscribe'] = symbols

        await self.websocket.send(json.dumps(subscriptions))

    async def unsubscribe(self, type = 'tick', symbols = None):
        subscriptions = {
            'access-token': self.token,
            'type': type,
        }
        if symbols is not None:
            subscriptions['unsubscribe'] = symbols

        await self.websocket.send(json.dumps(subscriptions))

    async def __receiver(self):
        self.websocket = await websockets.connect(self.url)

        if self.tick_callback is not None:
            await self.subscribe(subscription_type='tick', symbols=self.subscribe_ticks)
        if self.order_callback is not None:
            await self.subscribe(subscription_type='order')
        if self.robot_callback is not None:
            await self.subscribe(subscription_type='robot')

        while self.running:
            try:
                msg = await self.websocket.recv()
                msgtype = msg[0]
                if msgtype == 'T':
                    if self.tick_callback is not None:
                        self.tick_callback(self, msg)
                elif msgtype == 'O':
                    if self.order_callback is not None:
                        self.order_callback(self, msg)
                elif msgtype == 'R':
                    if self.robot_callback is not None:
                        self.robot_callback(self, msg)
                elif msgtype == 'S':
                    if self.system_callback is not None:
                        self.system_callback(self, msg)
            except Exception:
                self.running = False
                self.loop.stop()
                break
        await self.unsubscribe(subscription_type='tick', symbols=self.subscribe_ticks)
        self.websocket.close()

def on_tick(df: Datafeed, message):
    print("Tick: ", message)

def on_order(df: Datafeed, message):
    print("Order: ", message)

def on_robot(df: Datafeed, message):
    print("Robot: ", message)

def on_system(df: Datafeed, message):
    print("System: ", message)

d = Datafeed(datafeed_url, datafeed_token, ['PETR4'], tick_callback=on_tick, order_callback=on_order, robot_callback=on_robot, system_callback=on_system)
d.start()

