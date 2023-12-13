from types import NoneType
import csv

import requests
from bs4 import BeautifulSoup as bs


class Parser:

    def __init__(self, search: str) -> None:
        self.search = search
        self.url = "https://www.olx.ua/list/q-" + self.search

    def __createRequest(self, url) -> bs:
        self.page = requests.get(url).content
        self.bs = bs(self.page, "lxml")
        return self.bs

    def __pagination(self) -> int:
        pagination = self.__createRequest(self.url).findAll("li", class_ = "pagination-item")
        return int(pagination[-1].text)

    def __parse(self) -> list:
        items = []
        pag = self.__pagination()
        for page in range(1, pag+1):
            self.url = "https://www.olx.ua/list/q-" + self.search + "/?page=" + str(page)
            for elem in self.__createRequest(self.url).findAll("div", class_ = "css-1sw7q4x"):
                try:
                    if elem.find("p", class_ = "er34gjf0") is not None:
                        if elem.find("h6", class_ = "er34gjf0").text is not None:
                            items.append({
                                "title": elem.find("h6", class_ = "er34gjf0").text,
                                "price": elem.find("p", class_ = "er34gjf0").text,
                                "link": "https://olx.ua" + elem.find("a", class_ = "css-rc5s2u").get("href")
                            })
                except NoneType:
                    pass

        return items

    def writetocsv(self):
        with open(f"{self.search}.csv", "w", encoding="utf-8") as file:
            writer = csv.writer(file, quoting=csv.QUOTE_MINIMAL)
            writer.writerow(("Title", "Price", "Link"))
            for product in self.__parse():
                writer.writerow((product['title'], product['price'], product['link']))

        print("Successfully!")


search = str(input("Enter what you want to search >>> "))
t = Parser(search)
t.writetocsv()





