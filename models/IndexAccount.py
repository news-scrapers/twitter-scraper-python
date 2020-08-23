
import os
import datetime
from pymongo import MongoClient

class IndexAccount:
    def __init__(self, account, scraper_id, scraper_type):
        self.last_date = None
        self.account = account
        self.scraper_id = scraper_id
        self.last_updated = None
        self.scraper_type = scraper_type

        client = MongoClient(os.getenv("database_url"))
        db = client['tweets-scraping']
        self.collection=db.IndexAccount



    def get(self):
        result = self.collection.find_one({"account":self.account, "scraper_id":self.scraper_id})
        if  (result == None):
            self.last_date = datetime.datetime.now()
            return
        if  (not result["scraper_id"] == None):
            self.scraper_id = result["scraper_id"]

        if  (not result["last_date"] == None):
            self.last_date = result["last_date"]
        else:
            self.last_date = datetime.datetime.now()
            
    def serialize(self):
        obj={"last_date": self.last_date, "account":self.account, "scraper_id":self.scraper_id, "last_updated": datetime.datetime.now()}
        return obj


    def update_date(self, new_last_date):
        self.last_date = new_last_date
        self.collection.find_one_and_update( {"account" : self.account, "scraper_id":self.scraper_id},{"$set": self.serialize()},upsert=True)
