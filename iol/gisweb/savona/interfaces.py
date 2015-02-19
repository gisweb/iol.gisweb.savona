from zope.interface import Interface, Attribute


class IIolApp(Interface):
    """
    marker interface for iol document
    """
    iol_app = Attribute("Application Name")


class IIolPraticaWeb(Interface):
    """
    Marker interface for iol praticaweb
    """

class IIolAppsLayer(Interface):
    """Marker interface for the Browserlayer
    """

