#!/usr/bin/env python3
"""Complete seven-input classification for the broader outside pair (4,4).

All freely specified control words are retained. An abstract return does
not assert a consistent whole-integer carry history or palindrome safety.
"""

from itertools import product
import json
from pathlib import Path


def step(prefix, control):
    low = []
    carry = 0
    for coefficient in prefix:
        carry, digit = divmod(coefficient + carry, 10)
        low.append(digit)
    high = [0] * len(prefix)
    carry = control
    for i in range(len(prefix)-1, -1, -1):
        carry, high[i] = divmod(prefix[i] + carry, 10)
    aligned = [1] + high[:-1] if carry else high
    return tuple(a+b for a, b in zip(low, aligned)), carry


def main():
    records = []
    distinct = {}
    for controls in product((0, 1), repeat=7):
        prefix = (4, 4)
        trace, overflows = [prefix], []
        for control in controls:
            prefix, overflow = step(prefix, control)
            trace.append(prefix)
            overflows.append(overflow)
        returned = prefix == (4, 4)
        record = dict(controls=controls, prefixes=trace,
                      overflows=overflows, returned=returned)
        records.append(record)
        if returned:
            key = tuple(trace)
            distinct.setdefault(key, []).append(controls)
    assert len(records) == 128
    assert sum(r['returned'] for r in records) == 16
    assert len(distinct) == 3
    assert all(r['overflows'] == [0, 0, 1, 0, 1, 0, 1]
               for r in records if r['returned'])
    report = dict(
        status="complete finite control classification",
        all_control_words=len(records), returning_words=16,
        distinct_return_traces=3,
        branches=[dict(prefixes=trace, controls=controls)
                  for trace, controls in distinct.items()],
        records=records,
        corrected_hypothesis="00*0*11 describes only one branch; the broader44 return has three branches and sixteen control words.",
        scope="Abstract finite inputs; no infinite recurrence or safe whole-word realization is asserted. A future lift must preserve all three branches and allow branch switching at return times.")
    Path(__file__).with_name("two_column_controls.json").write_text(
        json.dumps(report, indent=2) + "\n")
    print(json.dumps({k: report[k] for k in (
        "status", "all_control_words", "returning_words", "distinct_return_traces")}))


if __name__ == "__main__":
    main()
