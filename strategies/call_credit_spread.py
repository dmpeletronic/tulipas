from simple_probability import probability_above_below

#https://robinhood.com/us/en/support/articles/advanced-options-strategies/
class CallCreditLock:
    def __init__(self, sellcall, buycall, underlying = None):
        self.sellcall = sellcall
        self.buycall = buycall
        self.underlying = underlying

    def Profit(self):
        profit = float(self.sellcall['bid']) - float(self.buycall['ask'])
        return profit

    def Risk(self):
        risk = float(self.buycall['strike']) - float(self.sellcall['strike'])
        return risk

    def Ratio(self):
        if (self.Risk() == 0):
            print("Error: Risk is 0 for SellCall " + self.sellcall['symbol'] + " and BuyCall " + self.buycall['symbol'])
            return 0
        ratio = 100*float(self.Profit()) / float(self.Risk())
        return ratio

    def AboveBelowProbability(self, spot, spot_iv):
        self.above, self.below = probability_above_below(
                            spot,
                            self.sellcall["strike"],
                            self.sellcall["days_to_maturity"],
                            spot_iv
                        )
        return self.above, self.below

    def to_str(self):
        # Sell: BBDCC123{CALL}[12.30] price: 0.25(200) Buy: BBDCC144{CALL}[14.00] price: 0.12(200) Profit: 0.13 Risk: 1.70 Ratio: 9%
        return ("Sell: " + self.sellcall['symbol'] + "{"+self.sellcall['maturity_type']+"}"+ "["+"{:.2f}".format(float(self.sellcall['strike']))+"]" +
               " price: R$"+"{:.2f}".format(float(self.sellcall['bid']))  +
               " Buy: " + self.buycall['symbol'] + "{"+self.buycall['maturity_type']+"}"+ "["+"{:.2f}".format(float(self.buycall['strike']))+"]" +
               " price: "+"{:.2f}".format(float(self.buycall['ask']))  +
               " Profit: R$" +  "{:.2f}".format(float(self.Profit())) + " Risk: R$"+"{:.2f}".format(float(self.Risk())) +
               " Ratio: {:.2f}%".format(float(self.Ratio())) +
               " BelowStrike: {:.2f}%".format(float(self.below))
               )


    def __str__(self):
        return self.to_str()

    def __repr__(self):
        return self.to_str()