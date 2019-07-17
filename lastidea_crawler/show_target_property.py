#coding: utf-8

import json


def load_itemlist(fd):
    data = []
    for line in fd:
        category, name, url = line.rstrip().split('\t')
        data.append((category, name, url))
    return data

def load_properties(fd):
    data = []
    for line in fd:
        name, jsontext = line.rstrip().split('\t')
        d = json.loads(jsontext)
        data.append(d)
    return data

def search_property(items, targetname):
    '''propnameを含むアイテムを検索する'''
    result = []
    for item in items:
        for prop in item['properties']:
            if prop[0] == targetname:
                result.append(item)
                break
    return result

def print_itemdata(items):
    #if target:
    #    sort_by_target

    for item in items:
        name = item['name']
        props = []
        for (propname, min_value, max_value) in item['properties']:
            s = '{}: {}～{}'.format(propname, min_value, max_value)
            props.append(s)
        print(name, ', '.join(props), sep='\t')

def parse_args():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('itemlist', type=argparse.FileType('r', encoding='utf-8'))
    parser.add_argument('propertydata', type=argparse.FileType('r', encoding='utf-8'))
    parser.add_argument('target', help='Target property')
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()

    itemlist = load_itemlist(args.itemlist)
    itemprop = load_properties(args.propertydata)

    items = search_property(itemprop, args.target)
    print_itemdata(items)
