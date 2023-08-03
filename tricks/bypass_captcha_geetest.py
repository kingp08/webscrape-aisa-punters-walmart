from twocaptcha import TwoCaptcha
from bs4 import BeautifulSoup
import requests 
import pandas as pd
import csv

# 2captcha api key
api_key = 'e6a7d01d6d2316a234862725253bcb6b'


page_url = "https://www.immobilienscout24.de/expose/131080031#/"
response_text = requests.get(page_url).text
soup = BeautifulSoup(response_text, "html5lib")

# Extract gt value
gt_start_pos = response_text.find("gt: ") + 5
gt_end_pos = response_text.find("\"", gt_start_pos)
gt = response_text[gt_start_pos:gt_end_pos]

# Extract challenge value
ch_start_pos = response_text.find("challenge: ") + 12
ch_end_pos = response_text.find("\"", ch_start_pos)
challenge = response_text[ch_start_pos:ch_end_pos]

# Create Solver Instance with api key
solver = TwoCaptcha(api_key)

result = solver.geetest(gt=gt,
                            apiServer='api.geetest.com',
                            challenge=challenge,
                            url='https://2captcha.com/demo/geetest')

# print(result)