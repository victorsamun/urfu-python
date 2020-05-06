#!/usr/bin/env python3

import time
import threading
import sys


s = 0
lock = threading.RLock()


def calc_sum(k, n):
    global s

    s0 = 0
    with open('data.bin', 'rb') as f:
        size = f.seek(0, 2)
        chunk_size = size//n

        f.seek(k*chunk_size, 0)

        for i in range(chunk_size//4):
            s0 += int.from_bytes(f.read(4), 'big')

    with lock:
        s += s0


t0 = time.perf_counter()

threads = [threading.Thread(target=calc_sum, args=(i, 8)) for i in range(8)]

for th in threads:
    th.start()

for th in threads:
    th.join()

t1 = time.perf_counter()

print((t1 - t0), s)
