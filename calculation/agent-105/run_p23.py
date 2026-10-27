#!/usr/bin/env python3
"""Reproduce Agent105's independent complete period-23 exterior audit.

Run: python3 run_p23.py
Requires Python3 and g++ (C++17).  Build products and the freshly generated
input manifest are placed beside this script.  Results remain on stdout;
no search logs or transcripts are written.  PASS means exactly all 1,502
head-admitted necklaces exhausted, with no accepting exterior boundary.
Limits, subprocess failures, malformed output, and missing words are UNDECIDED.
This is a COMPUTED exterior result, not a Lean certificate or an all-period
claim.  The solver enforces 4GiB address space; this driver enforces a total
solver wall limit of at most 1,200 seconds, independent of its per-word limit.
"""

import argparse
from collections import Counter, defaultdict
from hashlib import sha256
import json
from math import comb, isfinite
import os
from pathlib import Path
import selectors
import subprocess
import sys
import time


PERIOD = 23
EXPECTED_SURVIVORS = {6: 1, 7: 64, 8: 463, 9: 731, 10: 239, 11: 4}
HARD_WORD = "00001010101010100100111"
ROOT = Path(__file__).resolve().parent


def emit(value):
    print(json.dumps(value, sort_keys=True, separators=(",", ":")), flush=True)


def require(condition, message):
    if not condition:
        raise ValueError(message)


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def least_rotation(word):
    return min(word[k:] + word[:k] for k in range(len(word)))


def head_admitted(word):
    # Independent direct sets, not the generator's bitset relation.
    for initial in range(1, 19):
        possible = {initial}
        for bit in word:
            g = int(bit)
            possible = {
                2*x+c if g == 0 else x % 10+1
                for x in possible for c in (0, 1) if (x+c)//10 == g
            }
            if not possible:
                break
        if initial in possible:
            return True
    return False


def prepare(skip_build):
    if not skip_build:
        for stem in ("necklace_head", "exterior_tuple"):
            subprocess.run(
                ["g++", "-O3", "-std=c++17", "-Wall", "-Wextra", "-pedantic",
                 str(ROOT/(stem+".cpp")), "-o", str(ROOT/stem)],
                check=True, capture_output=True, text=True, timeout=60)
    manifest = ROOT/"p23-head-survivors.txt"
    generation = subprocess.run(
        [str(ROOT/"necklace_head"), str(PERIOD), str(manifest)],
        check=True, capture_output=True, text=True, timeout=60)
    census = json.loads(generation.stdout)
    require(not generation.stderr, "unexpected census stderr")
    require(census["status"] == "COMPLETE" and census["period"] == PERIOD,
            "incomplete or wrong-period census")
    # Since 23 is prime, nonconstant words have rotation orbit size 23.
    burnside = [1 if w in (0, PERIOD) else comb(PERIOD, w)//PERIOD
                for w in range(PERIOD+1)]
    require(census["necklaces_by_weight"] == burnside,
            "per-weight Burnside census mismatch")
    require(census["all_necklaces"] == sum(burnside) == 364724,
            "total necklace census mismatch")
    expected_weights = [EXPECTED_SURVIVORS.get(w, 0) for w in range(PERIOD+1)]
    require(census["survivors_by_weight"] == expected_weights,
            "head-survivor weight census mismatch")
    require(census["survivors"] == 1502, "head-survivor census total mismatch")
    raw = manifest.read_bytes()
    require(raw.endswith(b"\n"), "manifest missing final newline")
    words = raw.decode("ascii").splitlines()
    require(len(words) == len(set(words)) == 1502, "manifest size or uniqueness")
    require(all(len(w) == PERIOD and set(w) <= {"0", "1"} for w in words),
            "malformed manifest word")
    require(words == sorted(words, key=lambda w: (w.count("1"), w)),
            "manifest must be sorted by overflow weight and word")
    require(all(w == least_rotation(w) for w in words), "nonminimal rotation")
    require(dict(Counter(w.count("1") for w in words)) == EXPECTED_SURVIVORS,
            "manifest weight counts mismatch")
    require(all(head_admitted(w) for w in words), "manifest false head survivor")
    require(HARD_WORD in words, "known hard word missing")
    hashes = {name: digest(ROOT/name) for name in
              ("exterior_tuple.cpp", "necklace_head.cpp", "run_p23.py")}
    return manifest, words, census, hashes, sha256(raw).hexdigest()


