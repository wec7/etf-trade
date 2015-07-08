import pandas.io.data as web
import datetime

def read_yahooData(etf):
    start = datetime.datetime.today() - datetime.timedelta(days=60)
    price = web.DataReader(etf, 'yahoo', start)
    return price['Adj Close']