import pandas as pd

def macd(df, columns=['MACD', 'Signal', 'Close']):
	gain = pd.Series(index=df.index, dtype=float)
	invested, atPrice = False, 0.
	for i in df.index:
		row = df.loc[i]
		if invested:
			if row[columns[0]] <= row[columns[1]]:
				invested = False
				gain.loc[i] = (row[columns[2]] - atPrice) / atPrice * 100
		elif row[columns[0]] > row[columns[1]]:
			invested = True
			atPrice = row[columns[2]]
	return gain
