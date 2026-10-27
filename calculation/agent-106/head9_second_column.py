#!/usr/bin/env python3
"""Second-column obstruction for saturated decimal heads 9,18,9,18,...

The common padded B width must be at least two. Consider one temporal pair
with overflows 0,1, even head 9, odd head 18, and even second column q.
The inward even carry at the head is 0, so q+a<=9. The even low carry into
the second column is also 0; therefore its odd value is r=2*q+a.
The odd low carry into that column is 1. Write b for the odd inward carry
at the head, and c for the next odd inward carry. The carry consistency
is (r+c)//10=b. The next even second column is
    q2=(r+1)%10+(18+b)%10.
The following even phase requires q2<=9 again.

The resulting exact projected relation has three edges, none composable.
This is a finite local certificate, not a bounded-width or bounded-period
search. The paper proof supplies the bridge from padded A120 B cycles.
"""

from itertools import product


def local_rows():
    for q, a, b, c in product(range(10), (0, 1), (0, 1), (0, 1)):
        if q + a >= 10:
            continue
        r = 2 * q + a
        if (r + c) // 10 != b:
            continue
        q2 = (r + 1) % 10 + (18 + b) % 10
        if q2 <= 9:
            yield q, a, r, b, c, q2


def main():
    rows = list(local_rows())
    relation = sorted({(q, q2) for q, a, r, b, c, q2 in rows})
    assert relation == [(0, 9), (4, 8), (4, 9)]
    sources = {q for q, q2 in relation}
    targets = {q2 for q, q2 in relation}
    assert sources.isdisjoint(targets)
    print("HEAD9_SECOND_COLUMN_CHECK PASSED")
    print(f"input_assignments=80 surviving_assignments={len(rows)}")
    print("surviving_rows=" + str(rows))
    print("paired_relation=" + str(relation))
    print("composable_paired_edges=0")
    print("conclusion: no cyclic second-column trace for heads 9,18")


if __name__ == "__main__":
    main()
