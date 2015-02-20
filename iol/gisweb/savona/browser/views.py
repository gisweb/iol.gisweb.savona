from Products.CMFCore.utils import getToolByName
from plone.dexterity.browser.view import DefaultView
from plone import api

from zope.component import getUtility
from iol.gisweb.savona.IolApp import IolApp
from iol.gisweb.savona.IolPraticaWeb import IolWSPraticaWeb


class inviaPW(object):

    def __init__(self,context,request):
        self.context = context
        self.request = request

    def __call__(self):
        doc = self.aq_parent
        url = "http://webservice.gisweb.it/wspraticaweb/savona.wsPraticaweb.php?wsdl&test=4"
        wsDoc = IolWSPraticaWeb(doc)
        res = wsDoc.aggiungi_pratica()
        return res