# -*- coding: utf-8 -*-
from zope.i18nmessageid import MessageFactory
from AccessControl import allow_module
from zope import component
from .interfaces import IIolApp,IIolPraticaWeb
from iol.gisweb.utils import config
from .applications.default import defaultApp,defaultWsClient
from applications.scia import sciaApp,sciaWsClient
from applications.cila import cilaApp

allow_module("iol.gisweb.savona.IolApp")
allow_module("iol.gisweb.savona.IolPraticaWeb")

MessageFactory = MessageFactory('iol.gisweb.savona')

gsm = component.getGlobalSiteManager()

#Register Named Utility For Applications
app = defaultApp()
gsm.registerUtility(app, IIolApp, config.APP_FIELD_DEFAULT_VALUE)

app = sciaApp()
gsm.registerUtility(app, IIolApp, 'scia')

app = cilaApp()
gsm.registerUtility(app, IIolApp, 'cila')


#Register Named Utility For WebService Praticaweb
app = defaultWsClient()
gsm.registerUtility(app, IIolPraticaWeb, config.APP_FIELD_DEFAULT_VALUE)

app = sciaWsClient()
gsm.registerUtility(app, IIolPraticaWeb, 'scia')