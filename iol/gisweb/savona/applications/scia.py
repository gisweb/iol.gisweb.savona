from zope.interface import implements
from iol.gisweb.savona.interfaces import IIolApp
from zope import component
from AccessControl import ClassSecurityInfo
import simplejson as json
from plone import api

import sqlalchemy as sql
import sqlalchemy.orm as orm

from iol.gisweb.utils.config import USER_CREDITABLE_FIELD,USER_UNIQUE_FIELD,IOL_APPS_FIELD,STATUS_FIELD,IOL_NUM_FIELD

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
        query = dict(IOL_NUM_FIELD = dict(query=0, range='min'))

        brains = idx.dbsearch(query, sortindex=IOL_NUM_FIELD, reverse=1, only_allowed=False)
        if not brains:
            nuovoNumero = 1
        else:
            nuovoNumero = (brains[0].getObject().getItem(IOL_NUM_FIELD,0) or 0) +1

        return nuovoNumero

    security.declarePublic('InvioPraticaweb')
    def invioPraticaweb(self,obj):
        plominoData = getPlominoValues(obj)
        if plominoData['data_inizio_lavori_opt'] == 'scia_data_inizio_presentazione':
            plominoData["tipo"] = 21100
        else:
            plominoData["tipo"] = 21200

        data = getConvData('scia')
        for d in data:
            #cfg = conf(d)
            cfg = d
            try:
                db = sql.create_engine(cfg['conn_string'])
                metadata = sql.schema.MetaData(bind=db,reflect=True,schema=cfg['schema'])
                table = sql.Table(cfg['table'], metadata, autoload=True)
                orm.clear_mappers()
                rowmapper = orm.mapper(genericTable,table)
            except Exception as e:
                api.portal.show_message(message=u'Si sono verificati errori nella connessione al database : %s' %str(e), request=obj.REQUEST )
                return -1
            #creating session
            Sess = orm.sessionmaker(bind = db)
            session = Sess()
            row = genericTable(d['conversion_file'],plominoData)
            session = Sess()
            #adding row to database
            session.add(row)
            session.commit()
            session.close()
            db.dispose()
        return 1
