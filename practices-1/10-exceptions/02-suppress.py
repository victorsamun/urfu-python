#!/usr/bin/env python3

import contextlib
import sys
import traceback


@contextlib.contextmanager
def suppress(*exceptions):
    try:
        yield
    except BaseException as e:
        if not isinstance(e, exceptions):
            raise

        print('SUPPRESSED', file=sys.stderr)
        traceback.print_exception(*sys.exc_info(), file=sys.stderr)


if __name__ == '__main__':
    with suppress(ValueError):
        raise ValueError('exc 1')

    print()

    with suppress(TypeError, NameError):
        raise TypeError('exc 2')

    print()

    with suppress(Exception):
        raise NameError('exc 3')

    print()

    with suppress(ValueError):
        raise IndexError('exc 4')
