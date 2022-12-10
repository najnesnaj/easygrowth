## README ##


These scripts get data from nasdaq sweden-finland-denmark (nordic countries)


scrap_nasdaq_nordic.py
scrap_nasdaq_nordic_mid.py
scrap_nasdaq_nordic_small.py


The retrieved data is stored in "semicolon" separated values

nasdaq_nordic_large.csv
nasdaq_nordic_mid.csv
nasdaq_nordic_small.csv

There is a database with some additional fields. e.g. Yahoo-symbool to get extra data from finance.yahoo

nordic.db
nordicinfo.sql

Insert_ticker inserts all the data from the cvs files and gets the yahoo-ticker

insert_ticker.py

Update_ticker does some analytics and get ratio's off finance.yahoo.

update_ticker_nordic.py



Year_results_nordic.csv 

these values are retrieved from quickfs and contain multi-year data (10y)