def run_batch(args, manifest, words):
    command = [str(ROOT/"exterior_tuple"), "--batch", str(manifest),
               "--base", "10", "--cap", str(args.cap),
               "--seconds", str(args.seconds), "--all-accepts"]
    began = time.monotonic()
    process = subprocess.Popen(command, stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE, bufsize=0)
    selector = selectors.DefaultSelector()
    selector.register(process.stdout, selectors.EVENT_READ, "out")
    selector.register(process.stderr, selectors.EVENT_READ, "err")
    unfinished = b""
    stderr = bytearray()
    rows = {}
    errors = []
    expected = set(words)
    timed_out = False
    next_heartbeat = began+30

    def record(line):
        if not line:
            return
        try:
            row = json.loads(line)
            word = row["g"]
            require(word in expected and word not in rows, "unexpected or duplicate g")
            require(row["base"] == 10, "wrong solver base")
            require(row["status"] in {"EXHAUSTED", "ACCEPT", "CAPPED", "TIMEOUT"},
                    "unknown solver status")
            require(type(row["complete"]) is bool, "missing boolean completeness")
            require(isinstance(row["accepted"], list), "accepted must be a list")
            for key in ("states", "max_depth", "max_frontier", "generated_transitions",
                        "temporal_calls", "process_peak_rss_kb"):
                require(type(row[key]) is int and row[key] >= 0,
                        "invalid solver count "+key)
            require(row["states"] >= 1 and row["states"] <= args.cap,
                    "visited count outside total state cap")
            require(isfinite(row["seconds"]) and row["seconds"] >= 0,
                    "invalid elapsed time")
            if row["status"] == "EXHAUSTED":
                require(row["complete"] and not row["accepted"],
                        "EXHAUSTED requires complete graph and zero accepts")
            if row["status"] in {"CAPPED", "TIMEOUT"}:
                require(not row["complete"], "limited search cannot be complete")
            if row["status"] == "ACCEPT":
                require(bool(row["accepted"]), "ACCEPT requires a witness")
            rows[word] = row
            if len(rows) % 250 == 0 or word == HARD_WORD:
                progress = {"event": "PROGRESS", "processed": len(rows),
                            "total": len(words), "elapsed": round(time.monotonic()-began, 3),
                            "states": sum(r["states"] for r in rows.values()),
                            "peak_rss_kb": max(r["process_peak_rss_kb"] for r in rows.values())}
                if word == HARD_WORD:
                    progress["hard_case"] = row
                emit(progress)
        except (KeyError, TypeError, ValueError) as exc:
            errors.append(str(exc))

    def feed(chunk):
        nonlocal unfinished
        unfinished += chunk
        lines = unfinished.split(b"\n")
        unfinished = lines.pop()
        for line in lines:
            record(line)

    try:
        while selector.get_map():
            now = time.monotonic()
            if now-began >= args.timeout:
                timed_out = True
                process.kill()
                # Drain both pipes after kill; preserve every already completed row.
                remaining_out, remaining_err = process.communicate(timeout=10)
                feed(remaining_out)
                stderr.extend(remaining_err)
                break
            if now >= next_heartbeat:
                emit({"event": "HEARTBEAT", "processed": len(rows), "total": len(words),
                      "elapsed": round(now-began, 3),
                      "next_word": next((w for w in words if w not in rows), None)})
                next_heartbeat = now+30
            for key, _ in selector.select(min(1.0, args.timeout-(now-began))):
                chunk = os.read(key.fileobj.fileno(), 65536)
                if not chunk:
                    selector.unregister(key.fileobj)
                elif key.data == "out":
                    feed(chunk)
                else:
                    stderr.extend(chunk)
        if process.poll() is None:
            process.wait(timeout=max(0.01, args.timeout-(time.monotonic()-began)))
    except subprocess.TimeoutExpired:
        timed_out = True
        process.kill()
        remaining_out, remaining_err = process.communicate(timeout=10)
        feed(remaining_out)
        stderr.extend(remaining_err)
    finally:
        selector.close()
        if process.poll() is None:
            process.kill()
            process.communicate(timeout=10)
    if unfinished.strip():
        record(unfinished)
    if stderr:
        errors.append("solver stderr: "+stderr.decode("utf-8", errors="replace")[:2000])
    return rows, errors, timed_out, process.returncode, time.monotonic()-began, command


