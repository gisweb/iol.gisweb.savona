# -*- coding: utf-8 -*-
import os
from zope.interface import implements

from iol.gisweb.savona.interfaces import IIolApp,IIolPraticaWeb

from AccessControl import ClassSecurityInfo
import simplejson as json

from DateTime import DateTime

from base64 import b64encode

from iol.gisweb.utils.config import USER_CREDITABLE_FIELD,USER_UNIQUE_FIELD,IOL_APPS_FIELD,STATUS_FIELD,IOL_NUM_FIELD
from iol.gisweb.utils.IolDocument import IolDocument
from iol.gisweb.utils import loadJsonFile,dateEncoder

class cilaApp(object):
    implements(IIolApp)
    security = ClassSecurityInfo()
    def __init__(self):
        self.file = 'cila'
        self.path = os.path.dirname(os.path.abspath(__file__))

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

    # Returns dict with all information about wizard
    security.declarePublic('getWizardInfo')

    def getWizardInfo(self,obj):
        doc = obj

        result = dict(
            actions=[],
            state="",
            base_url="%s/content_status_modify?workflow_action=" % (doc.absolute_url()),
            forms=[]
        )
        info = loadJsonFile("%s/wizard_info/%s.json" % (self.path, self.file)).result
        iDoc = IolDocument(doc)
        wfInfo = iDoc.wfInfo()
        if doc.portal_type == 'PlominoForm':
            result["state"] = info["initial_state"]
        else:
            result["state"] = iDoc.wfState()
        for v in info["states"]:
            cls_list = list()
            if not iDoc.isActionSupported(v["action"]):
                cls_list.append('link-disabled')
                action = ""
            else:
                action = v["action"]
            if result["state"] == v["state"]:
                cls_list.append("active")

            i = {"label": v["label"], "class": " ".join(cls_list), "action": action}
            result["forms"].append(i)
        return result

class cilaWsClient(object):
    implements(IIolPraticaWeb)
    security = ClassSecurityInfo()
    def __init__(self):
        self.resp_proc = 24
        self.file = 'cila'
        self.path = os.path.dirname(os.path.abspath(__file__))




