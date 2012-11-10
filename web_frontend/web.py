#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#
# web - A web frontend for passwordcard
#
# Copyright © 2012 Nicolas Dandrimont <nicolas.dandrimont@crans.org>
#
#   This file is part of PasswordCard.
#
#   PasswordCard is free software: you can redistribute it and/or modify
#   it under the terms of the GNU Affero General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU Affero General Public License for more details.
#
#   You should have received a copy of the GNU Affero General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

import os
import random

import gevent.monkey
gevent.monkey.patch_all()
import bottle

import passwordcard

WIDTH = 29
HEIGHT = 8

TOP_CHARSET = passwordcard.CHARSETS['original.alphanumeric']
BOTTOM_CHARSET = passwordcard.CHARSETS['original.alphanumeric']

HEADER = passwordcard.HEADERS['original']

@bottle.route('/')
@bottle.route('/by_seed/<seed>')
def card(seed = None):
    if seed is None:
        seed = random.randrange(1<<64)
    else:
        seed = int("0x%s" % seed, 16)

    header, contents = passwordcard.generate_card(seed, WIDTH, HEIGHT, TOP_CHARSET, BOTTOM_CHARSET, HEADER)

    contents = u'\n'.join("%d %s" % (i+1, content) for i, content in enumerate(contents))

    return bottle.template('''<pre>  {{header}}\n\n{{contents}}</pre><p>0x<a href="/by_seed/{{seed}}">{{seed}}</a></p>''', header = header, contents = contents, seed = "%016x" % seed)

bottle.run(server='gevent', host='0.0.0.0', port=os.environ.get('PORT', 8080))