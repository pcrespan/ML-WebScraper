import requests
import re
import statistics
from bs4 import BeautifulSoup

# Need to look for price-tag-fraction on ML
# The search mechanism will be https://lista.mercadolivre.com.br/firstterm-secondterm
# The spaces are represented by -
# Next button - andes-pagination__link shops__pagination-link ui-search-link

# todo: add global input variable to store
# search link template

class Searcher:
    @staticmethod
    def search():
        search = input("Search: ").strip().lower()
        product = Searcher.format_search(search)
        return product
    
    @staticmethod
    def format_search(search):
        return re.sub(" ", "-", search)


class Scraper:

    @staticmethod
    def send(product):
        # Mimicking browser
        HEADERS = ({'User-Agent':
            'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
            'Accept-Language': 'en-US, en;q=0.5'})
        response = requests.get('https://lista.mercadolivre.com.br/' + product, headers=HEADERS)
        soup = BeautifulSoup(response.content, 'html.parser')
        print(response)
        return soup
        
    @staticmethod
    def get_prices(soup):
        prices = soup.find_all(class_="price-tag-fraction")
        return prices
    
    @staticmethod
    def extract_values(prices):
        for price in prices:
            yield price.text
        
    @staticmethod
    def avg(values):
        sum = 0
        for value in values:
            sum = sum + value
        return sum / len(values)


def main():
    product = Searcher.search()
    soup = Scraper.send(product)
    prices = Scraper.get_prices(soup)
    values = []

    for price in Scraper.extract_values(prices):
        values.append(int((re.sub("\.", "", price))))

    print(sorted(values))
    
    print(f"The average price for {product} is R${Scraper.avg(values)}")


if __name__ == "__main__":
    main()