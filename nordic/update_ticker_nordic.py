"""
Author: naj 
Date: 2022-12-08
MIT License
"""


import sqlite3
from datetime import datetime
import yfinance as yahooFinance
import pandas as pd
from statistics import mean
#update the table with companydata
# no finance , assurance
#
# tickerdata are small value stock


def updatedb(transrecord):
    sqliteConnection = sqlite3.connect('nordic.db')
    conn = sqlite3.connect('nordic.db')
    cursor = sqliteConnection.cursor()
    cursor = conn.cursor()
    print ("update record")

#        for i in enumerate(transrecord):
    try:
        symbool = transrecord[0]
        print (symbool)
        cursor.execute('''update nordicinfo set 
        "trailingPE" = ?       ,
        "EPS"  = ?  ,
        "analist_estimate" = ?  ,
        "Price_book" = ?  ,
        "TangibleValuePerShare" = ?  ,
        "enterpriseToEbitda"  = ? ,
        "totalDebt" = ?, 
        "currentRatio" = ?, 
        "growthRate" = ?, 
        "growthRate_quarter" = ?, 
        "beta" = ? ,
        "priceToSalesTrailing12Months" = ?,
        "extrainfo" = ?,
        "value_score" = ?,
        "risc_score" = ?,
        "growth_score" = ?
          where symbol = ?''' , (transrecord[1], transrecord[2], transrecord[3], transrecord[4], transrecord[5], transrecord[6], transrecord[7], transrecord[8], transrecord[9], transrecord[10], transrecord[11],transrecord[12], transrecord[13], transrecord[14], transrecord[15], transrecord[16], symbool))

        conn.commit()
    except sqlite3.Error as error:
        print("Error  sqlite", error)
#        
#        
    if conn:
        conn.close()



def update_compinfo_yahoo():
    conn = sqlite3.connect('nordic.db')
    cursor = conn.cursor()
    try:
        #cursor.execute('''SELECT * from nordicinfo where symbol like  \"WUF1V.HE\" ''')
        cursor.execute('''SELECT * from nordicinfo where rowid > 617 ''')
        rows = cursor.fetchall()
        for row in rows:
            print (row[0])
            GetCompanyInformation = yahooFinance.Ticker(row[0])
            infolen =  len(GetCompanyInformation.info)
            print ("lengte")
            print (infolen)
            if (infolen > 149):
                RISC=0
                GROWTH=0
                VALUE=0
                pnl = GetCompanyInformation.financials
                bs = GetCompanyInformation.balance_sheet
                cf = GetCompanyInformation.cashflow
                transposedfs = bs.T
                financials = pnl.T
                cashflow = cf.T
                col_name = 'Net Tangible Assets'
                if (type(GetCompanyInformation.info['totalDebt']) != type(None) ):
                    totaleschuld = GetCompanyInformation.info['totalDebt']
                else:
                    totaleschuld = 9999999999999999
                try:
                    echtewaarde = (transposedfs.iloc[0,22])
                except IndexError:
                    echtewaarde = 0 
                print ("**** lengte error dataframe *****")
                lengterevenue =  (len(financials));
                if (lengterevenue == 4):
                    gemiddelde = mean(financials["Total Revenue"].iloc[0:4])
                    vroegste = financials["Total Revenue"].iloc[3]
                    if (vroegste != 0):
                        groei = (gemiddelde - vroegste)/vroegste
                    else:
                        groei = 0
                else:
                    groei = 0
                if groei > 0.05:
                    GROWTH = GROWTH + 10
                if groei > 0.10:
                    GROWTH = GROWTH + 10
                if groei > 0.15:
                    GROWTH = GROWTH + 20

                #echtewaarde = (transposedfs.loc[date,col_name].iat[0])
                if (type(GetCompanyInformation.info['sharesOutstanding']) != type(None) ):
                    aantalaandelen = GetCompanyInformation.info['sharesOutstanding']
                else:
                    aantalaandelen = 0
                if (type(GetCompanyInformation.info['currentPrice']) != type(None) ):
                    prijs = GetCompanyInformation.info['currentPrice']
                else:
                    prijs = 0
                marketcap = aantalaandelen * prijs
                color = ""
                if (marketcap > 100000000000):
                    color = "BIG CAP"
#                    cursor.execute('''update garpinfo set color = (?) where symbol = (?)''', ("BIG CAP", row[0])) 
                if (marketcap < 250000000):
                    color = "SMALL CAP"
                    RISC = RISC + 10
