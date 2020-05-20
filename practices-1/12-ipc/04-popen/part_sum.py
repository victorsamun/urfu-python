#!/usr/bin/env python3

import sys


def main(filename, k, n):
    s = 0

    with open(filename, 'rb') as f:
        size = f.seek(0, 2)
        chunk_size = size//int(n)

        f.seek(int(k)*chunk_size, 0)

        for i in range(chunk_size//4):
            s += int.from_bytes(f.read(4), 'big')

    print(s)


if __name__ == '__main__':
    main(*sys.argv[1:])
