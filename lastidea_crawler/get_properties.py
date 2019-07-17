#coding: utf-8

'''
ラストイデア 5ch wikiの武器詳細ページから
武器のプロパティを得る
'''

import sys
import json
from bs4 import BeautifulSoup
from .myutil import *

logger = get_logger(__name__)

import logging
logging.getLogger('lastidea_crawler').setLevel(logging.DEBUG)
logging.getLogger('lastidea_crawler').addHandler(logging.StreamHandler())

#url = 'https://wikiwiki.jp/lastidea-5ch/%E3%83%9E%E3%82%B8%E3%83%83%E3%82%AF%E3%83%99%E3%83%AB%E3%83%88'
#url = 'https://wikiwiki.jp/lastidea-5ch/%E7%82%8E%E3%81%AE%E3%82%AF%E3%83%AA%E3%82%B9%E3%82%BF%E3%83%AB'


def main(url):
    html = get_html(url, cache_dir='html')
    soup = BeautifulSoup(html, 'html.parser')
    tables = soup.select('#body table tbody')
    data = []
    for table in tables:
        for row in table.find_all('tr'):
            d = [col for col in row.find_all(['td', 'th'])]
            # P1~P6を探す
            if not d[0].text.startswith('P'):
                continue
            
            property_name = d[1].text
            min_value = ''
            max_value = ''
            if len(d) == 5:
                min_value = d[2].text
                max_value = d[3].text
            elif len(d) == 4:
                value_text = d[2].text
                if value_text:
                    sp = value_text.split('～')
                    if len(sp) > 1:
                        min_value = sp[0]
                        max_value = sp[1]
            r = (property_name, min_value, max_value)
            data.append(r)
    return data


if __name__ == '__main__':
    for line in sys.stdin:
        category, name, url = line.rstrip().split('\t')
        if name.endswith('?'):
            continue
        uname = parse_wiki_url(url)
        if name != uname:
            logger.warning('Different name: %s %s', name, uname)
        p = main(url)
        d = {'name': uname, 'properties': p}
        print(uname, json.dumps(d), sep='\t')
