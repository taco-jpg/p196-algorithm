#!/usr/bin/env python3
"""Independent verifier: reads an explicit integer N_0 (base-b digits, LSB first, from the JSON) and iterates
N -> N + reverse(N) with Python big integers (base conversion by divmod), checking for palindromes.  No templates used."""
import sys, json
def to_digits(n, b):
    d = []
    while n:
        n, r = divmod(n, b); d.append(r)
    return d
def from_digits(d, b):
    n = 0
    for x in reversed(d): n = n * b + x
    return n
def main(fn, steps):
    J = json.load(open(fn))
    b = J['base']; d = J['N0_digits_lsb']
    assert all(0 <= x < b for x in d) and d[-1] >= 1
    n = from_digits(d, b)
    lens = []
    for s in range(steps):
        dd = to_digits(n, b)
        if dd == dd[::-1]:
            print('PALINDROME at step', s, '(N_%d)' % s); return 1
        n = n + from_digits(dd[::-1], b)
        if s % 100 == 0: lens.append(len(to_digits(n, b)))
    dd = to_digits(n, b)
    print(f'base {b}: N_0 has {len(d)} digits; {steps} reverse-and-add steps, no palindrome among N_0..N_{steps-1} (N_{steps} has {len(dd)} digits).')
    return 0
if __name__ == '__main__':
    sys.exit(main(sys.argv[1], int(sys.argv[2])))
