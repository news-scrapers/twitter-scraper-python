from dotenv import load_dotenv
from scrapers.AccountsScraper import AccountScrapper
from models.Config import Config
import os

load_dotenv()


def main():

    print("-----", os.getenv("account_list_file"), os.getenv("scraping_id"), os.getenv("scraper_type"))


    config = Config()

    scraper = AccountScrapper(config)

    while True :
        scraper.scrap_one_day_in_each_account()


if __name__ == '__main__':
	main()