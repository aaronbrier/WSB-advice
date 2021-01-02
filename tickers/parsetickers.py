import csv
import os
#a quick script that takes all the csv file in the current directory and adds the first column to a set in tickerslist.py

files = [file for file in os.listdir() if file.endswith(".csv")]
tickers = set()
for file in files:
	with open(file) as csv_file:
		csv_reader = csv.reader(csv_file, delimiter = ",")
		for row in csv_reader:
			if row[0] != "Symbol":
				tickers.add(row[0])
new_file = open("../tickerslist.py", "w")
new_file.write("TICKER_LIST = "+tickers.__repr__())
new_file.close()