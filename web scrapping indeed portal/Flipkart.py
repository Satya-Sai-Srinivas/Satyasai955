"""
Packages Required :
BeautifulSoup --> pip install bs4
html5lib --> pip install html5lib
"""

import requests
from bs4 import BeautifulSoup

base_url = """https://www.flipkart.com/search?q=gym+equipment"""
site_html = requests.get(base_url)
html = site_html.content

soup = BeautifulSoup(html, 'html5lib')
#print(soup.prettify())

complete_product_info = soup.find_all('div', class_ = "_13oc-S")

print(len(complete_product_info))
for each_product in complete_product_info:
    title = each_product.find("a", class_ = "s1Q9rs")
    print(title.text)
    try:
        rating = each_product.find("div", class_ = "_3LWZlK")
        print(rating.text)
    except:
        print("No rating")

    try:
        cost = each_product.find("div", class_ = "_30jeq3")
        print(cost.text)
    except:
        print("No cost")
    print("--------------------------------")