#                    cursor.execute('''update garpinfo set color = (?) where symbol = (?)''', ("SMALL CAP", row[0])) 
          #  print (row[0])

                if (type(aantalaandelen) != type(None)) : 
                    if (aantalaandelen > 0):
                        waardeperaandeel = (echtewaarde/aantalaandelen)
                        print ("echtewaarde")
                        print (echtewaarde)
                        print ("aantal aandelen")
                        print (aantalaandelen)
                        schuldperaandeel = (totaleschuld/aantalaandelen)
                    else:
                        waardeperaandeel = -99999999999 
                        schuldperaandeel = 99999999999
                else : 
                    aantalaandelen = 0
                    waardeperaandeel = 0
                if (prijs > 0):
                    realvalue = waardeperaandeel / prijs
                    realdebt = schuldperaandeel / prijs
                else: 
                     realvalue = 99999
                     realdebt = 99999
                print (realvalue)
                print(GetCompanyInformation.info)
                infothere = len(GetCompanyInformation.info)
                #print ("lengte", infothere)
                if (infothere > 115):
                    transrecord=[]
                    transrecord.append(row[0])
                    #transrecord.append(GetCompanyInformation.info['longName'])
                    sektor = (GetCompanyInformation.info['sector'])
                    if (sektor == 'Financial Services'):  
                        RISC = RISC + 10
                        color = "FINANCE"
                    #transrecord.append(sektor)
                    try:
                        trailingPE = GetCompanyInformation.info['trailingPE']
                        print ("trailingPE")
                        print (trailingPE)
                        #if Price/Earnings big : risc is big
                        if trailingPE < 15:
                            VALUE = VALUE + 10
                        if trailingPE < 10:
                            VALUE = VALUE + 10
                        if trailingPE > 15:
                            RISC = RISC +10
                        if trailingPE > 30:
                            RISC = RISC +10
                        transrecord.append(trailingPE)     
                    except KeyError:
                        transrecord.append(0)     
    
                    #transrecord.append(GetCompanyInformation.info['trailingPE'])
                    transrecord.append(GetCompanyInformation.info['trailingEps'])
                    #TODO analist estimate
                    transrecord.append(1)
                    if (type(GetCompanyInformation.info['priceToBook'])) != type(None) :
                        prijstobook = (GetCompanyInformation.info['priceToBook'])
                        if prijstobook < 2:
                            VALUE=VALUE+10
                        if prijstobook < 1:
                            VALUE=VALUE+10
                        transrecord.append(prijstobook)
                        if prijstobook > 2:
                            RISC=RISC + 10
                        if prijstobook > 3:
                            RISC=RISC + 10
                    else:
                        transrecord.append(0)
                        #riciso is verhoogd omdat je gegeven niet hebt
                        RISC=RISC + 20

                    #transrecord.append(GetCompanyInformation.info['totalCashPerShare'])
                    transrecord.append(realvalue)
                    if realvalue < .5:
                        RISC=RISC + 10
                        print ("real value < 0.5")
                    #transrecord.append(GetCompanyInformation.info['forwardPE'])
                    if (type(GetCompanyInformation.info['enterpriseToEbitda'])) != type(None) :
                        etoebitda = (GetCompanyInformation.info['enterpriseToEbitda'])
                        transrecord.append(etoebitda)
                        if etoebitda < 10:
                            VALUE=VALUE + 10
                        if etoebitda < 6:
                            VALUE=VALUE + 10
                    else:
                        transrecord.append(0)

                    #transrecord.append(GetCompanyInformation.info['debtToEquity'])
                    transrecord.append(realdebt)
                    if realdebt > .5:
                        RISC=RISC+10
                    if realdebt > 1:
                        RISC=RISC+10
                    if realdebt > 2:
                        RISC=RISC+20

                    #if (type(GetCompanyInformation.info['enterpriseToEbitda'])) != type(None) :
                    transrecord.append(GetCompanyInformation.info['currentRatio'])
                    transrecord.append(groei)
                    if groei < 0:
                        RISC=RISC+10
                    #TODO grow_rate_quater

                    
                    verandering=0
                    qebit = (GetCompanyInformation.quarterly_financials.T['Ebit'])
                    gemiddelde_ebit = mean(qebit)
                    vroegste = qebit.iloc[3]
                    laatste = qebit.iloc[0]
                    if vroegste != 0:
                        verandering = abs((laatste - vroegste)/vroegste) 
                        verhouding = (laatste/vroegste)
                    else:
                        verhouding = 0
                    if verhouding > 1:
                        GROWTH=GROWTH +10
                    if verhouding > 2: 
                        GROWTH=GROWTH +10
                    #else: 
                        #print('sommige quartaalcijfers zijn nul')
                    if (verandering < 0):
                        RISC = RISC + 10

                    transrecord.append(verhouding)
                    #seems like earningsGrowth in yahoo finance is an estimate, I've replace this with a calculations of Total Revenue Growth from the past 4 years
                    #transrecord.append(GetCompanyInformation.info['earningsGrowth'])
                    transrecord.append(GetCompanyInformation.info['beta'])
                    transrecord.append(GetCompanyInformation.info['priceToSalesTrailing12Months'])
                    transrecord.append(color)
                    #TODO value_score 
                    transrecord.append(VALUE)
                    #TODO risc_score 
                    transrecord.append(RISC)
                    #TODO growth_score
                    transrecord.append(GROWTH)
                    print (transrecord)
                    updatedb (transrecord)
               
    except sqlite3.Error as error:
        print("Error  sqlite", error)

    finally:
        if conn:
            conn.close()



#get latest financial data from yahoo
update_compinfo_yahoo()

