import tkinter as tk
from xml.dom.minidom import Attr
from scraper import *
from tkinter import *
import webbrowser

# (widget).grid_forget() will make it disappear

# You can use (widget).grid() to make it reappear,
# but it won't remember the parameters of it

# Instead of grid_forget(), use grid_remove(), because
# it will remember all of the parameters


class MLWebScraper(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.pack()
        self.createSearchWidgets()


    def exec(self, searchText):
        product = Searcher.search(str(searchText.get()))
        scraper = Scraper(product)   
        soup, response = Scraper.send(str(searchText.get()))

        if response.status_code == 200:
            self.searchField.grid_forget()
            self.searchButton.grid_remove()
            pass
        else:
            return

        valid, msg = Scraper.valid_response(response)
        try:
            if not valid and self.errorLabel:
                return
            # Need to add the case when it's valid and there's a server error
            else:
                try:
                    self.errorLabel.grid_remove()
                    pass
                except AttributeError:
                    pass
        except AttributeError:
            self.errorLabel = tk.Label(self, text = msg)
            self.errorLabel.grid()
            return

        # After executed, create new widgets
        self.createPageWidgets(scraper, soup)


    def createPageWidgets(self, scraper, soup):
        page_number = tk.StringVar()
        text_label = tk.StringVar()
        scraper.pages = scraper.total_pages(soup)
        scraper.prices = scraper.get_prices(soup)

        try:
            if self.pageButton and self.pageField and self.pageLabel:
                pass
        except AttributeError:
            self.pageLabel = tk.Label(self, text = text_label.set(f"Found {scraper.pages} pages. How many should be scraped? (Default: 1)"), textvariable = text_label)
            self.pageField = tk.Entry(self, text = "", textvariable = page_number)
            self.pageButton = tk.Button(self, text = "Select", command = lambda : self.scrape(scraper, page_number, soup, text_label))

            self.pageLabel.grid()
            self.pageField.grid()
            self.pageButton.grid()


    @staticmethod
    def callback(url):
        webbrowser.open_new(url)


    def validate_input(self, scraper, page_number):
        scraper.page_input = page_number.get()
        if scraper.check_input(page_number.get(), scraper.pages):
            return True
        else:
            return False


    def scrape(self, scraper, page_number, soup, text_label, counter = 1):
        while True:
            match self.validate_input(scraper, page_number):
                case 0:
                    self.hideWidgets()
                    Scraper.next_page(soup, scraper.prices, counter, int(scraper.page_input))
                    self.getLowHighPrices(scraper)
                    # Add search again button
                    break
                case -1:
                    text_label.set("Invalid input. Try again.")
                    break
                case 1:
                    self.hideWidgets()
                    self.getLowHighPrices(scraper)
                    break

    
    def hideWidgets(self):
        self.searchField.grid_remove()
        self.searchButton.grid_remove()
        self.pageLabel.grid_remove()
        self.pageField.grid_remove()
        self.pageButton.grid_remove()


    def getLowHighPrices(self, scraper):
        labelList = []
        links = []
        productList = scraper.lowest_highest_prices()

        for product in productList:
            title = f"Product: {product['title']}\n"
            price = f"Price: R${product['price']}\n"
            completeString = title + price
            labelList.append(completeString)
            links.append(product["link"])

        self.createPriceWidgets(links, labelList, scraper)
    

    def createPriceWidgets(self, links, labelList, scraper):
        self.lowestPrice = tk.Label(self, text=labelList[0])
        self.lowestPriceLink = tk.Label(self, text = "Link", cursor = "hand2")
        self.lowestPriceLink.bind("<Button-1>", lambda event: self.callback(links[0]))
        
        self.highestPrice = tk.Label(self, text=labelList[1])
        self.highestPriceLink = tk.Label(self, text = "Link", cursor = "hand2")
        self.highestPriceLink.bind("<Button-1>", lambda event: self.callback(links[1]))

        self.avgPrice = tk.Label(self, text = f"The average price for {scraper.product} is R${Scraper.avg(scraper.prices):.2f}")
        self.avgPrice.grid()

        self.lowestPrice.grid()
        self.lowestPriceLink.grid()
        self.highestPrice.grid()
        self.highestPriceLink.grid()


    def createSearchWidgets(self):
        # Quit button
        self.quitButton = tk.Button(self, text="Quit", command = self.quit)
        self.quitButton.grid()
        # Search field
        searchText = tk.StringVar()
        self.searchField = tk.Entry(self, text="", textvariable = searchText)
        self.searchField.grid()
        # Search button. Only executes command when clicked
        self.searchButton = tk.Button(self, text="Search", command = lambda : self.exec(searchText))
        self.searchButton.grid()

 
app = MLWebScraper()
app.master.title("MLWebScraper")
app.mainloop() 