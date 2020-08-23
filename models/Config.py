
import os
import datetime
from pymongo import MongoClient
import json

class Config:
    def __init__(self):
        client = MongoClient(os.getenv("database_url"))
        db = client['tweets-scraping']
        self.scraping_id = None
        self.accounts = None
        self.scraperType = "accounts"
        self.account_list_file = None
        self.account_index = 0
        self.collection=db.Config
        self.load_from_env()
        self.refresh()


    def load_from_env(self):
        self.account_list_file = os.getenv("account_list_file")
        self.scraping_id = os.getenv("scraping_id")
        self.scraper_type = os.getenv("scraper_type")
        print("-----", os.getenv("account_list_file"), os.getenv("scraping_id"), os.getenv("scraper_type"))
        if self.scraper_type == None:
            self.scraperType = "accounts"

        if not self.account_list_file == None:
            with open('./account_lists/'+ self.account_list_file , 'r') as f:
                accounts = json.load(f)
                print("scraping list:")
                print(accounts)
                self.accounts = accounts


    def refresh(self):
        result = self.collection.find_one({"scraping_id":self.scraping_id})
        if not result == None:
            self.load_from_dict(result)


    def load_from_dict(self, result):
        self.accounts = result["accounts"]
        self.scraping_id = result["scraping_id"]
        self.account_index = result["account_index"]
        self.account_list_file = result["account_list_file"]

    def update(self):
        self.collection.find_one_and_update( {"scraping_id" : self.scraping_id},{"$set": self.serialize()},upsert=True)

    def serialize(self):
        obj = {"accounts": self.accounts, "account_index":self.account_index, "last_updated":datetime.datetime.now(),"scraping_id":self.scraping_id,  "account_list_file":self.account_list_file}
        return obj
