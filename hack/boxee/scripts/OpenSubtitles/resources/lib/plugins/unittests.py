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

import unittest
import logging
import os

logging.basicConfig(level=logging.DEBUG)
'''
class TVShowRegexTestCase(unittest.TestCase):
    def runTest(self):
        import OpenSubtitles
        subdb = OpenSubtitles.OpenSubtitles()
        filenames = ('Futurama.S06E05.HDTV.XviD-aAF.avi', 'Parenthood.2010.S01E13.Lost.and.Found.HDTV.XviD-FQM.avi')
        for filename in filenames:
            print "%s => %s" %(filename, subdb.guessFileData(filename))


class RegexTestCase(unittest.TestCase):
    def runTest(self):
        import OpenSubtitles
        subdb = OpenSubtitles.OpenSubtitles()
        #filenames = ('Marley & Me.2008-L33t-DvDRiP.DivX.NoRaR', 'Dexter.S04E01.HDTV.XviD-NoTV', 'Night.Watch.2004.CD1.DVDRiP.XViD-FiCO' , 'Stargate.Universe.S01E06.HDTV.XviD-XII.avi', 'The.Office.US.S06E01.HDTV.XviD-2HD.[VTV]', 'Twilight[2008]DvDrip-aXXo', 'Heroes.S03E09.HDTV.XviD-LOL', 'Transformers.Revenge.of.the.Fallen.TS.XviD-DEViSE', 'My.Name.is.Earl.S04E24.HDTV.XviD-LOL', 'Wallace.And.Gromit.A.Matter.Of.Loaf.And.Death.HDTV.XviD-BiA', 'arw-spread.dvdrip-xvid', 'Rec.2.[Spanish].TS-Screener.XviD.[DTL]', 'X-Men Origins Wolverine [2009] dvd rip nlx', 'Saw VI (2009) TS DivXNL-Team', 'Michael Jackson This Is It 2009 CAM XVID-PrisM.NoRar.www.crazy-torrent.com', 'The.Goods.Live.Hard.Sell.Hard.2009.PROPER.DvDRiP.XviD-ExtraScene RG')
        #filenames = ('The.Hurt.Locker.2008.DVDRiP.XViD.CD1', 'Catwoman.CAM-NOX-CD2.avi','Marley & Me.2008-L33t-DvDRiP.DivX.NoRaR')
        filenames = ('Catwoman.CAM-NOX-CD2.avi', 'Funny People (2009) DVDRip XviD-MAXSPEED www.torentz.3xforum.ro')
        for filename in filenames:
            print "%s => %s" %(filename, subdb.guessFileData(filename))

class SubtitulosTestCase(unittest.TestCase):
    def runTest(self):
        import Subtitulos
        subdb = Subtitulos.Subtitulos()
        fname = "CSI.S10E13.HDTV.XvID-FQM.avi"
        fname = "rubicon.s01e01.repack.hdtv.xvid-fqm.avi"
        guessedData = subdb.guessFileData(fname)
        print fname
        print guessedData
        if guessedData['type'] == 'tvshow':
            subs = subdb.query(guessedData['name'], guessedData['season'], guessedData['episode'], guessedData['teams'])
            print subs

class Addic7edTestCase(unittest.TestCase):
    def runTest(self):
        import Addic7ed
        subdb = Addic7ed.Addic7ed()
        fname = "The.Big.Bang.Theory.S03E13.HDTV.XviD-2HD"
        guessedData = subdb.guessFileData(fname)
        print fname
        print guessedData
        if guessedData['type'] == 'tvshow':
            subs = subdb.query(guessedData['name'], guessedData['season'], guessedData['episode'], guessedData['teams'])
            print subs

class Addic7edTestCase(unittest.TestCase):
    def runTest(self):
        import Addic7ed
        subdb = Addic7ed.Addic7ed()
        #fname = "rubicon.s01e01.repack.hdtv.xvid-fqm.avi"
        fname = "24.1x03.2.00.am_3.00.am.ac3.dvdrip_ws_xvid-fov.avi"
        guessedData = subdb.guessFileData(fname)
        print fname
        print guessedData
        if guessedData['type'] == 'tvshow':
            subs = subdb.query(guessedData['name'], guessedData['season'], guessedData['episode'], guessedData['teams'])
            print subs

class OpenSubtitlesTestCase(unittest.TestCase):
    def runTest(self):
        import OpenSubtitles
        subdb = OpenSubtitles.OpenSubtitles()
        # movie hash if for night watch : http://trac.opensubtitles.org/projects/opensubtitles/wiki/XMLRPC
        results = subdb.query('Night.Watch.2004.CD1.DVDRiP.XViD-FiCO.avi', moviehash="09a2c497663259cb", bytesize="733589504")
        
        assert len(results) > 0, 'No result found for Night.Watch.2004.CD1.DVDRiP.XViD-FiCO.avi by movie hash'

class OpenSubtitlesTestCase(unittest.TestCase):
    def runTest(self):
        import OpenSubtitles
        subdb = OpenSubtitles.OpenSubtitles()
        # movie hash if for night watch : http://trac.opensubtitles.org/projects/opensubtitles/wiki/XMLRPC
        results = subdb.process('/burn/The.Office.US.S07E08.Viewing.Party.HDTV.XviD-FQM.[VTV].avi', None)
        print results
        assert len(results) > 0, 'No result found for Night.Watch.2004.CD1.DVDRiP.XViD-FiCO.avi by movie hash'

class OpenSubtitlesTestCaseFileName(unittest.TestCase):
    def runTest(self):
        import OpenSubtitles
        subdb = OpenSubtitles.OpenSubtitles()
        # movie hash if for night watch : http://trac.opensubtitles.org/projects/opensubtitles/wiki/XMLRPC
        filenames = []
        #filename = 'Dexter.S04E01.HDTV.XviD-NoTV'
        #filename = 'The.Office.US.S06E01.HDTV.XviD-2HD.[VTV]'
        #filenames.append('Marley & Me.2008-L33t-DvDRiP.DivX.NoRaR')
        filenames.append("Twilight[2008]DvDrip-aXXo")
        
        for filename in filenames:
            results = subdb.query(filename)
        
            if results :
                print "Found %s results" %len(results)
                print "Showing first for unit test::"
                print results[0]
            assert len(results) > 0, 'No result found for %s' %filename

class SubtitleSourceTestCase(unittest.TestCase):
    def runTest(self):
        import SubtitleSource
        subdb = SubtitleSource.SubtitleSource()
        results = subdb.query("PrisM-Inception.2010")
        print results
        assert len(results) > 0, "No result could be found for Heroes 3X9 and no languages"

class SubtitleSourceTestCase2(unittest.TestCase):
    def runTest(self):
        import SubtitleSource
        subdb = SubtitleSource.SubtitleSource()
        results = subdb.query("Transformers.Revenge.of.the.Fallen.TS.XviD-DEViSE", ["en"])
        assert len(results) > 0, "No result could be found for Transformer 2 in English"

class SubtitleSourceTestCase3(unittest.TestCase):
    def runTest(self):
        import SubtitleSource
        subdb = SubtitleSource.SubtitleSource()
        results = subdb.query("Transformers.Revenge.of.the.Fallen.TS.XviD-DEViSE", ["en", "fi"])
        assert len(results) > 0, "No result could be found for Transformer 2 in English or Finnish"

class SubtitleSourceTestCase3(unittest.TestCase):
    def runTest(self):
        import Podnapisi
        subdb = Podnapisi.Podnapisi()
        results = subdb.query("My.Name.is.Earl.S04E24.HDTV.XviD-LOL", ["en"])
        assert len(results) > 0, "No result could be found for My.Name.is.Earl.S04E24.HDTV.XviD-LOL in any languages"

class SubSceneTestCase(unittest.TestCase):
    def runTest(self):
        import SubScene
        subdb = SubScene.SubScene()
        results = subdb.query("Dexter.S04E01.HDTV.XviD-NoTV")
        print results
        assert len(results) > 0, "No result could be found for Dexter.S04E01.HDTV.XviD-NoTV and no languages"

class SubSceneStep2TestCase(unittest.TestCase):
    def runTest(self):
        import SubScene
        subdb = SubScene.SubScene()
        subtitle = {'release': u'Dexter.S04E01.HDTV.XviD-NoTV', 'lang': 'ar', 'link': None, 'page': u'http://subscene.com/arabic/Dexter-Fourth-Season/subtitle-263042.aspx', 'filename' : '/tmp/testSubScene.avi'}
        srtfilename = subdb.createFile(subtitle)
        assert srtfilename != None, "Could download a subtitle"

class SubSceneStep3TestCase(unittest.TestCase):
    def runTest(self):
        import SubScene
        subdb = SubScene.SubScene()
        #suburl = "http://subscene.com/arabic/Dexter-Fourth-Season/subtitle-263042-dlpath-78348/zip.zipx"
        suburl = "http://subscene.com/arabic/Dexter-Fourth-Season/subtitle-263042.aspx"
        localFile = "/tmp/testSubScene.zip"
        subdb.downloadFile(suburl, localFile)
        print os.path.getsize(localFile)
        assert srtfilename != None, "Could download a subtitle"

class Podnapisi2TestCase(unittest.TestCase):
    def runTest(self):
        import Podnapisi2
        subdb = Podnapisi2.Podnapisi()
        results = subdb.process("/burn/Entourage.S07E01.Stunted.HDTV.XviD-FQM.avi", None)
        print results
        assert len(results) > 5, "Not enough result could be found for The.Office.US.S06E01.HDTV.XviD-2HD and no languages (expected 6)"
'''
class PodnapisiTestCase(unittest.TestCase):
    def runTest(self):
        import Podnapisi
        subdb = Podnapisi.Podnapisi(None, None)
        results = subdb.process("Game.Of.Thrones.S01E10.mkv", None)
        assert len(results) > 5, "Not enough result could be found for Community.S01E01.Pilot.HDTV.XviD-FQM.avi and no languages (expected 6)"
        
        # Download the first
        # Expected by the prog
        results[0]["filename"] = "/tmp/testPodnapisi.avi"
        subdb.createFile(results[0])
        #TODO Check that /tmp/testPodnapisi.srt exists
