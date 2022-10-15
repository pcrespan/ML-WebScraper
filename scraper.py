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

