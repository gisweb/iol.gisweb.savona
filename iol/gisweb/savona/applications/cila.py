# -*- coding: utf-8 -*-
from zope.interface import implements
from iol.gisweb.savona.interfaces import IIolApp,IIolPraticaWeb
from zope import component
from AccessControl import ClassSecurityInfo
import simplejson as json
from plone import api

import sqlalchemy as sql
import sqlalchemy.orm as orm

from iol.gisweb.utils.config import USER_CREDITABLE_FIELD,USER_UNIQUE_FIELD,IOL_APPS_FIELD,STATUS_FIELD,IOL_NUM_FIELD

from .praticaweb import getConvData,genericTable
from plomino.replication.pgReplication import getPlominoValues

class cilaApp(object):
    implements(IIolApp)
    security = ClassSecurityInfo()
    def __init__(self):
        pass
    def __call__(self, *args, **kwargs):
        pass
    #Returns dict with all roles->users/groups defined in Iol application
    security.declarePublic('NuovoNumeroPratica')
    def NuovoNumeroPratica(self,obj):
        idx = obj.getParentDatabase().getIndex()
        query = dict(IOL_NUM_FIELD = dict(query=0, range='min'), iol_tipo_app = 'cila')

        brains = idx.dbsearch(query, sortindex=IOL_NUM_FIELD, reverse=1, only_allowed=False)
        if not brains:
            nuovoNumero = 1
        else:
            nuovoNumero = (brains[0].getObject().getItem(IOL_NUM_FIELD,0) or 0) +1

        return nuovoNumero

class cilaWsClient(object):
    implements(IIolPraticaWeb)
    security = ClassSecurityInfo()
    def __init__(self):
        self.resp_proc = 24
        self.file = 'cila'
        self.path = os.path.dirname(os.path.abspath(__file__))




