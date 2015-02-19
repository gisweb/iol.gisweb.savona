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
from DateTime import DateTime


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

    def aggiungi_pratica(self, pratica):
        client = self.client
        doc = self.document
        pr = client.factory.create('procedimento')
        if doc.getItem('data_inizio_lavori_opt','scia_data_inizio_presentazione'):
            pr['tipo'] = 21100
        else:
            pr['tipo'] = 21200
        pr['oggetto'] = doc.getItem('descrizione_intervento','')
        pr['protocollo'] = doc.getItem('protocollo','')
        pr['data_prot'] = doc.getItem('data_prot',DateTime()).strftime("%d/%m/%Y")
        pr['data_presentazione'] = doc.getItem('data_presentazione',DateTime()).strftime("%d/%m/%Y")

        #sogg = client.factory.create('soggetto')
        #ind = client.factory.create('indirizzo')
