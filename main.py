from dotenv import load_dotenv
from scrapers.AccountsScraper import AccountScrapper

load_dotenv()


def main():
    scraper = AccountScrapper(["realdonaldtrump"])
    

if __name__ == '__main__':
	main()