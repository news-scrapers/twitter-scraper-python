
import os
import datetime
from pymongo import MongoClient

class IndexAccount:
    def __init__(self, account):
        self.last_date = None
        self.account = account

        client = MongoClient(os.getenv("database_url"))
        db = client['tweets']
        self.collection=db.IndexAccount



    def get(self):
        result = self.collection.find_one({"account":self.account})
        print(result)
        if  (result == None):
            self.last_date = datetime.datetime.now()
            return

        if  (not result["last_date"] == None):
            self.last_date = result["last_date"]
        else:
            self.last_date = datetime.datetime.now()
            
    def serialize(self):
        obj={"last_date": self.last_date, "account":self.account}
        return obj


    def update_date(self, new_last_date):
        self.last_date = new_last_date
        self.collection.find_one_and_update( {"account" : self.account},{"$set": self.serialize()},upsert=True)
