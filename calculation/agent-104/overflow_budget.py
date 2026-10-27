#!/usr/bin/env python3
"""Exact base-10 exterior census for a prescribed total overflow budget.

The default G=2,4 run covers every possible period P<=4G.  The first-head
graph is only a necessary filter.  Surviving words are decided by the existing
unrestricted-width B position automaton, with all accepting e streams retained.
Only an empty final BFS frontier certifies exhaustive completion.  The source
is compiled through stdin with one diagnostics-only insertion; no shared source
is edited and no automaton implementation is copied into this directory.
"""

import argparse
from collections import Counter
import hashlib
import importlib.util
from itertools import combinations, product
import json
from math import comb, gcd, isfinite
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "calculation/neutral_band/structure/bauto.cpp"
BSYS = ROOT / "calculation/neutral_band/structure/bsys.py"
BASE = 10


def require(condition, detail):
    """Keep proof and coverage guards active even under python -O."""
    if not condition:
        raise RuntimeError(detail)


def head_edges(x):
    """Possible (overflow, next effective first coefficient); empty B has x=9."""
    for carry in (0, 1):
        if x + carry < BASE:
            yield 0, 2 * x + carry
        else:
            yield 1, x % BASE + 1


HEAD = {
    bit: tuple(sum(1 << (y - 1) for g, y in set(head_edges(x)) if g == bit)
               for x in range(1, 19))
    for bit in (0, 1)
}


def head_possible(word):
    for start in range(18):
        reach = 1 << start
        for ch in word:
            nxt = 0
            while reach:
                low = reach & -reach
                nxt |= HEAD[int(ch)][low.bit_length() - 1]
                reach -= low
            reach = nxt
            if not reach:
                break
        if reach & (1 << start):
            return True
    return False


def phi(n):
    return sum(gcd(k, n) == 1 for k in range(1, n + 1))


