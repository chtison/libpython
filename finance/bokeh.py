import bokeh.plotting
import numpy as np

def candlesticks(df, cds, columns=['Open Time', 'Open', 'High', 'Low', 'Close'], figure_opts={}):
	c = columns
	figure = bokeh.plotting.Figure(**figure_opts, x_axis_type='datetime')
	inc = bokeh.models.CDSView(source=cds, filters=[bokeh.models.BooleanFilter(df[c[4]] > df[c[1]])])
	dec = bokeh.models.CDSView(source=cds, filters=[bokeh.models.BooleanFilter(df[c[4]] <= df[c[1]])])
	figure.segment(c[0], c[2], c[0], c[3], source=cds, view=inc, color='green')
	figure.segment(c[0], c[2], c[0], c[3], source=cds, view=dec, color='red')
	width = (cds.data[c[0]][1] - cds.data[c[0]][0]) / np.timedelta64(1, 'ms')
	figure.vbar(c[0], width, c[1], c[4], source=cds, view=inc, fill_color='green', line_color=None)
	figure.vbar(c[0], width, c[1], c[4], source=cds, view=dec, fill_color='red', line_color=None)
	figure.yaxis.formatter = bokeh.models.NumeralTickFormatter(format='0.[00000000]')
	return figure

def macd(cds, columns=['Open Time', 'MACD', 'Signal', 'Histogram'], figure_opts={}):
	c = columns
	figure = bokeh.plotting.Figure(x_axis_type='datetime', **figure_opts)
	figure.title.text = 'MACD'
	figure.line(c[0], c[1], source=cds)
	figure.line(c[0], c[2], source=cds)
	figure.vbar(c[0], 1, c[3], source=cds)
	figure.yaxis.formatter = bokeh.models.NumeralTickFormatter(format='0.[00000000]')
	return figure
