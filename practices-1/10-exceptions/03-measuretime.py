#!/usr/bin/env python3

import contextlib
import time


class MeasureTime(contextlib.ContextDecorator):
    def __enter__(self):
        self._start = time.perf_counter()

    def __exit__(self, *exc_info):
        print(time.perf_counter() - self._start)
        return False


@MeasureTime()
def f(x):
    time.sleep(x / 1000)


if __name__ == '__main__':
    f(125)
    f(250)
    f(666)
