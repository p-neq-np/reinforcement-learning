import pymongo

# simplified for the purpose
class Storage:

    def __init__(self, coll_name="tsp_test"):
        self.coll_name = coll_name
        self._init_client() # connection
        self._init_db() # database
        self._init_collection(self.coll_name)

    def _init_client(self):
        # the connector
        self.client = pymongo.MongoClient("mongodb://localhost:27017/")

    def _init_db(self, name = "route_db"):
        # creates the db if it doesn't exist
        self.db = self.client[name]

    def _init_collection(self, coll_name):
        # collection is the table
        self.collection = self.db[coll_name]

    def insert_route(self, route_dict):
        """
        :param route_dict: {"graph","route"}
        :return: inserted_id of the record
        """
        return self.collection.insert_one(route_dict)

    def export_as_CSV(self, collection_name=None, field_name=None, filename=None):
        """
        :param collection_name: test table,filename: full path of the CSV
        :return: returns nothing
        """
        if filename and field_name and collection_name is not None:
            # subprocess
            pass
        else:
            print("Parameters are not valid")

    # simple print
    def print_table(self, limit=10):
        count = 0
        for x in self.collection.find():
            print(x)
            count += 1
            if count >= limit:
                break


