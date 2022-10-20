import tkinter as tk
from scraper import *
from tkinter import *

# (widget).grid_forget() will make it disappear

# You can use (widget).grid() to make it reappear,
# but it won't remember the parameters of it

# Instead of grid_forget(), use grid_remove(), because
# it will remember all of the parameters

class MLWebScraper(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.pack()
        self.createWidgets()

    def exec(self, searchText):
        scraper = Scraper(str(searchText.get()))   
        soup, response = Scraper.send(str(searchText.get()))
        Scraper.valid_response(response)
        # After executed, create new widgets
        page_number = tk.StringVar()
        text_label = tk.StringVar()
        scraper.pages = scraper.total_pages(soup)
        scraper.prices = scraper.get_prices(soup)

        self.pageLabel = tk.Label(self, text = text_label.set(f"Found {scraper.pages} pages. How many should be scraped? (Default: 1)"), textvariable = text_label)
        self.pageField = tk.Entry(self, text = "", textvariable = page_number)
        self.pageButton = tk.Button(self, text = "Select", command = lambda : self.validate_input(scraper, page_number, soup, text_label))

        self.pageLabel.grid()
        self.pageField.grid()
        self.pageButton.grid()


    def validate_input(self, scraper, page_number, soup, text_label, counter = 1):
        scraper.page_input = page_number.get()
        while True:
            if scraper.check_input(page_number.get(), scraper.pages):
                self.pageLabel.grid_remove()
                self.pageField.grid_remove()
                self.pageButton.grid_remove()
                Scraper.next_page(soup, scraper.prices, counter, int(scraper.page_input))
                scraper.show_prices()
                scraper.lowest_highest_prices()
                break
            else:
                text_label.set("Invalid input. Try again.")
                break


    def createWidgets(self):
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