import os
import csv
import json
import re
import time
import datetime
import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup

def beautify_url(seed, url):
    if url:
        if url[:4] != 'http':
            if url[0] == '/':
                if seed[-1] == '/':
                    url = seed + url[1:]
                else:
                    url = seed + url
            else:
                url = seed + '/' + url
    return url

def generate_cmc_web():
    cmc_url = 'https://coinmarketcap.com/all/views/all/'
    response = requests.get(cmc_url).text
    soup = BeautifulSoup(response, 'lxml')
    trs = soup.find_all('tr')
    filename = './coin_github_careers/' + str(datetime.datetime.now()) + '.csv'
    with open(filename, 'w', encoding='utf-8', newline='') as csvfile:
        cmc_web_writer = csv.writer(csvfile)
        cmc_web_writer.writerow(['name', 'symbol', 'marketcap_usd', 'price', 'volume', 'website', 'github', 'careers'])
        trs_len = len(trs[1:])
        for i, tr in enumerate(trs[1:]):
            name = tr.find('a', {'class': 'currency-name-container'}).text
            symbol = tr.find('span', {'class': 'currency-symbol'}).text
            marketcap_usd = tr.select('td.no-wrap.market-cap.text-right')[0].text.replace('\n', '')
            print(marketcap_usd)
            price = tr.find('a', {'class': 'price'}).text
            volume = tr.find('a', {'class': 'volume'}).text
            # 1h = tr.find('td', {'class': ['no-wrap', 'percent-change', 'text-right'], 'data-timespan': '1h'}).text
            # 24h = tr.find('td', {'class': ['no-wrap', 'percent-change', 'text-right'], 'data-timespan': '24h'}).text
            # 7d = tr.find('td', {'class': ['no-wrap', 'percent-change', 'text-right'], 'data-timespan': '7d'}).text
            print('Scraping {}, {}/{}'.format(name, i, trs_len))
            coin_url = tr.find('a').get('href')
            coin_url = 'https://coinmarketcap.com' + coin_url
            response = requests.get(coin_url).text
            soup = BeautifulSoup(response, 'lxml')


            website = soup.find('a', text='Website').get('href') if soup.find('a', text='Website') else None
            github = soup.find('a', text='Source Code').get('href') if soup.find('a', text='Source Code') else None
            careers = None

            if website:
                try:
                    response2 = requests.get(website, timeout=10).text
                    soup2 = BeautifulSoup(response2, 'lxml')

                    careers = soup2.find('a', {'href': re.compile(r'(careers|jobs)')}).get('href') if soup2.find('a', {'href': re.compile(r'(careers|jobs)')}) else None
                    careers = beautify_url(website, careers)

                    if not github:
                        github = soup2.find('a', {'href': re.compile(r'github')}).get('href') if soup2.find('a', {'href': re.compile(r'github')}) else None
                        github = beautify_url(website, github)
                except Exception as error:
                    careers = 'ERR'
                    if not github:
                        github = 'ERR'
                    print(error)
                    pass
            print([name, symbol, marketcap_usd, price, volume, website, github, careers])
            cmc_web_writer.writerow([name, symbol, marketcap_usd, price, volume, website, github, careers])
            time.sleep(0.5)
            break

start = time.time()
print("Scraping in progress... Please wait...")
generate_cmc_web()
end = time.time()
print("Done! " + "That took {} seconds.".format(end-start))