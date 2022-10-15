import requests
import re
from bs4 import BeautifulSoup

# Need to look for price-tag-fraction on ML
# The search mechanism will be https://lista.mercadolivre.com.br/firstterm-secondterm
# The spaces are represented by -

class Searcher:
    @staticmethod
    def search():
        search = input("Search: ").strip().lower()
        product = Searcher.format_search(search)
        return product
    
    @staticmethod
    def format_search(search):
        return re.sub(" ", "-", search)


class Scraper(Searcher):

    @staticmethod
    def send(product):
        response = requests.get('https://lista.mercadolivre.com.br/' + product)
        soup = BeautifulSoup(response.content, 'html.parser')
        return soup
        
    @staticmethod
    def get_prices(soup):
        prices = soup.find_all(class_='price-tag-fraction')
        return prices
    
    @staticmethod
    def extract_values(prices):
        for price in prices:
            print(price.text)


def main():
    product = Searcher.search()
    soup = Scraper.send(product)
    prices = Scraper.get_prices(soup)
    Scraper.extract_values(prices)


if __name__ == "__main__":
    main()