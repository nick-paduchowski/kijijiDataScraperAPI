# Importing Packages to be Used

import requests
import time
import pandas as pd
from bs4 import BeautifulSoup

import json
from datetime import datetime
import psycopg2

conn = psycopg2.connect(database="kijiji_ad_data",
                        host="localhost",
                        user="postgres",
                        password="12qazqaz",
                        port="5432",
                                )
if conn:
    print("Successfully connected to database")
else:
    print("Connection to database encounter an error")

cur = conn.cursor()


base_url = "https://www.kijiji.ca"

#URL for first test page

page_1_url = "https://www.kijiji.ca/b-reptiles-amphibians/canada/c14654004l0"

response = requests.get(page_1_url)

#Use Beautiful Soup to parse HTML response


#print(soup)

categories = {
    'pets': {
        'page1URL' : 'https://www.kijiji.ca/b-pets/canada/c112l0',
        'nextPageTemplate': 'https://www.kijiji.ca/b-pets/canada/page-2/c112l0'
    },
    'jobs': {
        'page1URL' : 'https://www.kijiji.ca/b-jobs/canada/c45l0'
    }
}
def getNumOfPages(webpage):
    pageNums = []
    numberList = webpage.find_all("li", attrs={"data-testid": ["pagination-list-item"]})
    for element in numberList:
        element = element.find("a").text
        num = element.split()
        pageNums.append(int(num[-1]))
    return pageNums[-1]


# Get All The Ads


# Remove marketing / third party ads

def get_ad_info(pageNumber, category):
    if (pageNumber==1):
        ad_info = []
        ad_links = []
        page_url = categories[category]['page1URL']
        print(page_url)
        response = requests.get(page_url)
        soup = BeautifulSoup(response.text, "lxml")
        ads = soup.find_all("h3", attrs={"data-testid": ["listing-title"]})
        filtered_ads = [x for x in ads if ("cas-channel" not in x["class"]) & ("third-party" not in x["class"])]
        for ad in filtered_ads:
            # Parse the link from the ad
            link = ad.find_all("a", {"data-testid": "listing-link"})
            # Add the link to the list
            for l in link:
                ad_links.append(base_url + l["href"])
        for advert in (ad_links):
                # Get Webpage Information & Parse With BeautifulSoup
            response = requests.get(advert)
            soup = BeautifulSoup(response.text, 'lxml')

                # Get Ad Title in Try/Catch Statement
            try:
                cur.execute("SELECT * FROM your_table_name WHERE title = %s", (title,))
                row = cur.fetchone()
                if row is not None:
                    continue  # Skips the current iteration of the loop if any data is returned
                title = soup.find("h1").text
            except AttributeError:
                title = ""

                    # Get Ad Price
            try:
                 price = soup.find("span", attrs={"itemprop": "price"}).text
            except AttributeError:
                 price = ""

                # Get Date Posted
            try:
                  date_posted = soup.find("div", attrs={"itemprop": "datePosted"})['content']
            except AttributeError:
                date_posted = ""

                # Get Ad Description
            try:
                  description = soup.find("div", attrs={"itemprop": "description"}).text
            except AttributeError:
                 description = ""

                # Get Ad City
            try:
                adCity = soup.find("span", attrs={"itemprop": "address"}).text
            except AttributeError:
                adCity = ""

            try:
                 mainImg_URL = soup.find("div", attrs={"class": "mainImage"}).picture.img['src']
            except AttributeError:
                mainImg_URL = ""

            ad_info.append({
                "category": category,
                "title": title,
                "price": price,
                "description": description,
                "date_posted": date_posted,
                "address": adCity,
                "url": advert,
                "image_url": mainImg_URL
             })
            cur.execute(
                    """INSERT INTO ads (category, title, price, description, date, address, url, image_url ) VALUES (
                    %s, %s, %s, %s, %s, %s, %s, %s)""",
                    (category, title, price, description, date_posted, adCity, advert, mainImg_URL))
            conn.commit()
        return ad_info

    elif(pageNumber > 1):
        ad_info = []
        ad_links = []
        page_url = 'https://www.kijiji.ca/b-' + category + '/canada/page-' + str(pageNumber) + '/c112l0'
        print(page_url)
        response = requests.get(page_url)
        soup = BeautifulSoup(response.text, "lxml")
        ads = soup.find_all("h3", attrs={"data-testid": ["listing-title"]})
        filtered_ads = [x for x in ads if ("cas-channel" not in x["class"]) & ("third-party" not in x["class"])]
        for ad in filtered_ads:
                # Parse the link from the ad
            link = ad.find_all("a", {"data-testid": "listing-link"})
                # Add the link to the list
            for l in link:
                ad_links.append(base_url + l["href"])
        for advert in (ad_links):
            print(advert)
            # Get Webpage Information & Parse With BeautifulSoup
            response = requests.get(advert)
            soup = BeautifulSoup(response.text, 'lxml')

                # Get Ad Title in Try/Catch Statement
            try:
                title = soup.find("h1").text
            except AttributeError:
                title = ""

                # Get Ad Price
            try:
                price = soup.find("span", attrs={"itemprop": "price"}).text
            except AttributeError:
                price = ""

            # Get Date Posted
            try:
                date_posted = soup.find("div", attrs={"itemprop": "datePosted"})['content']
            except AttributeError:
                date_posted = ""
            except TypeError:
                date_posted = ""

            # Get Ad Description
            try:
                description = soup.find("div", attrs={"itemprop": "description"}).text
            except AttributeError:
                description = ""

            # Get Ad City
            try:
                adCity = soup.find("span", attrs={"itemprop": "address"}).text
            except AttributeError:
                adCity = ""

            try:
                mainImg_URL = soup.find("div", attrs={"class": "mainImage"}).picture.img['src']
            except AttributeError:
                mainImg_URL = ""

            ad_info.append({
                "category": category,
                "title": title,
                "price": price,
                "description": description,
                "date_posted": date_posted,
                "address": adCity,
                "url": advert,
                "image_url": mainImg_URL
            })

            cur.execute("""INSERT INTO ads (category, title, price, description, date, address, url, image_url ) VALUES
                        (%s, %s, %s, %s, %s, %s, %s, %s)""", (category, title, price, description, date_posted,
                                                             adCity, advert, mainImg_URL))
            conn.commit()
        return ad_info

def loadDatabase():
    print("Loading the Database")
    for obj in categories:
        #print(categories[obj]['page1URL'])
        response = requests.get(categories[obj]['page1URL'])
        webpage =  BeautifulSoup(response.text, "lxml")
        numOfPages = getNumOfPages(webpage)
        for x in range(1, numOfPages):
            result = get_ad_info(x, obj)


loadDatabase()
conn.close()

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print("Script Running")