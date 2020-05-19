
import os
from pymongo import MongoClient

class Tweet:
    def __init__(self, tweet, scraper_id):
        self.tweet = tweet
        self.scraper_id = scraper_id

        self.client = MongoClient(os.getenv("database_url"))
        self.db = self.client['tweets-scraping']
        self.collection=self.db.ScrapedTweets

    
    def serialize(self):
        obj={"scraper_id":self.scraper_id, "username":self.tweet.username, "retweets":self.tweet.retweets, "to":self.tweet.to, "text": self.tweet.text, "date":self.tweet.date, "geo": self.tweet.geo, "favorites":self.tweet.favorites,"replies": self.tweet.replies, "permalink":self.tweet.permalink, "author_id": self.tweet.author_id, "id":self.tweet.id}
        return obj


    def save_or_update(self):
        obj = self.serialize()
        self.collection.find_one_and_update( {"id" : obj["id"]},{"$set": obj},upsert=True)