#!/usr/bin/env python3

import functools
import time


def time_str(end, start):
    return f'{int((end - start)*10**6)}µs'


def logging(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        str_args = ', '.join(map(repr, args))
        str_kwargs = ', '.join(map(lambda item: '{}={!r}'.format(*item),
                                   kwargs.items()))
        if str_args and str_kwargs:
            str_args_kwargs = f'{str_args}, {str_kwargs}'
        else:
            str_args_kwargs = str_args or str_kwargs
        str_call = f'{func.__name__}({str_args_kwargs})'

        t0 = time.perf_counter()

        try:
            value = func(*args, **kwargs)
            t1 = time.perf_counter()
            print(f'{str_call} -> {value!r}, time={time_str(t1, t0)}')
            return value
        except BaseException as e:
            t1 = time.perf_counter()
            print(f'{str_call} raises {e!r}, time={time_str(t1, t0)}')
            raise

    return wrapper


@logging
def func(x, y, z=0):
    time.sleep((x + y + z)/100)
    return x*y + z


if __name__ == '__main__':
    func(1, 2)
    func(1, 2, 3)
    func(1, 2, z=3)
    func(**{'x': 1, 'y': 2})
    func(1, [2], {3})
