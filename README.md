# ML-WebScraper

## Description
ML-WebScraper allows the user to search for specifc products being sold on [Mercado Libre](https://en.wikipedia.org/wiki/Mercado_Libre)'s website using a graphical user interface. Written in Python using mainly `Beautiful Soup`, `Tkinter` and `requests` modules. The program shows the lowest and highest prices related to the search, and also the average price based on number of pages scraped for prices (also provided by the user). Deals with HTTP error codes (404, 500, 503), displaying popup message boxes containing a description for the error. The program also contains a "Search Again" button, which allows a new search for a product without the need of restarting the program.

## DISCLAIMER:
Project made for educational purposes only, I'm not responsible for how the code is used. The mere presence of this code on my profile does not imply that I encourage scraping the website referenced in the code. The source code only help illustrate the technique behind web scraping. Read [Mercado Libre's rules](https://developers.mercadolivre.com.br/pt_br/termos-e-condicoes)

## Usage
Run on terminal on the same directory that the repo's files are:
```
python GUI.py
```
## Pre-requisites
> - Beautiful Soup
```
pip install bs4
```
> - Requests
```
pip install requests
```
