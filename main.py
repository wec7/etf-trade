# url 
import urllib
import urllib2

# remote data access
import pandas.io.data as web
import datetime

# data process
import pandas

def read_page():
    response = urllib2.urlopen('http://finance.yahoo.com/etf/lists/?mod_id=mediaquotesetf&tab=tab3&rcnt=50')
    the_page = response.read()
    return the_page

def parse_page(the_page):
    splits = the_page.split('<a href=\\"\/q?s=')
    etf_symbols = [split.split('\\')[0] for split in splits[1:]]
    return etf_symbols

def get_ETFSymbols():
    return pandas.read_csv('http://www.nasdaq.com/investing/etfs/etf-finder-results.aspx?download=Yes')['Symbol'].values

def read_yahooData(etf):
    start = datetime.datetime.today() - datetime.timedelta(days=60)
    price = web.DataReader(etf, 'yahoo', start)
    return price['Adj Close']

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

def find_validETF():
    ls_etf = []
    ls_rsi = []
    ls_bbd = []
    for etf in parse_page(read_page()):
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
    df.set_index('ETF').to_csv('ETF.csv')

def email(textfile, me, you, password):
    # Import smtplib for the actual sending function
    import smtplib

    # Import the email modules we'll need
    from email.mime.text import MIMEText

    # Open a plain text file for reading.  For this example, assume that
    # the text file contains only ASCII characters.
    fp = pandas.read_csv(textfile)
    # Create a text/plain message
    msg = MIMEText(fp.__repr__())

    # me == the sender's email address
    # you == the recipient's email address
    msg['Subject'] = 'The contents of %s' % textfile
    msg['From'] = me
    msg['To'] = you

    # Send the message via our own SMTP server, but don't include the
    # envelope header.
    s = smtplib.SMTP('smtp.gmail.com',587)

    s.ehlo()
    s.starttls()
    s.ehlo()
    s.login(me, password)

    s.sendmail(me, [you], msg.as_string())
    s.quit()

SUBSCRIBE_LIST = [
    'weiyi.alan.chen@gmail.com'
]

def main():
    print "Email Login - "
    me = raw_input("\tEmail: ")
    password = raw_input("\tPassword: ")
    find_validETF()
    for you in SUBSCRIBE_LIST:
        email('ETF.csv', me, you, password)

if __name__ == '__main__':
    main()