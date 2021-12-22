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
    def __init__(self, url, token, ticks, tick_callback = None, order_callback = None, robot_callback = None):
        self.url = url
        self.token = token
        self.running = False
        self.loop = asyncio.get_event_loop()
        self.loop.create_task(self.__tick())
        self.tick_callback = tick_callback
        self.subscribe_ticks = ticks

    def start(self):
        try:
            self.running = True
            self.loop.create_task(self.__tick())
            self.loop.run_forever()
        except Exception:
            self.loop.close()

    def stop(self):
        self.running = False
        self.loop.stop()

    async def subscribe(self, type = 'tick'):
        subscriptions = {
            'access-token': self.token,
            'type': type,
            'subscribe': self.subscribe_ticks
        }
        print("Subscribing:", json.dumps(subscriptions))
        await self.websocket.send(json.dumps(subscriptions))

    async def unsubscribe(self, type = 'tick'):
        subscriptions = {
            'access-token': self.token,
            'type': type,
            'unsubscribe': self.subscribe_ticks
        }
        print("Unsubscribing:", json.dumps(subscriptions))
        await self.websocket.send(json.dumps(subscriptions))

    async def __tick(self):
        self.websocket = await websockets.connect(self.url)
        await self.subscribe()
        while self.running:
            self.tick_callback(self, await self.websocket.recv())
        await self.unsubscribe()
        self.websocket.close()

def tick(df: Datafeed, message):
    print("Tick: ", message)

d = Datafeed(datafeed_url, datafeed_token, tick, ['PETR4'])
d.start()

