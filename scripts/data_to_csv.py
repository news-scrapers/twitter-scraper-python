from pymongo import MongoClient
import os
import pandas as pd

from dotenv import load_dotenv
load_dotenv()

output = "./data"

def main():
    client = MongoClient(os.getenv("database_url"))
    db = client['tweets-scraping']
    collection=db.ScrapedTweets

    scraping_id = "scraper_asociaciones"

    results = collection.find( {"scraper_id" : scraping_id})

    print(results)

    df =  pd.DataFrame(list(results))
    df['text'] = df['text'].replace(';',' ', regex=True)

    df.to_csv(output + "-" + scraping_id + ".csv", sep=";")
    print(df)

if __name__ == '__main__':
	main()