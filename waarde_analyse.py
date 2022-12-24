"""
Author: naj
Date: 2022-12-24
MIT License
"""


import yfinance as yf
import pandas as pd
import datetime
from statistics import mean


def schat_waarde(symbool):
#from dateutil.relativedelta import relativedelta
    VALUE=0
    
    today = datetime.datetime.now().strftime('%Y-%m-%d')
    todaynf = datetime.datetime.now()
   #print ("De gebruikte einddatum = ",today)
    #vroeger = todaynf - relativedelta(years=10)
    vroeger = todaynf - datetime.timedelta(days=4000)
    van =  vroeger.strftime('%Y-%m-%d')
    #print ("analysedatum nu :", todaynf)
    #print ("analyse vanaf :", van)
    #dhr = yf.Ticker('YIT.HE')
    dhr = yf.Ticker(symbool)
    #gemiddelde prijs van de afgelopen 30 dagen
    vanaf = todaynf - datetime.timedelta(days=30)
    dft = yf.download(symbool,start=vanaf,end=today)
    gemiddelde_prijs_30dagen = mean(dft['High'])
    #gemiddelde prijs tijdens covid
    start=datetime.datetime.strptime("20200301", "%Y%m%d")
    end=datetime.datetime.strptime("20200330", "%Y%m%d")
    #print ("dagen sinds COVID")
    vandaag = datetime.datetime.now()
    dagen_verschil = (vandaag-end)
    #take 7% = 0.07 year increase to bring covidprice till today
    aanpassing_prijs_covid = (dagen_verschil.days)/365*0.07
    #print (aanpassing_prijs_covid)
    try:
        dfcovid = yf.download(symbool,start,end)
        prijscovid = mean(dfcovid['High'])
    except:
        dfcovid = gemiddelde_prijs_30dagen
        prijscovid = dfcovid 
    #prijscovid = mean(dfcovid['High'])
    #print(prijscovid)
    prijscovid = prijscovid + prijscovid * aanpassing_prijs_covid
    #print(prijscovid)
    perc_tov_covid = (gemiddelde_prijs_30dagen-prijscovid)/gemiddelde_prijs_30dagen*100
    COVID_VALUE=0
    #the smaller the difference with the value during COVID, the more valuable
    #if it is cheaper it gets the full points
    if perc_tov_covid < 50:
       COVID_VALUE=COVID_VALUE + 1
    if perc_tov_covid < 40:
       COVID_VALUE=COVID_VALUE + 1
    if perc_tov_covid < 30:
       COVID_VALUE=COVID_VALUE + 1
    if perc_tov_covid < 20:
       COVID_VALUE=COVID_VALUE + 1
    if perc_tov_covid < 10:
       COVID_VALUE=COVID_VALUE + 1
    if perc_tov_covid < 0:
       COVID_VALUE=COVID_VALUE + 5
    #print (perct_tov_covid)
    #print ("gemiddelde_prijs_30dagen", gemiddelde_prijs_30dagen)
    #estime = dhr.analysis
    #print (dir(dhr))
    #print (dhr.get_capital_gains)
    #print (dhr._analysis)
    #print (dhr._fundamentals)
    KOERSWINST=0
    try:
        koerswinst = dhr.info['trailingPE']
    except KeyError:
        koerswinst = 1000
    if type(koerswinst)==type(None):
        koerswinst = 1000
    #if data is not present we do not want a positive result ...
    #print ("koers winst", koerswinst) 
    if koerswinst < 5:
        KOERSWINST=KOERSWINST+2
    if koerswinst < 6:
        KOERSWINST=KOERSWINST+2
    if koerswinst < 7:
        KOERSWINST=KOERSWINST+1
    if koerswinst < 8:
        KOERSWINST=KOERSWINST+1
    if koerswinst < 9:
        KOERSWINST=KOERSWINST+1
    if koerswinst < 10:
        KOERSWINST=KOERSWINST+1
    if koerswinst < 12:
        KOERSWINST=KOERSWINST+1
    if koerswinst < 15:
        KOERSWINST=KOERSWINST+1
   #print ()
   #print ("LUIK HUIDIGE BEURSWAARDERING")
    #print ("koerswinst onder de 12 is OK")
   #print ("koerswinst op een schaal van 10 = ", KOERSWINST)
    try:
        prijstobook = dhr.info['priceToBook']
    except KeyError:
        prijstobook=1000
    if type(prijstobook) == type(None):
        prijstobook=1000
    #if not found least favourable result
    WAARDE=0
    if prijstobook < 0.2 :
       WAARDE = WAARDE + 3
    if prijstobook < 0.5 :
       WAARDE = WAARDE + 2
    if prijstobook < 0.8 :
       WAARDE = WAARDE + 2
    if prijstobook < 1 :
       WAARDE = WAARDE + 1
    if prijstobook < 2 :
       WAARDE = WAARDE + 1
    if prijstobook < 3 :
       WAARDE = WAARDE + 1
    #print ("notering van de boekwaarde onder 2 is OK")
   #print ("de boekwaarde op een schaal van 10 = ", WAARDE)
    #print ("de notering tov maart 2020 COVID")
   #print ("de waardering tov COVID-LOW =",COVID_VALUE) 


    if (type(dhr.info['beta']) != type(None) ):
        beta = dhr.info['beta']
    else:
        beta = 99999999
    WAARDE_BETA = 0
    if beta < 0.3:
        WAARDE_BETA=WAARDE_BETA  + 1
    if beta < 0.6:
        WAARDE_BETA=WAARDE_BETA  + 1
    if beta < 0.9:
        WAARDE_BETA=WAARDE_BETA  + 1
    if beta < 1.2:
        WAARDE_BETA=WAARDE_BETA  + 1
    if beta < 1.4:
        WAARDE_BETA=WAARDE_BETA  + 1
   #print ("de beta waardering =",WAARDE_BETA) 

   #print ()
   #print ("LUIK FUNDAMENTALS")
    try:
        totaleschuld = dhr.info['totalDebt']
    except KeyError:
       #print ("totalDebt not found = results incorrect")
        totaleschuld =99999999999999
    if type(totaleschuld) == type(None):
        totaleschuld =99999999999999


    try:
        pricesales = dhr.info['priceToSalesTrailing12Months']
    except KeyError:
        pricesales = 0

    WAARDE_PRICESALES=0
    if pricesales < 0.2:
        WAARDE_PRICESALES=WAARDE_PRICESALES+1
    if pricesales < 0.4:
        WAARDE_PRICESALES=WAARDE_PRICESALES+1
    if pricesales < 0.6:
        WAARDE_PRICESALES=WAARDE_PRICESALES+1
    if pricesales < 0.8:
        WAARDE_PRICESALES=WAARDE_PRICESALES+1
    if pricesales < 1:
        WAARDE_PRICESALES=WAARDE_PRICESALES+1



    #not found least favourable result
    #print ("totale schuld", totaleschuld)
    #print (dhr.info)
    try:
        aantalaandelen = dhr.info['sharesOutstanding']
    except KeyError:
        aantalaandelen = 0
    if type(aantalaandelen)==type(None):
        aantalaandelen = 0

    #if (type(dhr.info['sharesOutstanding']) != type(None) ):
    #    aantalaandelen = dhr.info['sharesOutstanding']
    #else:
    #    aantalaandelen = 0
    #'regularMarketPrice'
    if (type(dhr.info['currentPrice']) != type(None) ):
        prijs = dhr.info['currentPrice']
    else:
        prijs = 0
    marketcap = aantalaandelen * prijs
    color = ""

    '''
    ebitda
    '''
    if (type(dhr.info['enterpriseToEbitda']) != type(None) ):
        enterpebitda = dhr.info['enterpriseToEbitda']
    else:
        enterpebitda = 999999999
    WAARDE_EBITDA=0
    if enterpebitda < 2:
        WAARDE_EBITDA=WAARDE_EBITDA + 1
    if enterpebitda < 3:
        WAARDE_EBITDA=WAARDE_EBITDA + 1
    if enterpebitda < 4:
        WAARDE_EBITDA=WAARDE_EBITDA + 1
    if enterpebitda < 5:
        WAARDE_EBITDA=WAARDE_EBITDA + 1
    if enterpebitda < 6:
        WAARDE_EBITDA=WAARDE_EBITDA + 1
    if enterpebitda < 7:
        WAARDE_EBITDA=WAARDE_EBITDA + 1
    if enterpebitda < 8:
        WAARDE_EBITDA=WAARDE_EBITDA + 1
    if enterpebitda < 9:
        WAARDE_EBITDA=WAARDE_EBITDA + 1
    if enterpebitda < 10:
        WAARDE_EBITDA=WAARDE_EBITDA + 1
    if enterpebitda < 11:
        WAARDE_EBITDA=WAARDE_EBITDA + 1
   #print ("enterprise value to ebitda score =", WAARDE_EBITDA)
    '''
    current ratio
    rate current assets/current liabilities should be bigger than 1.3
    '''
    try:
        current_asset = (dhr.balance_sheet.T['Current Assets'][0]) 
    except:
        current_asset = 0
    current_liability = 0
    try:
        current_liability = (dhr.balance_sheet.T['Current Liabilities'][0]) 
    except:
        current_liabitity = 9999999999999
    
    if current_liability != 0:
        current_ratio = current_asset/current_liability
    else:
        current_ratio = 0
    
    if current_ratio > 1.3:
        WAARDE_CURRENT = 1
    else:
        WAARDE_CURRENT = 0
    if current_ratio > 1.8:
        WAARDE_CURRENT = WAARDE_CURRENT + 1
    if current_ratio > 2.1:
        WAARDE_CURRENT = WAARDE_CURRENT + 1
    try: 
        gemiddelde_current_asset = mean(dhr.balance_sheet.T['Current Assets']) 
    except:
        gemiddelde_current_asset = 0
    try:
        gemiddelde_current_liability = mean(dhr.balance_sheet.T['Current Liabilities']) 
    except:
        gemiddelde_current_liability = 999999999999
   #print ("verhouding assets/liabilities = ", WAARDE_CURRENT)


    echtewaarde=0
    
    try: 
        intangible = (dhr.balance_sheet.T['Goodwill And Other Intangible Assets'][0]) 
    except KeyError:
        intangible = 999999999999
    #print ("intangible", intangible)
    try: 
        echtewaarde = (dhr.balance_sheet.T['Net Tangible Assets'][0]) 
    except KeyError:
        echtewaarde = 0 

    #print(dhr.balance_sheet.to_string())
    
    if (type(aantalaandelen) != type(None)) : 
        if (aantalaandelen > 0):
            waardeperaandeel = (echtewaarde/aantalaandelen)
            intangiperaandeel = intangible /aantalaandelen
            #print ("echtewaarde")
            #print (echtewaarde)
            #print ("aantal aandelen")
            #print (aantalaandelen)
            schuldperaandeel = (totaleschuld/aantalaandelen)
        else:
            waardeperaandeel = -99999999999 
            schuldperaandeel = 99999999999
            intangiperaandeel = 99999999999
    else : 
        aantalaandelen = 0
        waardeperaandeel = 0
        intangiperaandeel = 0
    
    if (prijs > 0):
        realvalue = waardeperaandeel / prijs
        realdebt = schuldperaandeel / prijs
        realintangible = intangiperaandeel / prijs
    else: 
         realvalue = 99999
         realdebt = 99999
         realintangible = 99999
    #print ("realvalue",realvalue)
    #print ("realdebt", realdebt)
    #print ("realintangible", realintangible)
    
    
    
    #intangible = (dhr.balance_sheet.T['Goodwill And Other Intangible Assets'][0]) 
    #print ("intangible", intangible)
    INTANGIBLE=0
    if realintangible > 0.05:
        INTANGIBLE=INTANGIBLE + 1
    if realintangible > 0.1:
        INTANGIBLE=INTANGIBLE + 1
    if realintangible > 0.15:
        INTANGIBLE=INTANGIBLE + 1
    if realintangible > 0.20:
        INTANGIBLE=INTANGIBLE + 1
    if realintangible > 0.30:
        INTANGIBLE=INTANGIBLE + 1
    if realintangible > 0.40:
        INTANGIBLE=INTANGIBLE + 1
    if realintangible > 0.50:
        INTANGIBLE=INTANGIBLE + 1
    if realintangible > 0.60:
        INTANGIBLE=INTANGIBLE + 1
    if realintangible > 0.70:
        INTANGIBLE=INTANGIBLE + 1
    if realintangible > 0.80:
        INTANGIBLE=INTANGIBLE + 1
    INTANGIBLE = 10 - INTANGIBLE 
    #in case no intangibles score is 10
   #print ("goodwill/intangible in balans = ", INTANGIBLE)

    '''
    realvalue is amount of assets per share
    '''
    WAARDE_AANDEEL=0 
    if realvalue > 0.1:
        WAARDE_AANDEEL = WAARDE_AANDEEL + 1
    if realvalue > 0.2:
        WAARDE_AANDEEL = WAARDE_AANDEEL + 1
    if realvalue > 0.3:
        WAARDE_AANDEEL = WAARDE_AANDEEL + 1
    if realvalue > 0.4:
        WAARDE_AANDEEL = WAARDE_AANDEEL + 1
    if realvalue > 0.5:
        WAARDE_AANDEEL = WAARDE_AANDEEL + 1
    if realvalue > 0.6:
        WAARDE_AANDEEL = WAARDE_AANDEEL + 1
    if realvalue > 0.7:
        WAARDE_AANDEEL = WAARDE_AANDEEL + 1
    if realvalue > 0.8:
        WAARDE_AANDEEL = WAARDE_AANDEEL + 1
    if realvalue > 0.9:
        WAARDE_AANDEEL = WAARDE_AANDEEL + 1
    if realvalue > 1:
        WAARDE_AANDEEL = WAARDE_AANDEEL + 1




    SCHULDGRAAD=0
    
    if realdebt > 0.1:
        SCHULDGRAAD=SCHULDGRAAD + 1
    
    if realdebt > 0.3:
        SCHULDGRAAD=SCHULDGRAAD + 1
    
    if realdebt > 0.5:
        SCHULDGRAAD=SCHULDGRAAD + 1
    
    if realdebt > 0.7:
        SCHULDGRAAD=SCHULDGRAAD + 1
    
    if realdebt > 0.9:
        SCHULDGRAAD=SCHULDGRAAD + 1
    
    if realdebt > 1.0:
        SCHULDGRAAD=SCHULDGRAAD + 5
    SCHULDGRAAD = 10 - SCHULDGRAAD
   #print ("schuldgraad van het bedrijf op schaal van 10 =", SCHULDGRAAD)
    
    




    #TODO
    #print (dhr.balance_sheet.to_string()) 
    #print (dhr.balance_sheet.T['Total Assets']) 
    
    
    '''
    by comparison, if two companies have the same intangible value on their balance sheet,
    the better one will be the company that is diminishing intangible assets
    '''
    
    try: 
        gemiddelde_intangible = mean(dhr.balance_sheet.T['Goodwill And Other Intangible Assets']) 
    except KeyError:
        gemiddelde_intangible = 99999999999999
    if intangible > gemiddelde_intangible:
        EVOLUTION_INTANGIBLE = 0 
    else:
        EVOLUTION_INTANGIBLE = 2 
   #print ()
   #print ("LUIK EVOLUTIE") 
   #print ("evolutie van intangible assets", EVOLUTION_INTANGIBLE)
    
    '''
    by comparison, if two companies have the same asset value on their balance sheet,
    the better one will be the company that has increasing assets
    '''
    try:
        echtewaarde = (dhr.balance_sheet.T['Total Assets'][0])
    except KeyError:
        echtewaarde = 0
    try:
        gemiddelde_waarde = mean(dhr.balance_sheet.T['Total Assets'])
    except KeyError:
        gemiddelde_waarde = 0

    if echtewaarde > gemiddelde_waarde:
        EVOLUTION_ASSET = 2 
    else:
        EVOLUTION_ASSET = 0 
    
   #print ("evolutie van assets = ", EVOLUTION_ASSET)
    
    '''
    by comparison, if two companies have the same liabilities on their balance sheet,
    the better one will be the company that has decreasing liabilities 
    '''
    
    try: 
        verplichting = (dhr.balance_sheet.T['Total Liabilities Net Minority Interest'][0]) 
    except KeyError:
        verplichting = 99999999999
    try:
        gemiddelde_verplichting = mean(dhr.balance_sheet.T['Total Liabilities Net Minority Interest']) 
    except:
        gemiddelde_verplichting = 0
    if verplichting > gemiddelde_verplichting:
        EVOLUTION_LIABILITY = 0 
    else: 
        EVOLUTION_LIABILITY = 2 
    
   #print ("evolutie van liability = ", EVOLUTION_LIABILITY)
    
    '''
    current ratio
    rate current assets/current liabilities should be bigger than 1.3
    try:
        current_asset = (dhr.balance_sheet.T['Current Assets'][0]) 
    except:
        current_asset = 0
    current_liability = 0
    try:
        current_liability = (dhr.balance_sheet.T['Current Liabilities'][0]) 
    except:
        current_liabitity = 9999999999999
    
    if current_liability != 0:
        current_ratio = current_asset/current_liability
    else:
        current_ratio = 0
    
    if current_ratio > 1.3:
        WAARDE_CURRENT = 1
    else:
        WAARDE_CURRENT = 0
    if current_ratio > 1.8:
        WAARDE_CURRENT = WAARDE_CURRENT + 1
    if current_ratio > 2.1:
        WAARDE_CURRENT = WAARDE_CURRENT + 1
    try: 
        gemiddelde_current_asset = mean(dhr.balance_sheet.T['Current Assets']) 
    except:
        gemiddelde_current_asset = 0
    try:
        gemiddelde_current_liability = mean(dhr.balance_sheet.T['Current Liabilities']) 
    except:
        gemiddelde_current_liability = 999999999999
    '''
    
    if current_asset > gemiddelde_current_asset:
        EVOLUTION_CURRENT_ASSET=2
    else:
        EVOLUTION_CURRENT_ASSET=0
    
    if current_liability > gemiddelde_current_liability:
        EVOLUTION_CURRENT_LIABILITY=0
    else:
        EVOLUTION_CURRENT_LIABILITY=2
    
   #print ("evolutie current assets = ", EVOLUTION_CURRENT_ASSET)
   #print ("evolutie current liability = ", EVOLUTION_CURRENT_LIABILITY)
    
    #print (dhr.balance_sheet.iloc[0][0]) 
    
    '''
    go back 11 years in time and count the dividend pay-out
    why 11, well there is probably no payout in the present year
    this way I get a score with 10 as a maximum
    
    what if the company does not exist for 10 years?
    Well that is a valuation as well
    Something that has been around for a longer stretch of time, inspires some confidence.
    '''
    
    #print (dhr.get_earnings_forecast)
    #print (dhr.dividends.info())
    DIVIDEND_SCORE=0
    #print (dhr.dividends)
    for i in (dhr.dividends.index):
        if i.strftime('%Y-%m-%d')>vroeger.strftime('%Y-%m-%d'):
            #print(i)
            DIVIDEND_SCORE = DIVIDEND_SCORE + 1 
    if DIVIDEND_SCORE > 10:
        DIVIDEND_SCORE = 10
    #print ("van de 10 voorgaande jaren werd er ", teller, " keer dividend uitbetaald")
   #print ("dividend score = ", DIVIDEND_SCORE , " op 10")
    #print (type(dhr.dividends))
    #print (dhr.major_holders)
    pnl=dhr.analyst_price_target
    
    #print (pnl)
    #print (pnl.info())
    
    pricetarget=dhr.analyst_price_target
    huidige_prijs = (pricetarget.T['currentPrice'][0])
    geschatte_prijs = (pricetarget.T['targetMeanPrice'][0])
    
    if type(huidige_prijs) == type(None) or type(geschatte_prijs) == type(None):
        huidige_prijs=0
        geschatte_prijs=0
    
    
    if geschatte_prijs != 0:
        prijs_verschil = ((geschatte_prijs-huidige_prijs)/geschatte_prijs) * 100
    else:
        prijs_verschil = 0
    
    ONDERSCHATTING = 0
    if prijs_verschil > 10:
        ONDERSCHATTING=ONDERSCHATTING +1
    if prijs_verschil > 20:
        ONDERSCHATTING=ONDERSCHATTING +1
    if prijs_verschil > 30:
        ONDERSCHATTING=ONDERSCHATTING +1
    if prijs_verschil > 40:
        ONDERSCHATTING=ONDERSCHATTING +1
    if prijs_verschil > 50:
        ONDERSCHATTING=ONDERSCHATTING +1
    if prijs_verschil > 60:
        ONDERSCHATTING=ONDERSCHATTING +1
    if prijs_verschil > 70:
        ONDERSCHATTING=ONDERSCHATTING +1
    if prijs_verschil > 80:
        ONDERSCHATTING=ONDERSCHATTING +1
    if prijs_verschil > 90:
        ONDERSCHATTING=ONDERSCHATTING +2
   #print ()
   #print ("LUIK SCHATTINGEN en AANNAMES")
   #print ("de onderschatting op schaal 10 = ", ONDERSCHATTING)


    ''' 
    de grootte van een bedrijf heeft ook een waarde impact
    te groot dan is het unmanageble
    te klein dan is er een risico
    '''


    OMVANG=0
    if (marketcap > 100000000000):
        color = "BIG CAP"
        OMVANG = 3
    elif (marketcap < 250000000):
        color = "SMALL CAP"
        OMVANG = 2
    else:
        OMVANG=5
    #TODO check sector
    #FINANCIALS als bank of verzekering, krijgen ze hier ook maar 2

   #print ("grootte bedrijf niet te groot of te klein scoort max")
   #print ("de score voor de omvang = ", OMVANG, "op 5")

    #print ("insiderholding", zzz)
    #pnl=dhr.analyst_price_target.iloc[2][0]
    #print ("insiderholding", pnl)
    #pnl=dhr.analyst_price_target.iloc[3][0]
    #print ("insiderholding", pnl)
    #pnl=dhr.analyst_price_target.iloc[4][0]
    #print ("insiderholding", pnl)
    #print (dhr._scrape_url)
    #print (dhr.major_holders)
    #print(dhr.major_holders.iloc[0][0])
    perc_major_holder = float(dhr.major_holders.iloc[0][0].strip('%'))
    
    
    #this is the percentage held by insiders 
    #the more the better
    #skin in the game
    INSIDER_VALUE=0
    if perc_major_holder > 1:
        INSIDER_VALUE=INSIDER_VALUE+1
    if perc_major_holder > 3:
        INSIDER_VALUE=INSIDER_VALUE+1
    if perc_major_holder > 6:
        INSIDER_VALUE=INSIDER_VALUE+1
    if perc_major_holder > 10:
        INSIDER_VALUE=INSIDER_VALUE+1
    if perc_major_holder > 20:
        INSIDER_VALUE=INSIDER_VALUE+1
    if perc_major_holder > 50:
        INSIDER_VALUE=INSIDER_VALUE+5
   #print ("insiders waarde ",INSIDER_VALUE, " op 10")
    #print (perc_major_holder)
    #print(dhr.major_holders.iloc[2][0])
    #print(dhr.major_holders.iloc[3][0])
    #print (dhr.major_holders)
    #print (dhr.mutualfund_holders)
    #print (dhr.info)
    #pd = (dhr.get_major_holders)
    #print (pd)
    
    
    print ("De gebruikte einddatum = ",today)
    print ()
    print ("LUIK HUIDIGE BEURSWAARDERING TOTAAL (50)=", KOERSWINST + WAARDE + COVID_VALUE + WAARDE_BETA + WAARDE_PRICESALES + WAARDE_AANDEEL)
    print ("-koerswinst (10) = ", KOERSWINST)
    print ("-de boekwaarde (10) =  ", WAARDE)
    print ("-tangible value/share (10) =  ", WAARDE_AANDEEL)
    print ("-de waardering tov COVID-LOW (10) =",COVID_VALUE) 
    print ("-de beta waardering (5) =",WAARDE_BETA) 
    print ("-price/sales (5)",WAARDE_PRICESALES) 
    print ()
    print ("LUIK FUNDAMENTALS TOTAAL (33) =", WAARDE_EBITDA + WAARDE_CURRENT + INTANGIBLE + SCHULDGRAAD)
    print ("-enterprise value to ebitda (10) =", WAARDE_EBITDA)
    print ("-verhouding current assets/liabilities (3)= ", WAARDE_CURRENT)
    print ("-goodwill/intangible in balans (10) = ", INTANGIBLE)
    print ("-schuldgraad (10) =", SCHULDGRAAD)
    print ()
    print ("LUIK EVOLUTIE TOTAAL (20) =", EVOLUTION_INTANGIBLE + EVOLUTION_ASSET + EVOLUTION_LIABILITY + EVOLUTION_CURRENT_ASSET + EVOLUTION_CURRENT_LIABILITY + DIVIDEND_SCORE) 
    print ("-evolutie van intangible assets (2)", EVOLUTION_INTANGIBLE)
    print ("-evolutie van assets (2)= ", EVOLUTION_ASSET)
    print ("-evolutie van liability(2) = ", EVOLUTION_LIABILITY)
    print ("-evolutie current assets (2) = ", EVOLUTION_CURRENT_ASSET)
    print ("-evolutie current liability (2) = ", EVOLUTION_CURRENT_LIABILITY)
    print ("-dividend score (10) = ", DIVIDEND_SCORE )
    print ()
    print ("LUIK SCHATTINGEN en AANNAMES TOTAAL (25) =", ONDERSCHATTING + OMVANG + INSIDER_VALUE)
    print ("-de onderschatting (10) = ", ONDERSCHATTING)
    print ("-de score voor de omvang of soort bedrijf (5) = ", OMVANG)
    print ("-insiders waarde (10) =",INSIDER_VALUE)
    TOTAAL = KOERSWINST + WAARDE + OMVANG + EVOLUTION_INTANGIBLE + EVOLUTION_ASSET + EVOLUTION_LIABILITY + WAARDE_CURRENT + EVOLUTION_CURRENT_ASSET  + EVOLUTION_CURRENT_LIABILITY  +  INTANGIBLE + SCHULDGRAAD + ONDERSCHATTING + INSIDER_VALUE + DIVIDEND_SCORE + COVID_VALUE + WAARDE_EBITDA + WAARDE_BETA + WAARDE_PRICESALES + WAARDE_AANDEEL
    print () 
    print ("TOTAAL (128) = ", TOTAAL)
    return (TOTAAL)

totaal=schat_waarde('PAAL-B.CO')
print ("---------------------------")
print ("de geschatte waarde = ",totaal)
