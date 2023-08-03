from bs4 import BeautifulSoup
import requests 
import pandas as pd
import csv

# URL: https://aisa.or.ke/aisa-member-schools/page/{ Page_No }/?action=archive

schools = []

# Scraping Schools List
def scraping_school_page(page_no):
    page_url = "https://aisa.or.ke/aisa-member-schools/page/{}/?action=archive".format(page_no)
    response_text = requests.get(page_url).text
    soup = BeautifulSoup(response_text, "html5lib")

    # Output current page no
    print(page_no)

    schools_container_tag = soup.find('div', class_='similar_school_list')
    if(schools_container_tag is None):
        return
    if schools_container_tag.ul != []:
        for school in schools_container_tag.ul.find_all("li"):
            schools.append({
                "title": school.h5.text,
                "url": school.a["href"]
            })
        # There are only 4 pages.
        if page_no < 5:
            scraping_school_page(page_no + 1)

# Scraping School's Detail
def scraping_school_detail(school_url, school_index):
    response_text = requests.get(school_url).text
    soup = BeautifulSoup(response_text, "html5lib")
    contact_container_tag = soup.find('ul', class_="school_details_list")

    if(contact_container_tag is None):
        return

    # Output current school no
    print(school_index)

    # Update School's Detail
    if(contact_container_tag.find('li', class_="head") is not None):
        schools[school_index]["header"] = contact_container_tag.find('li', class_="head").text

    if(contact_container_tag.find('li', class_="email") is not None):
        schools[school_index]["email"] = contact_container_tag.find('li', class_="email").a["href"]

    if(contact_container_tag.find('li', class_="number") is not None):
        schools[school_index]["number"] = contact_container_tag.find('li', class_="number").a["href"]

    if(contact_container_tag.find('li', class_="city") is not None):
        schools[school_index]["city"] = contact_container_tag.find('li', class_="city").text
    
    if(contact_container_tag.find('li', class_="country") is not None):
        schools[school_index]["country"] = contact_container_tag.find('li', class_="country").text

    if(contact_container_tag.find('li', class_="region") is not None):
        schools[school_index]["region"] = contact_container_tag.find('li', class_="region").text
    
    if(contact_container_tag.find('li', class_="population") is not None):
        schools[school_index]["population"] = contact_container_tag.find('li', class_="population").text


scraping_school_page(0)

for i in range(len(schools)):
    scraping_school_detail(schools[i]["url"], i)

# Output to csv file.
df = pd.DataFrame(schools)
df.to_csv(r'schools.csv')