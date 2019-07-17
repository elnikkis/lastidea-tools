#coding: utf-8

import os
import time
import urllib
import requests

import logging
logger = logging.getLogger(__name__)


site = 'https://wikiwiki.jp/lastidea-5ch/'
headers = {
    'User-Agent': 'lastidea-tool (noahluces@gmail.com)'
}


def get_logger(name):
    import logging
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    handler = logging.StreamHandler()
    logger.addHandler(handler)
    return logger


def parse_wiki_url(url):
    assert url.startswith(site)
    target = url[len(site):].strip('/')
    return urllib.parse.unquote(target)


def get_html(url, cache_dir):
    name = parse_wiki_url(url)
    store_path = os.path.join(cache_dir, 'wiki_%s.html' % name)
    if os.path.exists(store_path):
        logger.info('Load content from %s', store_path)
        with open(store_path) as fd:
            return fd.read()

    logger.info('Get content from %s', url)
    r = requests.get(url)
    time.sleep(1)
    with open(store_path, 'w') as fd:
        fd.write(r.text)
    logger.info('Saved content at %s', store_path)
    return r.text


#TODO アクセス間隔を制御する
class Crawler():
    pass
