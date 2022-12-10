"""
Author: naj 
Date: 2022-12-10
MIT License
"""


import sqlite3
import os
import yfinance as yf
from statistics import mean
import datetime
today = datetime.datetime.now().strftime('%Y-%m-%d')
todaynf = datetime.datetime.now()
print ("De gebruikte einddatum = ",today)
vroeger = todaynf - datetime.timedelta(days=30)
van =  vroeger.strftime('%Y-%m-%d')
#from datetime import datetime
#import yfinance as yahooFinance
#import pandas as pd
#from statistics import mean
#update the table with companydata
# no finance , assurance
#
# tickerdata are small value stock


#symbol names outside US contain a dot, these are considered first

def select_compinfo_yahoo():
    conn = sqlite3.connect('nordic.db')
    cursor = conn.cursor()
    try:
        #cursor.execute('''SELECT symbol from garpinfo where extrainfo like  \"8\"  and  symbol like \"%.%\" and color not like \"%CAP%\"  and color not like \"FINANCIALS\" ''')
        #cursor.execute('''SELECT symbol from nordicinfo where symbol like \"HH.CO\"    ''')
        cursor.execute('''SELECT symbol from nordicinfo    ''')
        rows = cursor.fetchall()
        for row in rows:
            print (row[0])
            hulpvar = row[0]

            tickerinfo = yf.Ticker(hulpvar)
            infolen =  len(tickerinfo.info)
            if (infolen > 149):
                dft = yf.download(hulpvar,start=van,end=today)
                gemiddelde_prijs_30dagen = mean(dft['High'])
    
                #ROA = tickerinfo.info['returnOnAssets']
                #ROE = tickerinfo.info['returnOnEquity']
                #print (hulpvar, ROA, ROE)
                #print ("ten opzichte van de gemiddelde prijs van de afgelopen 30 dagen = ",gemiddelde_prijs_30dagen)
                targetprijs =  (tickerinfo.info['targetMeanPrice'])
                print ("targetprijs van analisten in Yahoo = ", targetprijs)
                if (targetprijs != None):
                    perct_to_target = (targetprijs - gemiddelde_prijs_30dagen)/gemiddelde_prijs_30dagen
                    opwaarts = perct_to_target*100
                    print ("Het geschat opwaarts potentieel op 1 jaar? = ", opwaarts, " percent")
                else:
                    targetprijs = 0 
                    opwaarts = 0
                cursor.execute('''update nordicinfo set analist_estimate = (?) where symbol = (?)    ''', (opwaarts, hulpvar))
                conn.commit() 
                #start=datetime.datetime.strptime("20200301", "%Y%m%d")
                #end=datetime.datetime.strptime("20200330", "%Y%m%d")
    
                #print (start)
                #dfcovid = yf.download(hulpvar,start,end)
                #print (dfcovid)
                #prijscovid = mean(dfcovid['High'])
                #print(prijscovid)
    
                  
    
                #perct_tov_covid = (gemiddelde_prijs_30dagen-prijscovid)/gemiddelde_prijs_30dagen
                #neerwaarts = perct_tov_covid * 100
    
                #print ("neerwaarts = ", neerwaarts)
                #enkel als het prijsverschil met maart 2020 klein genoeg een rapport maken
                #if (neerwaarts < 60) and (opwaarts > 50) :
                #vroeger = todaynf - datetime.timedelta(days=30)
                #van =  vroeger.strftime('%Y-%m-%d')
                #    os.system('papermill -p symbool {0} generiek.ipynb generiekparam{0}.ipynb'.format(hulpvar))
               #     os.system("jupyter-nbconvert --to pdf --TemplateExporter.exclude_input=True generiekparam{0}.ipynb".format(hulpvar))
    except sqlite3.Error as error:
        print("Error  sqlite", error)

    finally:
        if conn:
            conn.close()



#get latest financial data from yahoo
select_compinfo_yahoo()

