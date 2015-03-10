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

        self.client = Client(service)

    def aggiungi_pratica(self):
        client = self.client
        doc = self.document

        utils = queryUtility(IIolPraticaWeb, name=self.tipo_app, default=config.APP_FIELD_DEFAULT_VALUE)
        if not 'getProcedimento' in dir(utils):
            utils = getUtility(IIolPraticaWeb, config.APP_FIELD_DEFAULT_VALUE)

        pr = utils.getProcedimento(self)

        utils = queryUtility(IIolPraticaWeb, name=self.tipo_app, default=config.APP_FIELD_DEFAULT_VALUE)
        if not 'getSoggetti' in dir(utils):
            utils = getUtility(IIolPraticaWeb, config.APP_FIELD_DEFAULT_VALUE)
        soggetti = utils.getSoggetti(self)

        utils = queryUtility(IIolPraticaWeb, name=self.tipo_app, default=config.APP_FIELD_DEFAULT_VALUE)
        if not 'getIndirizzi' in dir(utils):
            utils = getUtility(IIolPraticaWeb, config.APP_FIELD_DEFAULT_VALUE)

        indirizzi = utils.getIndirizzi(self)

        utils = queryUtility(IIolPraticaWeb, name=self.tipo_app, default=config.APP_FIELD_DEFAULT_VALUE)
        if not 'getNCT' in dir(utils):
            utils = getUtility(IIolPraticaWeb, config.APP_FIELD_DEFAULT_VALUE)

        nct = utils.getNCT(self)

        utils = queryUtility(IIolPraticaWeb,name=self.tipo_app, default=config.APP_FIELD_DEFAULT_VALUE)
        if not 'getNCEU' in dir(utils):
            utils = getUtility(IIolPraticaWeb, config.APP_FIELD_DEFAULT_VALUE)

        nceu = utils.getNCEU(self)

        utils = queryUtility(IIolPraticaWeb,name=self.tipo_app, default=config.APP_FIELD_DEFAULT_VALUE)
        if not 'getAllegati' in dir(utils):
            utils = getUtility(IIolPraticaWeb, config.APP_FIELD_DEFAULT_VALUE)

        allegati = utils.getAllegati(self)

        result = client.service.aggiungiPratica(pr,soggetti,indirizzi,nct, nceu, list())
        result = dict(result)
        if result["pratica"]:
            for allegato in allegati:
                res = client.service.aggiungiAllegato(result["pratica"],allegato)

        return result
