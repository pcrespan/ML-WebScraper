import requests
import re
from bs4 import BeautifulSoup

# Need to look for price-tag-fraction on ML
# The search mechanism will be https://lista.mercadolivre.com.br/firstterm-secondterm
# The spaces are represented by -
# Next button - andes-pagination__link shops__pagination-link ui-search-link

# todo: add global input variable to store
# search link template

HEADERS = ({'User-Agent':
            'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
            'Accept-Language': 'en-US, en;q=0.5'})

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
        response = requests.get('https://lista.mercadolivre.com.br/' + product, headers=HEADERS)
        soup = BeautifulSoup(response.content, 'html.parser')
        total_pages = soup.find('li', class_='andes-pagination__page-count')
        pages = re.search(r'(\d)', total_pages.text)
        print(response)
        return soup, int(pages.group(1))
        
    @staticmethod
    def get_prices(soup):
        prices = soup.find_all(class_="price-tag-fraction")
        return prices
    
    @staticmethod
    def extract_values(prices):
        for price in prices:
            yield int(re.sub('\.', '', price.text))
        
    @staticmethod
    def avg(values):
        sum = 0
        for value in values:
            sum = sum + value
        return sum / len(values)
    
    @staticmethod
    def next_page(soup, values, counter, pages):
        link = Scraper.get_btn_link(soup)
        if link:
            response = requests.get(link, headers=HEADERS)
            soup = BeautifulSoup(response.content, 'html.parser')
            prices = Scraper.get_prices(soup)
            for value in Scraper.extract_values(prices):
                values.append(value)
            counter += 1
            if counter <= pages:
                Scraper.next_page(soup, values, counter, pages)
        return values
            
    
    @staticmethod
    def get_btn_link(soup):
        btn = soup.find('a', class_='andes-pagination__link shops__pagination-link ui-search-link')
        link = btn['href']
        return link


def main():
    product = Searcher.search()
    soup, pages = Scraper.send(product)
    prices = Scraper.get_prices(soup)
    values = []

    for price in Scraper.extract_values(prices):
        values.append(price)

    print(sorted(values))
    
    print(f"The average price for {product} is R${Scraper.avg(values)}")

    val = []
    counter = 1
    print(sorted(Scraper.next_page(soup, val, counter, pages)))

    # While next_page doesn't return False/None, do the loop and get the prices


if __name__ == "__main__":
    main()