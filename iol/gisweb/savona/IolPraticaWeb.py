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
from zope.component import getUtility,queryUtility
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
        self.tipo_app = self.document.getItem(config.APP_FIELD,config.APP_FIELD_DEFAULT_VALUE)
        #if not service.endswith('?wsdl'):
        #    service = "%s?wsdl" %service

        self.client = Client(service)

    def _convertTipoPratica(self):
        pass 

    def aggiungi_pratica(self):
        client = self.client
        doc = self.document

        utils = queryUtility(IIolPraticaWeb,name=self.tipo_app, default=config.APP_FIELD_DEFAULT_VALUE)
        if not 'getProcedimento' in dir(utils):
            utils = getUtility(IIolPraticaWeb,config.APP_FIELD_DEFAULT_VALUE)

        pr = utils.getProcedimento(self)

        utils = queryUtility(IIolPraticaWeb,name=self.tipo_app, default=config.APP_FIELD_DEFAULT_VALUE)
        if not 'getSoggetti' in dir(utils):
            utils = getUtility(IIolPraticaWeb,config.APP_FIELD_DEFAULT_VALUE)
        soggetti = utils.getSoggetti(self)

        utils = queryUtility(IIolPraticaWeb,name=self.tipo_app, default=config.APP_FIELD_DEFAULT_VALUE)
        if not 'getIndirizzi' in dir(utils):
            utils = getUtility(IIolPraticaWeb,config.APP_FIELD_DEFAULT_VALUE)

        indirizzi = utils.getIndirizzi(self)

        res = client.service.aggiungiPratica(pr,soggetti,indirizzi)

        #####################################

        message = list()
        pratica = res['pratica']
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
            el.foglio = i[1]
            el.mappale = i[2]

            r = client.service.aggiungiCatastoTerreni(pratica,el)
            if r['success'] == -1:
                message.append("Errori nell'inserimento dei dati del catasto terreni")

        cu = doc.getItem('elenco_nceu',[])
        for i in cu:
            el = client.factory.create('particella')
            el.foglio = i[1]
            el.mappale = i[2]
            el.sub = i[3]
            r = client.service.aggiungiCatastoUrbano(pratica,el)
            if r['success'] == -1:
                message.append("Errori nell'inserimento dei dati del catasto urbano")

        return dict(success = res['success'],numero=res['numero_pratica'], messages = message)
        #sogg = client.factory.create('soggetto')
        #
