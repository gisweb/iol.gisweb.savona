# -*- coding: utf-8 -*-
from zope.interface import implements
from iol.gisweb.savona.interfaces import IIolApp,IIolPraticaWeb

from AccessControl import ClassSecurityInfo
import simplejson as json

from DateTime import DateTime

from iol.gisweb.utils.config import USER_CREDITABLE_FIELD,USER_UNIQUE_FIELD,IOL_APPS_FIELD,STATUS_FIELD,IOL_NUM_FIELD
from iol.gisweb.utils.IolDocument import IolDocument
from iol.gisweb.utils import loadJsonFile,dateEncoder

from .praticaweb import getConvData,genericTable
from plomino.replication.pgReplication import getPlominoValues

class sciaApp(object):
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
        query = dict(IOL_NUM_FIELD = dict(query=0, range='min'),iol_tipo_app = 'scia' )

        brains = idx.dbsearch(query, sortindex=IOL_NUM_FIELD, reverse=1, only_allowed=False)
        if not brains:
            nuovoNumero = 1
        else:
            nuovoNumero = (brains[0].getObject().getItem(IOL_NUM_FIELD,0) or 0) +1

        return nuovoNumero




class sciaWsClient(object):
    implements(IIolPraticaWeb)
    security = ClassSecurityInfo()
    def __init__(self):
        self.resp_proc = 24
        self.mapping = loadJsonFile('./mapping/scia.json')
        pass

    security.declarePublic('getProcedimento')
    def getProcedimento(self,obj):
        doc = obj.document
        pr = obj.client.factory.create('procedimento')
        if doc.getItem('data_inizio_lavori_opt','scia_data_inizio_presentazione')=='scia_data_inizio_presentazione':
            pr.tipo = 21100
        else:
            pr.tipo = 21200
        pr.oggetto = doc.getItem('descrizione_intervento','')
        pr.note = ""
        pr.protocollo = doc.getItem('numero_protocollo','')
        pr.data_prot = doc.getItem('data_prot',DateTime()).strftime("%d/%m/%Y")
        pr.data_presentazione = doc.getItem('data_presentazione',DateTime().strftime("%d/%m/%Y"))
        pr.online = 1
        pr.resp_proc = self.resp_proc
        pr.data_resp = DateTime().strftime("%d/%m/%Y")
        return pr

    def getSoggetti(self,obj):
        doc = obj.document
        idoc = IolDocument(doc)
        soggetti = list()
        # Recupero informazioni sui richiedenti/proprietari
        soggetto = obj.client.factory.create('soggetto')
        mapfields = self.mapping['richiedente']
        for k,v in mapfields.items():
            if v:
                soggetto[k] = json.dumps(doc.getItem(v,None), cls=dateEncoder, use_decimal=True)
        soggetto['richiedente'] = 1
        soggetto['comunicazioni'] = 1
        # Il richiedente è anche proprietario
        if doc.getItem('fisica_titolo', '').lower() == 'proprietario':
            soggetto['proprietario'] = 1
        soggetti.append(soggetto)
        for r in idoc.getDatagridValue('frm_scia_richiedenti','anagrafica_soggetti'):
            soggetto = obj.client.factory.create('soggetto')
            for k,v in mapfields.items():
                if v:
                    soggetto[k] = r[v]
            soggetto['richiedente'] = 1
            soggetto['comunicazioni'] = 1
            # Il richiedente è anche proprietario
            if r['fisica_titolo'].lower() == 'proprietario':
                soggetto['proprietario'] = 1
            soggetti.append(soggetto)

        # Recupero informazioni sul progettista
        soggetto = obj.client.factory.create('soggetto')
        mapfields = self.mapping['progettista']
        for k,v in mapfields.items():
            if v:
                soggetto[k] = json.dumps(doc.getItem(v,None), cls=dateEncoder, use_decimal=True)
        soggetto['progettista'] = 1
        soggetto['comunicazioni'] = 1
        soggetti.append(soggetto)

        direttore = doc.getItem('direttore_opt','nodirettore')

        # Il progettista è anche direttore lavori
        if direttore == 'direttoreesecutore':
            soggetto['direttore'] = 1
        # Recupero informazioni sul direttore lavori
        elif direttore == 'direttore':
            soggetto = obj.client.factory.create('soggetto')
            mapfields = self.mapping['direttore']
            for k,v in mapfields.items():
                if v:
                    soggetto[k] = json.dumps(doc.getItem(v,None), cls=dateEncoder, use_decimal=True)
            soggetto['direttore'] = 1
            soggetto['comunicazioni'] = 1
            soggetti.append(soggetto)

        # Recupero informazioni sugli esecutori se necessario
        if doc.getItem('lavori_economia_opt','economia'):
            pass
        else:
            soggetto = obj.client.factory.create('soggetto')
            mapfields = self.mapping['esecutore']
            for k,v in mapfields.items():
                if v:
                    soggetto[k] = json.dumps(doc.getItem(v,None), cls=dateEncoder, use_decimal=True)

            soggetto['esecutore'] = 1
            soggetto['comunicazioni'] = 1

            soggetti.append(soggetto)
            for r in idoc.getDatagridValue('frm_scia_altri_soggetti','altri_esecutori'):
                soggetto = obj.client.factory.create('soggetto')
                for k,v in mapfields.items():
                    if v:
                        soggetto[k] = r[v]
                soggetto['esecutore'] = 1
                soggetto['comunicazioni'] = 1
                soggetti.append(soggetto)
        return soggetti

    def getIndirizzi(self,obj):
        doc = obj.document
        indirizzi = list()
        indirizzo = obj.client.factory.create('indirizzo')
        mapfields = self.mapping['indirizzo']

        return indirizzi

    def getCT(self,obj):
        doc = obj.document
        ftype = obj.client.factory.create('particella')
        return ftype

    def getCU(self,obj):
        doc = obj.document
        ftype = obj.client.factory.create('particella')
        return ftype

    def getAllegati(self,obj):
        doc = obj.document
        ftype = obj.client.factory.create('allegato')
        return ftype