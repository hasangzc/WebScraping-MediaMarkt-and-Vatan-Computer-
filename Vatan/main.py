import requests
from bs4 import BeautifulSoup
import itertools
import json

base_url = "https://www.vatanbilgisayar.com/cep-telefonu-modelleri"


def multi_page_urls(base_url):
        urls = []
        page_number = 0
        for i in range(1, 13):
            page_number += 1
            next_page = base_url + "/?page=" + str(page_number)
            urls.append(next_page)
        return urls


def price_list(url_func):
    product_prices = []
    for u in url_func:
        soup = BeautifulSoup(requests.get(u).text, "html.parser")
        prices = [price.getText() for price in soup.find_all(name="span", class_="product-list__price", )]
        for i in range(10, len(prices)):
            product_prices.append(prices[i])
    return product_prices


# print(price_list(multi_page_urls(base_url)))

def id_list(url_func):
    product_ids = []
    for u in url_func:
        soup = BeautifulSoup(requests.get(u).text, "html.parser")
        ids = [id.getText() for id in soup.find_all(name="div", class_="product-list__product-code")]
        product_ids.append(ids)
    return product_ids

#print(id_list(multi_page_urls(base_url)))


output_ids = []


def reemovNestings(l):
    for i in l:
        if type(i) == list:
            reemovNestings(i)
        else:
            output_ids.append(i)
    return output_ids

# print(reemovNestings(id_list(multi_page_urls(base_url))))


def name_list(url_func):
    duplicate_product_names = []
    product_names = []
    for u in url_func:
        soup = BeautifulSoup(requests.get(u).text, "html.parser")
        all_names = soup.find_all(name="img", class_="owl-lazy")
        duplicate_names = [name.get("alt") for name in all_names]
        duplicate_product_names.append(duplicate_names)
        duplicate_all_product_names = itertools.chain.from_iterable(duplicate_product_names)

        for name in duplicate_all_product_names:
            if name not in product_names:
                product_names.append(name)
    return product_names

# print(name_list(multi_page_urls(base_url)))
# print(name_list(multi_page_urls(base_url))[0])
# data = []


for i in range(0, len(name_list(multi_page_urls(base_url)))):
    file = json.dumps({"product_id": reemovNestings(id_list(multi_page_urls(base_url)))[i].replace('\n', ""),
                      "product_name": name_list(multi_page_urls(base_url))[i],
                      'product_prices': price_list(multi_page_urls(base_url))[i]}, ensure_ascii=False, indent=3, separators=(',', ':'))
    last_file = file + ","
    print(last_file)

