from default import *
from tools import *

import threading
import stat
from urlgrabber.grabber import URLGrabber
from urlgrabber.progress import BaseMeter, format_time, format_number

class Navi_DOWNLOAD:
    def __init__(self, app):
        #Init vars
        self.app    = app
        self.active = False
        self.url    = ''
        self.saveto = ''
        self.chunk_size = 8192

    def start(self, url, filepath, infodata, infopath, filename):
        if self.active:
            return
        
        self.active = True

        self.url        = url
        self.filename   = checkUTF8(filename)
        self.infodata   = infodata
        self.infopath   = infopath
        self.file       = filepath

        #Start Download Thread
        t = threading.Thread(name='Downloader', target=self.run, args=())
        t.start()

    def run(self):
        #Check if file exists
        if os.path.isfile(self.file):
            os.chmod(self.file, stat.S_IWUSR)
            os.remove(self.file)

        ##Init url/path pointers
        #response     = urllib2.urlopen(self.url)
        #total_size   = response.info().getheader('Content-Length').strip()
        #self.total_size   = int(total_size)

        #freespace
        #freespace = get_free_space(self.app, path)

        #check if enough freespace
        #if self.freespace < total_size and self.freespace != 0:
        #    self.app.gui.ShowDialogNotification('Not enough freespace to download the item')
        #    self.active = False
        #    return

        self.app.gui.SetVisible(4000, True)
        progress = TextMeter(self.app)
        try:
            Log(self.app, 'Download started' )
            g = URLGrabber(reget='simple')
            g.urlgrab(self.url, filename=self.file, reget='simple', progress_obj=progress, text=self.filename)

            #Create info file as json
            json_dumps(self.infodata, self.infopath)
            self.app.gui.ShowDialogNotification('Download Complete')
        except:
            Log(self.app, traceback.format_exc() )
            self.app.gui.ShowDialogNotification('Error during download')

        self.app.gui.SetVisible(4000, False)
        self.active = False
        Log(self.app, 'Download finished' )

class TextMeter(BaseMeter):
    def __init__(self, app, fo=sys.stderr):
        BaseMeter.__init__(self)
        self.fo  = fo
        self.app = app
        self.i   = 100

    def _do_update(self, amount_read, now=None):
        pass

    def _do_end(self, amount_read, now=None):
        if self.i%100==0:
            etime = self.re.elapsed_time()
            fetime = format_time(etime)
            fread = format_number(amount_read)
            #self.size = None
            if self.text is not None:
                text = self.text
            else:
                text = self.basename
            if self.size is None:
                #out = '\r%-60.60s    %5sB %s ' % (text, fread, fetime)
                try:
                    self.app.gui.SetVisible(4000, True)
                    self.app.gui.SetTexture(4001, 'download/download-%s.png' % 0 )
                    self.app.gui.SetLabel(4002, '%3i%%  %5sB  %s' % (frac*100, fread, fetime))
                    self.app.gui.SetLabel(4005, 'Downloading: %s' % text  )
                    Log(self.app, '\r%-60.60s    %5sB %s ' % (text, fread, fetime))
                except:
                    pass
            else:
                rtime  = self.re.remaining_time()
                frtime = format_time(rtime)
                speed  = int(self.re.average_rate()) / 1024
                frac   = self.re.fraction_read()
                bar    = '='*int(25 * frac)

                #out = '\r%-25.25s %3i%% |%-25.25s| %5sB %8s ETA ' % (text, frac*100, bar, fread, frtime)
                try:
                    self.app.gui.SetVisible(4000, True)
                    self.app.gui.SetTexture(4001, 'download/download-%s.png' % int(round( frac*100, -1)) )
                    self.app.gui.SetLabel(4002, '%3i%%  %5sB  %skbps  %s ETA' % (frac*100, fread, speed, frtime))
                    self.app.gui.SetLabel(4005, 'Downloading: %s' % text  )
                    Log(self.app, '\r%-25.25s %3i%% |%-25.25s| %5sB %8s ETA ' % (text, frac*100, bar, fread, frtime))
                except:
                    pass
        self.i += 1
        