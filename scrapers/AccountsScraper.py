import GetOldTweets3 as got
from models.IndexAccount import IndexAccount
from models.Tweet import Tweet
from datetime import datetime, timedelta
from models.Config import Config
import time

class AccountScrapper:
    def __init__(self, config: Config):
        self.config = config
        self.scraping_id = config.scraping_id
        self.accounts = []
        self.sleep_time_between_requests = 2
        for account_str in config.accounts:
            account = IndexAccount(account_str, self.scraping_id)
            account.get()
            self.accounts.append(account)
            print(account)

    def scrap_one_day_in_each_account(self):
        index = 0
        if (self.config.account_index > len(self.accounts)):
            self.config.account_index = 0
            self.config.update()
            
        print("starting process in url index " +str(self.config.account_index))

        while index < len(self.accounts):
            index = self.config.account_index
            account = self.accounts[index]
            self.scrap_one_day(account)
            index = index + 1
            self.config.account_index = index
            self.config.update()

        self.config.account_index = 0
        self.config.update()

    def scrap_one_day(self, account: IndexAccount):
        date_to = account.last_date
        date_since = date_to - timedelta(days=1)
        
        since = date_since.strftime("%Y-%m-%d")
        until = date_to.strftime("%Y-%m-%d")

        try:
            print("scraping " + account.account + " in period ", since,until)
            tweetCriteria = got.manager.TweetCriteria().setUsername(account.account).setSince(since).setUntil(until)
            tweets = got.manager.TweetManager.getTweets(tweetCriteria)
        except:
            time.sleep(self.sleep_time_between_requests +2)
            print("retrying scraping " + account.account + " in period ", since,until)
            tweetCriteria = got.manager.TweetCriteria().setUsername(account.account).setSince(since).setUntil(until)
            tweets = got.manager.TweetManager.getTweets(tweetCriteria)


        
        print("updating "+ str(len(tweets)) +" tweets")
        for tweet in tweets:
            item = Tweet(tweet, self.scraping_id)
            item.save_or_update()

        account.update_date(date_since)
        time.sleep(self.sleep_time_between_requests)

        

            


#tweetCriteria = got.manager.TweetCriteria().setUsername("realdonaldtrump").setMaxTweets(1)
#tweet = got.manager.TweetManager.getTweets(tweetCriteria)[0]

#print(tweet.__class__())