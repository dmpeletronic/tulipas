import math
#https://www.optionstrategist.com/calculators/probability
#https://towardsdatascience.com/monte-carlo-pricing-in-python-eafc29e3b6c9

def probability_above_below(price, strike, days, volatility):
  '''
  From:
  https://www.optionstrategist.com/calculators/probability
  '''
  p=float(price)
  q=float(strike)
  t=int(days)/365
  v=float(volatility)/100

  vt= v * math.sqrt(t)
  lnpq = math.log(q/p)
  d1 = lnpq / vt

  y = math.floor(1/(1+.2316419*abs(d1))*100000)/100000

  z = math.floor(.3989423*math.exp(-((d1*d1)/2))*100000)/100000

  y5=1.330274*math.pow(y,5)
  y4=1.821256*math.pow(y,4)
  y3=1.781478*math.pow(y,3)
  y2=.356538*math.pow(y,2)
  y1=.3193815*y
  x=1-z*(y5-y4+y3-y2+y1)
  x=math.floor(x*100000)/100000

  if (d1<0):
    x = 1 - x

  pbelow = math.floor(x*1000)/10
  pabove = math.floor((1-x)*1000)/10

  return pabove, pbelow

#Testcode
def test1():
  acima, abaixo = probability_above_below(56, 60, 10, 30)
  print(acima)
  print(abaixo)