# -*- coding: utf-8 -*-
from zope.interface import Interface, implements, Attribute
from zope.component import adapts
from plone import api
from AccessControl import ClassSecurityInfo
from App.class_init import InitializeClass
from Products.CMFPlomino.interfaces import IPlominoDocument, IPlominoForm
from zope.component import getGlobalSiteManager
from iol.gisweb.utils import config
from iol.gisweb.utils.IolDocument import IolDocument
from gisweb.iol.permissions import IOL_READ_PERMISSION, IOL_EDIT_PERMISSION, IOL_REMOVE_PERMISSION
from zope.component import getUtility,queryUtility
from iol.gisweb.savona.interfaces import IIolPraticaWeb
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
   
    def aggiungi_inizio_lavori(self):
        client = self.client
        doc = self.document
        
        utils = queryUtility(IIolPraticaWeb, name=self.tipo_app, default=config.APP_FIELD_DEFAULT_VALUE)
        if not 'getComunicazioneInizioLavori' in dir(utils):
            utils = getUtility(IIolPraticaWeb, config.APP_FIELD_DEFAULT_VALUE)

        lavori = utils.getComunicazioneInizioLavori(self)

        utils = queryUtility(IIolPraticaWeb,name=self.tipo_app, default=config.APP_FIELD_DEFAULT_VALUE)
        if not 'getAllegati' in dir(utils):
            utils = getUtility(IIolPraticaWeb, config.APP_FIELD_DEFAULT_VALUE)

        allegati = utils.getAllegati(self)
        procedimento = client.service.trovaProcedimento(doc.getItem('numero_pratica'))
        result = dict(procedimento)
        if result['id'] != None:
            pratica = result['id'] 
            client.service.comunicazioneInizioLavori(pratica,lavori)

            # aggiunge allegati per ciascuna pratica        
            files_ok = files_err = 0
            for allegato in allegati:
                res = client.service.aggiungiAllegato(pratica,allegato)
                nfiles = len(allegato.files)
                res = dict(res)
                
        return result

    def aggiungi_fine_lavori(self):
        client = self.client
        doc = self.document

        utils = queryUtility(IIolPraticaWeb, name=self.tipo_app, default=config.APP_FIELD_DEFAULT_VALUE)
        if not 'getComunicazioneFineLavori' in dir(utils):
            utils = getUtility(IIolPraticaWeb, config.APP_FIELD_DEFAULT_VALUE)

        lavori = utils.getComunicazioneFineLavori(self)

        utils = queryUtility(IIolPraticaWeb,name=self.tipo_app, default=config.APP_FIELD_DEFAULT_VALUE)
        if not 'getAllegati' in dir(utils):
            utils = getUtility(IIolPraticaWeb, config.APP_FIELD_DEFAULT_VALUE)

        allegati = utils.getAllegati(self)
        procedimento = client.service.trovaProcedimento(doc.getItem('numero_pratica'))
        result = dict(procedimento)
        if result['id'] != None:
            pratica = result['id']
            client.service.comunicazioneFineLavori(pratica,lavori)

            # aggiunge allegati per ciascuna pratica
            files_ok = files_err = 0
            for allegato in allegati:
                res = client.service.aggiungiAllegato(pratica,allegato)
                nfiles = len(allegato.files)
                res = dict(res)

        return result
 
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
            files_ok = files_err = 0
            for allegato in allegati:
                res = client.service.aggiungiAllegato(result["pratica"],allegato)
                nfiles = len(allegato.files)
                res = dict(res)

                #if(res['success']==1):
                #    files_ok += res['cont']
                #    files_err += res['err']
                #else:
                #    files_err += nfiles
            #if files_err:
            #    result['messages'].append("Si sono verificati %d errori nel trasferimento degli allegati" % files_err)
            #if files_ok:
            #    result['messages'].append("Sono stati trasferiti correttamente %d allegati" % files_ok)
        return result
    security.declarePublic('infoProcedimento')
    def infoProcedimento(self,tipo_sogg):
        client = self.client
        doc = self.document
        idoc = IolDocument(doc)
        procedimento = client.service.trovaProcedimento(doc.getItem('numero_pratica'))
        result = dict(procedimento)
        infoDoc = idoc.serializeDoc()
        if result["id"]:
            res = dict(client.service.infoPratica(result["id"]))
            
	    if res["success"]:
                r = dict(res["result"])
                for k,v in r.items():
                    infoDoc[k] = v

            res = dict(client.service.infoSoggetto(result["id"],tipo_sogg))
            #import pdb;pdb.set_trace();
	    if res["success"]:
                r = list(res["result"])
                infoDoc["soggetti"] = list()
                for v in r:
                    infoDoc["soggetti"].append(dict(v))
            
            res = dict(client.service.infoIndirizzi(result["id"]))
            #import pdb;pdb.set_trace()
            if res["success"]:
                r = list(res["result"])
                infoDoc["indirizzi"] = list()
                for v in r:
                    infoDoc["indirizzi"].append(dict(v))

        return infoDoc


InitializeClass(IolWSPraticaWeb)
