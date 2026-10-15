#!/usr/bin/env python3
"""Finite arithmetic controls for the separate all-base written proof.

Uses literal integer normalization for each isolated block and the whole
word. The complete bounded catalog is retained, including base-2 failures.
"""
import gzip
import hashlib
import io
import itertools
import json
import os
from pathlib import Path

HERE = Path(__file__).resolve().parent


def digits(value, base):
    result = []
    while value:
        result.append(value % base)
        value //= base
    return result or [0]


def polynomial(word, base):
    return sum(coefficient * base ** i for i, coefficient in enumerate(word))


def control(q, base, mask):
    length = len(q)
    cuts = [0] + [i for i in range(1, length) if mask >> (i - 1) & 1] + [length]
    d = digits(polynomial(q, base), base)
    width = len(d)
    assert width in (length, length + 1)
    e = [0] * (length + 1)
    isolated = [0] * length
    actual = [0]
    for coefficient in q:
        actual.append((coefficient + actual[-1]) // base)
    k = [0] * (length + 1)
    for start, end in zip(cuts, cuts[1:]):
        block_digits = digits(polynomial(q[start:end], base), base)
        for i, digit in enumerate(block_digits):
            e[start + i] += digit
        carry = 0
        for i in range(start, end):
            carry = (q[i] + carry) // base
            isolated[i] = carry
        for i in range(start, end):
            if q[i] != base - 1:
                break
            k[i] = actual[start]
    assert not any(e[width:])
    assert not any(k[width:])
    full_d = d + [0] * (length + 1 - width)
    for i in range(length + 1):
        previous_c = isolated[i - 1] if i else 0
        current_c = isolated[i] if i < length else 0
        coefficient = q[i] if i < length else 0
        assert e[i] == coefficient + previous_c - base * current_c
        assert full_d[i] - e[i] == (k[i - 1] if i else 0) - base * k[i]
    assert sum(full_d) == sum(e) - (base - 1) * sum(k)
    raw_symmetric = e[:width] == e[:width][::-1]
    actual_symmetric = d == d[::-1]
    classified = (max(q) < base or
                  (q[0] == base + 1 and all(x in (0, base + 1) for x in q)))
    if base >= 3:
        assert raw_symmetric == actual_symmetric == classified
        if actual_symmetric:
            assert e == full_d and not any(k)
    # Realize a canonical seed independently, including odd-center parity.
    seed_digits = [0] * length
    for i in range(length // 2):
        seed_digits[i] = max(0, q[i] - (base - 1))
        seed_digits[length - 1 - i] = min(base - 1, q[i])
    if length % 2:
        seed_digits[length // 2] = q[length // 2] // 2
    seed = polynomial(seed_digits, base)
    assert seed_digits[-1] > 0
    assert seed + polynomial(seed_digits[::-1], base) == polynomial(q, base)
    return dict(base=base, q=q, cut_mask=mask, seed=seed, digits=d,
                raw=e[:width], isolated_carries=isolated, seam_mask=k[:width],
                raw_symmetric=raw_symmetric, actual_symmetric=actual_symmetric,
                classification=classified)


def main():
    records = []
    counts = {}
    binary_failures = []
    for base in range(2, 13):
        words = partitions = 0
        for length in range(1, 5):
            for half in itertools.product(range(2 * base - 1), repeat=(length + 1) // 2):
                if not half[0] or (length % 2 and half[-1] % 2):
                    continue
                q = list(half) + list(reversed(half[:length // 2]))
                words += 1
                for mask in range(1 << (length - 1)):
                    row = control(q, base, mask)
                    if base == 2 and (row["raw_symmetric"] != row["actual_symmetric"] or
                                      (any(row["seam_mask"]) and row["actual_symmetric"])):
                        binary_failures.append(len(records))
                    records.append(row)
                    partitions += 1
        counts[str(base)] = dict(words=words, partitions=partitions)
    explicit = control([1, 2, 1], 2, 3)
    assert explicit["seed"] == 6
    assert explicit["raw"] == [1, 0, 2, 0]
    assert explicit["digits"] == [1, 0, 0, 1]
    assert explicit["seam_mask"] == [0, 0, 1, 0]
    payload = (json.dumps(records, separators=(",", ":")) + "\n").encode()
    buffer = io.BytesIO()
    with gzip.GzipFile(fileobj=buffer, mode="wb", filename="", mtime=0) as stream:
        stream.write(payload)
    artifact = HERE / "all_controls.json.gz"
    temporary = artifact.with_suffix(".atomic-tmp")
    temporary.write_bytes(buffer.getvalue())
    os.replace(temporary, artifact)
    report = dict(status="PASS_BOUNDED_CONTROLS", bases=[2, 12], widths=[1, 4],
                  counts_by_base=counts, total_controls=len(records),
                  binary_failure_indices=binary_failures, binary_counterexample=explicit,
                  artifact=dict(filename=artifact.name,
                                compressed_bytes=artifact.stat().st_size,
                                sha256=hashlib.sha256(artifact.read_bytes()).hexdigest(),
                                uncompressed_sha256=hashlib.sha256(payload).hexdigest()),
                  scope="Finite arithmetic controls only. GENERAL_BASE_SEAMS.md supplies the all-base, all-width proof; base2 failures are intentionally retained.")
    (HERE / "verification.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(dict(status=report["status"], total_controls=len(records),
                         binary_failures=len(binary_failures))))


if __name__ == "__main__":
    main()
