# -*- coding: utf-8 -*-
from zope.i18nmessageid import MessageFactory
from AccessControl import allow_module
from zope import component
from iol.gisweb.utils import config

from .interfaces import IIolApp, IIolPraticaWeb
from .applications.default import defaultApp, defaultWsClient
from applications.scia import sciaApp, sciaWsClient
from applications.suapcila import cilaApp, cilaWsClient
from applications.suapcila import suapcilaApp, suapcilaWsClient

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

app = suapcilaApp()
gsm.registerUtility(app, IIolApp, 'suapcila')

#Register Named Utility For WebService Praticaweb
app = defaultWsClient()
gsm.registerUtility(app, IIolPraticaWeb, config.APP_FIELD_DEFAULT_VALUE)

app = sciaWsClient()
gsm.registerUtility(app, IIolPraticaWeb, 'scia')

app = cilaWsClient()
gsm.registerUtility(app, IIolPraticaWeb, 'cila')

app = suapcilaWsClient()
gsm.registerUtility(app, IIolPraticaWeb, 'suapcila')

