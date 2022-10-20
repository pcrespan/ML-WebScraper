import requests
import re
import sys
import logging
from bs4 import BeautifulSoup


# Need to look for price-tag-fraction on ML
# The search mechanism will be https://lista.mercadolivre.com.br/<something>
# The spaces are represented by -
# Next button - andes-pagination__link shops__pagination-link ui-search-link

# todo: ALLOW USER TO SPECIFY HOW MANY PAGES THEY WANT TO SEARCH - done
# todo: DISPLAY LINK AND TITLE FOR MAX AND MIN PRICES


# Configuring logging
logging.basicConfig(level=logging.INFO)

# Global variable to mimic browser behavior
HEADERS = ({'User-Agent':
            'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
            'Accept-Language': 'en-US, en;q=0.5'})

class Searcher:
    @staticmethod
    def search(raw_string):
        # Asking for product
        search = raw_string.strip().lower()
        # Formatting input and returning string
        product = Searcher.format_search(search)
        return product


    # Formats user input
    @staticmethod
    def format_search(search):
        return re.sub(" ", "-", search)


class Scraper:
    # Initializer
    def __init__(self, product, prices=None):
        self.product = product
        self.prices = prices
        # Links for lowest and highest prices
        self.links = [
            'https://lista.mercadolivre.com.br/' + self.product + '_OrderId_PRICE_NoIndex_True',
            'https://lista.mercadolivre.com.br/' + self.product + '_OrderId_PRICE*DESC_NoIndex_True'
        ]
        self.pages = None
        self.page_input = None


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
    def total_pages(self, soup):
        # Finding number of pages
        total_pages = soup.find('li', class_='andes-pagination__page-count')
        # Cleaning text and returning in the form of an integer
        pages = re.search(r'(\d+)', total_pages.text)
        # Waiting for user input. If it's invalid, prompt it again
        return int(pages.group(1))


    # Checks for user input. Returns false for invalid
    # input and True for inputs valid and different from one
    def check_input(self, input, pages):
        # Checking if input is not empty, is not a character
        # and is not bigger than the total amount of pages found
        if input and (input.isalpha() or int(input) <= 0 or int(input) > pages):
            print('Invalid input. Try again.')
            return False
        else:
            # Testing for the case the input is equal 
            # to the default value or empty
            print(input)
            if input == '1' or not input:
                print('Using default value...')
                self.show_prices()
                self.lowest_highest_prices()
                sys.exit(0)
            return True


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
        Scraper.valid_response(response)
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
    
    
    # Possible redundancy
    # Checks for request errors, returns boolean
    @staticmethod
    def valid_response(response):
        match response.status_code:
            case 200:
                logging.info('Success')
            case 404:
                logging.error('Product not found. Exitting...')
                sys.exit(1)
            case 503:
                logging.error('Server error')
                sys.exit(1)
    

    # Prints average price
    def show_prices(self):
        print(f'The average price for {self.product} is R${Scraper.avg(self.prices)}')

    
    # NEEDS BETTER DESIGN
    # Finds max and min prices, prints product information
    def lowest_highest_prices(self):
        print('Lowest and highest prices related to your search: ')
        # Creating dictionary that will store
        # product information
        product_info = {}
        # Iterating through list of links (class attribute)
        for link in self.links:
            # Sending request and returning soup object
            # to search for all the information needed
            soup, response = Scraper.send('', link)
            # Checking HTTP response
            Scraper.valid_response(response)
            # Finding HTML element that contains product
            # information (link and title)
            info = soup.find('a', class_= 'ui-search-result__content ui-search-link')
            product_link = info['href']
            product_title = info['title']
            # Finding div that contains product price
            div = soup.find('div', class_='ui-search-price ui-search-price--size-medium shops__price')
            # Searching inside of div to find span that
            # stores product price and cleaning output
            price_str = div.find('span', class_= 'price-tag-fraction')
            price = int(re.sub('\.', '', price_str.text))
            # Storing product information inside of dict
            product_info = {
                'title': product_title,
                'link': product_link,
                'price': price
            }
            # Printing product info
            print(f'Link: {product_info["link"]}')
            print(f'Product: {product_info["title"]}')
            print(f'Price: {product_info["price"]}')


    # Execute all functions
    def scrape(self):
        product = self.product
        soup, response = Scraper.send(product)
        # Testing HTTP response for first request
        Scraper.valid_response(response)
        # Storing prices of first page
        self.prices = Scraper.get_prices(soup)
        # Storing how many pages the user want
        # to scrape for prices
        pages = self.total_pages(soup)
        # Defining page counter and iterating through 
        # all pages, getting prices of each one
        counter = 1
        Scraper.next_page(soup, self.prices, counter, pages)
        # Getting lowest and highest prices for the product
        # and showing the average price
        self.show_prices()
        self.lowest_highest_prices()


def main():
    product = Searcher.search()
    scraper = Scraper(product)
    scraper.scrape()


if __name__ == "__main__":
    main()