# Importing Packages to be Used
import requests
import time
from bs4 import BeautifulSoup
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

DB_PASS = os.geten('USER_PASS')

conn = psycopg2.connect(database="kijiji_ad_data",
                        host="localhost",
                        user="postgres",
                        password=DB_PASS,
                        port="5432",
                                )
if conn:
    print("Successfully connected to database")
else:
    print("Connection to database encounter an error")

cur = conn.cursor()


base_url = "https://www.kijiji.ca"


categories = {
    'accounting-management': {
        'page1URL' : 'https://www.kijiji.ca/b-accounting-management-jobs/canada/c58l0',
    },
    'construction-trades': {
        'page1URL': 'https://www.kijiji.ca/b-construction-trades-jobs/canada/c50l0',
    },
    'drivers-security':{
        'page1URL': 'https://www.kijiji.ca/b-driver-security-jobs/canada/c148l0',
    },

    'childcare': {
        'page1URL': 'https://www.kijiji.ca/b-childcare-jobs/canada/c47l0',
    },
    'general-labour': {
        'page1URL': 'https://www.kijiji.ca/b-general-labour-jobs/canada/c149l0',
    },
    'other-jobs': {
        'page1URL': 'https://www.kijiji.ca/b-other-jobs/canada/c62l0',
    },
    'cleaning': {
        'page1URL': 'https://www.kijiji.ca/b-cleaning-housekeeper-jobs/canada/c146l0',
    },
    'healthcare': {
        'page1URL': 'https://www.kijiji.ca/b-healthcare-jobs/canada/c898l0',
    },
    'hospitality': {
        'page1URL': 'https://www.kijiji.ca/b-bar-food-hospitality-jobs/canada/c60l0',
    },
    'sales': {
        'page1URL': 'https://www.kijiji.ca/b-sales-retail-jobs/canada/c61l0',
    },
    'part-time-and-students': {
        'page1URL': 'https://www.kijiji.ca/b-part-time-student-jobs/canada/c59l0',
    },
    'customer-service':{
        'page1URL': 'https://www.kijiji.ca/b-customer-service-jobs/canada/c147l0',
    },
    'hair-stylist-salon': {
        'page1URL': 'https://www.kijiji.ca/b-hair-stylist-salon-jobs/canada/c150l0',
    },
    'office-manager-receptionist': {
        'page1URL': 'https://www.kijiji.ca/b-office-manager-receptionist-jobs/canada/c46l0',
    },
    'computers-programming': {
        'page1URL': 'https://www.kijiji.ca/b-programmer-computer-jobs/canada/c54l0',
    },
    'graphic-desgin': {
        'page1URL': 'https://www.kijiji.ca/b-graphic-web-design-jobs/canada/c152l0',
    },
    'tv-media-fashion': {
        'page1URL': 'https://www.kijiji.ca/b-tv-media-fashion-jobs/canada/c55l0',
    },
    'cannabis-sector': {
        'page1URL': 'https://www.kijiji.ca/b-cannabis-sector/canada/c420l0',
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
        #Fetching the page URL
        response = requests.get(page_url, headers={ "user-agent" : "npaduchowski@hotmail.com", "message" : "Permission obtained to use data from Kijiji." })
        # Use Beautiful Soup to parse HTML response
        soup = BeautifulSoup(response.text, "lxml")
        #Get all the data with the data-testid of listing-title
        ads = soup.find_all("h3", attrs={"data-testid": ["listing-title"]})
        # Filtering out 3rd party ads
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
            try:
                # Skips the current iteration of the loop if any data is returned
                cur.execute("SELECT * FROM job_data WHERE url = %s", (advert,))
                row = cur.fetchone()
                if row is not None:
                    print("Already in database")
                    continue
            except AttributeError:
                print("AttributeError")

            # Get Ad Title in Try/Catch Statement
            try:
                title = soup.find("h1").text
            except AttributeError:
                title = ""

            #Getting Ad Price is no longer part of this API
            # Get Ad Price
            #try:
            #     price = soup.find("span", attrs={"itemprop": "price"}).text
            #except AttributeError:
            #     price = ""

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
                adCity = soup.find("span", attrs={"itemprop": "addressLocality"}).text
            except AttributeError:
                adCity = ""


            # Getting the Ad Province
            try:
                adProvince = soup.find("span", attrs={"itemprop": "addressRegion"}).text
            except AttributeError:
                adProvince = ""

            # Getting main img url
            try:
                 mainImg_URL = soup.find("div", attrs={"class": "mainImage"}).picture.img['src']
            except AttributeError:
                mainImg_URL = ""

            # Getting the employment type - full-time, part-time, contract
            try:
                jobType = soup.find("dd", attrs={"itemprop": "employmentType"}).text
            except AttributeError:
                jobType = "Please Contact"

            # Gets the hiring organization, if none is found on the ad page
            try:
                companyName = soup.find("dd", attrs={"itemprop": "hiringOrganization"}).text
            except AttributeError:
                companyName = ""

            # Prints the ad data so I can verify it while the script is running
            print({
                "category": category,
                "title": title,
                "company_name": companyName,
                "description": description,
                "date_posted": date_posted,
                "city": adCity,
                "province": adProvince,
                "url": advert,
                "image_url": mainImg_URL,
             })
            # Inserts the data into database
            cur.execute("""INSERT INTO job_data (category, title, description, date, city, province, url, img_url, job_type, company_name) VALUES
                    (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", (category, title, description, date_posted,
                                                                    adCity, adProvince, advert, mainImg_URL,
                                                                    jobType, companyName))
            # Commits the data to the database immediately in case of a script or connection failure
            conn.commit()
            # Waits 5 seconds before looping again to ensure I don't accidentally DDoS a server lol
            time.sleep(5)
        return ad_info

    elif(pageNumber > 1):
        ad_info = []
        ad_links = []
        # Gets the base URL
        originalURL = categories[category]['page1URL']
        # Cut out the end from the firt page URL by finding the last / in the string
        cut_off_point = originalURL.rfind('/')
        url_id = originalURL[cut_off_point:]
        # Formatting the url for pages after the first page
        page_url = 'https://www.kijiji.ca/b-' + category + '/canada/page-' + str(pageNumber) + str(url_id)
        # Print the page_url to confirm progress
        print(page_url)
        # Get the webpage
        response = requests.get(page_url)
        # Use BeautifulSoup to parse the returned webpage
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
            try:
                # Skips the current iteration of the loop if any data is returned
                cur.execute("SELECT * FROM job_data WHERE url = %s", (advert,))
                row = cur.fetchone()
                if row is not None:
                    print("Already in database")
                    continue
            except AttributeError:
                print("AttributeError")
            # Get Webpage Information & Parse With BeautifulSoup
            response = requests.get(advert)
            soup = BeautifulSoup(response.text, 'lxml')

                # Get Ad Title in Try/Catch Statement
            try:
                title = soup.find("h1").text
            except AttributeError:
                title = ""

                # Get Ad Price
            #try:
            #    price = soup.find("span", attrs={"itemprop": "price"}).text
            #except AttributeError:
            #    price = ""

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
                adCity = soup.find("span", attrs={"itemprop": "addressLocality"}).text
            except AttributeError:
                adCity = ""

            try:
                adProvince = soup.find("span", attrs={"itemprop": "addressRegion"}).text
            except AttributeError:
                adProvince = ""

            try:
                mainImg_URL = soup.find("div", attrs={"class": "mainImage"}).picture.img['src']
            except AttributeError:
                mainImg_URL = ""

            try:
                jobType = soup.find("dd", attrs={"itemprop": "employmentType"}).text
            except AttributeError:
                jobType = "Please Contact"

            try:
                companyName = soup.find("dd", attrs={"itemprop": "hiringOrganization"}).text
            except AttributeError:
                companyName = ""

            print({
                "category": category,
                "title": title,
                "description": description,
               "date_posted": date_posted,
                "city": adCity,
                "province": adProvince,
                "url": advert,
                "image_url": mainImg_URL,
                "job_type": jobType,
                "company_name": companyName
            })

            cur.execute("""INSERT INTO job_data (category, title, description, date, city, province, url, img_url, job_type, company_name) VALUES
                            (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", (category, title, description, date_posted,
                                                                 adCity, adProvince, advert, mainImg_URL, jobType, companyName))
            conn.commit()
            time.sleep(5)
        return ad_info

def loadDatabase():
    print("Loading the Database")
    for obj in categories:
        #print(categories[obj]['page1URL'])
        response = requests.get(categories[obj]['page1URL'])
        webpage =  BeautifulSoup(response.text, "lxml")
        numOfPages = getNumOfPages(webpage)
        if (obj == "customer-service"):
            for x in range(5, numOfPages):
                print("Page Number: " + str(x) + " And Category: " + str(obj))
                result = get_ad_info(x, obj)
        else:
            for x in range(2, numOfPages):
                print("Page Number: " + str(x) + " And Category: " + str(obj))
                result = get_ad_info(x, obj)


loadDatabase()
conn.close()

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print("Script Running")