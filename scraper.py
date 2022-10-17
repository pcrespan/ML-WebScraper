import requests
import re
import sys
import logging
from bs4 import BeautifulSoup

# Host on Heroku or PythonAnywhere - in the case the user wants to use the "remind me" function
# Need to look for price-tag-fraction on ML
# The search mechanism will be https://lista.mercadolivre.com.br/<something>
# The spaces are represented by -
# Next button - andes-pagination__link shops__pagination-link ui-search-link

# todo: ALLOW USER TO SPECIFY HOW MANY PAGES THEY WANT TO SEARCH
# todo: SEARCH FOR MINIMUM AND MAXIMUM PRICES
# todo: DISPLAY LINK AND TITLE FOR FOUND RESULTS
# todo: ALLOW TO SEARCH BY REVIEWS
# search link template

# Configuring logging
logging.basicConfig(level=logging.INFO)

# Global variable to mimic browser behavior
HEADERS = ({'User-Agent':
            'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
            'Accept-Language': 'en-US, en;q=0.5'})

class Searcher:
    @staticmethod
    def search():
        # Asking for product
        search = input("Search: ").strip().lower()
        # Formatting input and returning string
        product = Searcher.format_search(search)
        return product
    
    # Formats user input
    @staticmethod
    def format_search(search):
        return re.sub(" ", "-", search)


class Scraper:
    # Sends request for specific link, returns soup object
    @staticmethod
    def send(product='', link='https://lista.mercadolivre.com.br/'):
        # Sending GET request for a specific link, default value
        # is the first page of any product that the user inputs
        response = requests.get(link + product, headers=HEADERS)
        # Default value of response is its code (200, 404 etc),
        # using BeautifulSoup to parse its actual content and
        # find specific elements on the page
        soup = BeautifulSoup(response.content, 'html.parser')
        print(response)
        # Returning soup object
        return soup, response


    # Gets all the prices of the current page, returns a list
    @staticmethod
    def get_prices(soup):
        # Searching for all divs with main price, returns a list with soup objects
        divs = soup.find_all('div', class_='ui-search-price ui-search-price--size-medium shops__price')
        # Creating empty list to store prices and declaring empty
        # string to store raw soup object
        prices = []
        price_str = ''
        # Iterating through list of divs (soup objects)
        # and extracting the text of each one (price itself),
        # appending to prices list
        for div in divs:
            price_str = div.find('span', class_='price-tag-fraction')
            prices.append(int(re.sub('\.', '', price_str.text)))
        # Returning list with all prices of the current page
        return prices
    

    # Finds the total number of pages, returns an integer
    @staticmethod
    def total_pages(soup):
        # Finding number of pages
        total_pages = soup.find('li', class_='andes-pagination__page-count')
        # Cleaning text and returning in the form of an integer
        pages = re.search(r'(\d+)', total_pages.text)
        return int(pages.group(1))
        

    # Calculates average price, returns a float
    @staticmethod
    def avg(values):
        sum = 0
        for value in values:
            sum = sum + value
        return sum / len(values)
    

    # Navigates through next pages, returns list of prices
    @staticmethod
    def next_page(soup, values, counter, pages):
        # Getting the link for next page, sending request
        # to it and returning soup object that will look for prices
        link = Scraper.get_btn_link(soup)
        soup, response = Scraper.send('', link)
        # Checking if HTTP response is valid
        if Scraper.valid_response(response):
            pass
        else:
            sys.exit(1)
        # get_prices returns a list of prices of each page - one at a time - 
        # and the for loop appends each element to the existing list values
        for value in Scraper.get_prices(soup):
            values.append(value)
        # Increasing counter that represent the page number
        counter += 1
        # Checking if all pages have been scraped, if not, call function
        # to check for prices on the next page. Pages minus one because
        # it already scraped the prices from the first page
        if counter <= pages - 1:
            Scraper.next_page(soup, values, counter, pages)
        # Return list of prices
        return sorted(values)
            
    # Captures link for next page, returns string
    @staticmethod
    def get_btn_link(soup):
        # Finding 'next page' button
        btn = soup.find('a', class_='andes-pagination__link shops__pagination-link ui-search-link')
        # Storing link for next page
        link = btn['href']
        return link
    
    
    # Checks for request errors, returns boolean
    @staticmethod
    def valid_response(response):
        match response.status_code:
            case 200:
                logging.info('Success')
                return True
            case 404:
                logging.error('Product not found. Exitting...')
                return False
            case 503:
                logging.error('Server error')
                return False
    

    @staticmethod
    def scrape():
        # Defining page counter
        counter = 1

        product = Searcher.search()
        soup, response = Scraper.send(product)

        # Testing HTTP response for first request
        if Scraper.valid_response(response):
            pass
        else:
            sys.exit(1)

        pages = Scraper.total_pages(soup)
        page_amount = input(f'Found {pages} pages. How many of them should be scraped for prices? (Default: 1) ').strip()

        # Also need to test if user inputted text
        if not page_amount:
            page_amount = 1

        page_amount = int(page_amount) - 1
        prices = Scraper.get_prices(soup)
        # Automatically tests for HTTP response on every next page
        print(Scraper.next_page(soup, prices, counter, page_amount))
        print(f"The average price for {product} is R${Scraper.avg(prices)}")


def main():
    Scraper.scrape()


if __name__ == "__main__":
    main()