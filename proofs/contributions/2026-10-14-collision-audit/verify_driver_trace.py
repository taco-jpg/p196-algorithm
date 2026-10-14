#!/usr/bin/env python3
"""Independently stream-check the finite separated-driver certificate.

This program does not import the search program and retains only adjacent
states. Its central-block recurrence is implemented by padding a normalized
digit word and adding its reversal, rather than the searcher's index updates.
The trace proves only the explicitly saved finite horizon.
"""

import argparse
from collections import Counter
import gzip
import hashlib
import json
from pathlib import Path
import struct
import sys


MAGIC = b"P196DRV1"
CATEGORIES = (
    "both_safe", "exterior_only_bad", "core_only_bad",
    "both_bad_different_overflow", "both_bad_same_overflow",
)


def file_hash(path):
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def require(condition, message):
    if not condition:
        raise ValueError(message)


def normalize_independent(word):
    # Replace coefficients by decimal digits, transferring tens rightwards.
    work = list(word) + [0]
    for index in range(len(word)):
        quotient = work[index] // 10
        work[index] -= 10 * quotient
        work[index + 1] += quotient
    overflow = work[-1]
    require(overflow in (0, 1), "normalization overflow is not a bit")
    if not overflow:
        work.pop()
    require(all(0 <= digit < 10 for digit in work), "invalid decimal digit")
    return work, overflow


def next_state(exterior, core):
    bd, e = normalize_independent(exterior)
    hd, f = normalize_independent(core)
    delta = int(bool(e or f))
    bp = bytes(bd[index] + bd[-1-index] for index in range(len(bd)))
    half = [0] * (delta - e) + hd + [0] * (delta - f)
    hp = bytes(half[index] + half[-1-index] for index in range(len(half)))
    return bp, hp, delta


