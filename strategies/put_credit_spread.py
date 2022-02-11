from simple_probability import probability_above_below

#https://robinhood.com/us/en/support/articles/advanced-options-strategies/
class PutCreditLock:
    def __init__(self, sellput, buyput, underlying_asset = None):
        '''
        Tambem conhecido como "TRAVA DE ALTA COM PUTS"
        O lucro ocorre quando a acao esta em alta, nesse caso tanto a PUT vendida
        quanto a PUT comprada viram po, e o lucro eh dado pelo premio recebido menos
        o premio pago.

        sellput: the PUT that we are gonna sell
        buyput: the PUT that we are gonna buy
        '''
        self.sellput = sellput
        self.buyput = buyput
        self.underlying = underlying_asset

    def Profit(self):
        profit = float(self.sellput['bid']) - float(self.buyput['ask'])
        return profit

    def Risk(self):
        risk = float(self.sellput['strike']) - float(self.buyput['strike'])
        return risk


    def Ratio(self):
        if (self.Risk() == 0):
            print("Error: Risk is 0 for SellCall " + self.sellput['symbol'] + " and BuyCall " + self.buyput['symbol'])
            return 0
        ratio = 100*float(self.Profit()) / float(self.Risk())
        return ratio

    def AboveBelowProbability(self, spot, spot_iv):
        self.above, self.below = probability_above_below(
                            spot,
                            self.buyput["strike"],
                            self.buyput["days_to_maturity"],
                            spot_iv
                        )
        return self.above, self.below

    def to_str(self):
        # Sell: BBDCC123{CALL}[12.30] price: 0.25(200) Buy: BBDCC144{CALL}[14.00] price: 0.12(200) Profit: 0.13 Risk: 1.70 Ratio: 9%
        return ("Sell: " + self.sellput['symbol'] + "{"+self.sellput['maturity_type']+"}"+ "["+"{:.2f}".format(float(self.sellput['strike']))+"]" +
               " price: "+"{:.2f}".format(float(self.sellput['bid'])) +
               " Buy:" + self.buyput['symbol'] + "{"+self.buyput['maturity_type']+"}"+ "["+"{:.2f}".format(float(self.buyput['strike']))+"]" +
               " price: "+"{:.2f}".format(float(self.buyput['ask'])) +
               " Profit: " +  "{:.2f}".format(float(self.Profit())) +
               " Risk: "+"{:.2f}".format(float(self.Risk())) +
               " Ratio: {:.2f}%".format(float(self.Ratio())) +
               " AboveStrike: {:.2f}%".format(float(self.above))
        )

    def __str__(self):
        return self.to_str()

    def __repr__(self):
        return self.to_str()
