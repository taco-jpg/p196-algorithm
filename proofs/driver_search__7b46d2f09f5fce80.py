#!/usr/bin/env python3
"""Search one universal separated driver, preserving every tested state.

The parameter r does not occur in the driver.  At a state of cumulative
spacer loss S, its palindrome event applies to every r >= S+2.
Absent such an event this program makes no all-time assertion.
"""

import argparse
import gzip
import hashlib
import json
from pathlib import Path
import struct
import time


def normalize(word):
    carry = 0
    out = bytearray()
    for coefficient in word:
        carry, digit = divmod(coefficient + carry, 10)
        out.append(digit)
    assert carry in (0, 1)
    if carry:
        out.append(carry)
    return out, carry


def pair(digits):
    return bytearray(a + b for a, b in zip(digits, reversed(digits)))


def bad_class(word):
    if max(word) <= 9:
        return 0
    if word[0] == 11 and all(x in (0, 11) for x in word):
        return 1
    return None


def driver_step(b, h):
    bd, e = normalize(b)
    hd, f = normalize(h)
    delta = max(e, f)
    hn = bytearray(len(h) + 2 * delta - e)
    for i, x in enumerate(hd):
        hn[delta - e + i] += x
        hn[len(h) + delta - 1 - i] += x
    return pair(bd), hn, delta, e, f


def admissible(word):
    return (bool(word) and word[0] > 0 and max(word) <= 18
            and word == word[::-1]
            and (len(word) % 2 == 0 or word[len(word) // 2] % 2 == 0))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--steps", type=int, default=10000)
    args = parser.parse_args()
    assert args.steps > 0
    directory = Path(__file__).resolve().parent
    trace_path = directory / "driver_trace.bin.gz"
    summary_path = directory / "driver_summary.json"
    b, h = bytearray((1, 1)), bytearray((1, 8, 14, 8, 1))
    loss = 0
    hit = None
    cases = {"both_safe": 0, "exterior_only_bad": 0,
             "core_only_bad": 0, "both_bad_different_overflow": 0,
             "both_bad_same_overflow": 0}
    checkpoints = []
    exceptional_states = []
    started = time.monotonic()
    # Reproducible gzip header; uncompressed format: eight-byte magic,
    # then repeated <t:uint32, loss:uint32, |B|:uint32, |H|:uint32>, B, H.
    with trace_path.open("wb") as raw:
        with gzip.GzipFile(fileobj=raw, mode="wb", mtime=0, filename="") as trace:
            trace.write(b"P196DRV1")
            for t in range(args.steps):
                assert admissible(b) and admissible(h)
                last_tested_widths = dict(exterior=len(b), core=len(h))
                trace.write(struct.pack("<IIII", t, loss, len(b), len(h)))
                trace.write(b)
                trace.write(h)
                bc, hc = bad_class(b), bad_class(h)
                if bc is None and hc is None:
                    category = "both_safe"
                elif bc is not None and hc is None:
                    category = "exterior_only_bad"
                elif bc is None and hc is not None:
                    category = "core_only_bad"
                elif bc != hc:
                    category = "both_bad_different_overflow"
                else:
                    category = "both_bad_same_overflow"
                cases[category] += 1
                if bc is not None or hc is not None:
                    exceptional_states.append(dict(t=t, spacer_loss=loss,
                                                    exterior=list(b), core=list(h),
                                                    exterior_class=bc, core_class=hc))
                if t < 20 or t % 1000 == 0:
                    checkpoints.append(dict(t=t, spacer_loss=loss,
                                            exterior_width=len(b), core_width=len(h),
                                            exterior_class=bc, core_class=hc))
                if category == "both_bad_same_overflow":
                    hit = dict(driver_time=t, ordinary_first_hit=t + 1,
                               spacer_loss=loss, all_parameter_threshold=loss + 2,
                               shared_predecessor_class=bc)
                    break
                b, h, delta, _, _ = driver_step(b, h)
                loss += delta
    digest = hashlib.sha256(trace_path.read_bytes()).hexdigest()
    result = dict(
        status="universal driver hit found" if hit else "UNKNOWN beyond tested horizon",
        tested_states=t + 1, tested_driver_times=[0, t], first_hit=hit,
        category_counts=cases, checkpoints=checkpoints,
        exceptional_states=exceptional_states,
        final_tested_widths=last_tested_widths,
        trace=dict(filename=trace_path.name, bytes=trace_path.stat().st_size,
                   sha256=digest, magic="P196DRV1",
                   format="little-endian uint32 t,loss,B_length,H_length, then raw coefficient bytes B,H"),
        scope="One parameter-independent driver only; no inference of infinite safety from absent hits.",
    )
    summary_path.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(dict(status=result["status"], tested_states=t + 1,
                          first_hit=hit, categories=cases,
                          trace_bytes=trace_path.stat().st_size,
                          elapsed_seconds=round(time.monotonic() - started, 3))))


if __name__ == "__main__":
    main()
