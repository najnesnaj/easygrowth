import pandas as pd
import requests
from bs4 import BeautifulSoup



def get_symbol_for_isin(isin):
        url = 'https://query1.finance.yahoo.com/v1/finance/search'
        headers = { 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.109 Safari/537.36', }
        params = dict( q=isin, quotesCount=1, newsCount=0, listsCount=0, quotesQueryId='tss_match_phrase_query')
        resp = requests.get(url=url, headers=headers, params=params)
        #print (resp)
            #print ("respons 400 suppose this is OK")
        try:
            data = resp.json()
        except JSONDecodeError:
            data = ""
        if 'quotes' in data and len(data['quotes']) > 0:
            return data['quotes'][0]['symbol']
        else:
            return None




headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
r = requests.get(f'https://www.nasdaqomxnordic.com/shares/listed-companies/nordic-mid-cap', headers=headers)
soup = BeautifulSoup(r.content, 'html5lib')
tag = soup.tbody
teller=0
veld_nummer=0
for beschrijf in tag.strings:
    if beschrijf == "\n":
        teller = teller + 1
    else:
        if (teller>1):
            print()
            veld_nummer=0
        print (beschrijf, end=";")
        veld_nummer=veld_nummer+1
        if veld_nummer == 4:
            yahoo_symbool = get_symbol_for_isin(beschrijf)
            print (yahoo_symbool, end= ";")
        #print (teller)
        teller = 0
#print (soup)
