#!/usr/bin/env python3


for x in range(10**4, 10**5):
    a5 = x % 10
    a4 = (x//10) % 10
    a3 = (x//100) % 10
    a2 = (x//1000) % 10
    a1 = (x//10000) % 10

    if (a1*a2 == 24 and a1 + a2 + a3 + a4 + a5 == 26 and 2*a4 == a2 and
            a1 + a3 == a2 + a4):
        print(x)
