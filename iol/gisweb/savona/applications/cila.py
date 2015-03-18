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




class cilaWsClient(object):
    implements(IIolPraticaWeb)
    security = ClassSecurityInfo()

    def __init__(self):
        self.resp_proc = 24
        self.file = 'cila'
        self.path = os.path.dirname(os.path.abspath(__file__))
        self.mapping = loadJsonFile("%s/mapping/%s.json" % (self.path,self.file)).result
        self.elenchi = loadJsonFile("%s/mapping/elenchi.json" % (self.path)).result

    security.declarePublic('getProcedimento')

    def getProcedimento(self, obj):
        doc = obj.document
        idoc = IolDocument(doc)
        pr = obj.client.factory.create('procedimento')
        pr.tipo = 21300
        pr.oggetto = doc.getItem('descrizione_intervento','')
        pr.note = '\n'.join(idoc.getLabels('tipologia_intervento'))
        pr.protocollo = doc.getItem('numero_protocollo','')
        pr.data_prot = doc.getItem('data_prot',DateTime()).strftime("%d/%m/%Y")
        pr.data_presentazione = doc.getItem('data_presentazione',DateTime().strftime("%d/%m/%Y"))
        pr.online = 1
        pr.resp_proc = self.resp_proc
        pr.data_resp = DateTime().strftime("%d/%m/%Y")
        return pr

    def getSoggetti(self, obj):
        doc = obj.document
        idoc = IolDocument(doc)
        soggetti = list()
        ruoli = ['richiedente','proprietario','progettista','direttore','esecutore','sicurezza']

        #########################################################################################
        #
        # Recupero informazioni sui richiedenti/proprietari
        #
        #########################################################################################

        soggetto = obj.client.factory.create('soggetto')
        for i in ruoli:
            soggetto[i] = 0;
        mapfields = self.mapping['richiedente']
        for k, v in mapfields.items():
            if v:
                soggetto[k] = json.dumps(doc.getItem(v,None), cls=dateEncoder, use_decimal=True)

        soggetto['richiedente'] = 1
        soggetto['comunicazioni'] = 1
        if soggetto['sesso'] == 'Maschile':
            soggetto['sesso'] = 'M'
        else:
            soggetto['sesso'] = 'F'
        # Il richiedente è anche proprietario
        if doc.getItem('fisica_titolo', '').lower() == 'proprietario':
            soggetto['proprietario'] = 1
        if doc.getItem('soggetto_resp_sicurezza','') == 'richiedente':
            soggetto['sicurezza'] = 1
        soggetti.append(soggetto)
        for r in idoc.getDatagridValue('anagrafica_soggetti'):
            soggetto = obj.client.factory.create('soggetto')
            for i in ruoli:
                soggetto[i] = 0;
            for k, v in mapfields.items():
                if v:
                    if v in r.keys():
                        soggetto[k] = r[v]
                    else:
                        soggetto[k] = ''
            soggetto['richiedente'] = 1
            soggetto['comunicazioni'] = 1
            if soggetto['sesso'] == 'Maschile':
                soggetto['sesso'] = 'M'
            else:
                soggetto['sesso'] = 'F'
            # Il richiedente è anche proprietario
            if 'fisica_titolo' in r.keys():
                titolo = r['fisica_titolo']
            else:
                titolo = ''
            if titolo.lower() == 'proprietario':
                soggetto['proprietario'] = 1
            soggetti.append(soggetto)

        ##################################################################################################
        #
        # Recupero informazioni sul progettista
        #
        ##################################################################################################

        soggetto = obj.client.factory.create('soggetto')
        for i in ruoli:
            soggetto[i] = 0;
        mapfields = self.mapping['progettista']
        for k, v in mapfields.items():
            if v:
                value = doc.getItem(v,None)
                if isinstance(value,DateTime):
                    soggetto[k] = value.strftime("%d/%m/%Y")
                else:
                    soggetto[k] = value

        soggetto['progettista'] = 1
        soggetto['comunicazioni'] = 1
        if doc.getItem('soggetto_resp_sicurezza','') == 'progettista':
            soggetto['sicurezza'] = 1

        if soggetto['sesso'] == 'Maschile':
            soggetto['sesso'] = 'M'
        else:
            soggetto['sesso'] = 'F'

        direttore = doc.getItem('direttore_opt','nodirettore')
        if direttore == 'direttoreesecutore':
            soggetto['direttore'] = 1
        soggetti.append(soggetto)
        # Il progettista è anche direttore lavori
        # Recupero informazioni sul direttore lavori

        if direttore == 'direttore':
            soggetto = obj.client.factory.create('soggetto')
            for i in ruoli:
                soggetto[i] = 0;
            mapfields = self.mapping['direttore']
            for k, v in mapfields.items():
                if v:
                    soggetto[k] = json.dumps(doc.getItem(v,None), cls=dateEncoder, use_decimal=True)
            soggetto['direttore'] = 1
            soggetto['comunicazioni'] = 1
            if soggetto['sesso'] == 'Maschile':
                soggetto['sesso'] = 'M'
            else:
                soggetto['sesso'] = 'F'
            soggetti.append(soggetto)
        #######################################################################################################
        #
        # Recupero informazioni sugli esecutori se necessario
        #
        ######################################################################################################
        if doc.getItem('lavori_economia_opt','economia'):
            pass
        else:
            soggetto = obj.client.factory.create('soggetto')
            for i in ruoli:
                soggetto[i] = 0;
            mapfields = self.mapping['esecutore']
            for k, v in mapfields.items():
                if v:
                    soggetto[k] = json.dumps(doc.getItem(v,None), cls=dateEncoder, use_decimal=True)

            soggetto['esecutore'] = 1
            soggetto['comunicazioni'] = 1
            if soggetto['sesso'] == 'Maschile':
                soggetto['sesso'] = 'M'
            else:
                soggetto['sesso'] = 'F'

            soggetti.append(soggetto)
            for r in idoc.getDatagridValue('altri_esecutori'):
                soggetto = obj.client.factory.create('soggetto')
                for i in ruoli:
                    soggetto[i] = 0;
                for k, v in mapfields.items():
                    if v:
                        if v in r.keys():
                            soggetto[k] = r[v]
                        else:
                            soggetto[k] = ''
                soggetto['esecutore'] = 1
                soggetto['comunicazioni'] = 1
                if soggetto['sesso'] == 'Maschile':
                    soggetto['sesso'] = 'M'
                else:
                    soggetto['sesso'] = 'F'
                soggetti.append(soggetto)
        ########################################################################################################
        #
        # Recupero Informazioni su Respunsabile Sicurezza (Se Necessario)
        #
        ########################################################################################################

        if doc.getItem('soggetto_resp_sicurezza', '') != 'altro':
            pass
        else:
            soggetto = obj.client.factory.create('soggetto')
            for i in ruoli:
                soggetto[i] = 0;

            mapfields = self.mapping['sicurezza']
            for k, v in mapfields.items():
                if v:
                    soggetto[k] = json.dumps(doc.getItem(v,None), cls=dateEncoder, use_decimal=True)

            soggetto['sicurezza'] = 1
            soggetto['comunicazioni'] = 1


        return soggetti

    def getIndirizzi(self, obj):
        doc = obj.document
        idoc = IolDocument(doc)
        results = list()
        elencoVie = dict()
        vie = obj.client.service.elencoVie()[2]
        for via in vie:
            elencoVie[str(via.value)] = str(via.label)

        mapfields = self.mapping['indirizzo']
        for r in idoc.getDatagridValue('elenco_civici'):
            fType = obj.client.factory.create('indirizzo')
            for k, v in mapfields.items():
                if v:
                    if k == 'via':
                        fType[k] = elencoVie[r[v]]
                    else:
                        fType[k] = r[v]
            results.append(fType)
        return results

    def getNCT(self, obj):
        doc = obj.document
        idoc = IolDocument(doc)
        results = list()
        mapfields = self.mapping['nct']
        for r in idoc.getDatagridValue('elenco_nct'):
            fType = obj.client.factory.create('particella')
            for k, v in mapfields.items():
                if v:
                    fType[k] = r[v]
            results.append(fType)
        return results

    def getNCEU(self, obj):
        doc = obj.document
        idoc = IolDocument(doc)
        results = list()
        mapfields = self.mapping['nceu']
        for r in idoc.getDatagridValue('elenco_nceu'):
            fType = obj.client.factory.create('particella')
            for k, v in mapfields.items():
                if v:
                    fType[k] = r[v]
            results.append(fType)
        return results

    def getAllegati(self, obj):
        doc = obj.document
        idoc = IolDocument(doc)
        results = list()
        mapfields = self.mapping['allegato']
        for k, v in mapfields.items():
            allegato = obj.client.factory.create('allegato')
            files_allegati = list()
            for el in v:
                f = idoc.getAttachmentInfo(el)
                if f:
                    for info in f:
                        file_allegato = obj.client.factory.create('file_allegato')
                        file_allegato.nome_file = info['name']
                        file_allegato.tipo_file = info['mimetype']
                        file_allegato.size_file = info['size']
                        #file_allegato.file = ''
                        file_allegato.file = info['b64file']
                        files_allegati.append(file_allegato)
                allegato.documento = k
                allegato.allegato = 1
                allegato.files = files_allegati
            if allegato.files and allegato.documento:
                results.append(allegato)
        return results

    def getProgetto(self,obj):
        doc = obj.document
        progetto = obj.client.factory.create('progetto')
        dval = doc.getItem('immobile_destinazione', '')
        progetto.destuso1 = self.elenchi['destuso'][dval]
        return progetto





