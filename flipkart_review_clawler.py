import requests
from bs4 import BeautifulSoup
import bs4 as bs
from selenium import webdriver
from pymongo import MongoClient
from datetime import datetime



links_list =[]

count=0

def flip_spider():
    url="https://www.flipkart.com/"
    source_code = requests.get(url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text, "html.parser")
    for link in soup.findAll('a'):
        href = link.get('href')
        if(str(href).lower().find("laptops")==1):
            temp = 'https://www.flipkart.com/'+href
            get_personal_data(temp)


def get_personal_data(profile_url):
    global count
    source_code = requests.get(profile_url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text, "html.parser")
    for name in soup.findAll('a', {'class': '_1UoZlX'}):
        href = name.get('href')
        temp = "https://www.flipkart.com"+href
        count+=1
        sub_gather_link_1(temp)

def sub_gather_link_1(data_url):
    page=1
    source_code = requests.get(data_url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text, "html.parser")
    for temp_link in soup.findAll('a'):
        test = temp_link.get('href')
        if(test[1:46]==data_url[25:70]):
            if(str(test).find("reviews")!=-1):
                temp='https://www.flipkart.com'+test
                index = temp.find("?")

                test_str= temp[:index+1]+'page'+str(page)
                test_str_1=test_str+'&'+temp[index+1:]




                print(test_str_1)

                review_clawler(test_str_1)


def review_clawler(in_url):
    client = MongoClient()
    db = client.review
    browser = webdriver.Chrome(executable_path=r"D:\softwares\chromedriver.exe")
    browser.get(in_url)
    html_source = browser.page_source
    browser.quit()
    soup = bs.BeautifulSoup(html_source, "html.parser")

    list_names_dates=[]
    list_reviews=[]

    for test in soup.findAll('div', {'class': 'Sw6kZ2'}):
        item_name = test.string

    for name in soup.findAll('p', {'class': '_3LYOAd'}):
        list_names_dates.append(name.string)

    for name in soup.findAll('div', {'class': 'qwjRop'}):
        for name_1 in name.findAll('div'):
            for name_2 in name_1.findAll('div'):
                list_reviews.append(name_2.string)

    print(list_names_dates)
    print(list_reviews)

    count_names = 0
    count_review = 0
    for i in list_reviews:
        result = db.review_data.insert_one(
            {
                "item-name": item_name,
                "name": list_names_dates[count_names],
                "date": list_names_dates[count_names + 1],
                "review": list_reviews[count_review]
            }
        )
        count_names += 2
        count_review += 1

    list_names_dates=[]
    list_reviews=[]

flip_spider()

print(count)