# Importing Packages to be Used

import requests
import time
import pandas as pd
from bs4 import BeautifulSoup

from flask import *
import json

app = Flask(__name__)



base_url = "https://www.kijiji.ca"

#URL for first test page

page_1_url = "https://www.kijiji.ca/b-reptiles-amphibians/canada/c14654004l0"

response = requests.get(page_1_url)

#Use Beautiful Soup to parse HTML response

soup = BeautifulSoup(response.text, "lxml")
#print(soup)

# Get All The Ads

ads = soup.find_all("h3", attrs={"data-testid": ["listing-title"]})

# Remove marketing / third party ads
filtered_ads = [x for x in ads if ("cas-channel" not in x["class"]) & ("third-party" not in x["class"])]

ad_links = []
for ad in filtered_ads:
    #Parse the link from the ad
    link = ad.find_all("a", {"data-testid": "listing-link"})
    # Add the link to the list
    for l in link:
        ad_links.append(base_url + l["href"])

#@app.route('/', methods=['GET'])
#def get_ad_info():
ad_info = []
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
        "title": title,
        "price": price,
        "description": description,
        "date_posted": date_posted,
        "address": adCity,
        "url": advert,
        "image_url": mainImg_URL
    })


print(ad_info)




# Press the green button in the gutter to run the script.
if __name__ == '__main__':
#    app.run(port=3333)
   print("Hello")
