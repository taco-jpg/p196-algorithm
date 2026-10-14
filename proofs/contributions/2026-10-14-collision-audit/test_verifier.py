#!/usr/bin/env python3
"""Small positive/corruption fixtures; never copies the large search trace."""

import gzip
import hashlib
import json
from pathlib import Path
import struct
import tempfile

from verify_driver_trace import verify


def main():
    b0, h0 = bytes([1, 1]), bytes([1, 8, 14, 8, 1])
    b1, h1 = bytes([2, 2]), bytes([2, 17, 8, 17, 2])

    def record(t, loss, b, h):
        return struct.pack("<IIII", t, loss, len(b), len(h)) + b + h

    initial = record(0, 0, b0, h0)
    second = record(1, 0, b1, h1)
    baseline = b"P196DRV1" + initial + second
    cases = []
    with tempfile.TemporaryDirectory(prefix="p196-trace-audit-") as temporary:
        directory = Path(temporary)
        trace = directory / "fixture.bin.gz"
        summary = directory / "fixture.json"

        def run(name, data=baseline, mutation=None, expected="PASS"):
            compressed = gzip.compress(data, mtime=0)
            trace.write_bytes(compressed)
            document = dict(
                status="UNKNOWN beyond tested horizon", tested_states=2,
                tested_driver_times=[0, 1], first_hit=None,
                category_counts=dict(both_safe=0, exterior_only_bad=2,
                                     core_only_bad=0, both_bad_different_overflow=0,
                                     both_bad_same_overflow=0),
                checkpoints=[dict(t=t, spacer_loss=0, exterior_width=2,
                                  core_width=5, exterior_class=0, core_class=None)
                             for t in (0, 1)],
                final_tested_widths=dict(exterior=2, core=5),
                trace=dict(filename=trace.name, bytes=len(compressed),
                           sha256=hashlib.sha256(compressed).hexdigest(),
                           magic="P196DRV1",
                           format="little-endian uint32 t,loss,B_length,H_length, then raw coefficient bytes B,H"),
            )
            if mutation:
                mutation(document)
            summary.write_text(json.dumps(document), encoding="utf-8")
            try:
                actual = verify(trace, summary)["audit_status"]
            except (ValueError, EOFError, OSError):
                actual = "REJECTED"
            if actual != expected:
                raise AssertionError(f"{name}: expected {expected}, got {actual}")
            cases.append(dict(name=name, outcome=actual, passed=True))

        run("two hand-computed states")
        run("wrong initial state", b"P196DRV1"+record(0, 0, b1, h0)+second, expected="REJECTED")
        run("wrong transition but admissible state", b"P196DRV1"+initial+record(1, 0, b1, bytes([2, 17, 10, 17, 2])), expected="REJECTED")
        run("asymmetric state", b"P196DRV1"+initial+record(1, 0, b1, bytes([2, 16, 8, 17, 2])), expected="REJECTED")
        run("coefficient above 18", b"P196DRV1"+initial+record(1, 0, b1, bytes([2, 19, 8, 19, 2])), expected="REJECTED")
        run("odd central coefficient", b"P196DRV1"+initial+record(1, 0, b1, bytes([2, 17, 9, 17, 2])), expected="REJECTED")
        run("wrong cumulative spacer loss", b"P196DRV1"+initial+record(1, 1, b1, h1), expected="REJECTED")
        run("duplicate time", b"P196DRV1"+initial+record(0, 0, b1, h1), expected="REJECTED")
        run("truncated state", baseline[:-1], expected="REJECTED")
        run("trailing partial record", baseline+b"x", expected="REJECTED")
        run("wrong SHA256", mutation=lambda d: d["trace"].update(sha256="0"*64), expected="SUMMARY_MISMATCH")
        run("wrong final tested width", mutation=lambda d: d["final_tested_widths"].update(core=6), expected="SUMMARY_MISMATCH")
        run("wrong count", mutation=lambda d: d.update(tested_states=3), expected="SUMMARY_MISMATCH")
        run("wrong category count", mutation=lambda d: d["category_counts"].update(both_safe=2), expected="SUMMARY_MISMATCH")
        run("wrong checkpoint", mutation=lambda d: d["checkpoints"][1].update(spacer_loss=1), expected="SUMMARY_MISMATCH")
        run("wrong exceptional witness", mutation=lambda d: d.update(exceptional_states=[]), expected="SUMMARY_MISMATCH")

    result = dict(status="PASS", fixtures=len(cases), cases=cases,
                  scope="Hand-computed two-state fixtures and deliberate corruptions only; no longer search.")
    output = Path(__file__).resolve().parent / "verifier_tests.json"
    output.write_text(json.dumps(result, indent=2)+"\n", encoding="utf-8")
    print(json.dumps(dict(status="PASS", fixtures=len(cases))))


if __name__ == "__main__":
    main()
