import requests
import re
from bs4 import BeautifulSoup

# Need to look for price-tag-fraction on ML
# The search mechanism will be https://lista.mercadolivre.com.br/firstterm-secondterm
# The spaces are represented by -

search = input("What do you want to search for? ").strip().lower()
print(search)

lst = []

product = re.sub(" ", "-", search)
print(product)

response = requests.get('https://lista.mercadolivre.com.br/' + product)

soup = BeautifulSoup(response.content, 'html.parser')

# To search by class, use find_all(class_='something')
prices = soup.find_all(class_='price-tag-fraction')

# Extracting text from HTML
for price in prices:
    print(price.text)