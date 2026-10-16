#!/usr/bin/env python3
"""Review the frozen neutral-exterior controls using integer evaluation.

Replays the producer only in a temporary directory. Independent checking
extracts normalized digits from the integer value, without its carry loop.
"""

import gzip
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent / "2026-10-15-neutral-exterior-overflow"


def digest(blob):
    return hashlib.sha256(blob).hexdigest()


def main():
    files = ("NEUTRAL_EXTERIOR.md", "check.py", "controls.json.gz", "verification.json")
    before = {name: digest((SOURCE/name).read_bytes()) for name in files}
    declared = json.loads((SOURCE/"verification.json").read_text())
    packed = (SOURCE/"controls.json.gz").read_bytes()
    raw = gzip.decompress(packed)
    assert digest(packed) == declared["compressed_sha256"]
    assert digest(raw) == declared["raw_sha256"]
    assert len(packed) == declared["compressed_bytes"]
    assert len(raw) == declared["raw_bytes"]
    assert digest((SOURCE/"check.py").read_bytes()) == declared["source_sha256"]
    table = json.loads(raw)
    assert table["columns"] == ["base", "input", "value", "digits", "pairs", "overflow", "witness"]
    seen, counts = set(), {}
    overflows = neutral = 0
    for base, p, value, ds, pairs, overflow, witness in table["records"]:
        M = len(p)
        assert 2 <= base <= 10 and M in (1, 2, 3, 4, 5, 6, 8)
        assert p == p[::-1] and p[0] == base-1
        assert all(0 <= x <= 2*base-2 for x in p)
        key = (base, tuple(p))
        assert key not in seen
        seen.add(key)
        counts[base, M] = counts.get((base, M), 0)+1
        number = 0
        for x in reversed(p):
            number = base*number+x
        assert number == value
        actual, remainder = [], number
        while remainder:
            remainder, digit = divmod(remainder, base)
            actual.append(digit)
        assert actual == ds
        assert pairs == [actual[i]+actual[-1-i] for i in range(len(actual))]
        assert overflow == (number >= base**M)
        assert len(actual) == M+int(overflow)
        changes = [i for i, x in enumerate(p) if x != base-1]
        neutral += not changes
        if overflow:
            overflows += 1
            j = changes[0]
            assert witness == j and 1 <= j <= (M-1)//2
            assert p[j] >= base
            assert M-1-j < M-j < M
            assert p[M-j] == base-1
            assert actual[j] == p[j]-base and actual[M-j] == 0
            assert pairs[j] == p[j]-base <= base-2
        else:
            assert witness is None
    expected = 0
    for base in range(2, 11):
        for M in (1, 2, 3, 4, 5, 6, 8):
            free = 0 if M == 1 else (M//2-1)+(M % 2)
            amount = (2*base-1)**free
            assert counts[base, M] == amount
            expected += amount
    assert expected == len(seen) == declared["cases"] == 22773
    assert overflows == declared["overflow_cases"] == 11355
    assert neutral == 63 and 2*overflows+neutral == expected
    with tempfile.TemporaryDirectory(prefix="p196-neutral-exterior-review-") as temporary:
        replay = Path(temporary)
        shutil.copyfile(SOURCE/"check.py", replay/"check.py")
        result = subprocess.run([sys.executable, str(replay/"check.py")],
                                check=True, text=True, capture_output=True)
        (HERE/"temporary_replay.log").write_text(result.stdout+result.stderr)
        assert (replay/"controls.json.gz").read_bytes() == packed
        assert json.loads((replay/"verification.json").read_text()) == declared
    assert before == {name: digest((SOURCE/name).read_bytes()) for name in files}
    report = {
        "result": "PASS", "scope": "Independent mathematical/source review and finite integer-value audit; not a Lean theorem.",
        "cases": expected, "overflow_cases": overflows, "all_neutral_cases": neutral,
        "ordinary_integer_digit_extraction": True,
        "exact_catalog_counts_and_unique_inputs": True,
        "temporary_replay_matches_exact_archive_and_report": True,
        "producer_files_unchanged": True, "source_sha256": before,
        "review_checker_sha256": digest(Path(__file__).read_bytes()),
    }
    (HERE/"independent_audit.json").write_text(json.dumps(report, indent=2)+"\n")
    print(json.dumps({"result": "PASS", "cases": expected, "overflow_cases": overflows}))


if __name__ == "__main__":
    main()
