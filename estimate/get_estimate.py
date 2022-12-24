'''
author: naj
Date: 2022-12-12
MIT License
'''

import yfinance as yf
import pandas as pd
dhr = yf.Ticker('TSLA')
#estime = dhr.analysis
#pd = dhr.get_earnings_forecast()
print (dir(dhr))
print(dhr.analysis)
#print(dhr.get_analysis())
#print (estime.info())
#print (estime.info)
#print (estime['Growth'])
#print (estime['Eps Trend Current'])
