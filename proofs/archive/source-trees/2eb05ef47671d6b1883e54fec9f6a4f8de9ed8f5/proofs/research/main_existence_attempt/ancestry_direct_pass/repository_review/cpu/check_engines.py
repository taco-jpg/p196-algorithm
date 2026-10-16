"""Independent strict CLI checks; upstream files are read but never modified."""
from pathlib import Path
from collections import Counter
import hashlib
import json
import os
import random
import re
import subprocess
import sys
import tempfile
import time

sys.set_int_max_str_digits(0)
HERE = Path(__file__).resolve().parent
WORK_ROOT = HERE / "work" / "strict"
WORK_ROOT.mkdir(parents=True, exist_ok=True)
WORK = Path(tempfile.mkdtemp(prefix="run-", dir=WORK_ROOT))
ENV = dict(os.environ, OMP_NUM_THREADS="2", EMU_CERTCHECK="1")
RNG = random.Random(19620261014)
records = []
totals = Counter()


def reference(s, horizon):
    value = int(s)
    for k in range(1, horizon + 1):
        value += int(str(value)[::-1])
        s = str(value)
        if s == s[::-1]:
            return k, s
    return None, str(value)


def run_case(label, s, horizon, config, start=0, save=0):
    first, expected = reference(s, horizon)
    case = WORK / f"case_{len(records):04d}"
    case.mkdir(exist_ok=False)
    inp, out = case / "input.txt", case / "output.txt"
    inp.write_text(s + "\n")
    binary, flags = config
    # Bench positional K has precedence over --K; align both intentionally.
    configured_k = next((f.split("=", 1)[1] for f in flags if f.startswith("--K=")), "33")
    if "--mode=step" in flags:
        configured_k = next((f.split("=", 1)[1] for f in flags if f.startswith("--batch=")), configured_k)
    command = [str(HERE / "bin" / binary), str(inp), str(horizon), str(out),
               str(start), configured_k, str(save)] + flags
    before = time.monotonic()
    result = subprocess.run(command, env=ENV, text=True, capture_output=True, timeout=45)
    log = result.stderr
    assert f" K={configured_k} " in log, (label, "CLI K precedence")
    (case / "stderr.txt").write_text(log)
    hit = re.search(r"PALINDROME at iteration (\d+)", log)
    if first is None:
        assert result.returncode == 0, (label, result.returncode, log[-1000:])
        assert hit is None, (label, "unexpected palindrome report")
        assert out.read_text().strip() == expected, (label, "final value")
    else:
        assert result.returncode == 3, (label, result.returncode, log[-1000:])
        assert hit and int(hit.group(1)) == start + first, (label, "first-hit iteration")
        palfile = Path(str(out) + f".palindrome_{start+first}.txt")
        assert palfile.read_text().strip() == expected, (label, "palindrome value")
        assert "cpu_check=PASS" in log, (label, "missing materialized palindrome check")
    if save and first is None:
        v = int(s)
        for k in range(1, horizon+1):
            v += int(str(v)[::-1])
            if k % save == 0 and k < horizon:
                checkpoint = Path(str(out) + f".next_{start+k}.txt")
                assert checkpoint.read_text().strip() == str(v), (label, "checkpoint value/label")
    cert = re.search(r"blocks certified=(\d+) failed=(\d+) violations=(\d+) SOUND", log)
    assert cert and int(cert.group(3)) == 0, (label, "certification soundness record")
    hy = re.search(r"hybrid blocks=(\d+) \(failed (\d+)\)", log)
    cross = re.search(r"blocks cross-checked against the v6r3 path=(\d+) \(block-steps with no mismatch: (\d+)\)", log)
    entry = {"label": label, "input_digits": len(s), "requested_steps": horizon,
             "binary": binary, "flags": flags, "actual_K": int(configured_k),
             "first_palindrome_step": first,
             "exit_code": result.returncode, "seconds": time.monotonic()-before,
             "input_sha256": hashlib.sha256(s.encode()).hexdigest(),
             "expected_output_sha256": hashlib.sha256(expected.encode()).hexdigest(),
             "certified_blocks": int(cert.group(1)), "failed_certification_blocks": int(cert.group(2)),
             "hybrid_blocks": int(hy.group(1)) if hy else 0,
             "failed_hybrid_blocks": int(hy.group(2)) if hy else 0,
             "cross_checked_hybrid_blocks": int(cross.group(1)) if cross else 0,
             "quiet_block_steps": int(cross.group(2)) if cross else 0,
             "replay_messages": log.count("exact replay with per-step kernel"),
             "log": str(case / "stderr.txt")}
    records.append(entry)
    for key in ("certified_blocks", "failed_certification_blocks", "hybrid_blocks",
                "failed_hybrid_blocks", "cross_checked_hybrid_blocks", "quiet_block_steps",
                "replay_messages"):
        totals[key] += entry[key]
    print(json.dumps({"case": len(records), "label": label, "first_hit": first,
                      "hybrid": entry["hybrid_blocks"], "replays": entry["replay_messages"]}), flush=True)


