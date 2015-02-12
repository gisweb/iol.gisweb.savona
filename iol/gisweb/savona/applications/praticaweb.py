# -*- coding: utf-8 -*-

import simplejson as json
import os

def convert(conv,obj):
    res = dict()
    keys = obj.keys()
    for item_old,item_new in conv.items():
        if item_old in keys:
            res[item_new] = obj[item_old]

    return res

def getConvData(json_file):
    fName = "mapping/%s.json" %json_file
    if os.path.isfile(json_file):
        json_data=open(json_file)
        try:
            data = json.load(json_data)
        except ValueError, e:
            data = dict()
        json_data.close()
    else:
        data = dict()
    return data

class table(object):
    def __init__(self,json_file,**entries):
        data = getConvData(json_file)
        if not isinstance(entries,dict):
            data = dict()
        values = convert(data,entries)
        self.__dict__.update(values)




