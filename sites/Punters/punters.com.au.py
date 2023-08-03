from bs4 import BeautifulSoup
import requests 
import pandas as pd
import csv
import datetime
from urllib.parse import urlencode

API_KEY = '7e1d13eb-40b1-4cf6-8aeb-ac39d7fd6d6c'

def get_scrapeops_url(url):
    payload = {'api_key': API_KEY, 'url': url}
    proxy_url = 'https://proxy.scrapeops.io/v1/?' + urlencode(payload)
    return proxy_url

races = []

def scraping_races(page_url):
    response_text = requests.get(get_scrapeops_url(page_url)).text
    soup = BeautifulSoup(response_text, "html5lib")
    tables = soup.find_all('table')

    for table in range(len(tables)):
        print(table)
        race_info = {}
        race_info["Title"] = tables[table].find('thead').find('tr').find_all('th')[0].find('b').text
        race_info["Distance"] = tables[table].find('thead').find('tr').find_all('th')[0].find('abbr', class_="conversion").text
        race_info["Award"] = tables[table].find('thead').find('tr').find_all('th')[0].find_all('span', class_="results-table__capital")[0].text.replace('\n', '')
        if tables[table].find('thead').find('tr').find_all('th')[0].find_all('span', class_="results-table__capital")[1] is not None:
            race_info["Type"] = tables[table].find('thead').find('tr').find_all('th')[0].find_all('span', class_="results-table__capital")[1].text.replace('\n','')

        timestamp = tables[table].find('thead').find('tr').find_all('th')[0].find_all('div', class_="results-table__details")[1].abbr["data-utime"]
        race_info["Time"] = datetime.datetime.fromtimestamp(int(timestamp))
        race_info["URL"] = tables[table].find('thead').find('tr').find_all('th')[0].find_all('div', class_="results-table__details")[1].span.a["href"]

        history = pd.DataFrame(columns=["Rank", "Horse_Name", "Top_Tote"])

        for tr_index in range(len(tables[table].find('tbody').find_all('tr'))):
            rank = tables[table].find('tbody').find_all('tr')[tr_index].find_all('td')[0].span.text
            horse_name = tables[table].find('tbody').find_all('tr')[tr_index].find_all('td')[1].span.text
            odds = tables[table].find('tbody').find_all('tr')[tr_index].find_all('td')[2].text

            history = pd.concat([history, pd.DataFrame([{'Rank': rank, 'Horse_Name': horse_name, 'Top_Tote': odds}], columns=["Rank", "Horse_Name", "Top_Tote"])], ignore_index=True)

        history.set_index('Rank', drop=True, inplace=True)
        race_info["Race_History"] = history.__repr__()
        races.append(race_info)

# def scraping_race_detail(race_url, index):
#     response_text = requests.get(get_scrapeops_url(race_url)).text
#     soup = BeautifulSoup(response_text, "html5lib")

#     table = soup.find('table')
#     print(len(table.find_all('tr')))
#     for i in range(len(table.find_all('tr'))):
#         tr_tag = table.find_all('tr')[i]
#         print(tr_tag.find_all('td')[1].find('a', class_="form-guide-overview__horse-link").text)


url = "https://www.punters.com.au/racing-results/"
scraping_races(url)

df = pd.DataFrame(races)
df.to_csv(r'races.csv')