def realize_pairs(q, odd=False):
    n = 2*len(q) - int(odd)
    digits = [0]*n
    for j, v in enumerate(q):
        lo, hi = max(0, v-9), min(9, v)
        a = RNG.randint(lo, hi)
        if j == 0:
            a = max(1, a)
        if j == n-1-j:
            a = v//2
        assert 0 <= v-a <= 9
        digits[j], digits[n-1-j] = a, v-a
    return "".join(map(str, digits))


CONFIGS = [
    ("emu_v8_j8", ["--mode=step", "--batch=7"]),
    ("emu_v8_j8", ["--K=7", "--tile=4", "--window=29", "--hybrid=0"]),
    ("emu_v8_j8", ["--K=64", "--tile=8", "--window=137"]),
    ("emu_v8_j16", ["--K=33", "--tile=32", "--window=101"]),
]
for s, horizon in [("196", 500), ("89", 40), ("10911", 70),
                   ("1186060307891929990", 300), ("1", 3), ("10", 10), ("1200", 30)]:
    for config in CONFIGS:
        run_case("known_"+s, s, horizon, config, start=1000)
for config in CONFIGS:
    run_case("checkpoint_labels", "196", 150, config, start=5000, save=17)

# Large inputs activate the hybrid path and exercise word/center boundaries.
for index in range(12):
    n = RNG.choice([6001, 12000, 16001])
    digits = [RNG.randrange(10) for _ in range(n)]
    for _ in range(25):
        a = RNG.randrange(n//2)
        for j in range(a, min(n//2, a+RNG.choice([31,33,64,120,180]))):
            digits[n-1-j] = 9-digits[j]
    digits[0] = max(1, digits[0])
    s = "".join(map(str, digits))
    for config in CONFIGS[1:]:
        run_case(f"carry_runs_{index}", s, RNG.choice([41,65,99]), config)

# Force the prefix growth detector to encounter more than 128 propagating pairs.
for index in range(4):
    q = [4,14,14,4]*40 + [RNG.randrange(19) for _ in range(1840)]
    s = realize_pairs(q)
    for config in CONFIGS[1:]:
        run_case(f"prefix_growth_{index}", s, 35, config)

# Search independent sparse disturbances for first hits inside hybrid windows.
found = 0
for attempt in range(5000):
    q = [RNG.randrange(2) for _ in range(4000)]
    q[0] = 1
    for _ in range(RNG.randrange(1,4)):
        q[RNG.randrange(1,3999)] = RNG.choice([5,6,10,11,12])
    s = realize_pairs(q)
    first, _ = reference(s, 10)
    if first is not None and first >= 3:
        for config in CONFIGS[2:]:
            run_case(f"hybrid_late_palindrome_{found}", s, 70, config, start=2000)
        found += 1
        if found == 4:
            break
assert found == 4, "late-palindrome generator coverage incomplete"
assert totals["failed_certification_blocks"] > 0
assert totals["failed_hybrid_blocks"] > 0
assert totals["cross_checked_hybrid_blocks"] > 0
assert totals["quiet_block_steps"] > 0
summary = {"status": "PASS", "cases": len(records), "totals": dict(totals),
           "records": records, "v9_tested": False, "cuda_hardware_tested": False,
           "scope": "Finite CPU tests; independent arithmetic oracle and strict first-hit checks."}
(HERE / "engine_results.json").write_text(json.dumps(summary, indent=2)+"\n")
(WORK / "results.json").write_text(json.dumps(summary, indent=2)+"\n")
print(json.dumps({"status": "PASS", "cases": len(records), "totals": dict(totals)}), flush=True)
