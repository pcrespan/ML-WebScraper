import tkinter as tk
import tkinter
from scraper import *
from tkinter import *
from tkinter import messagebox
import webbrowser

# (widget).grid_forget() will make it disappear

# You can use (widget).pack() to make it reappear,
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

        valid, msg = Scraper.valid_response(response)
        if not valid:
            tkinter.messagebox.showerror(title="Error", message=msg)
            return

        self.searchField.pack_forget()
        self.searchButton.pack_forget()

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
            self.pageButton = tk.Button(self, text = "Select", command = lambda : self.scrape(scraper, page_number, soup))
            self.pageLabel.pack_forget()
            self.pageField.pack_forget()
            self.pageButton.pack_forget()

            self.quitButton.pack(padx=5, pady=10, side=tk.BOTTOM)
            self.pageLabel.pack(padx=2, pady=40)
            self.pageField.pack(padx=5)
            self.pageButton.pack(padx=5, pady=10, side=tk.BOTTOM)


    @staticmethod
    def callback(url):
        webbrowser.open_new(url)


    def scrape(self, scraper, page_number, soup, counter = 1):
        while True:
            match scraper.check_input(page_number.get(), scraper.pages):
                case 0:
                    self.hideWidgets()
                    Scraper.next_page(soup, scraper.prices, counter, int(page_number.get()))
                    self.getLowHighPrices(scraper)
                    self.searchAgain = tk.Button(self, text="Search again", command= lambda :self.searchAgain_func())
                    self.searchAgain.pack(pady=10)
                    # Add search again button
                    break
                case -1:
                    tkinter.messagebox.showerror(title="Error", message="Invalid input. Try again.")
                    break
                case 1:
                    self.hideWidgets()
                    self.getLowHighPrices(scraper)
                    self.searchAgain = tk.Button(self, text="Search again", command= lambda :self.searchAgain_func())
                    self.searchAgain.pack()
                    break

    def searchAgain_func(self):
        self.quitButton.pack_forget()
        self.avgPrice.pack_forget()
        self.lowestPrice.pack_forget()
        self.lowestPriceLink.pack_forget()
        self.highestPrice.pack_forget()
        self.highestPriceLink.pack_forget()
        self.searchAgain.pack_forget()

        # Re-creating search widgets
        self.createSearchWidgets()

    
    def hideWidgets(self):
        self.searchField.pack_forget()
        self.searchButton.pack_forget()
        self.pageLabel.pack_forget()
        self.pageField.pack_forget()
        self.pageButton.pack_forget()

        del self.searchField
        del self.searchButton
        del self.pageLabel
        del self.pageField
        del self.pageButton


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
        self.avgPrice.pack()

        self.lowestPrice.pack()
        self.lowestPriceLink.pack()
        self.highestPrice.pack()
        self.highestPriceLink.pack()


    def createSearchWidgets(self):
        # Quit button
        self.quitButton = tk.Button(self, text="Quit", command = self.quit)
        self.quitButton.pack(padx=8, pady=15, side=tk.RIGHT)
        # Search field
        searchText = tk.StringVar()
        self.searchField = tk.Entry(self, text="", textvariable = searchText)
        self.searchField.pack(padx=5, pady=100, side=tk.LEFT)
        # Search button. Only executes command when clicked
        self.searchButton = tk.Button(self, text="Search", command = lambda : self.exec(searchText))
        self.searchButton.pack(padx=5, pady=100, side=tk.LEFT)

 
app = MLWebScraper()
app.master.title("MLWebScraper")
app.mainloop() 