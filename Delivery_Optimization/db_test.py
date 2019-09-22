import pymongo
from route_db import Storage

db = Storage("tsp_table")

mydict = {"input_graph": [2,3,4], "route": [4,3,2] }

v = db.insert_route(mydict)
db.print_table()