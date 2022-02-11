class Instrument:
    def __init__(self):
        self.symbol = ""        #i.e: ITUBN345
        self.underlying_symbol = "" #i.e: ITUB4
        self.description = ""   #i.e: ITUB
        self.strike = 0         #i.e: 34.50
        self.option_type = ""   #i.e: PUT or CALL
        self.option_style = ""  #i.e: A
        self.bestbuy = 0        #i.e: 0.20
        self.bestbuy_volume = 0 #i.e: 100
        self.bestsell = 0       #i.e: 0.25
        self.bestsell_volume = 0 #i.e: 100
        self.days_to_expire  = 0 #i.e: 20days
        self.last_trade = 0

    def set(self, symbol="", relative_asset="", desc="", strike=0, opttype="", optstyle="", bestbuy=0, bestbuy_volume=0, bestsell=0, bestsell_volume=0, days_to_expire=0, last_trade=0):
        self.symbol = symbol
        self.underlying_symbol = relative_asset
        self.description = desc
        self.strike = strike
        self.option_type = opttype
        self.option_style = optstyle
        self.bestbuy = bestbuy
        self.bestbuy_volume = bestbuy_volume
        self.bestsell = bestsell
        self.bestsell_volume = bestsell_volume
        self.days_to_expire  = days_to_expire
        self.last_trade = last_trade

    def to_str(self):
        return (self.symbol +" {"+self.option_style+"}"+ "["+"{:.2f}".format(float(self.strike))+"]" + "[Exp:"+str(self.days_to_expire)+"]"+
               " Cpa:"+"{:.2f}".format(float(self.bestbuy))  + "("+ str(int(self.bestbuy_volume))  + ")" +
               " Vda:"+"{:.2f}".format(float(self.bestsell)) + "(" + str(int(self.bestsell_volume)) + ")" )

    def __str__(self):
        return self.to_str()

    def __repr__(self):
        return self.to_str()
