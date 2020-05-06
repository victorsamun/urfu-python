#!/usr/bin/env python3

import time


t0 = time.perf_counter()

with open('data.bin', 'rb') as f:
    size = f.seek(0, 2)
    f.seek(0, 0)

    s = 0
    for i in range(size // 4):
        s += int.from_bytes(f.read(4), 'big')

t1 = time.perf_counter()

print((t1 - t0), s)
