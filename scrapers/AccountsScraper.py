import GetOldTweets3 as got
from models.IndexAccount import IndexAccount
from models.Tweet import Tweet
from datetime import datetime, timedelta

class AccountScrapper:
    def __init__(self, accounts):
        self.accounts = []
        for account_str in accounts:
            account = IndexAccount(account_str)
            account.get()
            self.accounts.append(account)
            print(account)
        self.scrap_one_day(self.accounts[0])

    def scrap_one_day(self, account: IndexAccount):
        date_to = account.last_date
        date_since = date_to - timedelta(days=1)
        
        since = date_since.strftime("%Y-%m-%d")
        until = date_to.strftime("%Y-%m-%d")
        print("scraping " + account.account + " in period ", since,until)
        tweetCriteria = got.manager.TweetCriteria().setUsername(account.account).setSince(since).setUntil(until)
        tweets = got.manager.TweetManager.getTweets(tweetCriteria)
        
        for tweet in tweets:
            print("updating tweet ", tweet)
            item = Tweet(tweet)
            item.save_or_update()

        account.update_date(date_since)

            


#tweetCriteria = got.manager.TweetCriteria().setUsername("realdonaldtrump").setMaxTweets(1)
#tweet = got.manager.TweetManager.getTweets(tweetCriteria)[0]

#print(tweet.__class__())