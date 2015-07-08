import pandas

def rsi(price, n=14):
    ''' rsi indicator '''
    delta = price.diff()
    dUp, dDown = delta.copy(), delta.copy()
    dUp[dUp < 0] = 0
    dDown[dDown > 0] = 0

    RolUp = pandas.rolling_mean(dUp, n)
    RolDown = pandas.rolling_mean(dDown, n).abs()

    RS = RolUp / RolDown
    rsi = 100.0 - (100.0 / (1.0 + RS))
    return rsi.values[-1]

def bbands(price, length=20, numsd=2):
    """ returns average, upper band, and lower band"""
    ave = pandas.stats.moments.rolling_mean(price,length)
    sd = pandas.stats.moments.rolling_std(price,length)
    upband = ave + (sd*numsd)
    dnband = ave - (sd*numsd)
    return (price.values[-1] - dnband.values[-1]) / (upband.values[-1] - dnband.values[-1])