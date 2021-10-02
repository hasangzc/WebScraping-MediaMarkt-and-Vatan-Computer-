import requests
from bs4 import BeautifulSoup

base_url = "https://www.vatanbilgisayar.com"

response = requests.get("https://www.vatanbilgisayar.com/cep-telefonu-modelleri/")
vatan_web_page = response.text
# print(vatan_web_page)
soup = BeautifulSoup(vatan_web_page, "html.parser")
# price = soup.find(name="span", class_= "product-list__price").getText()

prices_first_page = [price.getText() for price in soup.find_all(name="span", class_= "product-list__price")]
print(prices_first_page)

page_all = soup.find_all(name="a", class_='pagination__content')
# print(page_all)

pages = []

for page in page_all:
    link = page.get("href")
    pages.append(link)

print(pages)



"""def get_next_page(soup):
    pages = []
    urls = []
    page_all = soup.find_all(name="a", class_='pagination__content')
    for page in page_all:
        link = page.get("href")
        pages.append(link)
        print(pages)

    for i in pages:
        new_url = base_url + str(i)
        urls.append(new_url)

    print(urls)
get_next_page(soup)

"""
