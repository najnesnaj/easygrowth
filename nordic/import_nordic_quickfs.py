import pandas as pd
import requests
import sqlite3
conn = sqlite3.connect('quickfs_nordic.db')
curs = conn.cursor()
#rows = curs.execute("SELECT company_ticker from company_list where rowid > 34479 and rowid < 40000;").fetchall()
print ("")
#for row in rows:
#    TICKER = (row[0])
TICKER = "GN:DK"
#    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:106.0) Gecko/20100101 Firefox/106.0'}
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
html = requests.get(f'https://api.quickfs.net/stocks/{TICKER}/ovr/Annual/?sortOrder=ASC', headers=headers)
df = pd.read_html(html.json()['datasets']['ovr'], header=0, index_col=0)[0]

    #print (html.json()['datasets']['metadata']['qfs_symbol_v2'])
omgekeerd = df.transpose()
print (omgekeerd)
try:
    ISIN = html.json()['datasets']['metadata']['ISIN']
    omgekeerd['ISIN']= ISIN
except KeyError:
    omgekeerd['ISIN']='not found'
try:
    CUSIP = html.json()['datasets']['metadata']['cusip']
    omgekeerd['CUSIP']=CUSIP
except KeyError:
    omgekeerd['CUSIP']='not found'
    omgekeerd['ticker']=TICKER
    #print (omgekeerd.index)
try:
    omgekeerd.to_sql('quick_temp', conn, if_exists='append')
except sqlite3.Error as error:
    print("Error  sqlite", error)

