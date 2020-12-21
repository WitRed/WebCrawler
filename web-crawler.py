import requests
import urllib
from bs4 import BeautifulSoup

def search():
    urlList = []
    newUrlList = []
    articlesList = []

    keyword = input("Aramak istediğiniz haber: ")
    text = urllib.parse.quote_plus(keyword)

    baseUrl = "https://news.google.com/search?q=" + text + "when:1h" + "&hl=tr&gl=TR&ceid=TR%3Atr"

    res = requests.get(baseUrl)

    if res.status_code == 200:
        soup = BeautifulSoup(res.text, 'lxml')

        # haber başlıkları
        for info in soup.find_all("h3"):
            articlesList.append(info.text)

        # haber url'leri
        for url in soup.find_all("a", href=True):
            if url['href'].startswith("./articles"):
                urlList.append(url['href'])

        while urlList:
            newUrls = urlList[0].replace("./articles", "articles")
            newUrlList.append(newUrls)
            urlList.pop(0)

        while newUrlList:
            haberLink = "https://news.google.com/" + newUrlList[0]

            newUrlList.pop(0)

            print(haberLink)


search()