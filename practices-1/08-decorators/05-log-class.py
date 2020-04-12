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


def cls_logging(cls):
    for (name, attr) in cls.__dict__.items():
        if callable(attr):
            setattr(cls, name, logging(attr))
    return cls



@cls_logging
class A:
    def __init__(self, x=0):
        self.x = x

    def f(self, x):
        return self.x + x


if __name__ == '__main__':
    a = A()
    a.f(1)
    A() == A()
    A.f(a, 2)
