import os
from oplab import Client

c = Client()
email = os.getenv("EMAIL", default="dmpeletronic@gmail.com")
password = os.getenv("PASSWORD", default="daiana10!")

print("email:", email)
print("password:", password)
print("User data:", c.login(email, password))
print("API url", c.domain.url())
print("Portifolios:", c.domain.get_portfolios())

default_portfolio_id = 0
portifolios = c.domain.get_portfolios()
# find in array of json, the one with is_default = True
for p in portifolios:
    if p["is_default"]:
        default_portfolio_id = p["id"]
        break
print("Default portfolio id:", default_portfolio_id)
print("Default portfolio id:", c.domain.get_default_portfolio_id())

print("Get strategies", c.domain.get_strategies(default_portfolio_id))



