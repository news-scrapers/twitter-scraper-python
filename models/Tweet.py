
import os
from pymongo import MongoClient

class Tweet:
    def __init__(self, tweet):
        self.tweet = tweet

        self.client = MongoClient(os.getenv("database_url"))
        self.db = self.client['tweets']
        self.collection=self.db.ScrapedTweets

    
    def serialize(self):
        obj={"text": self.tweet.text, "date":self.tweet.date, "geo": self.tweet.geo, "favorites":self.tweet.favorites,"replies": self.tweet.replies, "permalink":self.tweet.permalink, "author_id": self.tweet.author_id, "id":self.tweet.id}
        return obj


    def save_or_update(self):
        obj = self.serialize()
        self.collection.find_one_and_update( {"id" : obj["id"]},{"$set": obj},upsert=True)