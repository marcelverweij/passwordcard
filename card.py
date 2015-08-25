#!/usr/bin/python

import sys
import random
from passwordcard import *

def card(seed = None, HEIGHT = 8, WIDTH = 29):
	if seed is None:
		seed = random.randrange(1 << 64)
	else:
		seed = int("0x%s" % seed, 16)

	TOP_CHARSET = passwordcard.CHARSETS['original.alphanumeric']
	BOTTOM_CHARSET = passwordcard.CHARSETS['original.alphanumeric']
	HEADER = passwordcard.HEADERS['original']

	header, contents = passwordcard.generate_card(seed, WIDTH, HEIGHT, TOP_CHARSET, BOTTOM_CHARSET, HEADER)

	print header
	for i in range(len(contents)):
		print str(i + 1) + ' ' + contents[i]
	print ("%x" % seed).center(WIDTH, ' ')


seed = None
if len(sys.argv) > 1:
	seed = sys.argv[1]
card(seed, 16)
