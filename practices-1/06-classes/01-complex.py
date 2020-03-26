#!/usr/bin/env python3

import unittest


class Complex:
    def __init__(self, re=0.0, im=0.0):
        if not isinstance(re, (int, float)):
            raise TypeError('Wrong type of "re"')

        if not isinstance(im, (int, float)):
            raise TypeError('Wrong type of "im"')

        self.re = re
        self.im = im

    def get_real(self):
        return self.re

    def __add__(self, rhs):
        if isinstance(rhs, (int, float)):
            return Complex(self.re + rhs, self.im)

        if not isinstance(rhs, Complex):
            return NotImplemented

        return Complex(self.re + rhs.re, self.im + rhs.im)

    def __iadd__(self, rhs):
        self.re += rhs.re
        self.im += rhs.im
        return self

    def __radd__(self, rhs):
        if isinstance(rhs, (int, float)):
            return Complex(self.re + rhs, self.im)

    def __sub__(self, rhs):
        if isinstance(rhs, (int, float)):
            return Complex(self.re - rhs, self.im)

        if not isinstance(rhs, Complex):
            return NotImplemented

        return Complex(self.re - rhs.re, self.im - rhs.im)

    def __rsub__(self, rhs):
        # A - B == A.__sub__(B) -> B.__rsub__(A)
        if not isinstance(rhs, Complex):
            return Complex(rhs) - self

    def __isub__(self, rhs):
        if not isinstance(rhs, Complex):
            self -= Complex(rhs)
            return self

        self.re -= rhs.re
        self.im -= rhs.im
        return self

    def __neg__(self):
        return Complex(-self.re, -self.im)

    def __pos__(self):
        return Complex(self.re, self.im)

    def __eq__(self, rhs):
        if not isinstance(rhs, Complex):
            return self == Complex(rhs)

        return (self.re, self.im) == (rhs.re, rhs.im)

    def __str__(self):
        if abs(self.im) < 1e-9:
            return str(self.re)
        return "{}{}{}i".format(
            str(self.re), '+' if self.im > 0 else '', str(self.im))


class ComplexTest(unittest.TestCase):
    def test_real_part(self):
        a = Complex(5)
        self.assertEqual(5, a.get_real())

    def test_add(self):
        self.assertEqual(3 + Complex(1, 1), Complex(4, 1))
        self.assertEqual(Complex(1, 1) + 3, Complex(4, 1))

    def test_eq(self):
        self.assertEqual(Complex(1, 2), Complex(1, 2))
        self.assertEqual(2, Complex(2))
        self.assertEqual(Complex(2), 2)
        self.assertNotEqual(Complex(1, 3), Complex(1, 2))
        self.assertNotEqual(3, Complex(2))
        self.assertNotEqual(Complex(2), 3)

    def test_sub(self):
        self.assertEqual(5, Complex(5, 4) - Complex(0, 4))
        self.assertEqual(Complex(5, 1), Complex(6, 1) - 1)
        self.assertEqual(Complex(5), 6 - Complex(1))


if __name__ == '__main__':
    unittest.main()
