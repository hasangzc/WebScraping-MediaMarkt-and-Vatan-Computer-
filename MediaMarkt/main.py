from bs4 import BeautifulSoup
import requests
import ast  # abstract syntax tree to parse dictionary text
import json

base_url = 'https://www.mediamarkt.com.tr/tr/category/_android-telefonlar-675172.html?searchParams=&sort=&view'
infos = []


def multi_page_urls(base_url):
    urls = []
    page_number = 0
    for i in range(1, 7):
        page_number += 1
        next_page = base_url + "=&page=" + str(page_number)
        urls.append(next_page)
    return urls


for u in multi_page_urls(base_url):
    soup = BeautifulSoup(requests.get(u).text, "html.parser")
    scripts = soup.find_all('script')

    for s in scripts:
        if 'var product' in s.text[0:12]:          # find the script of interest
            d = s.text.split(' = ')[1].strip(';')  # get the product information
            # parse information as dictionary text
            data = ast.literal_eval(d)
            infos.append(data)

product_names = [i["name"] for i in infos]
product_id = [i["id"] for i in infos]
product_price = [i["price"] for i in infos]


for i in range(0, len(product_names)):
    file = json.dumps({"product_id": product_id[i],
                      "product_name": product_names[i],
                      'product_prices': product_price[i]},ensure_ascii=False, indent=3, separators=(',', ':'))
    last_file = file + ","
    print(last_file)
