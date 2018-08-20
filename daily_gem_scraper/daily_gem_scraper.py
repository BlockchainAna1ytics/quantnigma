import os
import csv
import json
import re
import time
import datetime
import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup

def get_crypto_info(i):
    api_url = 'https://api.coinmarketcap.com/v2/ticker/?start='+str(i)
    response = requests.get(api_url)

    if response.status_code == 200:
        return json.loads(response.content.decode('utf-8'))
    else:
        return None

def generate_cmc_api(i):
    with open('cmc_api.csv', 'w', encoding='utf-8', newline='') as csvfile:
        cmc_api_writer = csv.writer(csvfile)
        cmc_api_writer.writerow(['circulating_supply', 'ID', 'last_updated',\
                                 'max_supply', 'name', 'market_cap',\
                                 'percent_change_1h', 'percent_change_24h', 'percent_change_7d',\
                                 'price', 'volume_24h', 'rank',\
                                 'symbol', 'total_supply', 'website_slug'])
        while get_crypto_info(i):
            for crypto in get_crypto_info(i)['data']:
                c = get_crypto_info(i)['data'][crypto]
                circulating_supply = c['circulating_supply']
                ID = c['id']
                last_updated = c['last_updated']
                max_supply = c['max_supply']
                name = c['name']
                q = c['quotes']['USD']
                market_cap = q['market_cap']
                percent_change_1h = q['percent_change_1h']
                percent_change_24h = q['percent_change_24h']
                percent_change_7d = q['percent_change_7d']
                price = q['price']
                volume_24h = q['volume_24h']
                rank = c['rank']
                symbol = c['symbol']
                total_supply = c['total_supply']
                website_slug = c['website_slug']
                cmc_api_writer.writerow([circulating_supply, ID, last_updated,\
                                         max_supply, name, market_cap,\
                                         percent_change_1h, percent_change_24h, percent_change_7d,\
                                         price, volume_24h, rank,\
                                         symbol, total_supply, website_slug])
            i += 100

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
    with open('cmc_web.csv', 'w', encoding='utf-8', newline='') as csvfile:
        cmc_web_writer = csv.writer(csvfile)
        cmc_web_writer.writerow(['name', 'symbol', 'website', 'github', 'careers'])
        for tr in trs[1:]:
            symbol = tr.find('span', {'class': 'currency-symbol'}).text
            name = tr.find('a', {'class': 'currency-name-container'}).text

            coin_url = tr.find('a').get('href')
            coin_url = 'https://coinmarketcap.com' + coin_url
            response = requests.get(coin_url).text
            soup = BeautifulSoup(response, 'lxml')


            website = soup.find('a', text='Website').get('href') if soup.find('a', text='Website') else None
            github = soup.find('a', text='Source Code').get('href') if soup.find('a', text='Source Code') else None
            careers = None

            if website:
                try:
                    response2 = requests.get(website).text
                    soup2 = BeautifulSoup(response2, 'lxml')

                    careers = soup2.find('a', {'href': re.compile(r'(careers|jobs)')}).get('href') if soup2.find('a', {'href': re.compile(r'(careers|jobs)')}) else None
                    careers = beautify_url(website, careers)

                    if not github:
                        github = soup2.find('a', {'href': re.compile(r'github')}).get('href') if soup2.find('a', {'href': re.compile(r'github')}) else None
                        github = beautify_url(website, github)
                except Exception:
                    pass
            cmc_web_writer.writerow([name, symbol, website, github, careers])
            time.sleep(0.5)

def generate_cmc_gems(i):
    with open('cmc_gems.csv', 'w', encoding='utf-8', newline='') as csvfile:
        cmc_gems_writer = csv.writer(csvfile)
        cmc_gems_writer.writerow(['circulating_supply', 'ID', 'last_updated',\
                                 'max_supply', 'name', 'market_cap',\
                                 'percent_change_1h', 'percent_change_24h', 'percent_change_7d',\
                                 'price', 'volume_24h', 'rank',\
                                 'symbol', 'total_supply', 'website_slug', 'website', 'github'])
        while get_crypto_info(i):
            for crypto in get_crypto_info(i)['data']:
                c = get_crypto_info(i)['data'][crypto]
                q = c['quotes']['USD']
                market_cap = q['market_cap']
                volume_24h = q['volume_24h']
                if volume_24h is not None:
                    if market_cap is None and volume_24h > 500000:
                        circulating_supply = c['circulating_supply']
                        ID = c['id']
                        last_updated = c['last_updated']
                        max_supply = c['max_supply']
                        name = c['name']
                        percent_change_1h = q['percent_change_1h']
                        percent_change_24h = q['percent_change_24h']
                        percent_change_7d = q['percent_change_7d']
                        price = q['price']
                        rank = c['rank']
                        symbol = c['symbol']
                        total_supply = c['total_supply']
                        website_slug = c['website_slug']
                        
                        # Extract website and github
                        cmc_gem_url = 'https://coinmarketcap.com/currencies/' + website_slug
                        response = requests.get(cmc_gem_url).text
                        soup = BeautifulSoup(response, 'lxml')
                        website = soup.find('a', text='Website').get('href') if soup.find('a', text='Website') else None
                        github = soup.find('a', text='Source Code').get('href') if soup.find('a', text='Source Code') else None
                        
                        cmc_gems_writer.writerow([circulating_supply, ID, last_updated,\
                                                 max_supply, name, market_cap,\
                                                 percent_change_1h, percent_change_24h, percent_change_7d,\
                                                 price, volume_24h, rank,\
                                                 symbol, total_supply, website_slug,\
                                                 website, github])
            i += 100

