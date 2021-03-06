'''
Created on 10.03.2013

@author: hm
'''
import re, os.path

from webbasic.page import Page
from pyygle_src.sqlite3db import SqLite3Db
from pyygle_src.searchengine import SearchEngine
from pyygle_src.pyygle import Logger

class SearchPage(Page):
    '''
    Handles the search page
    '''


    def __init__(self, session):
        '''
        Constructor.
        @param session: the session info
        '''
        Page.__init__(self, 'search', session)
        self._searchResults = None
        self._rexprDocument = re.compile(r'(.*?)[-_][a-z]{2}(-[a-z]{2})?\.htm$')

    def defineFields(self):
        '''Defines the fields of the page.
        This allows a generic handling of the fields.
        '''
        self.addField('phrases')
        self.addField('help', 'T')

    def changeContent(self, body):
        '''Changes the template in a customized way.
        @param body: the HTML code of the page
        @return: the modified body
        '''
        if self._searchResults == None:
            code = ''
        else:
            isEmpty = self._searchResults == ''
            snippet = 'EMPTY_RESULT' if isEmpty else 'RESULT_LIST'
            code = self._snippets.get(snippet)
            if not isEmpty and self._searchResults != None:
                code = code.replace('{{search.results}}', self._searchResults)
        if self.getField('help') == 'T':
            helpBody = self._snippets.get('HELP')
            helpButton = self._snippets.get('HELP_OFF')
        else:
            helpBody = ''
            helpButton = self._snippets.get('HELP_ON')
            
        body = body.replace('{{HELP}}', helpBody)
        body = body.replace('{{HELP_BUTTON}}', helpButton)
                
        body = body.replace('{{RESULT}}', code)
        return body
    
    def buildUrl(self, docName, anchor):
        '''Builds an URL from a document name and (optionally) an anchor.
        @param docName: the filename containing the source
        @param anchor: the anchor of the hit
        @param: a link to the hit
        '''
        if anchor == None:
            anchor = ''
        elif anchor != '':
            anchor = '#' + anchor
        docName = os.path.basename(docName)
        matcher = self._rexprDocument.match(docName)
        if matcher == None:
            link = '/static/{:s}/{:s}.htm{:s}'.format(
                self._session._language, docName, self._session._language, anchor)
        else:
            link = matcher.group(1) + anchor
        return link

    def doSearch(self, phrases):
        '''Runs a search and stores the result in _searchResults
        @param phrases: the search phrases as a list
        '''
        if self._session._language =='':
            self._session._language = 'de'
        dbName =  '{:s}data/sidu-manual_{:s}.db'.format(
            self._session._homeDir, self._session._language)
        logger = Logger(None)
        db = SqLite3Db(dbName, logger)
        engine = SearchEngine(db)
        url = '!search'
        if len(phrases) <= 0:
            self._searchResults = None
        else:
            self._searchResults = engine.search(phrases, url, False, self)
        db.close()
        
    def splitPhrases(self, source):
        '''Split a string into words and phrases.
        A phrase is a text delimited with "".
        @param: the text to split
        @return: a list of words and phrases
        '''
        rc = []
        end = 0
        rexpr = re.compile(r'\s+')
        while end >= 0:
            start = source.find('"', end)
            start2 = source.find("'", end)
            if start2 >= 0 and start2 < start:
                start = start2
                delim = "'"
            else:
                delim = '"'
            if start < 0:
                src = source[end:].strip()
                if src != '':
                    rc.extend(rexpr.split(src))
                break
            else:
                src = source[end:start].strip()
                if src != '':
                    rc.extend(rexpr.split(src))
                end = source.find(delim, start+1)
                if end < 0:
                    rc.append(source[start:] + '"')
                else:
                    phrase = '=' + source[start+1:end]
                    rc.append(phrase)
                    end += 1
        return rc   
    def handleButton(self, button):
        '''Do the actions after a button has been pushed.
        @param button: the name of the pushed button
        @return: None: OK<br>
                otherwise: a redirect info (PageResult)
        '''
        pageResult = None
        self._searchResults = None
        if button == 'button_search':
            phrases = self._pageData.get('phrases')
            if phrases != None:
                phrases = self.splitPhrases(phrases)
                self.doSearch(phrases)
        elif button == 'button_help_on':
            self.putField('help', 'T')
        elif button == 'button_help_off':
            self.putField('help', 'F')
        else:
            self.buttonError(button)
            
        return pageResult
    