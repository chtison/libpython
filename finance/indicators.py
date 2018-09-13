import pandas as pd

def _ema(x, previousEMA, multiplier):
    if len(previousEMA) == 0:
        previousEMA.append(x.mean())
    else:
        previousEMA[0] = (x[-1] - previousEMA[0]) * multiplier + previousEMA[0]
    return previousEMA[0]

def ema(df, periods=12, column='Close'):
    return df[column].rolling(periods, min_periods=periods).apply(_ema, raw=False, args=([], 2 / (periods + 1)))

def macd(df, fast=12, slow=26, signal=9, columns=['Close', None, None]):
    newdf = pd.DataFrame()
    columns = columns + [None for i in range(3-len(columns))]
    if columns[1] == None:
        columns[1] = 'EMA {}'.format(fast)
        newdf[columns[1]] = ema(df, periods=fast, column=columns[0])
    else:
        newdf[columns[1]] = df[columns[1]]
    if columns[2] == None:
        columns[2] = 'EMA {}'.format(slow)
        newdf[columns[2]] = ema(df, periods=slow, column=columns[0])
    else:
        newdf[columns[2]] = df[columns[2]]
    newdf['MACD'] = newdf[columns[1]] - newdf[columns[2]]
    newdf['Signal'] = ema(newdf, periods=signal, column='MACD')
    newdf['Histogram'] = newdf['MACD'] - newdf['Signal']
    return newdf
