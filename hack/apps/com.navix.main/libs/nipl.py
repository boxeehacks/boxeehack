from default import *
from tools import *

#Module specific Imports
import traceback
import urllib

from urllib import quote_plus

######
### NIPL
######
### Interprets the NIPL scripts from NAVI servers
######

### Class to process navi-x NIPL scripts
class NIPL:
    ### Init
    def __init__(self, app, item, phase, datalist):
        Log(app, 'NAVI-X NIPL: Init.... phase ' + str(phase))

        #init vars
        self.__app__ = app
        self.__item__ = item

        self.s_url = item.path
        self.s_method = 'get'
        self.s_action = 'read'
        self.s_agent = app.url_useragent
        self.s_referer = ''
        self.s_cookie = ''
        self.s_postdata = ''
        self.s_headers = {}

        self.url = item.path
        self.swfplayer = item.swfplayer
        self.playpath = item.playpath
        self.agent = app.url_useragent
        self.app = ''
        self.pageurl = item.pageurl
        self.swfVfy = ''
        self.referer = ''
        self.player = item.player

        self.verbose = 0
        self.regex = ''
        self.nomatch = '0'
        self.phase = phase
        self.cacheable = 0
        self.nookies = {}
        self.nookie_expires = '0'
        self.htmRaw = ''
        self.cookies = {}
        self.headers = {}
        self.geturl = ''

        self.__matchresults__ = {}

        #Set main NIPL function to call key->function
        self.__functions__ = {
                'concat':self.concat,
                'debug':self.debug,
                'print':self._print,
                'error':self.error,
                'match':self.match,
                'play':self.play,
                'replace':self.replace,
                'report':self.report,
                'report_val':self.report_val,
                'scrape':self.scrape,
                'unescape':self.unescape
                }

        #Set main NIPL operators to call key->function
        self.__operators__ = {
                'if':self._if,
                'elseif': self._elseif,
                'else': self._else,
                'endif':self._endif
        }

        #Set list of collectables
        self.__collectable__ = ['s_headers','headers','cookies', 'nookies']

        self.__cache__ = list(datalist)
        if self.phase == 0: datalist.pop(0)
        self.__datalist__ = datalist

        self.getNookie()

    ### NOOKIE FUNCTIONS
    # Functions for data retreival from navi db
    def getNookie(self):
        id = "".join(['nookie', self.__item__.processor, '?url=', quote_plus(self.__item__.path)])

        if self.nookie_expires == '0':
            period = 16070400
        elif len(self.nookie_expires) < 4:
            try:
                if 'h' in self.nookie_expires: period = int(self.nookie_expires.replace('h', '').replace(' ',''))*3600
                elif 'd' in self.nookie_expires: period = int(self.nookie_expires.replace('d', '').replace(' ',''))*3600*24
                elif 'm' in self.nookie_expires: period = int(self.nookie_expires.replace('m', '').replace(' ',''))*60
                else: period = 86400
            except: period = 86400
        else:
            period = 86400

        data = self.__app__.storage.get(id, age = period, persistent = True)
        if data:
            self.nookies = data

    def saveNookie(self):
        if len(self.nookies) > 0:
            id = "".join(['nookie', self.__item__.processor, '?url=', quote_plus(self.__item__.path)])
            self.__app__.storage.set(id, self.nookies, persistent = True)

    def saveCache(self):
        if self.cacheable > 1:
            id = "".join([__item__.processor, '?url=', quote_plus(__item__.path)])
            self.__app__.storage.set(id, self.__cache__)

    ### MAIN INTERPRETER FUNCTION
    ### Main Process functions, iterates the NIPL script
    def process(self):
        functions = self.__functions__.keys()
        operators = self.__operators__.keys()

        self.skip = False
        self._pass = False
        self._error = False

        for line in self.__datalist__:
            if self._pass: continue
            if self.verbose > 1 or self.__app__.debug:
                if not self.skip: print 'NAVI-X NIPL: EXEC Line - ' + str(line)
                else: print 'NAVI-X NIPL: SKIP Line - ' + str(line)

            try:
                linelist = line.split(' ')
                if not self.skip:
                    function = [key for key in functions if key == linelist[0]]
                    if len(function) > 0:
                        line = line.replace(function[0], '')
                        if line[:1] == " ": line = line[1:]
                        if len(line) < 2: self.__functions__[function[0]]()
                        else: self.__functions__[function[0]](line)
                        continue

                operator = [key for key in operators if line.startswith(key, 0, 7)]
                if len(operator) > 0:
                    line = line.replace(operator[0], '')
                    if line[:1] == " ": line = line[1:]
                    self.__operators__[operator[0]](line)
                    continue

                self.setValue(line=line)
            except: Log(self.__app__, traceback.format_exc() )

        self.saveCache()
        self.saveNookie()

        if self._error:
            self.__item__.path = ''
            self.__item__.error = self._error

        return self.__item__

    ### NIPL FUNCTIONS
    #String operations NIPL Script
    def checkString(self, line):
        if line[:1] == "'": return True
        elif line[:2] == "\'": return True
        else: return False

    def getValue(self, var):
        varsplit = var.split('.')
        if self.checkString(var): return var[1:]
        elif len(varsplit) > 1:
            if varsplit[0] in self.__collectable__:
                try: return str(vars(self)[varsplit[0]][varsplit[1]])
                except: return ''
            else: return ''
        else:
            try: return str(vars(self)[var])
            except: return ''

    def setValue(self, **kwargs):
        if kwargs.get('line', False):
            splitdata = kwargs.get('line').split('=')
            if not len(splitdata) > 1: return
            var = splitdata.pop(0)
            value = self.getValue("=".join(splitdata))
        elif kwargs.get('var', False):
            var = kwargs.get('var')
            value = kwargs.get('value', '')
        else: return

        varsplit = var.split('.')
        if len(varsplit) > 1:
            if varsplit[0] in self.__collectable__:
                vars(self)[varsplit[0]][varsplit[1]] = value
        else:
            if var in ['verbose', 'cacheable', 'phase', 'verbose']:
                if value.isdigit(): vars(self)[var] = int(value)
            else: vars(self)[var] = value

    #Main NIPL EXEC functions
    def concat(self, line):
        splitdata = line.split(' ', 1)
        if len(splitdata) > 1:
            try: var1 = vars(self)[splitdata[0]]
            except: var1 = ''
            var2 = self.getValue(splitdata[1])
            self.setValue(var=splitdata[0], value="".join([var1, var2]))

    def debug(self, line):
        if self.verbose > 0:
            var1 = self.getValue(line)
            try: print " ".join(['NAVI-X NIPL: ', str(line), '=', str(var1)])
            except: pass

    def _print(self, line):
        var1 = self.getValue(line)
        print " ".join(['NAVI-X NIPL: ', str(line), '=', str(var1)])


    def error(self, line):
        self._pass = True
        var1 = self.getValue(line)
        self._error = str(var1)
        print 'NAVI-X NIPL: Error! %s' %str(var1)


    def match(self, line):
        var1 = self.getValue(line)
        self._match(var1)

    def _match(self, var):
        try: results = re.compile(self.regex).search(var).groups()
        except: results = []

        self.__matchresults__ = {}
        if len(results):
            for i in xrange(len(results)):
                var = "".join(['v', str(i+1)])
                vars(self)[var] = results[i]
                self.__matchresults__[var] = results[i]

                self._printv(0, 'Match Result - ' + str(var) + ' '+ str(results[i]))
                self.nomatch = '0'
        else:
            for i in xrange(10):
                var = "".join(['v', str(i+1)])
                del vars(self)[var]
            self.nomatch = '1'

    def play(self):
        self.playurl = str(self.url)
        parse = ['playurl','swfplayer','playpath','agent','app','pageurl','swfVfy', 'referer', 'player']
        self._printv(0, 'PLAY Variables')
        for item in parse:
            self._printv(0, str(item) + ' - ' + str(vars(self)[item]))
            self.__item__.setVar(item, vars(self)[item])
        self._pass = True

    def replace(self, line):
        splitdata = line.split(' ')
        if len(splitdata) > 1:
            var1 = self.getValue(splitdata[0])
            var2 = self.getValue(splitdata[1])
            try: self.setValue(var=splitdata[0], value=re.sub(self.regex, var2, var1))
            except: self.setValue(var=splitdata[0], value=var1)

    def report(self):
        vars = ["".join([key,'=',quote_plus(item)]) for (key, item) in self.__matchresults__.items()]
        vars.append("".join(['phase=', str(self.phase+1)]))
        url = "".join([self.__item__.processor, '?', "&".join(vars) ])

        self._printv(0, 'Report with url= '+url)
        rawdata = urlopen(self.__app__, str(url), {'cookie':'version='+str(self.__app__.navi_version)+'.'+str(self.__app__.navi_sub_version)+'; platform='+self.__app__.os})

        htmRaw = rawdata['content'].read()
        htmRaw = re.sub('(?m)\r[#].+|\n[#].+|^\s+|\s+$', '\r\n', htmRaw)    #remove comments and tabs
        htmRaw = re.sub('[\r\n]+', '\n', htmRaw)                            #remove empty lines
        datalist = htmRaw.replace('\t','').split('\n')
        rawdata['content'].close()

        self._pass = True
        nipl = NIPL(self.__app__, self.__item__, self.phase+1, datalist)
        return nipl.process()

    def report_val(self, line):
        splitdata = line.split('=')
        if len(splitdata) > 1:
            var = splitdata.pop(0)
            value = self.getValue("".join(splitdata))
            self.__matchresults__[var] = value

    def _printv(self, i, string):
        if self.verbose >= i or self.__app__.debug:
            print 'NAVI-X NIPL: %s' % string

    def scrape(self):
        url_vars = {
            'agent' : self.s_agent,
            'referer': self.s_referer,
            'cookie': self.s_cookie,
            'method': self.s_method,
            'postdata':self.s_postdata,
            'headers': self.s_headers,
        }

        for i in xrange(5):
            try: del vars(self)["".join(['v', str(i+1)])]
            except: pass

        self._printv(2, 'Scrape - ' + self.s_url)
        self._printv(2, 'Regex - ' + self.regex)
        self._printv(2, 'Params - ' + str(url_vars))

        rawdata = urlopen(self.__app__, self.s_url, url_vars)
        if self.s_action == 'read':
            self.htmRaw = rawdata['content'].read()
            rawdata['content'].close()

            self._printv(1, 'Scrape htmRaw - ' + self.htmRaw)
            self._match(self.htmRaw)

        elif self.s_action == 'headers':
            self.htmRaw = ''
        elif self.s_action == 'geturl':
            self.htmRaw = ''
            self.v1 = rawdata['geturl']

        self.cookies = rawdata['cookies']
        self.headers = rawdata['headers']
        self.geturl = rawdata['geturl']

    def unescape(self, line):
        line = line.replace(' ','')
        var2 = self.getValue(line)
        var2 = urllib.unquote_plus(var2)
        self.setValue(var=line, value=var2)

    ### OPERATOR FUNCTIONS
    #Operators functions from NIPL Script
    def _if(self, line):
        operators = ['<', '<=', '=','==', '>=', '>', '!=', '<>']
        match = [operator for operator in operators if operator in line]

        if len(match) > 0:
            linedata = line.split(match[0])
            var1 = self.getValue(linedata[0])
            var2 = self.getValue(linedata[1])
            operator = match[0]
            self._printv(2, " ".join(['IF CHECK', '"'+str(linedata[0])+'"', match[0], '"'+str(linedata[1])+'" ,' , 'Values', '"'+ str(var1)+ '"', match[0],'"'+str(var2)+'"']))
            if operator == '<':
                if len(var1) < len(var2): self.skip = False
                else: self.skip = True
            elif operator == '<=':
                if len(var1) <= len(var2): self.skip = False
                else: self.skip = True
            elif operator == '=':
                if var1 == var2: self.skip = False
                else: self.skip = True
            elif operator == '==':
                if var1 == var2: self.skip = False
                else: self.skip = True
            elif operator == '=>':
                if len(var1) >= len(var2): self.skip = False
                else: self.skip = True
            elif operator == '>':
                if len(var1) > len(var2): self.skip = False
                else: self.skip = True
            elif operator == '!=':
                if var1 != var2: self.skip = False
                else: self.skip = True
            elif operator == '<>':
                if var1 != var2: self.skip = False
                else: self.skip = True
        else:
            value = self.getValue(line.replace(' ',''))
            if value != '' and value != '0':
                self.skip = False
            else:
                self.skip = True
        self._printv(2, 'IF CHECK RESULT - ' + str(not self.skip))

    def _elseif(self, line):
        if self.skip == True:
            self._if(line)
            self._printv(2, 'ELSEIF')

    def _else(self, line):
        if self.skip == True:
            self.skip = False
            self._printv(2, 'ELSE')
        else: self.skip = True

    def _endif(self, line):
        self.skip = False
        self._printv(2, 'ENDIF')
