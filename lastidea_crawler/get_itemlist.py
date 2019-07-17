#coding: utf-8

'''
ラストイデア 5ch wikiの武器一覧ページをクロールして、
カテゴリごとの武器リストを得る
'''

import sys
import csv
from urllib.parse import urljoin
from bs4 import BeautifulSoup

from .myutil import *

logger = get_logger(__name__)

import logging
logging.getLogger('lastidea_crawler').setLevel(logging.DEBUG)
logging.getLogger('lastidea_crawler').addHandler(logging.StreamHandler())


root_pages = [
    '剣', '両手剣', '斧', '両手斧', '両手槍', '杖', 'オーブ', '弓',
    '盾', '頭', '上半身', '下半身', '腕', '足',
    'リング', 'アミュレット', 'ベルト',
]

if __name__ == '__main__':
    for target in root_pages:
        url = urljoin(site, target)

        html = get_html(url, cache_dir='html')
        soup = BeautifulSoup(html, 'html.parser')
        tables = soup.select('#body table tbody')
        data = []
        for table in tables:
            for row in table.find_all('tr'):
                d = [col for col in row.find_all(['td', 'th'])]
                r = (target, d[1].text, urljoin(site, d[1].find('a')['href']))
                data.append(r)

        writer = csv.writer(sys.stdout, delimiter='\t')
        for d in data:
            writer.writerow(d)
