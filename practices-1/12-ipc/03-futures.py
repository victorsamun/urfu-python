#!/usr/bin/env python3

import time
import sys
from concurrent.futures import ThreadPoolExecutor


def calc_sum(k, n):
    s = 0
    with open('data.bin', 'rb') as f:
        size = f.seek(0, 2)
        chunk_size = size//n

        f.seek(k*chunk_size, 0)

        for i in range(chunk_size//4):
            s += int.from_bytes(f.read(4), 'big')

    return s


t0 = time.perf_counter()

with ThreadPoolExecutor(max_workers=8) as pool:
    futures = [pool.submit(calc_sum, i, 8) for i in range(8)]
    s = sum(f.result() for f in futures)

t1 = time.perf_counter()

print((t1 - t0), s)
