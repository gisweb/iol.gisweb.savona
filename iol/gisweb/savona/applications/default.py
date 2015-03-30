# -*- coding: utf-8 -*-
from zope.interface import implements
from zope import component
from AccessControl import ClassSecurityInfo
from plone import api
from iol.gisweb.savona.interfaces import IIolApp,IIolPraticaWeb
from gisweb.iol.permissions import IOL_READ_PERMISSION, IOL_EDIT_PERMISSION, IOL_REMOVE_PERMISSION

from iol.gisweb.utils.config import USER_CREDITABLE_FIELD,USER_UNIQUE_FIELD,IOL_APPS_FIELD,STATUS_FIELD,IOL_NUM_FIELD
from Products.CMFCore.utils import getToolByName
import os
import simplejson as json

class defaultApp(object):
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
        query = dict(IOL_NUM_FIELD = dict(query=0, range='min'))
        brains = idx.dbsearch(query, sortindex=IOL_NUM_FIELD, reverse=1, only_allowed=False)
        if not brains:
            nuovoNumero = 1
        else:
            nuovoNumero = (brains[0].getObject().getItem(IOL_NUM_FIELD,0) or 0) +1

        return nuovoNumero

    #Procedure that search all documents of the selected user, assign him ownership, and move him in iol groups
    security.declarePublic('accreditaUtente')
    def accreditaUtente(self,obj):
        user = obj.getOwner()
        username = user.getUserName()
        apps = obj.getItem(IOL_APPS_FIELD,[])  
                                                                                                                                                                                                                 
        self._assignGroups(obj,username,apps)

        catalog = api.portal.get_tool('portal_catalog')
        brains = catalog(portal_type='PlominoDatabase')
        unique = obj.getItem(USER_UNIQUE_FIELD,'')
        cont = 0
        brains = []
        for brain in brains:
            db = brain.getObject()
            idx = db.getIndex()
            req = dict(USER_CREDITABLE_FIELD = unique)
            for br in idx.dbsearch(req,only_allowed=False):
                doc = br.getObject()
                self._assignOwner(doc,user)
                cont += 1
        return cont

    def getConvData(self,json_file):
        fName = "%s/mapping/%s.json" %(os.path.dirname(os.path.abspath(__file__)),json_file)
        
        if os.path.isfile(fName):
            json_data=open(fName)

            try:
                data = json.load(json_data)

            except ValueError, e:
                data = str(e)
                json_data.close()
               
        else:
            return fName
            data = dict()
        return data    

    security.declarePublic('createPdf')
    def createPdf(selfself,obj,filename,itemname,overwrite):
        filename = '%s.pdf' % filename or obj.REQUEST.get('filename') or obj.getId()

        try:
            res = obj.restrictedTraverse('@@wkpdf').get_pdf_file()
        except Exception as err:

            msg1 = "%s" % (str(err))
            msg2 = "Attenzione! Non è stato possibile allegare il file: %s" % filename
            api.portal.show_message(message=msg1, request=obj.REQUEST,type='error')
            api.portal.show_message(message=msg2, request=obj.REQUEST,type='warning')
        else:
            (f,c) = obj.setfile(res,filename=filename,overwrite=overwrite,contenttype='application/pdf')
            if f and c:
                old_item = obj.getItem(itemname, {}) or {}
                old_item[filename] = c
                obj.setItem(itemname, old_item)        
    
    security.declarePublic('updateStatus')
    def updateStatus(self,obj):
        obj.setItem(STATUS_FIELD,api.content.get_state(obj=obj) )
        self.reindex_doc(obj)

    security.declarePublic('reindex_doc')
    def reindex_doc(self,obj):
        db = obj.getParentDatabase()
        # update index
        db.getIndex().indexDocument(obj)
        # update portal_catalog
        if db.getIndexInPortal():
            db.portal_catalog.catalog_object(obj, "/".join(db.getPhysicalPath() + (obj.getId(),)))

class defaultWsClient(object):
    implements(IIolPraticaWeb)
    security = ClassSecurityInfo()
    def __init__(self):
        pass

    security.declarePublic('getProcedimento')
    def getProcedimento(self,obj):
        pr = obj.client.factory.create('procedimento')
        return pr

    def getSoggetti(self,obj):
        ftype = obj.client.factory.create('soggetto')
        return ftype

    def getIndirizzi(self,obj):
        ftype = obj.client.factory.create('indirizzo')
        return ftype

    def getCT(self,obj):
        ftype = obj.client.factory.create('particella')
        return ftype

    def getCU(self,obj):
        ftype = obj.client.factory.create('particella')
        return ftype