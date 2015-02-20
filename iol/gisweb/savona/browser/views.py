from Products.CMFCore.utils import getToolByName
from plone.dexterity.browser.view import DefaultView
from plone import api

from zope.component import getUtility
from iol.gisweb.savona.IolApp import IolApp
from iol.gisweb.savona.IolPraticaWeb import IolWSPraticaWeb
import random

class inviaPW(object):

    def __init__(self,context,request):
        self.context = context
        self.request = request

    def __call__(self):
        doc = self.aq_parent
        url = "http://webservice.gisweb.it/wspraticaweb/savona.wsPraticaweb.php?wsdl&test=%d" %random.randint(1,100000)
        wsDoc = IolWSPraticaWeb(doc,url)
        res = wsDoc.aggiungi_pratica()
        wftool = getToolByName(doc,'portal_workflow')
        wftool.doActionFor(doc,'i1_protocolla')
        doc.REQUEST.RESPONSE.redirect(doc.absolute_url())
        #doc.REQUEST.RESPONSE.redirect(doc.absolute_url())
        return res