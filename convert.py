""""""

def rgb_to_uicolor(color, alpha=1, precision=2, prefix='UI'):
	"""Convert a string in RGB COLOR format to UIColor (ios AppKit)"""
	if color[0] != '#' and len(color) == 6:
		color = '#' + color
	color = color.replace('#', '0x')
	color = int(color, base=16)
	r = round(((color & 0xFF0000) >> 16) / 255.0, 2)
	g = round(((color & 0x00FF00) >>  8) / 255.0, 2)
	b = round(((color & 0x0000FF) >>  0) / 255.0, 2)
	return '{prefix}Color(red:{:.{prec}f}, green:{:.{prec}f}, blue:{:.{prec}f}, alpha:{alpha})'.format(r, g, b, alpha=alpha, prec=precision, prefix=prefix)

if __name__ == '__main__':
	from cmds import main
	cmds = [
		'rgb_to_uicolor',
	]
	main('convert', cmds)
