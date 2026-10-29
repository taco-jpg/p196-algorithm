#!/usr/bin/env python3
"""Independent genuine-integer replay for AA56's scoped 360-step negative test."""
B = [10,4,6,6,7,12,9,16,16,13,0,2,10,17,7,0,18,6,5,18,4,18,14,9,14,8,12,17,10,4,6,4,0,5]
W = [5,18,4,8,1,15,4,0,5]
J = [5]
U = [9,14,4]
C = [10]

def realize_pair(p):
    d = [0] * len(p)
    for i in range(len(d)//2):
        hi = min(9, p[i])
        lo = p[i] - hi
        assert 0 <= lo <= 9, (i, p[i])
        d[i], d[-1-i] = lo, hi
    if len(d) % 2:
        mid = p[len(d)//2]
        assert mid % 2 == 0, mid
        d[len(d)//2] = mid // 2
    assert d[-1] != 0
    return int(''.join(map(str, reversed(d))))

def rev_add(n):
    return n + int(str(n)[::-1])

def pairword(n):
    d = list(map(int, str(n)[::-1]))
    return [d[i] + d[-1-i] for i in range(len(d))]

def replay(q, k, steps=360):
    h = B + W*q + J + U*k
    source_pair = h + C + h[::-1]
    n = realize_pair(source_pair)
    overflow = []
    for _ in range(steps):
        before = len(str(n))
        n = rev_add(n)
        overflow.append(len(str(n)) - before)
    target_h = B + W*q + J + U*(k + 15)
    target = target_h + C + target_h[::-1]
    got = pairword(n)
    mismatch = next((i for i, (x, y) in enumerate(zip(got, target)) if x != y),
                    min(len(got), len(target)) if len(got) != len(target) else None)
    return mismatch, sum(overflow), ''.join(map(str, overflow[:48])), len(got), len(target)

def main():
    expected = {20:148, 40:328, 80:688, 160:1408}
    for q in (20, 40, 80, 160):
        k = q
        mismatch, total, prefix, got_len, target_len = replay(q, k)
        assert mismatch == expected[q], (q, mismatch, expected[q])
        assert total == 90, (q, total)
        assert got_len == target_len, (q, got_len, target_len)
        assert prefix == '100010001000' * 4, (q, prefix)
        print(f'q={q} k={k} steps=360 overflow_sum={total} '
              f'first_mismatch={mismatch} expected_9q_minus_32={9*q-32} '
              f'pairword_lengths={got_len}/{target_len}')
    print('AA56 scoped negative replay PASS; no all-width claim.')

if __name__ == '__main__':
    main()
