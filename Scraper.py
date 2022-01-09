from bs4 import BeautifulSoup
import requests
import json

class Scraper:
    def scraper():
        page = requests.get('https://www.gtu.ac.in/Circular.aspx').text
        soup = BeautifulSoup(page, 'lxml')
        event_list = soup.find_all("div", class_ = "event-list")
        mainDict = {}
        x = 1
        for event in event_list:
            try:
                date = event.find("div", class_="date-in").text.replace("\n", "")
                titleTag = event.find('div', class_="text")
                title = titleTag.find('a').contents[0]
                link = titleTag.find('a')['href'].replace(" ", "%20")
                eventDict = {
                "date":date,
                "title":title,
                "link":link
                }
            except Exception:
                date = "Date Not Found"
                title = "Title Not Found"

            mainDict[x] = eventDict
            x+=1
        # mainDictJSON = json.dumps(mainDict)
        # with open("data.json", "w") as fd:
        #     fd.write(mainDictJSON)
        return mainDict