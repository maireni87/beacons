import requests
from bs4 import BeautifulSoup
import urllib2
import io

def trade_spider(max_pages):
    page = 1
    while page <= max_pages:
        url = 'https://newjersey.craigslist.org/search/sss?s=' + str(page)
        source_code = requests.get(url)
        plain_text = source_code.text
        soup = BeautifulSoup(plain_text, 'lxml')
        for link in soup.findAll('a',{'class':'hdrlnk'}):
            href = "https://newjersey.craigslist.org/search/sss?s=100" + link.get('href')
            title = link.text
            #print(href)
            #print(title)
            get_single_item_data(href)
        page += 1

    trade_spider(1)
   
def writing_function():
    with open('c:\Python\gitHub\Beacons\Beaconapp\src\Scraper\craigslistfree.txt', 'a') as f:
        for ind, i in enumerate(soup.find_all('div', {'class': 'hdrlnk'}),1):
            f.write("{}. {}".format(ind, i.text.replace("\n","")))

