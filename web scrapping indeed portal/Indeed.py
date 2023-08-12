import requests
from bs4 import BeautifulSoup
import pandas as pd
import sqlite3

class Indeed:


    def __init__(self):
        self.keyword = input("Enter keyword to search : ")
        self.title = []
        self.location =  []
        self.salary = []
        self.posted_on = []
        self.company_name = []

    def Scrap_indeed(self, page_count = 5):
        for page in range(0,page_count*10+1, 10):
            page_url = f'''https://in.indeed.com/jobs?q={self.keyword}&l=Hyderabad%2C%20Telangana&start={page}'''
            site_html = requests.get(page_url)
            html = site_html.content
            soup = BeautifulSoup(html, 'html5lib')
            print("Extracting info of page : ", page//10 + 1)
            self.Scrap_page(soup)

    def Scrap_page(self, soup):
        tile_data = soup.find_all("div", class_="job_seen_beacon")
        print("Website Scraped and Saved in Html")
        for each_tile in tile_data:
            self.title.append(each_tile.find("h2", "jobTitle").text)
            self.location.append(each_tile.find("div", class_="companyLocation").text)
            try:
                self.company_name.append(each_tile.find("span", class_ = "companyName").text)
            except:
                self.company_name.append("-")
            try:
                self.salary.append(each_tile.find("div", class_="salary-snippet").text)
            except:
                self.salary.append("-")
            self.posted_on.append(each_tile.find("span", class_="date").text)

    def get_posted_day(self):
        self.posted_in_day = []
        for text in self.posted_on:
            number = ''
            for char in text:
                if char.isdigit():
                    number += char
            try:
                self.posted_in_day.append(int(number))
            except:
                self.posted_in_day.append(100)

    def save_results(self, file_name = "indeed_data", format = "csv"):
        mydata = pd.DataFrame(list(zip(self.title, self.company_name, self.location, self.salary, self.posted_on, self.posted_in_day)),
                              columns=["Title", "Company Name", "Location", "Salary", "Posted on", "day"])
        mydata.sort_values(by = ["day"], inplace=True)
        if format == "csv":
            mydata.to_csv(file_name+"."+format)
        if format == "db":
            con = sqlite3.connect(file_name+"."+format)
            mydata.to_sql("Indeed", con, if_exists="append")
        #print(mydata)



indeed = Indeed()
pages_required = int(input("How many pages to be scraped : "))
indeed.Scrap_indeed(pages_required)
indeed.get_posted_day()
file_name = input("Enter file name to store the data : ")
format = input("Which format you want to store the data : csv or db - " )
indeed.save_results(file_name=file_name, format=format)