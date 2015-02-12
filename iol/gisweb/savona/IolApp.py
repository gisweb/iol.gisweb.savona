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
from .interfaces import IIolApp


class IolApp(object):
    implements(IIolApp)
    adapts(IPlominoForm,IPlominoDocument)
    tipo_app = u""
    security = ClassSecurityInfo()
    security.declareObjectPublic()

    def __init__(self,obj):
        self.document = obj

    security.declarePublic('NuovoNumeroPratica')
    def NuovoNumeroPratica(self):
        app = self.document.getItem(config.APP_FIELD,config.APP_FIELD_DEFAULT_VALUE)
        utils = getUtility(IIolApp,app)
        return utils.NuovoNumeroPratica(self.document)

    security.declareProtected(IOL_EDIT_PERMISSION,'invioPraticaweb')
    def invioPraticaweb(self):
        app = self.document.getItem(config.APP_FIELD,config.APP_FIELD_DEFAULT_VALUE)
        utils = getUtility(IIolApp,app)
        return utils.invioPraticaweb(self.document)

InitializeClass(IolApp)