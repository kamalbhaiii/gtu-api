from bs4 import BeautifulSoup
import requests

class ResultListScraper:
    def scraper():
        page = requests.get("https://www.gtu.ac.in/result.aspx").text

        mainDict = {}

        soup = BeautifulSoup(page, "lxml")
        event_list = soup.find_all("div", class_="event-list")
        x = 1
        for event in event_list:
            try:
                date = event.find("div",class_="date-in").text
                title = event.find("h3", class_="Content").text
                link = event.find("a")["href"]
            except Exception:
                link = "Link not available"

            dataDict = {
                "date":date,
                "title":title,
                "link":link
            }

            mainDict[x] = dataDict
            x += 1

        return mainDict