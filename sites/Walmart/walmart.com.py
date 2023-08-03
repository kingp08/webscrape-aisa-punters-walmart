import requests
from lxml import html
import json

#Finding the product ID and name from the webpage.

headers = {
    'authority': 'www.walmart.com',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
    'accept-language': 'en-US,en;q=0.8',
    'cache-control': 'max-age=0',
    'referer': 'https://www.walmart.com/',
    'sec-ch-ua': '"Brave";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-gpc': '1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
}

response = requests.get('https://www.walmart.com/search?q=laptop', headers=headers)

cookies=response.cookies

tree=html.fromstring(response.text)

product=tree.xpath('//script[@id="__NEXT_DATA__"]//text()')

data=json.loads(product[0])

product_list=data['props']['pageProps']['initialData']['searchResult']['itemStacks'][0]['items']


#Creating a dictionary with key as product ID and value as title of the product.

products={}


for i in product_list:
    temp={}
    if i.get('usItemId') != None:
        temp["Type"]=i.get('__typename')
        temp["Title"]=i.get('name')
        temp["Seller"]=i.get('sellerName')
        temp['Description']=i.get('shortDescription')
        products[i.get('usItemId')]=temp


#Collecting seller information for items and updating the dictionary with that information.
pro_id=products.keys()


with open("Data.json", "w") as f:
    json.dump(products,f,indent=4)
