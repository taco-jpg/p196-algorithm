#!/usr/bin/env python3
"""Reproduce agent-15 F2 census using the repository's bauto5 and agent15_generate_f1.

Compile both C++ files to ./bauto5 and ./generate_f1, then run from an empty
working directory. The F1 root filter is necessary, never sufficient.
"""
from collections import Counter
from pathlib import Path
import re
import subprocess

BINARY = Path.cwd() / "bauto5"
GEN = Path.cwd() / "generate_f1"
CAP = 3000000
BASES = (7, 19, 22, 25)

def run(*args):
    return subprocess.run([str(a) for a in args], capture_output=True, text=True, check=True).stdout

def main():
    assert BINARY.exists() and GEN.exists(), "Build both C++ binaries in this directory"
    b9 = run(BINARY, 9, 10, 10, "-g", "1100011000", "-cap", CAP)
    b13 = run(BINARY, 13, 10, 10, "-g", "1010010000", "-cap", CAP)
    assert "minc=4" in b9 and "minc=1" in b13, "Mandatory positive controls failed"
    b7 = run(BINARY, 7, 24, 24, "-g", "10"*12, "-cap", CAP)
    assert "minc=6" in b7, "Repeated-stream positive control failed"
    print("CONTROLS PASS", flush=True)
    for base in BASES:
        subprocess.run([str(GEN), str(base), "17", "24"], check=True)
        for period in range(17, 25):
            words = Path(f"streams_b{base}_p{period}.txt").read_text().splitlines()
            counts = Counter()
            capped, candidates = [], []
            for i, word in enumerate(words, 1):
                assert len(word) == period
                output = run(BINARY, base, period, period, "-g", word, "-cap", CAP)
                assert re.search(r"SUMMARY b=%d p=%d streams=1 .*skipped=0" % (base, period), output), (base, period, word, output)
                if "CAPPED p=" in output:
                    counts["capped"] += 1
                    capped.append(word)
                else:
                    counts["decided"] += 1
                    if "CYC p=" in output:
                        counts["short_cycles"] += 1
                        candidates.append(word)
                if i % 50 == 0:
                    print("CHECKPOINT", base, period, i, "/", len(words), flush=True)
            print("RESULT", base, period, "primitive", len(words),
                  "decided", counts["decided"], "capped", counts["capped"],
                  "short_cycles", counts["short_cycles"], flush=True)
            for word in capped:
                print("CAPPED", base, period, word, flush=True)
            for word in candidates:
                print("CYCLE_CANDIDATE", base, period, word, flush=True)

if __name__ == "__main__":
    main()
