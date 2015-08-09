import pandas

from emails import SUBSCRIBE_LIST, email_login, send_mail
from remoteDataAccess import read_yahooData
from indicator import rsi, bbands
from url import get_ETFSymbols

def find_validETF(filename):
    ls_etf = []
    ls_rsi = []
    ls_bbd = []
    for etf in get_ETFSymbols('Nasdaq'):
        try:
            price = read_yahooData(etf)
        except IOError:
            continue
        relative_strength = rsi(price)
        bollinger_band = bbands(price)

        if relative_strength < 30. and bollinger_band < 0.:
            ls_etf.append(etf)
            ls_rsi.append(round(relative_strength,3)) 
            ls_bbd.append(round(bollinger_band,3))

    df = pandas.DataFrame({
        'ETF': ls_etf,
        'Relative Strength': ls_rsi,
        'Bollinger Band': ls_bbd
    })
    df.set_index('ETF').to_csv(filename)

def run(me, password):
    find_validETF('ETF.csv')
    send_mail(
        send_from = 'NoReply@gmail.com', 
        send_to = SUBSCRIBE_LIST, 
        subject = 'Suggested ETF', 
        text = """Hello,

Attachment includes the ETFs with today's close lower than Bollinger Bottom and Relative Strength Index lower than 30.

Sincerely,
-Weiyi
""", 
        files = ['ETF.csv'], 
        server = 'smtp.gmail.com',
        username = me,
        password = password
    )

if __name__ == '__main__':
    me, password = email_login()
    run(me, password)