#!/usr/bin/env python3
"""Independent exact checks of the sparse-orbit zero-gap proof.

No code is imported from the proof author's implementation.  These finite
checks support, but do not replace, the accompanying general proof audit.
"""
from itertools import product
import json
from pathlib import Path


def digits(n):
    return [int(x) for x in str(n)[::-1]]


def pair_sums(ds):
    return [x + y for x, y in zip(ds, ds[::-1])]


def zero_runs(q):
    result = []
    start = None
    for i, x in enumerate(q + [1]):
        if x == 0 and start is None:
            start = i
        elif x != 0 and start is not None:
            result.append((start, i - 1))
            start = None
    return result


def gap(q):
    return max((b - a + 1 for a, b in zero_runs(q)), default=0)


def ordinary_representative(q):
    """Build canonical source digits whose mirrored sums are q."""
    L = len(q)
    ds = [0] * L
    for i in range(L // 2):
        x = q[i]
        high = min(x, 9)
        ds[L - 1 - i] = high
        ds[i] = x - high
    if L % 2:
        assert q[L // 2] % 2 == 0
        ds[L // 2] = q[L // 2] // 2
    assert ds[-1] != 0
    assert pair_sums(ds) == q
    return int(''.join(map(str, ds[::-1])))


COUNTS = {
    "canonical_pair_words": 0,
    "nonoverflow_steps": 0,
    "overflow_steps": 0,
    "new_long_zero_runs": 0,
    "inherited_zero_runs": 0,
    "nine_core_zero_runs": 0,
}
MAX_GAPS = [0, 0]


def check(q, numeric=False):
    L = len(q)
    assert L >= 1 and q[0] > 0 and q == q[::-1]
    carries = [0]
    out = []
    for x in q:
        total = x + carries[-1]
        out.append(total % 10)
        carries.append(total // 10)
    assert all(c in (0, 1) for c in carries)
    h = carries[-1]
    actual_digits = out + ([1] if h else [])
    assert actual_digits[-1] > 0
    nxt = pair_sums(actual_digits)
    backward = carries[::-1]
    reflected = out[::-1]
    assert all(q[i] + backward[i + 1] == reflected[i] + 10 * backward[i]
               for i in range(L))
    if h:
        formula = [out[0] + 1]
        formula.extend(out[i] + reflected[i - 1] for i in range(1, L))
        formula.append(out[0] + 1)
    else:
        formula = [out[i] + reflected[i] for i in range(L)]
    assert formula == nxt
    assert nxt[0] > 0 and nxt[-1] > 0
    if numeric:
        n = ordinary_representative(q)
        m = n + int(str(n)[::-1])
        assert digits(m) == actual_digits
        assert pair_sums(digits(n)) == q

    M = sum(q)
    G = gap(q)
    H = gap(nxt)
    assert H <= max(G, 2, M // 9 + 1)
    if h:
        assert H <= max(max(G - 1, 0), 2, M // 9 + 1)
    else:
        assert H <= max(G, 1, M // 9)
    MAX_GAPS[0] = max(MAX_GAPS[0], G)
    MAX_GAPS[1] = max(MAX_GAPS[1], H)
    for a, b in zero_runs(nxt):
        k = b - a + 1
        assert 1 <= a <= b <= len(nxt) - 2
        if k < 2 + h:
            continue
        COUNTS["new_long_zero_runs"] += 1
        core = q[a:b + 1 - h]
        assert len(core) == k - h >= 2
        assert core == [0] * len(core) or core == [9] * len(core)
        if core[0] == 0:
            inherited = q[a - h:b + 1]
            assert inherited == [0] * (k + h)
            COUNTS["inherited_zero_runs"] += 1
        else:
            assert 9 * (k - h) <= M
            COUNTS["nine_core_zero_runs"] += 1
    COUNTS["canonical_pair_words"] += 1
    COUNTS["overflow_steps" if h else "nonoverflow_steps"] += 1


def local_checks():
    zero_edges = []
    for a, ap, b, bp in product(range(2), repeat=4):
        for q in range(19):
            if q + a == 10 * ap and q + bp == 10 * b:
                zero_edges.append(((a, b), (ap, bp), q))
    assert set(zero_edges) == {
        ((0, 0), (0, 0), 0),
        ((0, 1), (1, 0), 10),
        ((1, 1), (1, 1), 9),
    }
    paths = []
    for first, second in product(zero_edges, repeat=2):
        if first[1] == second[0]:
            paths.append((first[2], second[2]))
    assert set(paths) == {(0, 0), (9, 9)}
    return {"simultaneous_zero_edges": zero_edges,
            "two_site_simultaneous_zero_words": paths}


def all_canonical_q(max_length):
    for L in range(1, max_length + 1):
        half = (L + 1) // 2
        alphabets = [range(19)] * half
        alphabets[0] = range(1, 19)
        if L % 2:
            alphabets[-1] = range(2 if L == 1 else 0, 19, 2)
        for prefix in product(*alphabets):
            yield list(prefix) + list(prefix[:-1] if L % 2 else prefix)[::-1]


def main():
    report = {"local": local_checks()}
    for q in all_canonical_q(8):
        check(q, numeric=True)
    report["exhaustive_length_at_most_8"] = dict(COUNTS)
    report["maximum_source_and_target_zero_gap"] = list(MAX_GAPS)

    # Larger gaps explicitly cover inheritance through overflow, outer zeros
    # in the ordinary source, and the one-site q=10 exceptional case.
    structured = []
    for L in (9, 10, 31, 32, 99, 100, 299, 300):
        for endpoint in range(1, 19):
            for background in (0, 9):
                q = [endpoint] + [background] * (L - 2) + [endpoint]
                if L % 2:
                    q[L // 2] = 0 if background == 0 else 10
                check(q, numeric=True)
                structured.append((L, endpoint, background))
    for n in (1, 5, 9, 10, 100, 1000, 950, 999, 9990, 9999000,
              10**300, 10**300 + 1, 9 * 10**299 + 5 * 10**150):
        check(pair_sums(digits(n)), numeric=True)
    report["structured_long_word_cases"] = len(structured)
    report["explicit_numeric_edge_cases"] = 13
    report["total_checks"] = dict(COUNTS)
    report["status"] = "PASS"
    path = Path(__file__).with_name("zero_gap_audit_results.json")
    path.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
