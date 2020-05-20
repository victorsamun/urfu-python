#!/usr/bin/env python3

import os.path
import subprocess
import sys
import time


t0 = time.perf_counter()

sum_script = 'part_sum.py'
data_file = '../data.bin'

procs = [
    subprocess.Popen(['python3', sum_script, data_file, str(i), '8'],
                     stdout=subprocess.PIPE) for i in range(8)
]


s = 0
for p in procs:
    with p:
        p.wait()
        s += int(p.stdout.read().strip())

t1 = time.perf_counter()

print((t1 - t0), s)