'''
class PodnapisiTestCaseMultiPart(unittest.TestCase):
    def runTest(self):
        import Podnapisi
        subdb = Podnapisi.Podnapisi()
        results = subdb.process("/tmp/Catwoman.CAM-NOX-CD1.avi", None)
        assert len(results) > 0
        results = subdb.process("/tmp/Catwoman.CAM-NOX-CD2.avi", None)
        assert len(results) > 0

class PodnapisiTestCaseTwoSerbian(unittest.TestCase):
    def runTest(self):
        import Podnapisi
        subdb = Podnapisi.Podnapisi()
        results = subdb.process("Twilight[2008]DvDrip-aXXo", None)
        assert len(results) > 0, "Not enough result could be found"

class TvSubtitlesTestCase(unittest.TestCase):
    def runTest(self):
        import TvSubtitles
        subdb = TvSubtitles.TvSubtitles()
        fname = "The.Big.Bang.Theory.S03E15.The.Large.Hadron.Collision.HDTV.XviD-FQM"
        guessedData = subdb.guessFileData(fname)
        subs = subdb.query(guessedData['name'], guessedData['season'], guessedData['episode'], guessedData['teams'], ['en'])
        for s in subs:
            print "Sub : %s" %s

class BierDopjeTestCase(unittest.TestCase):
    def runTest(self):
        import BierDopje
        subdb = BierDopje.BierDopje()
        video = "The.Office.US.S07E08.Viewing.Party.HDTV.XviD-FQM.[VTV]"
        #video = "Dexter.S04E01.HDTV.XviD-NoTV"
        #video = "the.walking.dead.s01e02.720p.hdtv.x264-ctu"
        video = "the.mentalist.s01e06.720p.hdtv.x264-ctu"
        results = subdb.query(video)
        print results
        assert len(results) > 0, "No result could be found for %s and no languages" %( video )
'''

if __name__ == "__main__":
    unittest.main()
