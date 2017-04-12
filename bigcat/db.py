#!/usr/bin/venv35 python3
# -*- coding: utf-8 -*-
from settings import *
from pymongo import MongoClient
__doc__ = "Database driver"


client = MongoClient("127.0.0.1", 27017, maxPoolSize=75, waitQueueMultiple=10, connect=False)
# client = MongoClient(DB_URI)
db = client[DB_NAME]
coll = db[DB_COLL]