def validate_word(word, label, time):
    require(len(word) > 0, f"t={time}: empty {label}")
    require(word[0] != 0, f"t={time}: zero {label} endpoint")
    require(all(x <= 18 for x in word), f"t={time}: oversized {label} coefficient")
    require(word == word[::-1], f"t={time}: asymmetric {label}")
    require(len(word) % 2 == 0 or word[len(word)//2] % 2 == 0,
            f"t={time}: odd central {label} coefficient")


def predecessor_class(word):
    # These are exact coefficient patterns, not floating-point statistics.
    if all(coefficient < 10 for coefficient in word):
        return 0
    if word[0] == 11 and set(word).issubset({0, 11}):
        return 1
    return None


def category_of(bc, hc):
    if bc is None:
        return "both_safe" if hc is None else "core_only_bad"
    if hc is None:
        return "exterior_only_bad"
    return "both_bad_same_overflow" if bc == hc else "both_bad_different_overflow"


def verify(trace_path, summary_path):
    summary_bytes = summary_path.read_bytes()
    summary = json.loads(summary_bytes)
    counts = Counter({key: 0 for key in CATEGORIES})
    checkpoints = []
    exceptional = {key: [] for key in CATEGORIES if key != "both_safe"}
    exceptional_states = []
    component_bad_times = {"exterior": [], "core": []}
    raw_digest = hashlib.sha256()
    uncompressed_bytes = 0
    count = 0
    first_hit = None
    expected = (bytes([1, 1]), bytes([1, 8, 14, 8, 1]), 0)
    final = None
    terminal_successor = None
    max_widths = {"exterior": 0, "core": 0}

    with gzip.open(trace_path, "rb") as handle:
        def read_exact(size):
            nonlocal uncompressed_bytes
            data = handle.read(size)
            require(len(data) == size, f"truncated record at t={count}")
            raw_digest.update(data)
            uncompressed_bytes += len(data)
            return data

        require(read_exact(8) == MAGIC, "incorrect trace magic")
        while True:
            header = handle.read(16)
            if not header:
                break
            require(len(header) == 16, "truncated record header")
            raw_digest.update(header)
            uncompressed_bytes += 16
            t, loss, nb, nh = struct.unpack("<IIII", header)
            require(t == count, f"expected t={count}, got t={t}")
            require(first_hit is None, "trace continues after its first hit")
            require(nb == len(expected[0]) and nh == len(expected[1]),
                    f"t={t}: incorrect state widths")
            b, h = read_exact(nb), read_exact(nh)
            validate_word(b, "exterior", t)
            validate_word(h, "core", t)
            require((b, h, loss) == expected, f"t={t}: state or cumulative spacer loss mismatch")
            bc, hc = predecessor_class(b), predecessor_class(h)
            category = category_of(bc, hc)
            counts[category] += 1
            if category != "both_safe":
                exceptional[category].append(t)
                exceptional_states.append(dict(t=t, spacer_loss=loss,
                                               exterior=list(b), core=list(h),
                                               exterior_class=bc, core_class=hc))
            if bc is not None:
                component_bad_times["exterior"].append(t)
            if hc is not None:
                component_bad_times["core"].append(t)
            if t < 20 or t % 1000 == 0:
                checkpoints.append(dict(t=t, spacer_loss=loss,
                                        exterior_width=nb, core_width=nh,
                                        exterior_class=bc, core_class=hc))
            if category == "both_bad_same_overflow":
                first_hit = dict(driver_time=t, ordinary_first_hit=t+1,
                                 spacer_loss=loss, all_parameter_threshold=loss+2,
                                 shared_predecessor_class=bc)
            final = dict(t=t, spacer_loss=loss, exterior_width=nb, core_width=nh)
            max_widths["exterior"] = max(max_widths["exterior"], nb)
            max_widths["core"] = max(max_widths["core"], nh)
            # This successor is needed to verify the next saved transition.
            # For the last record it is diagnostic only, not a tested state.
            bp, hp, delta = next_state(b, h)
            expected = (bp, hp, loss + delta)
            terminal_successor = dict(exterior=len(bp), core=len(hp), spacer_loss=loss+delta)
            count += 1

    require(count > 0, "trace has no saved states")
    compressed_hash = file_hash(trace_path)
    checks = {
        "status": "universal driver hit found" if first_hit else "UNKNOWN beyond tested horizon",
        "tested_states": count,
        "tested_driver_times": [0, count-1],
        "first_hit": first_hit,
        "category_counts": dict(counts),
        "checkpoints": checkpoints,
        "final_tested_widths": {"exterior": final["exterior_width"], "core": final["core_width"]},
    }
    discrepancies = []
    for key, actual in checks.items():
        if summary.get(key) != actual:
            discrepancies.append(dict(field=key, reported=summary.get(key), verified=actual))
    expected_trace = dict(filename=trace_path.name, bytes=trace_path.stat().st_size,
                          sha256=compressed_hash, magic=MAGIC.decode(),
                          format="little-endian uint32 t,loss,B_length,H_length, then raw coefficient bytes B,H")
    for key, actual in expected_trace.items():
        reported = summary.get("trace", {}).get(key)
        if reported != actual:
            discrepancies.append(dict(field="trace."+key, reported=reported, verified=actual))
    # Accept optional extra evidence without trusting it for verification.
    if "exceptional_state_times" in summary:
        reported = summary["exceptional_state_times"]
        if reported != exceptional:
            discrepancies.append(dict(field="exceptional_state_times", reported=reported, verified=exceptional))
    if "exceptional_states" in summary:
        reported = summary["exceptional_states"]
        if reported != exceptional_states:
            discrepancies.append(dict(field="exceptional_states", reported=reported, verified=exceptional_states))

    return dict(
        audit_status="PASS" if not discrepancies else "SUMMARY_MISMATCH",
        mathematical_status=checks["status"],
        checked_records=count, checked_saved_transitions=count-1,
        checked_initial_state=True, every_saved_state_admissible=True,
        every_saved_transition_exact=True, every_cumulative_spacer_loss_exact=True,
        tested_driver_times=[0, count-1], first_hit=first_hit,
        category_counts=dict(counts), exceptional_state_times=exceptional,
        component_bad_times=component_bad_times, final_tested_state=final,
        maximum_saved_widths=max_widths,
        untested_successor_diagnostic=terminal_successor,
        trace=dict(filename=trace_path.name, compressed_bytes=trace_path.stat().st_size,
                   compressed_sha256=compressed_hash, uncompressed_bytes=uncompressed_bytes,
                   uncompressed_sha256=raw_digest.hexdigest()),
        summary_sha256=hashlib.sha256(summary_bytes).hexdigest(), discrepancies=discrepancies,
        scope="Finite trace audit only. No conclusion about later driver times, post-collision evolution, or P196.",
        memory="Adjacent states plus small counters/checkpoints; compressed trace is neither copied nor modified.",
    )


def main():
    directory = Path(__file__).resolve().parent
    original = directory.parent / "2026-10-14-collision-review"
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--trace", type=Path, default=original / "driver_trace.bin.gz")
    parser.add_argument("--summary", type=Path, default=original / "driver_summary.json")
    parser.add_argument("--output", type=Path, default=directory / "verification.json")
    args = parser.parse_args()
    result = verify(args.trace, args.summary)
    result["verifier_sha256"] = file_hash(Path(__file__).resolve())
    args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({key: result[key] for key in
                      ("audit_status", "checked_records", "checked_saved_transitions",
                       "final_tested_state", "discrepancies")}, indent=2))
    return 0 if result["audit_status"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
