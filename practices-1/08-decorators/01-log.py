#!/usr/bin/env python3

import functools


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

        try:
            value = func(*args, **kwargs)
            print(f'{str_call} -> {value!r}')
            return value
        except BaseException as e:
            print(f'{str_call} raises {e!r}')
            raise

    return wrapper


@logging
def func(x, y, z=0):
    return x*y + z


if __name__ == '__main__':
    func(1, 2)
    func(1, 2, 3)
    func(1, 2, z=3)
    func(**{'x': 1, 'y': 2})
    func(1, [2], {3})
