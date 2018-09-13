import requests
import pandas as pd

BINANCE_API = 'https://api.binance.com/api'

def get_klines(symbol, interval):
	params = {
	    'symbol': symbol,
	    'interval': interval,
	}
	data = []
	while True:
	    response = requests.get(BINANCE_API+'/v1/klines', params=params)
	    if len(response.json()) == 0: break
	    data = response.json() + data
	    params['endTime'] = data[0][0] - 1
	df = pd.DataFrame(data)
	df.columns = [
		'Open Time',
		'Open',
		'High',
		'Low',
		'Close',
		'Volume',
		'Close Time',
		'Quote Asset Volume',
		'Number of Trades',
		'Taker Buy Base Asset Volume',
		'Taker Buy Quote Asset Volume',
		'Ignore',
	]
	df['Open Time'] = pd.to_datetime(df['Open Time'], unit='ms')
	df['Close Time'] = pd.to_datetime(df['Close Time'], unit='ms')
	df = df.set_index('Open Time').sort_index()
	df = df.astype({
	    'Open': float,
	    'High': float,
	    'Low': float,
	    'Close': float,
	    'Volume': float,
	    'Quote Asset Volume': float,
	    'Number of Trades': int,
	    'Taker Buy Base Asset Volume': float,
	    'Taker Buy Quote Asset Volume': float,
	    'Ignore': float,
	})
	return df



if __name__ == '__main__':
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument("SYMBOL")
	parser.add_argument("INTERVAL")
	args = parser.parse_args()
	df = get_klines(args.SYMBOL, args.INTERVAL)
	df.to_csv('{}-{}.json'.format(args.SYMBOL, args.INTERVAL))
