from dotenv import load_dotenv
from scrapers.AccountsScraper import AccountScrapper
from models.Config import Config

load_dotenv()


def main():

    config = Config()

    scraper = AccountScrapper(config.accounts, config)

    while True :
        scraper.scrap_one_day_in_each_account()


if __name__ == '__main__':
	main()