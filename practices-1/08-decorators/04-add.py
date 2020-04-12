#!/usr/bin/env python3

import functools


def add(value):
    def add_value(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs) + value
        return wrapper
    return add_value


class Add:
    def __init__(self, value):
        self._value = value

    def __call__(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs) + self._value
        return wrapper


@add(5)
def two():
    return 2


@Add(5)
def f(x):
    return x


if __name__ == '__main__':
    print(two())
    print(f(1))
    print(f(x=5))
