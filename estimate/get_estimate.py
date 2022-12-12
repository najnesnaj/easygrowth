'''
author: naj
Date: 2022-12-12
MIT License
'''

import yfinance as yf

dhr = yf.Ticker('AAPL')
estime = dhr.analysis
print (estime.info())
print (estime)
