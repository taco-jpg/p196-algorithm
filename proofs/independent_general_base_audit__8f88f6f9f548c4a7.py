#!/usr/bin/env python3
"""Independent sequential-carry replay of the retained general-base catalog.

No producer imports. Whole words and blocks are normalized column by
column with a carry; integer-to-digit normalization is not used for them.
Catalog completeness follows from separate closed domain counts.
"""

from collections import Counter
import gzip
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def normalize_columns(word, base, incoming=0):
    carry = incoming
    retained = []
    carries = [incoming]
    for coefficient in word:
        total = coefficient + carry
        digit = total % base
        carry = (total - digit) // base
        assert 0 <= digit < base and carry in (0, 1)
        retained.append(digit)
        carries.append(carry)
    return retained + [carry], carries


def value(word, base):
    result = 0
    for coefficient in reversed(word):
        result = result * base + coefficient
    return result


def seed_digits(seed, base):
    digits = []
    while seed:
        digits.append(seed % base)
        seed //= base
    return digits or [0]


def main():
    catalog = HERE / "all_controls.json.gz"
    report_path = HERE / "verification.json"
    report = json.loads(report_path.read_text())
    payload = gzip.decompress(catalog.read_bytes())
    rows = json.loads(payload)
    assert sha(catalog) == report["artifact"]["sha256"]
    assert hashlib.sha256(payload).hexdigest() == report["artifact"]["uncompressed_sha256"]
    seen = set()
    words = {base: set() for base in range(2, 13)}
    width_counts = Counter()
    binary_failures = []
    binary_one_block_residuals = []
    block_response_controls = 0
    palindrome_counts = Counter()
    active_counts = Counter()

    for row_index, row in enumerate(rows):
        base, q, mask = row["base"], row["q"], row["cut_mask"]
        length = len(q)
        assert 2 <= base <= 12 and 1 <= length <= 4
        assert q == q[::-1] and q[0] > 0
        assert all(0 <= coefficient <= 2 * base - 2 for coefficient in q)
        assert not length % 2 or q[length // 2] % 2 == 0
        assert 0 <= mask < 2 ** (length - 1)
        key = (base, tuple(q), mask)
        assert key not in seen
        seen.add(key)
        words[base].add(tuple(q))
        width_counts[base, length] += 1

        full_d, actual_carry = normalize_columns(q, base)
        overflow = actual_carry[-1]
        width = length + overflow
        d = full_d[:width]
        assert d[-1] > 0 and not any(full_d[width:])
        assert d == row["digits"]
        cuts = [0]
        cuts.extend(i for i in range(1, length) if mask & (2 ** (i - 1)))
        cuts.append(length)
        raw = [0] * (length + 1)
        isolated = [0] * length
        seam = [0] * (length + 1)
        actual_block_sum = [0] * (length + 1)
        seam_incoming_sum = [0] * (length + 1)

        for start, end in zip(cuts, cuts[1:]):
            block = q[start:end]
            zero_digits, zero_carry = normalize_columns(block, base, 0)
            one_digits, one_carry = normalize_columns(block, base, 1)
            for i, digit in enumerate(zero_digits):
                raw[start + i] += digit
            isolated[start:end] = zero_carry[1:]
            neutral_run = 0
            while neutral_run < len(block) and block[neutral_run] == base - 1:
                neutral_run += 1
            # The input-one carry difference lasts exactly through the
            # initial base-minus-one run, including an all-neutral block.
            assert [one_carry[i + 1] - zero_carry[i + 1]
                    for i in range(len(block))] == [int(i < neutral_run) for i in range(len(block))]
            for i in range(len(block) + 1):
                expected = (1 if i == 0 else 0)
                expected += (1 if 1 <= i <= neutral_run else 0)
                expected -= base * int(i < neutral_run)
                assert one_digits[i] - zero_digits[i] == expected
            block_response_controls += 1

            incoming = actual_carry[start]
            incoming_digits, incoming_carries = normalize_columns(block, base, incoming)
            assert incoming_carries == actual_carry[start:end + 1]
            for i, digit in enumerate(incoming_digits):
                actual_block_sum[start + i] += digit
            if start:
                seam_incoming_sum[start] += incoming
            for i in range(neutral_run):
                seam[start + i] += incoming

        # Every actual block's terminal carry is included once extra at
        # its successor's start; subtract exactly those seam terms.
        assert actual_block_sum == [d_i + extra for d_i, extra in zip(full_d, seam_incoming_sum)]
        assert isolated == row["isolated_carries"]
        assert raw[:width] == row["raw"] and not any(raw[width:])
        assert seam[:width] == row["seam_mask"] and not any(seam[width:])
        for i in range(length + 1):
            previous_c = isolated[i - 1] if i else 0
            current_c = isolated[i] if i < length else 0
            q_i = q[i] if i < length else 0
            assert raw[i] == q_i + previous_c - base * current_c
            assert full_d[i] - raw[i] == (seam[i - 1] if i else 0) - base * seam[i]
        assert value(raw, base) == value(d, base)
        assert value(d, base) < base ** width
        assert sum(raw) - sum(d) == (base - 1) * sum(seam)

        paired_d = [a + b for a, b in zip(d, reversed(d))]
        raw_at_width = raw[:width]
        paired_raw = [a + b for a, b in zip(raw_at_width, reversed(raw_at_width))]
        assert sum(paired_raw) - sum(paired_d) == 2 * (base - 1) * sum(seam)
        raw_symmetric = raw_at_width == raw_at_width[::-1]
        actual_symmetric = d == d[::-1]
        classification = (all(coefficient <= base - 1 for coefficient in q)
                          or (q[0] == base + 1 and all(coefficient in (0, base + 1) for coefficient in q)))
        assert raw_symmetric == row["raw_symmetric"]
        assert actual_symmetric == row["actual_symmetric"]
        assert classification == row["classification"]
        residual = [coefficient - (base + 1) * carry for coefficient, carry in zip(q, isolated)]
        assert all(-2 <= coefficient <= base - 1 for coefficient in residual)
        if raw_symmetric:
            if not overflow:
                assert not any(isolated)
            else:
                scaled_residual = sum(coefficient * base ** (length - 1 - i)
                                      for i, coefficient in enumerate(residual))
                assert scaled_residual == 0
                if base >= 3:
                    assert not any(residual)
                elif mask == 0 and any(residual):
                    binary_one_block_residuals.append(dict(q=q, residual=residual))
        if base >= 3:
            assert raw_symmetric == actual_symmetric == classification
            if raw_symmetric or actual_symmetric:
                assert raw == full_d and not any(seam)
            if any(seam):
                assert not actual_symmetric
        else:
            if raw_symmetric != actual_symmetric or (any(seam) and actual_symmetric):
                binary_failures.append(row_index)
        palindrome_counts[base] += actual_symmetric
        active_counts[base] += bool(any(seam))

        # Check the supplied seed by its own ordinary base digits; this
        # is independent of the producer's particular split construction.
        seed = seed_digits(row["seed"], base)
        assert len(seed) == length and seed[-1] > 0
        assert [a + b for a, b in zip(seed, reversed(seed))] == q
        assert row["seed"] + value(list(reversed(seed)), base) == value(d, base)

    # Closed domain sizes for lengths1..4 establish completeness without
    # repeating the producer's half-word Cartesian-product enumeration.
    counts = {}
    for base in range(2, 13):
        domain = [base - 1, 2 * base - 2, (2 * base - 2) * base,
                  (2 * base - 2) * (2 * base - 1)]
        for length, word_count in enumerate(domain, 1):
            assert width_counts[base, length] == word_count * 2 ** (length - 1)
        counts[str(base)] = dict(words=len(words[base]), partitions=sum(width_counts[base, length]
                                                                      for length in range(1, 5)))
        assert counts[str(base)] == dict(words=(base - 1) * (6 * base + 1),
                                        partitions=(base - 1) * (40 * base - 11))
    assert counts == report["counts_by_base"]
    assert len(rows) == len(seen) == report["total_controls"] == 22154
    assert binary_failures == report["binary_failure_indices"]
    counterexample = report["binary_counterexample"]
    assert counterexample in rows
    assert counterexample["q"] == [1, 2, 1] and counterexample["seed"] == 6
    assert counterexample["digits"] == [1, 0, 0, 1] and value(counterexample["digits"], 2) == 9
    assert counterexample["raw"] == [1, 0, 2, 0]
    assert counterexample["seam_mask"] == [0, 0, 1, 0]
    assert dict(q=[1, 2, 1], residual=[1, -1, -2]) in binary_one_block_residuals

    result = dict(status="PASS_GENERAL_BASE_REPLAY", total_controls=len(rows),
                  base_range=[2, 12], physical_input_width_range=[1, 4],
                  block_response_controls=block_response_controls,
                  counts_by_base=counts,
                  palindrome_partition_cases_by_base=dict(sorted(palindrome_counts.items())),
                  active_seam_cases_by_base=dict(sorted(active_counts.items())),
                  binary_failure_indices=binary_failures,
                  binary_one_block_nonzero_residuals=binary_one_block_residuals,
                  binary_counterexample=counterexample,
                  whole_and_block_normalization="sequential retained digit/carry recurrence, including every terminal carry",
                  completeness="unique valid catalog keys plus exact per-base/per-width domain counts",
                  checked_identities=["E=Q+(x-b)C", "sum actual block normalizations=D+internal incoming seam terms",
                                      "D-E=(x-b)K", "D(1)=E(1)-(b-1)K(1)",
                                      "paired raw mass minus actual pair mass=2(b-1)K(1)"],
                  catalog_sha256=sha(catalog), catalog_uncompressed_sha256=hashlib.sha256(payload).hexdigest(),
                  producer_source_sha256=sha(HERE / "check_general_base.py"),
                  producer_report_sha256=sha(report_path),
                  reviewed_proof_sha256=sha(HERE / "GENERAL_BASE_SEAMS.md"),
                  scope="Complete independent replay of the retained bounded catalog. The all-base/all-width conclusion is justified by the separately reviewed written proof, not this finite catalog alone.")
    (HERE / "independent_general_base_audit.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({key: result[key] for key in ("status", "total_controls", "block_response_controls", "binary_failure_indices")}))


if __name__ == "__main__":
    main()
