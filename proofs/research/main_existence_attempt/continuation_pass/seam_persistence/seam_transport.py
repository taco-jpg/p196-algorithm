"""Exact active-seam masks, typed transport, and annihilation controls.

The all-width arguments are in METHOD_AND_PROOF.md.  This program does not
infer induction from a finite sample and imports none of the older seam code.
"""
from __future__ import annotations

import gzip
import hashlib
import itertools
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent


def normalize(q, incoming=0):
    digits, carries = [], [incoming]
    for x in q:
        y = x + carries[-1]
        digits.append(y % 10)
        carries.append(y // 10)
    return tuple(digits), tuple(carries)


def pair_step(q):
    d, a = normalize(q)
    if a[-1]:
        d += (a[-1],)
    return tuple(x + y for x, y in zip(d, d[::-1]))


def integer_pair_step(q):
    n = sum(x * 10**i for i, x in enumerate(q))
    d = tuple(map(int, str(n)[::-1]))
    return tuple(x + y for x, y in zip(d, d[::-1]))


def canonical_words(max_width):
    for width in range(1, max_width + 1):
        if width == 1:
            yield from ((2 * k,) for k in range(1, 10))
            continue
        for outside in range(1, 19):
            for middle in itertools.product(range(19), repeat=width // 2 - 1):
                left = (outside,) + middle
                centers = ((2 * k,) for k in range(10)) if width % 2 else ((),)
                for center in centers:
                    yield left + center + left[::-1]


def nine_runs(q):
    i = 0
    while i < len(q):
        if q[i] != 9:
            i += 1
            continue
        start = i
        while i < len(q) and q[i] == 9:
            i += 1
        yield start, i


def active_runs(q):
    return tuple((a, b) for a, b in nine_runs(q) if a > 0 and q[a - 1] >= 10)


def maximal_mask(q):
    _, a = normalize(q)
    return tuple(int(x == 9 and a[i] == 1) for i, x in enumerate(q))


def partition_mask(q, cuts):
    _, actual = normalize(q)
    isolated, c = [], 0
    for i, x in enumerate(q):
        if i in cuts:
            c = 0
        c = (x + c) // 10
        isolated.append(c)
    return tuple(a - c for a, c in zip(actual[1:], isolated))


def predicted_masks(q):
    runs = active_runs(q)
    out = set()
    for lengths in itertools.product(*(range(b - a + 1) for a, b in runs)):
        mask = [0] * len(q)
        for (a, b), length in zip(runs, lengths):
            mask[b - length:b] = [1] * length
        out.add(tuple(mask))
    return out


def is_palindrome_predecessor(q):
    return max(q) <= 9 or (q[0] == 11 and all(x in (0, 11) for x in q))


def check_transport(q, out, records):
    _, a = normalize(q)
    _, backward_reversed = normalize(q[::-1])
    beta = backward_reversed[::-1]
    gamma = a[-1]
    if gamma == 0:
        for i, x in enumerate(q):
            assert (out[i] == 9) == (x in (4, 9, 14) and a[i] != beta[i + 1])
    else:
        for i in range(1, len(q)):
            x, y = q[i - 1:i + 1]
            if x != 9 and y != 9:
                f = lambda z: z - 9 * (z >= 10)
                assert out[i] == f(x) + f(y)
    for start, end in nine_runs(q):
        if start == 0 or end == len(q):
            continue
        h, l = q[start - 1], q[end]
        if not (h >= 10 and l <= 8):
            continue
        ell = end - start
        exterior_left, exterior_right = a[start - 1], beta[end + 1]
        if gamma:
            expected = (h - 10,) + (9,) * (ell - 1) + (l + 10,)
            observed = out[start:end + 1]
            assert observed == expected
            if ell >= 2:
                # The output whole word is symmetric; the reflected edge is H9.
                assert any(maximal_mask(out))
        else:
            expected = (2 * h - 20 + exterior_left,) + (9,) * ell + (2 * l + 1 + exterior_right,)
            observed = out[start - 1:end + 1]
            assert observed == expected
            if h >= 15 or l >= 5 or (l == 4 and exterior_right == 1):
                assert any(maximal_mask(out))
        records.append({"q": q, "gamma": gamma, "run": [start, end],
                        "exterior_carries": [exterior_left, exterior_right],
                        "output_factor": observed})


def annihilation_families():
    records = []
    for r in (1, 2, 3, 4, 8, 31, 100):
        q = (10,) + (9,) * (2 * r) + (10,)
        n = 10 ** (2 * r + 2) - 10 ** (r + 1) + 1
        ds = tuple(map(int, str(n)[::-1]))
        assert tuple(x + y for x, y in zip(ds, ds[::-1])) == q
        first = n + int(str(n)[::-1])
        second = first + int(str(first)[::-1])
        assert first == 11 * 10 ** (2 * r + 1)
        assert second == 11 * (10 ** (2 * r + 1) + 1)
        expected = (1, 1) + (0,) * (2 * r - 1) + (1, 1)
        assert pair_step(q) == expected
        assert sum(maximal_mask(q)) == 2 * r
        assert str(first) != str(first)[::-1] and str(second) == str(second)[::-1]
        records.append({"family": "arbitrary_density_annihilation", "r": r,
                        "q": q, "seed": str(n), "first": str(first),
                        "second": str(second), "next_pair": expected,
                        "maximal_mask_mass": 2 * r})
    for ell in (1, 2, 3, 8, 31, 100):
        q = (1,) + (9,) * ell + (10,) + (9,) * ell + (1,)
        expected = (3,) + (9,) * ell + (0,) + (9,) * ell + (3,)
        assert pair_step(q) == expected
        assert sum(maximal_mask(q)) == ell
        assert is_palindrome_predecessor(expected)
        records.append({"family": "mixed_run_annihilation", "ell": ell,
                        "q": q, "next_pair": expected, "maximal_mask_mass": ell})
        q = (8,) + (9,) * ell + (18,) + (9,) * ell + (8,)
        first = (17,) + (9,) * ell + (16,) + (9,) * ell + (17,)
        second = (8, 8) + (0,) * (ell - 1) + (7, 7) + (0,) * (ell - 1) + (8, 8)
        assert pair_step(q) == first and pair_step(first) == second
        assert any(maximal_mask(q)) and any(maximal_mask(first))
        assert is_palindrome_predecessor(second)
        records.append({"family": "guarded_run_delayed_annihilation", "ell": ell,
                        "q": q, "first_pair": first, "second_pair": second})
    return records


def main():
    counts = {"canonical_words": 0, "partitions": 0, "active_words": 0,
              "no_overflow": 0, "overflow": 0, "distinct_masks": 0}
    digest = hashlib.sha256()
    transports = []
    failures = {"active_to_inactive": 0, "active_to_palindrome_predecessor": 0}
    first_failures = {}
    for q in canonical_words(7):
        counts["canonical_words"] += 1
        out = pair_step(q)
        assert out == integer_pair_step(q)
        mask = maximal_mask(q)
        active = any(mask)
        assert active == any(x >= 10 and y == 9 for x, y in zip(q, q[1:]))
        assert sum(mask) == sum(b - a for a, b in active_runs(q))
        counts["active_words"] += active
        counts["overflow" if len(out) > len(q) else "no_overflow"] += 1
        if active:
            assert not is_palindrome_predecessor(q)
            if not any(maximal_mask(out)):
                failures["active_to_inactive"] += 1
                first_failures.setdefault("active_to_inactive", {"q": q, "next_pair": out})
            if is_palindrome_predecessor(out):
                failures["active_to_palindrome_predecessor"] += 1
                first_failures.setdefault("active_to_palindrome_predecessor", {"q": q, "next_pair": out})
        if len(q) <= 5:
            masks = set()
            for cutbits in range(1 << (len(q) - 1)):
                cuts = {i + 1 for i in range(len(q) - 1) if cutbits >> i & 1}
                observed = partition_mask(q, cuts)
                masks.add(observed)
                counts["partitions"] += 1
            expected = predicted_masks(q)
            assert masks == expected
            assert len(masks) == __import__("math").prod(b - a + 1 for a, b in active_runs(q))
            assert {sum(m) for m in masks} == set(range(sum(mask) + 1))
            counts["distinct_masks"] += len(masks)
            digest.update(json.dumps([q, sorted(masks)], separators=(",", ":")).encode())
        check_transport(q, out, transports)
    family_records = annihilation_families()
    payload = json.dumps({"transport_controls": transports, "annihilation_controls": family_records},
                         sort_keys=True, separators=(",", ":")).encode()
    archive = HERE / "seam_transport_controls.json.gz"
    archive.write_bytes(gzip.compress(payload, mtime=0))
    summary = {"status": "PASS; all-width proofs are separate; no persistent safety invariant claimed",
               "counts": counts, "failure_counts": failures, "first_failures": first_failures,
               "transport_controls": len(transports),
               "transport_overflow_controls": sum(r["gamma"] for r in transports),
               "annihilation_controls": len(family_records),
               "mask_enumeration_sha256": digest.hexdigest(),
               "archive": archive.name, "archive_payload_sha256": hashlib.sha256(payload).hexdigest()}
    (HERE / "seam_transport_results.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
