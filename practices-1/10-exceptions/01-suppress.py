#!/usr/bin/env python3

import sys
import traceback


class Suppress:
    def __init__(self, *exceptions):
        self._exceptions = exceptions

    def __enter__(self):
        pass

    def __exit__(self, etype, val, tb):
        suppressed = bool(etype and issubclass(etype, self._exceptions))
        if suppressed:
            print('SUPPRESSED', file=sys.stderr)
            traceback.print_exception(etype, val, tb, file=sys.stderr)
        return suppressed


if __name__ == '__main__':
    with Suppress(ValueError):
        raise ValueError('exc 1')

    print()

    with Suppress(TypeError, NameError):
        raise TypeError('exc 2')

    print()

    with Suppress(Exception):
        raise NameError('exc 3')

    print()

    with Suppress(ValueError):
        raise IndexError('exc 4')
