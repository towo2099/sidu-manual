# Create your views here.
import os.path

from djinn.django.http import HttpResponse, HttpResponsePermanentRedirect
from msource.session import Session
from webbasic.menu import Menu
from webbasic.htmlsnippets import HTMLSnippets
from msource.searchpage import SearchPage
from msource.languagepage import LanguagePage
from msource.globalpage import GlobalPage
from msource.checkpage import CheckPage
from msource.expertpage import ExpertPage
from util.util import Util

def getSession(request):
    homeDir = request.documentRoot if hasattr(request, "documentRoot") else None
    session = Session(request, homeDir)
    # store globalpage for getMenu() and handlePage()
    session._globalPage = GlobalPage(session, request.COOKIES)
    return session

def getFields(request):
    fields = request.GET
    if len(fields) < len(request.POST):
        fields = request.POST
    return fields
    
def getMenu(session, request):
    fields = getFields(request)
    expertMode = session._globalPage.getField("expert")
    isExtended = expertMode == "T"
    menu = Menu(session, 'menu', True, fields, isExtended)
    menu.read()
    snippets = HTMLSnippets(session)
    snippets.read('menu')
    menuHtml = menu.buildHtml(snippets)
    return menuHtml

def handlePage(page, request, session):
    page._globalPage = session._globalPage
    
    htmlMenu = getMenu(session, request)
    fields = getFields(request)
    pageResult = page.handle(htmlMenu, fields, request.COOKIES)
    if pageResult._body != None:
        rc = HttpResponse(pageResult._body)
    else:
        url = pageResult._url
        session.trace(u'redirect to {:s} [{:s}]'.format(
            Util.toUnicode(url), pageResult._caller))
        absUrl = session.buildAbsUrl(url)
        rc = HttpResponsePermanentRedirect(absUrl)
    cookies = request.COOKIES
    for cookie in cookies:
        rc.set_cookie(cookie, session.toUnicode(cookies[cookie]))
    return rc
    
def index(request):
    session = getSession(request)
    absUrl = session.buildAbsUrl('/welcome')
    rc = HttpResponsePermanentRedirect(absUrl) 
    return rc

def expert(request):
    session = getSession(request)
    rc = handlePage(ExpertPage(session), request, session)
    return rc

def search(request):
    session = getSession(request)
    rc = handlePage(SearchPage(session), request, session)
    return rc

def check(request):
    session = getSession(request)
    rc = handlePage(CheckPage(session), request, session)
    return rc

def language(request):
    session = getSession(request)
    rc = handlePage(LanguagePage(session), request, session)
    return rc

def staticPage(request, page = None):
    if page == None:
        page = request.META["PATH_INFO"]
        if page.startswith("/"):
            page = page[1:]
    session = getSession(request)
    menuHtml = getMenu(session, request)
    body = session.buildStaticPage(page, menuHtml)
    rc = HttpResponse(body)
    return rc

def staticFiles(request):
    url = request.META["PATH_INFO"]
    documentRoot = request.META["DOCUMENT_ROOT"]
    fn = documentRoot + url
    if not os.path.exists(fn):
        rc = ["File not found: " + fn]
    else:
        rc = ["File found: " + fn]
    return rc
    
def home(request):
    session = getSession(request)
    homePage = session.getConfigOrNoneWithoutLanguage('.home.page')
    if homePage == None:
        homePage = 'welcome'
    absUrl = session.buildAbsUrl(homePage)
    rc = HttpResponsePermanentRedirect(absUrl) 
    return rc
