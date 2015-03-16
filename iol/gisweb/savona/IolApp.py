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
from .interfaces import IIolApp
from iol.gisweb.utils.IolDocument import IolDocument


class IolApp(object):
    implements(IIolApp)
    adapts(IPlominoForm, IPlominoDocument)
    tipo_app = u""
    security = ClassSecurityInfo()
    security.declareObjectPublic()

    def __init__(self, obj):
        self.document = obj
        iDoc = IolDocument(obj)
        self.tipo_app = iDoc.getIolApp()

    security.declarePublic('NuovoNumeroPratica')
    def NuovoNumeroPratica(self):

        utils = queryUtility(IIolApp,name=self.tipo_app, default=config.APP_FIELD_DEFAULT_VALUE)
        if not 'NuovoNumeroPratica' in dir(utils):
            utils = getUtility(IIolApp,config.APP_FIELD_DEFAULT_VALUE)
        return utils.NuovoNumeroPratica(self.document)

    security.declarePublic('invioPraticaweb')
    def invioPraticaweb(self):
        utils = queryUtility(IIolApp,name=self.tipo_app, default=config.APP_FIELD_DEFAULT_VALUE)
        if not 'invioPraticaweb' in dir(utils):
            utils = getUtility(IIolApp,config.APP_FIELD_DEFAULT_VALUE)        
        return utils.invioPraticaweb(self.document)

    security.declarePublic('accreditaUtente')
    def accreditaUtente(self):
        utils = queryUtility(IIolApp,name=self.tipo_app, default=config.APP_FIELD_DEFAULT_VALUE)
        if not 'accreditaUtente' in dir(utils):
            utils = getUtility(IIolApp,config.APP_FIELD_DEFAULT_VALUE)        
        return utils.accreditaUtente(self.document)


    security.declarePublic('createPdf')
    def createPdf(self,filename,itemname='documento_da_firmare',overwrite=False):
        utils = queryUtility(IIolApp,name=self.tipo_app, default=config.APP_FIELD_DEFAULT_VALUE)
        if not 'createPdf' in dir(utils):
            utils = getUtility(IIolApp,config.APP_FIELD_DEFAULT_VALUE)        
        return utils.createPdf(self.document,filename,itemname,overwrite)

    security.declarePublic('updateStatus')
    def updateStatus(self):
        utils = queryUtility(IIolApp,name=self.tipo_app, default=config.APP_FIELD_DEFAULT_VALUE)
        if not 'updateStatus' in dir(utils):
            utils = getUtility(IIolApp,config.APP_FIELD_DEFAULT_VALUE)
        return utils.updateStatus(self.document)

    security.declarePublic('reindex_doc')
    def reindex_doc(self):
        utils = queryUtility(IIolApp,name=self.tipo_app, default=config.APP_FIELD_DEFAULT_VALUE)
        if not 'reindex_doc' in dir(utils):
            utils = getUtility(IIolApp,config.APP_FIELD_DEFAULT_VALUE)
        return utils.reindex_doc(self.document) 

    # Wizard Info
    security.declarePublic('getWizardInfo')

    def getWizardInfo(self):
        utils = queryUtility(IIolApp,name=self.tipo_app, default=config.APP_FIELD_DEFAULT_VALUE)
        if not 'getWizardInfo' in dir(utils):
            return dict()
        return utils.getWizardInfo(self.document)
InitializeClass(IolApp)