def generate_cmc_gems_daily(i, gems_names):
    filename = './cmc_gems_daily/' + str(datetime.datetime.now()) + '.csv'
    with open(filename, 'w', encoding='utf-8', newline='') as csvfile:
        cmc_gems_daily_writer = csv.writer(csvfile)
        cmc_gems_daily_writer.writerow(['circulating_supply', 'ID', 'last_updated',\
                                 'max_supply', 'name', 'market_cap',\
                                 'percent_change_1h', 'percent_change_24h', 'percent_change_7d',\
                                 'price', 'volume_24h', 'rank',\
                                 'symbol', 'total_supply', 'website_slug', 'website', 'github'])
        start_ranks = [i]
        n_written = 1
        with open(r'cmc_gems.csv', 'a') as f:
            cmc_gems_writer = csv.writer(f)
            cmc_gems_writer.writerow([])
            while get_crypto_info(i):
                for crypto in get_crypto_info(i)['data']:
                    c = get_crypto_info(i)['data'][crypto]
                    q = c['quotes']['USD']
                    market_cap = q['market_cap']
                    volume_24h = q['volume_24h']
                    if volume_24h is not None:
                        if market_cap is None and volume_24h > 90000 and c['name'] not in gems_names:
                            circulating_supply = c['circulating_supply']
                            ID = c['id']
                            last_updated = c['last_updated']
                            max_supply = c['max_supply']
                            name = c['name']
                            percent_change_1h = q['percent_change_1h']
                            percent_change_24h = q['percent_change_24h']
                            percent_change_7d = q['percent_change_7d']
                            price = q['price']
                            rank = c['rank']
                            symbol = c['symbol']
                            total_supply = c['total_supply']
                            website_slug = c['website_slug']

                            # Extract website and github
                            cmc_gem_url = 'https://coinmarketcap.com/currencies/' + website_slug
                            response = requests.get(cmc_gem_url).text
                            soup = BeautifulSoup(response, 'lxml')
                            website = soup.find('a', text='Website').get('href') if soup.find('a', text='Website') else None
                            github = soup.find('a', text='Source Code').get('href') if soup.find('a', text='Source Code') else None

                            results = [circulating_supply, ID, last_updated,\
                                                     max_supply, name, market_cap,\
                                                     percent_change_1h, percent_change_24h, percent_change_7d,\
                                                     price, volume_24h, rank,\
                                                     symbol, total_supply, website_slug, website, github]
                            cmc_gems_daily_writer.writerow(results)
                            cmc_gems_writer.writerow(results)
                            print('Have Written {} result(s) so far...'.format(n_written))
                            n_written += 1

                        elif market_cap is not None:
                            start_ranks.append(c['rank']+1)

                i += 100
            f.close()
        f = open('gem_start_rank.txt','w')
        f.write(str(min(start_ranks)))
        f.close()

def find_cmc_gems():
    if not os.path.exists('gem_start_rank.txt'):
        f = open('gem_start_rank.txt','w')
        f.write('0')
        f.close()
        
    f = open('gem_start_rank.txt')
    start_rank = int(f.readlines()[0])
    f.close()
    
    if not os.path.exists('cmc_gems.csv'):
        generate_cmc_gems(start_rank)
    else:
        cmc_gems = pd.read_csv('cmc_gems.csv')
        generate_cmc_gems_daily(start_rank, cmc_gems['name'].values)

start = time.time()
print("Scraping in progress... Please wait...")
find_cmc_gems()
end = time.time()
print("Done! " + "That took {} seconds.".format(end-start))