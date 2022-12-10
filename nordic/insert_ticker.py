import csv
import yfinance as yahooFinance
import sqlite3



def insertdb(transrecord):
    sqliteConnection = sqlite3.connect('nordic.db')
    conn = sqlite3.connect('nordic.db')
    cursor = sqliteConnection.cursor()
    cursor = conn.cursor()
    print ("insert record")

#        for i in enumerate(transrecord):
    try: 
        cursor.execute('''INSERT INTO nordicinfo( 
        "symbol" ,
        "name"    ,
        "currency"     ,
        "sector"  ,
        "sectorcode"        ,
        "ISIN"    
        ) VALUES(?,?,?,?,?,?)''' , (transrecord[0:6]))

        conn.commit()
    except sqlite3.Error as error:
        print("Error  sqlite", error)
#        
#        
    if conn:
        conn.close()








def check_ticker_large():
#    try:
    print ("test")
    with open('nasdaq_nordic_large.csv', 'r') as fin:
        dr = csv.DictReader(fin,delimiter=';')
        for rij in dr:
            transrecord=[]
            transrecord.append(rij['symbol'])
            transrecord.append(rij['name'])
            transrecord.append(rij['currency'])
            transrecord.append(rij['sector'])
            transrecord.append(rij['sector_code'])
            transrecord.append(rij['isin'])
            print(transrecord)
            insertdb(transrecord)


def check_ticker_mid():
#    try:
    print ("test")
    with open('nasdaq_nordic_mid.csv', 'r') as fin:
        dr = csv.DictReader(fin,delimiter=';')
        for rij in dr:
            transrecord=[]
            transrecord.append(rij['symbol'])
            transrecord.append(rij['name'])
            transrecord.append(rij['currency'])
            transrecord.append(rij['sector'])
            transrecord.append(rij['sector_code'])
            transrecord.append(rij['isin'])
            print(transrecord)
            insertdb(transrecord)

def check_ticker_small():
#    try:
    print ("test")
    with open('nasdaq_nordic_small.csv', 'r') as fin:
        dr = csv.DictReader(fin,delimiter=';')
        for rij in dr:
            transrecord=[]
            transrecord.append(rij['symbol'])
            transrecord.append(rij['name'])
            transrecord.append(rij['currency'])
            transrecord.append(rij['sector'])
            transrecord.append(rij['sector_code'])
            transrecord.append(rij['isin'])
            print(transrecord)
            insertdb(transrecord)
#filter()
check_ticker_large()
check_ticker_mid()
check_ticker_small()

