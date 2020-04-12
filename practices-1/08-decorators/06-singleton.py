#!/usr/bin/env python3

import functools


# Taken from 'https://wiki.python.org/moin/PythonDecoratorLibrary#Singleton'

def singleton(cls):
    cls.__old_new__ = cls.__new__

    @functools.wraps(cls.__new__)
    def __new__(cls, *args, **kwargs):
        instance = cls.__dict__.get('__instance__')
        if instance is None:
            instance = cls.__old_new__(cls, *args, **kwargs)
            cls.__instance__ = instance
            instance.__old_init__(*args, **kwargs)

        return instance

    cls.__new__ = __new__
    cls.__old_init__ = cls.__init__
    cls.__init__ = object.__init__

    return cls


@singleton
class A:
    def __new__(cls):
        cls.x = 1
        return object.__new__(cls)

    def __init__(self):
        print(self.x == 1)
        self.x = 2


if __name__ == '__main__':
    print(A().x == 2)
    A().x = 3
    print(A().x == 3)
