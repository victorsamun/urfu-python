#!/usr/bin/env python3

import collections
import urllib.request


URL = 'ftp://shannon.usu.edu.ru/python/hw2/home.html'
names = []

with urllib.request.urlopen(URL) as f:
    text = f.read().decode('cp1251')

    pos = 0
    while True:
        start = text.find('/>', pos)
        if start == -1:
            break
        end = text.find('</', start)

        names.append(text[start + 2:end].split()[-1])
        pos = end

for (name, count) in collections.Counter(names).most_common():
    print(f'{count:>3}\t{name}')

# print(max(names, key=len))
