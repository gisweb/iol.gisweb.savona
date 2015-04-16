# -*- coding: utf-8 -*-
from Products.CMFCore.utils import getToolByName
from plone.dexterity.browser.view import DefaultView
from plone import api

from zope.component import getUtility
from iol.gisweb.savona.IolApp import IolApp
from iol.gisweb.savona.IolPraticaWeb import IolWSPraticaWeb
from iol.gisweb.savona.IolApp import IolApp
import random
import simplejson as json
import DateTime

class inviaPW(object):

    def __init__(self,context,request):
        self.context = context
        self.request = request

    def __call__(self):
        doc = self.aq_parent
        url = "http://10.129.67.229/wspraticaweb/savona.wsPraticaweb.php?wsdl&test=%d" %random.randint(1,100000)
        wsDoc = IolWSPraticaWeb(doc,url)

        tipo_richiesta = doc.getItem('iol_tipo_richiesta','comunicazione')
        if tipo_richiesta == 'integrazione':
            res = wsDoc.invia_integrazione()
            res = dict(res)
            if res["success"]:

                wftool = getToolByName(doc, 'portal_workflow')
                wftool.doActionFor(doc, 'i1_protocolla')
                message = u"La richiesta di integrazione è stata inviata correttamente al Servizio Edilizia con Numero di pratica %s" % res["numero_pratica"]
                t = 'info'
            else:
                message = u"Si sono verificati alcuni errori durante l'invio della pratica"
                t = 'error'
        elif tipo_richiesta == 'inizio_lavori':
            res = wsDoc.aggiungi_inizio_lavori()
            res = dict(res)
            if res["success"]:
                wftool = getToolByName(doc, 'portal_workflow')
                wftool.doActionFor(doc, 'i1_protocolla')
                message = u"La domanda è stata inviata correttamente al Servizio Edilizia con Numero di pratica %s" % res["numero_pratica"]
                t = 'info'
            else:
                message = u"Si sono verificati alcuni errori durante l'invio della pratica"
                t = 'error'

        elif tipo_richiesta == 'fine_lavori':
            res = wsDoc.aggiungi_fine_lavori()
            res = dict(res)
            if res["success"]:
                #doc.setItem("numero_pratica",res["numero_pratica"])
                wftool = getToolByName(doc, 'portal_workflow')
                wftool.doActionFor(doc, 'i1_protocolla')
                message = u"La domanda è stata inviata correttamente al Servizio Edilizia con Numero di pratica %s" % res["numero_pratica"]
                t = 'info'
            else:
                message = u"Si sono verificati alcuni errori durante l'invio della pratica"
                t = 'error'

        else:
            res = wsDoc.aggiungi_pratica()
            res = dict(res)
            if res["success"]:
                doc.setItem("numero_pratica",res["numero_pratica"])
                wftool = getToolByName(doc, 'portal_workflow')
                wftool.doActionFor(doc, 'i1_protocolla')
                message = u"La domanda è stata inviata correttamente al Servizio Edilizia con Numero di pratica %s" % res["numero_pratica"]
                t = 'info'
            else:
                message = u"Si sono verificati alcuni errori durante l'invio della pratica"
                t = 'error'
        api.portal.show_message(message=message, type=t, request=doc.REQUEST)
	port = api.portal.get() 
        doc.REQUEST.RESPONSE.redirect(port['scrivania-protocolli'].absolute_url())
        #doc.REQUEST.RESPONSE.redirect(doc.absolute_url())




# Returns Info about Wizard Workflow
class wfWizardInfo(object):

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.state = api.content.get_state(obj=self.aq_parent)

    def __call__(self):
        doc = self.aq_parent
        aDoc = IolApp(doc)
        res = aDoc.getWizardInfo()
        #doc.REQUEST.RESPONSE.headers['Content-Type'] = 'application/json'
        return json.dumps(res)

class infoProcedimento(object):
    def __init__(self, context, request):
        self.context = context
        self.request = request


    def __call__(self):
        doc = self.aq_parent
        url = "http://10.129.67.229/wspraticaweb/savona.wsPraticaweb.php?wsdl&test=%d" %random.randint(1,100000)
        wsDoc = IolWSPraticaWeb(doc,url)
        res = wsDoc.infoProcedimento()
        return json.dumps(res,default=DateTime.DateTime.ISO,use_decimal=True)
