import csv
import pandas as pd
import requests
import sqlite3

conn = sqlite3.connect('quickfs_nordic.db')
curs = conn.cursor()
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

with open('quickfssymbol.csv', 'r') as fin:
    dr = csv.reader(fin,delimiter=';')
    for rij in dr:
        TICKER =  rij[0]
        print (TICKER)
        html = requests.get(f'https://api.quickfs.net/stocks/{TICKER}/ovr/Annual/?sortOrder=ASC', headers=headers)
        try:
            df = pd.read_html(html.json()['datasets']['ovr'], header=0, index_col=0)[0]
            omgekeerd = df.transpose()
            print (omgekeerd)
            try:
                ISIN = html.json()['datasets']['metadata']['ISIN']
                omgekeerd['ISIN']= ISIN
            except KeyError:
                omgekeerd['ISIN']='not found'
            omgekeerd['ticker']=TICKER
            try:
                omgekeerd.to_sql('quick_temp', conn, if_exists='append')
            except sqlite3.Error as error:
                print("Error  sqlite", error)
        except KeyError:
            print ('KeyError  maybe not found ....on quickfs') 
    #print (html.json()['datasets']['metadata']['qfs_symbol_v2'])
    #print (omgekeerd.index)

