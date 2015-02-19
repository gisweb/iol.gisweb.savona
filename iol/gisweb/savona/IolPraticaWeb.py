# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
from zope.interface import Interface, implements, Attribute
from zope.component import adapts
from plone import api
from AccessControl import ClassSecurityInfo
from App.class_init import InitializeClass
from Products.CMFPlomino.interfaces import IPlominoDocument, IPlominoForm
from zope.component import getGlobalSiteManager
from iol.gisweb.utils import config
from gisweb.iol.permissions import IOL_READ_PERMISSION, IOL_EDIT_PERMISSION, IOL_REMOVE_PERMISSION
from zope.component import getUtility
from .interfaces import IIolPraticaWeb
from suds.client import Client

class IolWSPraticaWeb(object):
    implements(IIolPraticaWeb)
    adapts(IPlominoForm,IPlominoDocument)
    security = ClassSecurityInfo()
    security.declareObjectPublic()

    def __init__(self,obj,service):
        self.document = obj
        self.service = service
        if not service.endswith('?wsdl'):
            service = "%s?wsdl" %service

        self.client = Client(service)

    def _convertTipoPratica(self):
        pass 

    def aggiungi_pratica(self, pratica,soggetti=[],indirizzi=[],particelle_terreni=[],particelle_urbano=[],pareri=[],allegati=[]):
        client = self.client
        pr = client.factory.create('pratica')

        sogg = client.factory.create('soggetto')
        ind = client.factory.create('indirizzo')
