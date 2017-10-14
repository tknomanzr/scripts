#! /usr/bin/python
# A simple utility that will calculate bitcoin balance from an electrum wallet.
# Requires: gdax, pandas, matplotlib
# Assumes: you currently have bitcoin stored in an electrum wallet.
# Author: William Bradley
# BunsenLabs Forum Handle: tknomanzr
# License: GPL3.0.

import gdax
import pandas as pd
import matplotlib.pyplot as plt 
plt.style.use('dark_background')
import datetime
import subprocess
import os, fcntl
def run_once():
    global fh
    fh=open(os.path.realpath(__file__),'r')
    try:
        fcntl.flock(fh,fcntl.LOCK_EX|fcntl.LOCK_NB)
    except:
        os._exit(0)
if __name__ == "__main__":
	run_once()
	# Get historical bitcoin price information from gdax     
	client = gdax.PublicClient()
	rates = client.get_product_historic_rates('BTC-USD', granularity=60*60*24)
	# Modify the dates from ISO 8601 to human readable.
	dates = [datetime.date.fromtimestamp(element[0]) for element in rates]
	# Create the pandas plot. 
	df = pd.DataFrame(rates, columns = ['date', 'low', 'high', 'open', 'close', 'volume'])
	df['date'] = [datetime.date.fromtimestamp(element[0]) for element in rates]
	df = df.head(30)
	df = df.sort_values('date', ascending = True)
	df.plot('date', 'close', kind='line', use_index=True, title='Bitcoin closing prices by date', rot=90, grid=True, figsize=[6,9])
	plt.show()
	