def summarize(rows, words):
    by_weight = defaultdict(lambda: {"words": 0, "states": 0, "max_states": 0,
                                     "max_depth": 0, "seconds": 0.0,
                                     "statuses": Counter(), "accepted_streams": 0})
    for word, row in rows.items():
        group = by_weight[word.count("1")]
        group["words"] += 1
        group["states"] += row["states"]
        group["max_states"] = max(group["max_states"], row["states"])
        group["max_depth"] = max(group["max_depth"], row["max_depth"])
        group["seconds"] += row["seconds"]
        group["statuses"][row["status"]] += 1
        group["accepted_streams"] += len(row["accepted"])
    for group in by_weight.values():
        group["seconds"] = round(group["seconds"], 6)
    return {
        "processed": len(rows), "expected": len(words),
        "unprocessed": len(set(words)-set(rows)),
        "statuses": dict(Counter(row["status"] for row in rows.values())),
        "accepted_streams": sum(len(row["accepted"]) for row in rows.values()),
        "complete_words": sum(row["complete"] for row in rows.values()),
        "total_states": sum(row["states"] for row in rows.values()),
        "max_states": max((row["states"] for row in rows.values()), default=0),
        "max_depth": max((row["max_depth"] for row in rows.values()), default=0),
        "max_frontier": max((row["max_frontier"] for row in rows.values()), default=0),
        "process_peak_rss_kb": max((row["process_peak_rss_kb"] for row in rows.values()), default=0),
        "per_weight": dict(by_weight), "hard_case": rows.get(HARD_WORD),
        "capped": sum(row["status"] == "CAPPED" for row in rows.values()),
        "word_timeouts": sum(row["status"] == "TIMEOUT" for row in rows.values())}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cap", type=int, default=12000000)
    parser.add_argument("--seconds", type=float, default=1100)
    parser.add_argument("--timeout", type=float, default=1200)
    parser.add_argument("--skip-build", action="store_true")
    args = parser.parse_args()
    started = time.monotonic()
    try:
        require(1 < args.cap <= 12000000, "cap must lie in 2..12000000")
        require(isfinite(args.timeout) and 0 < args.timeout <= 1200,
                "total subprocess timeout must lie in (0,1200]")
        require(isfinite(args.seconds) and 0 < args.seconds <= args.timeout,
                "per-word timeout must lie in (0,total timeout]")
        manifest, words, census, sources, manifest_hash = prepare(args.skip_build)
        emit({"event": "BEGIN", "base": 10, "period": PERIOD,
              "all_necklaces": census["all_necklaces"],
              "necklaces_by_weight": census["necklaces_by_weight"],
              "survivors": len(words), "survivors_by_weight": EXPECTED_SURVIVORS,
              "source_sha256": sources, "manifest_sha256": manifest_hash,
              "cap": args.cap, "word_seconds": args.seconds,
              "total_solver_timeout": args.timeout, "address_space_bytes": 4*1024**3})
        rows, errors, timed_out, returncode, elapsed, command = run_batch(args, manifest, words)
        result = summarize(rows, words)
        passed = (not errors and not timed_out and returncode == 0
                  and set(rows) == set(words)
                  and all(row["status"] == "EXHAUSTED" and row["complete"]
                          and not row["accepted"] for row in rows.values()))
        result.update({"event": "RESULT", "outcome": "PASS" if passed else "UNDECIDED",
                       "claim": "COMPUTED: no period-23 decimal B-cycle" if passed else None,
                       "source_sha256": sources, "manifest_sha256": manifest_hash,
                       "command": command, "process_returncode": returncode,
                       "external_timeout": timed_out, "errors": errors,
                       "solver_elapsed": round(elapsed, 6),
                       "total_elapsed": round(time.monotonic()-started, 6)})
        emit(result)
        return 0 if passed else 1
    except Exception as exc:
        emit({"event": "RESULT", "outcome": "UNDECIDED", "stage": "driver",
              "error": type(exc).__name__+": "+str(exc),
              "total_elapsed": round(time.monotonic()-started, 6)})
        return 2


if __name__ == "__main__":
    sys.exit(main())
