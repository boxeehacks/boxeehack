# -*- coding: utf-8 -*-

#   This file is part of periscope.
#   Copyright (c) 2008-2011 Patrick Dessalle <patrick@dessalle.be>
#
#    periscope is free software; you can redistribute it and/or modify
#    it under the terms of the GNU Lesser General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    periscope is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Lesser General Public License for more details.
#
#    You should have received a copy of the GNU Lesser General Public License
#    along with periscope; if not, write to the Free Software
#    Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

import TheSubDB
import BierDopje
import logging

logging.basicConfig(level=logging.DEBUG)

filename = "/burn/30.Rock.S05E16.HDTV.XviD-LOL.avi"

p = TheSubDB.TheSubDB(None, None)
subfname = filename[:-3]+"srt"
logging.info("Processing %s" % filename)
subs = p.process(filename, ["en", "pt"])

print subs

if not subs:
    p.uploadFile(filename, subfname, 'en')
    subs = p.process(filename, ["en", "pt"])
    print subs


#bd = BierDopje.BierDopje()
#subs = bd.process(filename, ["en"])



