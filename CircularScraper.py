from bs4 import BeautifulSoup
import requests

class CircularScraper:
    def scraper():
        page = requests.get('https://www.gtu.ac.in/Circular.aspx').text
        soup = BeautifulSoup(page, 'lxml')
        event_list = soup.find_all("div", class_ = "event-list")
        mainDict = {}
        x = 0
        for event in event_list:
            try:
                date = event.find("div", class_="date-in").text.replace("\n", "")
                titleTag = event.find('div', class_="text")
                title = titleTag.find('a').contents[0]
                link = titleTag.find('a')['href'].replace(" ", "%20")
            except Exception:
                date = "Date Not Found"
                title = "Title Not Found"
                link = "Link Not Found"

            mainDict[x] = {"date":date,
                "title":title,
                "link":link}
            x+=1
        return mainDict

# print(CircularScraper.scraper())