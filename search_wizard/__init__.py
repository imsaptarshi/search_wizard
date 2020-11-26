import requests
from bs4 import BeautifulSoup
import pandas as pd


class SearchWizard:
    config = {
        "base": "https://www.google.com/search?q=",
        "query": None,
        "format": "json"
    }

    search_results = []

    def __init__(self, query: str = None):
        if not query == None:
            self.config["query"] = query

    def get_config(self) -> dict:
        return self.config

    def get_results(self, query: str = None, flag: str = None) -> list:

        if not query == None:
            self.config["query"] = query

        if not self.config["query"] == None:

            r = requests.get(self.config["base"]+self.config["query"])
            htmlContent = r.content

            soup = BeautifulSoup(htmlContent, "html.parser")

            titles = soup.find_all("h3", class_="zBAuLc")
            descriptions = soup.find_all('div', class_="BNeawe s3v9rd AP7Wnd")
            urls = soup.find_all("div", class_="kCrYT")

            for title, description, url in zip(titles, descriptions, urls):

                description = description.get_text().replace(u"\xa0", "")

                try:
                    url = str(url.find("a")["href"])
                except:
                    url = "NaN"

                self.search_results.append(
                    {
                        "title": title.get_text(),
                        "description": description if description.find("...") == -1 else description[:description.find("...")+3],
                        "url": url[7:url.find("&sa")]
                    }
                )

            if not flag == None:
                if flag == "head":
                    return self.search_results[:3]
                elif flag == "tail":
                    return self.search_results[len(self.search_results)-3:]
            else:
                return self.search_results
        else:
            raise Exception(
                "QueryNotFound: Try mentioning the search query before using.\nHint: SearchWizard(query) or SearchWizard().get_results(query)")

    def prettify(self, flag=None):
        if not self.config["query"] == None:
            if not flag == None:
                if flag == "head":
                    print(pd.DataFrame(self.get_results(flag="head")))
                elif flag == "tail":
                    print(pd.DataFrame(self.get_results(flag="tail")))
            else:
                print(pd.DataFrame(self.get_results()))
        else:
            raise Exception(
                "QueryNotFound: Try mentioning the search query before using.\nHint: SearchWizard(query) or SearchWizard().get_results(query)")
