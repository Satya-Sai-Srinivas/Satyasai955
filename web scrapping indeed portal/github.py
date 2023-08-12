import requests
from bs4 import BeautifulSoup


keyword = input("Enter keyword to search : ")

base_url = "https://github.com/search?q="
search_url = base_url+keyword

site_html = requests.get(search_url)
html = site_html.content

soup = BeautifulSoup(html, 'html5lib')
#print(soup.prettify())
project_tile = soup.find_all("div", class_= "mt-n1 flex-auto")
for tile in project_tile:
    title = tile.find("div", class_ = "f4 text-normal")
    desc = tile.find('p', class_ = "mb-1")
    print(title.text.strip())
    print(desc.text.strip())