def necklaces(period, weight):
    """All fixed-weight rotation classes, including words of smaller period."""
    words = []
    for locations in combinations(range(period), weight):
        chars = ["0"] * period
        for t in locations:
            chars[t] = "1"
        word = "".join(chars)
        if all(word <= word[t:] + word[:t] for t in range(1, period)):
            words.append(word)
    count = sum(phi(d) * comb(period // d, weight // d)
                for d in range(1, gcd(period, weight) + 1)
                if period % d == 0 and weight % d == 0) // period
    require(len(words) == count,
            f"necklace count mismatch: P={period} G={weight} got={len(words)} expected={count}")
    return sorted(words)


def load_bstep():
    spec = importlib.util.spec_from_file_location("a104_existing_bsys", BSYS)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.bstep


def selftest(bstep):
    # Check every legal B of width <=3, including the exceptional empty word.
    checked = 0
    for width in range(4):
        for digits in product(range(19), repeat=width):
            if digits and not digits[0]:
                continue
            nxt, _, _, gamma = bstep(BASE, list(digits))
            x, y = (digits[0] if digits else 9), (nxt[0] if nxt else 9)
            require((gamma, y) in set(head_edges(x)),
                    f"head projection mismatch: B={digits} nextB={nxt} gamma={gamma}")
            checked += 1
    require(bstep(BASE, []) == ([10], 0, 0, 1), "empty-B transition mismatch")
    require(checked == 19 ** 3, f"head projection coverage mismatch: {checked}")

    # Enumerate every segment starting just after an overflow and ending at the
    # next overflow.  Non-overflow steps strictly increase x, so this terminates.
    segments = set()
    for initial in range(1, 11):
        todo = [(initial, 0)]
        while todo:
            x, length = todo.pop()
            for gamma, y in head_edges(x):
                if gamma:
                    segment = (initial, y, length + 1)
                    segments.add(segment)
                    require(length + 1 <= 4 + (initial == 1) - (y == 1),
                            f"overflow-segment bound fails: {segment}")
                else:
                    require(y > x, f"non-overflow head is not increasing: {x}->{y}")
                    todo.append((y, length + 1))
    tight = {(x, y) for x, y, length in segments
             if length == 4 + (x == 1) - (y == 1)}
    recurrent = []
    for initial in range(1, 11):
        seen, todo = set(), [y for x, y in tight if x == initial]
        while todo:
            x = todo.pop()
            if x in seen:
                continue
            seen.add(x)
            todo.extend(y for a, y in tight if a == x)
        if initial in seen:
            recurrent.append(initial)
    require(recurrent == [1], f"tight recurrent head set mismatch: {recurrent}")
    require((1, 1, 4) in segments, "missing tight length-four segment at head 1")
    require(not head_possible("0"), "unexpected zero-overflow head cycle")
    return {"head_projection_checks": checked, "empty_B_checked": True,
            "segment_triples": len(segments), "bound": "P<=4G",
            "tight_recurrent_states": recurrent}


def compile_automaton(binary, compiler):
    source = SOURCE.read_text()
    marker = "      if(!accE.empty()){"
    if source.count(marker) != 1:
        raise RuntimeError("bauto.cpp changed: diagnostic insertion is ambiguous")
    diagnostic = (
        '      fprintf(stderr,"A104_COMPLETE b=%d p=%d g=%s exhausted=%d '
        'depth=%d states=%zu accepts=%zu\\n",b,p,gs.c_str(),'
        'fr.empty()?1:0,depth,seen.size(),accE.size());\n'
    )
    instrumented = source.replace(marker, diagnostic + marker)
    subprocess.run([compiler, "-O2", "-std=c++17", "-x", "c++", "-", "-o",
                    str(binary)], input=instrumented, text=True, check=True,
                   timeout=60)
    return hashlib.sha256(source.encode()).hexdigest()


COMPLETE = re.compile(
    r"A104_COMPLETE b=(\d+) p=(\d+) g=([01]+) exhausted=([01]) "
    r"depth=(\d+) states=(\d+) accepts=(\d+)")
ACCEPT = re.compile(
    r"ACCEPT b=(\d+) p=(\d+) g=([01]+) e=([01]+) depth=(\d+) "
    r"states=(\d+) B_t=(.*)")


def decide(word, binary, cap, seconds, bstep):
    period = len(word)
    # Existing source uses a 128-bit key, a uint64 phase mask and arrays of 64.
    if period >= 63 or 2 * period + 4 * word.count("1") > 127:
        raise ValueError("word exceeds existing bauto representation limits")
    command = [str(binary), "10", str(period), str(period), "-g", word,
               "-v", "-w", "-cap", str(cap)]
    try:
        run = subprocess.run(command, text=True, capture_output=True, timeout=seconds)
    except subprocess.TimeoutExpired:
        return {"g": word, "status": "UNDECIDED", "reason": "timeout",
                "seconds": seconds, "command": command, "accepts": []}
    if run.returncode:
        raise RuntimeError(f"bauto failed ({run.returncode}): {run.stderr}")
    terminals = COMPLETE.findall(run.stderr)
    if len(terminals) != 1:
        raise RuntimeError(f"missing unique completion diagnostic: {run.stderr}")
    b, p, g, exhausted, depth, states, naccepts = terminals[0]
    require((int(b), int(p), g) == (10, period, word),
            f"completion diagnostic identifies the wrong run: {terminals[0]}")
    accepted = []
    for line in run.stdout.splitlines():
        match = ACCEPT.fullmatch(line)
        if not match:
            raise RuntimeError(f"unrecognized bauto output: {line}")
        b1, p1, g1, e, width, total, blocks = match.groups()
        require((b1, p1, g1, total) == (b, p, g, states),
                f"acceptance diagnostic identifies the wrong run: {line}")
        require(len(e) == period, f"accepted carry-stream length mismatch: {e}")
        pieces = re.findall(r"\[([0-9,]*)\]", blocks)
        require("".join("[" + item + "]" for item in pieces) == blocks,
                f"unparsed B witness text: {blocks}")
        witnesses = [[int(x) for x in item.split(",") if x] for item in pieces]
        require(len(witnesses) == period,
                f"B witness phase count mismatch: got={len(witnesses)} expected={period}")
        trims = []
        for t, exterior in enumerate(witnesses):
            nxt, trim, carry, gamma = bstep(BASE, exterior)
            require(nxt == witnesses[(t + 1) % period],
                    f"B witness does not return at phase {t}: g={word} e={e}")
            require((carry, gamma) == (int(e[t]), int(word[t])),
                    f"B witness carry/overflow mismatch at phase {t}: g={word} e={e}")
            trims.append(trim)
        require(sum(trims) == word.count("1"),
                f"B witness trim total mismatch: g={word} trims={trims}")
        accepted.append({"e": e, "first_accept_depth": int(width),
                         "B_lengths": [len(x) for x in witnesses],
                         "u": trims})
    require(len(accepted) == int(naccepts),
            f"accepted-stream count mismatch: got={len(accepted)} expected={naccepts}")
    require(len({item["e"] for item in accepted}) == len(accepted),
            f"duplicate accepted carry stream: g={word}")
    complete = exhausted == "1" and "state cap reached" not in run.stderr
    result = {"g": word, "status": "EXHAUSTED" if complete else "UNDECIDED",
              "depth": int(depth), "states": int(states),
              "accepts": sorted(accepted, key=lambda item: item["e"])}
    if not complete:
        result["reason"] = "state cap" if "state cap reached" in run.stderr else "depth cap"
        result["command"] = command
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--weights", type=int, nargs="+", default=[2, 4])
    parser.add_argument("--state-cap", type=int, default=2_000_000)
    parser.add_argument("--seconds", type=float, default=90)
    parser.add_argument("--binary", type=Path, default=Path("/tmp/agent104-bauto"))
    parser.add_argument("--compiler", default="c++")
    parser.add_argument("--selftest-only", action="store_true")
    args = parser.parse_args()
    if any(weight <= 0 or weight % 2 for weight in args.weights):
        parser.error("joint certificate overflow weights must be positive and even")
    if args.state_cap <= 0:
        parser.error("--state-cap must be positive")
    if not isfinite(args.seconds) or args.seconds <= 0:
        parser.error("--seconds must be finite and positive")
    bstep = load_bstep()
    checks = selftest(bstep)
    print("SELFTEST " + json.dumps(checks, sort_keys=True), flush=True)
    if args.selftest_only:
        return 0
    digest = compile_automaton(args.binary, args.compiler)
    print("SOURCE " + json.dumps({"path": str(SOURCE.relative_to(ROOT)),
                                  "sha256": digest}, sort_keys=True), flush=True)
    all_results = []
    necklace_totals = Counter()
    for weight in sorted(set(args.weights)):
        for period in range(weight, 4 * weight + 1):
            words = necklaces(period, weight)
            necklace_totals[weight] += len(words)
            survivors = [word for word in words if head_possible(word)]
            results = [decide(word, args.binary, args.state_cap, args.seconds, bstep)
                       for word in survivors]
            all_results.extend((weight, period, item) for item in results)
            summary = {"G": weight, "P": period, "necklaces": len(words),
                       "head_survivors": len(survivors),
                       "exhausted": sum(item["status"] == "EXHAUSTED" for item in results),
                       "undecided": sum(item["status"] == "UNDECIDED" for item in results),
                       "accepted_g": sum(bool(item["accepts"]) for item in results),
                       "accepted_e": sum(len(item["accepts"]) for item in results),
                       "states": sum(item.get("states", 0) for item in results)}
            print("PERIOD " + json.dumps(summary, sort_keys=True), flush=True)
            for item in results:
                print("WORD " + json.dumps({"G": weight, "P": period, **item},
                                            sort_keys=True), flush=True)
    tally = Counter(item["status"] for _, _, item in all_results)
    print("FINAL " + json.dumps({"complete": not tally["UNDECIDED"],
          "weights": sorted(set(args.weights)), "exhausted_words": tally["EXHAUSTED"],
          "necklaces": sum(necklace_totals.values()),
          "necklaces_by_weight": dict(necklace_totals),
          "undecided_words": tally["UNDECIDED"],
          "accepted_g": sum(bool(item["accepts"]) for _, _, item in all_results),
          "accepted_e": sum(len(item["accepts"]) for _, _, item in all_results)},
          sort_keys=True), flush=True)
    return 2 if tally["UNDECIDED"] else 0


if __name__ == "__main__":
    sys.exit(main())
