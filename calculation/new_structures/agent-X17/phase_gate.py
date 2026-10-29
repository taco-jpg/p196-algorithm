#!/usr/bin/env python3
"""Independent Python-bigint oracle for X17's length-residue carry gate."""
import csv
import sys

sys.set_int_max_str_digits(0)
MOTIF = "88283583"
NS = (2001, 2009, 6001, 6009, 10001, 10009, 20001, 20009)
TIMES = (106, 107, 108, 109)

def reverse_add(x):
    s = str(x)
    return x + int(s[::-1])

def words_at(n):
    # Here source strings are constructed MSD-first, unlike the C++ digit engine.
    p = int("".join(MOTIF[min(i, n - i - 1) % 8] for i in range(n)))
    q = p + 10 ** (n // 2 - 1)
    for t in range(max(TIMES) + 1):
        if t in TIMES:
            a, b = str(p)[::-1], str(q)[::-1]
            assert len(a) == len(b)
            size = len(a)
            left = next((i for i in range(size) if a[i] != b[i]), size)
            right = next((i for i in range(size) if a[size - 1 - i] != b[size - 1 - i]), size)
            pairs = [int(a[i]) + int(a[size - 1 - i]) for i in range(size)]
            st = size - right
            run = 0
            while st + run < size and pairs[st + run] == 9:
                run += 1
            stop = pairs[st + run] if st + run < size else -1
            yield (n, t, size, left, right, run, stop)
        p, q = reverse_add(p), reverse_add(q)

def main(output):
    assert [reverse_add(z) for z in (196, 89, 1001)] == [887, 187, 2002]
    rows = [r for n in NS for r in words_at(n)]
    lookup = {(n, t): (length, left, right, run, stop)
              for n, t, length, left, right, run, stop in rows}
    for n in NS:
        if n % 16 == 1:
            l, left, right, run, stop = lookup[n, 107]
            assert left == right == (n - 39) // 2
            assert run == (n - 161) // 2 and stop == 10
            assert lookup[n, 108][2] == 60
            assert lookup[n, 109][1] == 60
        else:
            assert n % 16 == 9
            assert lookup[n, 107][3] == 0
            assert lookup[n, 108][1] > 900 and lookup[n, 108][2] > 900
    with open(output, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(('n', 't', 'length', 'same_lsd', 'same_msd',
                         'nine_run_from_high_defect_boundary', 'first_stopper'))
        writer.writerows(rows)
    print('PASS:', len(rows), 'exact Python bigint checkpoints across', len(NS),
          'seeds, residue-dependent 9-carry gate at t=107 -> 108')

if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else 'phase_gate.csv')