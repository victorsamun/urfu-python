#!/usr/bin/env python3

import collections
import re
import sys


def parse_line(line):
    items = line.split(', ')
    if len(items) != 15:
        return None

    return {
        'client': items[0],
        'type': items[12],
        'page': items[13]
    }


def count_client(stat, item):
    stat[item['client']] += 1


def count_page(stat, item):
    stat[item['page']] += 1


def count_user(stat, item):
    if item['type'] != 'GET':
        return

    user = re.findall(r'^/home/(.*?)/', item['page'])
    if user:
        stat[user[0]] += 1


STAT_FN = [
    count_client,
    count_page,
    count_user
]


def main(filename):
    with open(filename, errors='replace') as f:
        data = f.readlines()

    stats = []
    for _ in STAT_FN:
        stats.append(collections.Counter())

    for line in data:
        item = parse_line(line)
        if item is None:
            continue

        for (i, func) in enumerate(STAT_FN):
            func(stats[i], item)

    for stat in stats:
        for (key, count) in stat.most_common(5):
            print(key, count)

        print()


if __name__ == '__main__':
    main(*sys.argv[1:])
