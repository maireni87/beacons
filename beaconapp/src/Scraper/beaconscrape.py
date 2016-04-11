from lxml import html
import requests
from bs4 import BeautifulSoup
import json

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
            print(href)
            #print(title)
        page += 1

        tabs = []

for table in tables:
    tab = []
    for row in table:
        for col in row:
            var = col.text_content()
            var = var.strip().replace(" ", "")
            var = var.split('\n')
            if regular_expression.match('^\d{4}$', var[0].strip()):
                tab_row = {}
                tab_row["data-pid"] = var[0].strip()

json_data = json.dumps(row)

output = open("beaconscraper.txt", "w")
output.write(json_data)
output.close()

trade_spider(1)

