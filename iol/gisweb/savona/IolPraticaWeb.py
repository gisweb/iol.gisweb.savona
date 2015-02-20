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
        #if not service.endswith('?wsdl'):
        #    service = "%s?wsdl" %service

        self.client = Client(service)

    def _convertTipoPratica(self):
        pass 

    def aggiungi_pratica(self):
        client = self.client
        doc = self.document
        pr = client.factory.create('procedimento')
        if doc.getItem('data_inizio_lavori_opt','scia_data_inizio_presentazione'):
            pr['tipo'] = 21100
        else:
            pr['tipo'] = 21200
        pr['oggetto'] = doc.getItem('descrizione_intervento','')
        pr['protocollo'] = doc.getItem('numero_protocollo','')
        pr['data_prot'] = doc.getItem('data_prot',DateTime()).strftime("%d/%m/%Y")
        pr['data_presentazione'] = doc.getItem('data_presentazione',DateTime().strftime("%d/%m/%Y"))
        pr['online'] = 1
        pr['resp_proc'] = 24
        pr['data_resp'] = DateTime().strftime("%d/%m/%Y")
        res = client.service.aggiungiPratica(pr)
        pratica=res['pratica']
        indirizzi = doc.getItem('elenco_civici',[])
        for i in indirizzi:
            ind = client.factory.create('indirizzo')
            ind.via = i[0]
            ind.civico = i[1]
            ind.interno = i[2]
            client.service.aggiungiIndirizzo(pratica,ind)

        ct = doc.getItem('elenco_nct',[])
        for i in ct:
            el = client.factory.create('particella')
            el.sezione = i[1]
            el.mappale = i[2]

            res = client.service.aggiungiCatastoTerreni(pratica,el)

        cu = doc.getItem('elenco_nceu',[])
        for i in cu:
            el = client.factory.create('particella')
            el.sezione = i[1]
            el.mappale = i[2]
            el.sub = i[3]
            client.service.aggiungiCatastoUrbano(pratica,el)

        return res
        #sogg = client.factory.create('soggetto')
        #
