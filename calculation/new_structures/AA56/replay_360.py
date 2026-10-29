#!/usr/bin/env python3
"""Independent genuine-integer replay for AA56's scoped 360-step diagnostics."""
B = [10,4,6,6,7,12,9,16,16,13,0,2,10,17,7,0,18,6,5,18,4,18,14,9,14,8,12,17,10,4,6,4,0,5]
W = [5,18,4,8,1,15,4,0,5]
CASES = [
    ([5], [9,14,4], [10], -32),
    ([6,4], [9,2,16], [12], -36),
    ([1,8,2], [9,0,18], [4,8,4], -34),
    ([5], [14,4,9], [10], -33),
]

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

def final_pairword(q, k, J, U, C, steps=360):
    h = B + W*q + J + U*k
    n = realize_pair(h + C + h[::-1])
    overflow = []
    for _ in range(steps):
        before = len(str(n))
        n = rev_add(n)
        overflow.append(len(str(n)) - before)
    return pairword(n), overflow

def replay(q, k, J, U, C, steps=360):
    got, overflow = final_pairword(q, k, J, U, C, steps)
    target_h = B + W*q + J + U*(k + 15)
    target = target_h + C + target_h[::-1]
    mismatch = next((i for i, (x, y) in enumerate(zip(got, target)) if x != y),
                    min(len(got), len(target)) if len(got) != len(target) else None)
    return mismatch, sum(overflow), ''.join(map(str, overflow[:48])), len(got), len(target)

def signatures(q, k, J, U, C):
    p, _ = final_pairword(q, k, J, U, C)
    w_suffix = tuple(p[len(B):len(B)+9*q][-90:])
    mid = len(p)//2
    centre = tuple(p[mid-10:mid+11])
    return w_suffix, centre

def main():
    # Known candidate seeds, not a census of seam space.
    runs = 0
    for idx, (J, U, C, offset) in enumerate(CASES):
        for q in (20, 40, 80, 160):
            for k in sorted(set((max(20, q//2), q, 2*q))):
                mismatch, total, prefix, got_len, target_len = replay(q, k, J, U, C)
                assert mismatch == 9*q + offset, (idx, q, k, mismatch, 9*q+offset)
                assert total == 90, (idx, q, k, total)
                assert got_len == target_len, (idx, q, k, got_len, target_len)
                assert prefix == '100010001000' * 4, (idx, q, k, prefix)
                runs += 1
                print(f'case={idx} q={q} k={k} steps=360 overflow_sum={total} '
                      f'first_mismatch={mismatch} boundary_offset={34+9*q-mismatch}')

    # Test whether a finite boundary apron is stable once both widths are >= 40.
    for idx, (J, U, C, _) in enumerate(CASES):
        baseline_apron = None
        centres_by_k = {k: [] for k in (40, 80, 160)}
        for q in (40, 80, 160):
            for k in (40, 80, 160):
                apron, centre = signatures(q, k, J, U, C)
                if baseline_apron is None:
                    baseline_apron = apron
                assert apron == baseline_apron, ('apron depends on q,k', idx, q, k)
                centres_by_k[k].append(centre)
        for k, windows in centres_by_k.items():
            assert all(x == windows[0] for x in windows), ('centre depends on q in sample', idx, k)
        centre_states = {windows[0] for windows in centres_by_k.values()}
        assert len(centre_states) > 1, ('centre did not vary with k', idx)
        runs += 9
        print(f'case={idx} W-apron-90 stable for q,k=40,80,160; '
              f'centre-window stable across q at fixed k but varies with k')
    print(f'AA56 scoped diagnostic PASS; big-int replays={runs}; no all-width claim.')

if __name__ == '__main__':
    main()
