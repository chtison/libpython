""""""
from importlib import import_module
from inspect import getsource
import sys

def usage(cmds, module=None, symbol=None):
	if module is not None and symbol is not None:
		print(getsource(getattr(import_module(module), symbol)).split('\n', 1)[0])
	else:
		print('Usage: available commands are:')
		print('- help COMMAND')
		for cmd in cmds:
			print('- {}'.format(cmd))
	exit(1)

def main(module, cmds, argv=sys.argv):
	if len(sys.argv) is 1:
		usage(cmds)
	if sys.argv[1] == 'help':
		if len(sys.argv) is 3:
			usage(cmds, module, sys.argv[2])
		usage(cmds)
	fn = getattr(import_module(module), argv[1], None)
	if fn is None:
		usage(cmds)
	print(fn(*argv[2:]))
