#!/usr/bin/env python3

import os.path
import subprocess
import sys
import time


t0 = time.perf_counter()

sum_script = 'part_sum.py'
data_file = '../data.bin'

procs = [
    subprocess.run(['python3', sum_script, data_file, str(i), '8'],
                   stdout=subprocess.PIPE) for i in range(8)
]


s = sum(int(p.stdout.strip()) for p in procs)

t1 = time.perf_counter()

print((t1 - t0), s)
