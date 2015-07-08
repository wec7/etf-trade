import urllib2

def read_page():
    response = urllib2.urlopen('http://finance.yahoo.com/etf/lists/?mod_id=mediaquotesetf&tab=tab3&rcnt=50')
    the_page = response.read()
    return the_page

def parse_page(the_page):
    splits = the_page.split('<a href=\\"\/q?s=')
    etf_symbols = [split.split('\\')[0] for split in splits[1:]]
    return etf_symbols

def get_ETFSymbols(source):
    if source.lower() == 'yahoo':
        return parse_page(read_page())
    elif source.lower == 'nasdaq':
        return pandas.read_csv('http://www.nasdaq.com/investing/etfs/etf-finder-results.aspx?download=Yes')['Symbol'].values