import tkinter as tk
import scraper
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
    

    def createWidgets(self):
        # Quit button
        self.quitButton = tk.Button(self, text="Quit", command=self.quit)
        self.quitButton.grid()
        # Search field
        searchText = tk.StringVar()
        self.searchField = tk.Entry(self, text='', textvariable=searchText)
        self.searchField.grid()
        # Search button. Only executes command when clicked
        self.searchButton = tk.Button(self, text="Search", command= lambda :scraper.main(searchText.get()))
        self.searchButton.grid()


    
app = MLWebScraper()
app.master.title("MLWebScraper")
app.mainloop() 