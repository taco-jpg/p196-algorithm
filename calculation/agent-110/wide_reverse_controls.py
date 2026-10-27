#!/usr/bin/env python3
"""Independent unsigned-256, wide-mask, exact-frontier and full-seam controls.

No import of another search/checker implementation. A temporary C++ harness
exercises the public Count256 interface against Python arbitrary integers.
Only bounded controls are run; this script never launches the decimal P48
scientific search. Optional output contains mathematical witnesses and finite
preimage sets, not solver transcripts.
"""
import argparse
from collections import Counter
import hashlib
import itertools
import json
import math
from pathlib import Path
import random
import subprocess
import tempfile
import time


HERE = Path(__file__).resolve().parent
MASK64 = (1 << 64) - 1
LIMIT256 = 1 << 256
HARNESS = r'''
#include "count256.hpp"
#include <array>
#include <cstdint>
#include <iostream>
#include <stdexcept>
#include <string>
using agent110::Count256;
static void show(const char* prefix, const Count256& value) {
    std::cout << prefix << ' ' << value.decimal();
    for (auto limb : value.limbs()) std::cout << ' ' << limb;
    std::cout << '\n';
}
int main() {
    std::string op;
    while (std::cin >> op) {
        std::array<std::uint64_t,4> aa{},bb{};
        std::uint32_t divisor = 0;
        for (auto& limb : aa) if (!(std::cin >> limb)) return 2;
        for (auto& limb : bb) if (!(std::cin >> limb)) return 2;
        if (!(std::cin >> divisor)) return 2;
        Count256 a=Count256::from_limbs(aa), b=Count256::from_limbs(bb);
        try {
            if (op=="ADD") show("OK",a+b);
            else if (op=="ADD_ASSIGN") { auto* address=&(a+=b); if(address!=&a) return 3; show("OK",a); }
            else if (op=="SUB") show("OK",a-b);
            else if (op=="SUB_ASSIGN") { auto* address=&(a-=b); if(address!=&a) return 3; show("OK",a); }
            else if (op=="SELFADD") { a+=a; show("OK",a); }
            else if (op=="SELFSUB") { a-=a; show("OK",a); }
            else if (op=="DIV") {
                auto r=a.divmod(divisor);
                std::cout << "DIV " << a.decimal() << ' ' << r;
                for(auto limb:a.limbs()) std::cout << ' ' << limb;
                std::cout << '\n';
            } else if(op=="DEC") show("OK",a);
            else if(op=="CTOR") { Count256 value(aa[0]); show("OK",value); }
            else if(op=="CMP") {
                std::cout << "CMP " << (a==b) << ' ' << (a!=b) << ' ' << (a<b) << ' '
                          << (a>b) << ' ' << (a<=b) << ' ' << (a>=b) << ' '
                          << bool(a) << ' ' << bool(b) << '\n';
            } else return 4;
        } catch(const std::overflow_error&) { show("OVERFLOW",a); }
          catch(const std::underflow_error&) { show("UNDERFLOW",a); }
          catch(const std::invalid_argument&) { show("INVALID",a); }
    }
}
'''


class Controls:
    def __init__(self, args):
        self.args = args
        self.started = time.monotonic()
        self.captures = {"witnesses": [], "preimage_controls": []}

    def remaining(self):
        remaining = self.args.seconds - (time.monotonic() - self.started)
        if remaining <= 0:
            raise RuntimeError("control-suite time cap")
        return remaining

    def run(self, binary, base, e, g, flags, payload=None):
        command = [str(binary.resolve()), str(base), e, g] + list(flags)
        if "--seconds" not in flags:
            command += ["--seconds", str(max(1, min(30, math.ceil(self.remaining()))))]
        result = subprocess.run(command, input=None if payload is None else json.dumps(payload),
                                text=True, capture_output=True, check=False,
                                timeout=min(self.remaining(), 40))
        return result

    def states(self, binary, base, e, g, flags, payload=None):
        run = self.run(binary, base, e, g, flags, payload)
        if run.returncode != 0:
            raise RuntimeError("incomplete finite-set control: " + run.stderr + run.stdout[:1000])
        rows = json.loads(run.stdout)
        if not isinstance(rows, list):
            raise RuntimeError("expected complete state array")
        result = set()
        for row in rows:
            if (not isinstance(row, list) or len(row) != 3 or type(row[0]) is not int
                    or type(row[1]) is not int or not isinstance(row[2], list)
                    or not 0 <= row[0] < 1 << len(g) or not 0 <= row[1] < 1 << len(g)
                    or len(row[2]) != g.count("1")
                    or any(type(x) is not int or not 0 <= x < base for x in row[2])):
                raise RuntimeError("malformed finite-set state")
            result.add((row[0], row[1], tuple(row[2])))
        if len(result) != len(rows):
            raise RuntimeError("duplicate exported state")
        return result

    def records(self, base, e, g, flags, expected):
        run = self.run(self.args.engine, base, e, g, flags)
        records = [json.loads(line) for line in run.stdout.splitlines() if line.strip()]
        finals = [row for row in records if row.get("type") == "RESULT"]
        if len(finals) != 1 or finals[0]["status"] != expected:
            raise RuntimeError("unexpected search control: " + run.stdout[:2000] + run.stderr)
        if run.returncode != (2 if expected == "UNDECIDED" else 0):
            raise RuntimeError("incorrect completion exit code")
        witnesses = [row for row in records if row.get("type") == "WITNESS"]
        if expected == "ACCEPT":
            if len(witnesses) != 1:
                raise RuntimeError("positive lacks one concrete witness")
            replay(witnesses[0], base, e, g)
            self.captures["witnesses"].append(witnesses[0])
        elif witnesses:
            raise RuntimeError("unexpected witness in a nonpositive control")
        return finals[0], witnesses


def limbs(value):
    return [(value >> (64 * j)) & MASK64 for j in range(4)]


def count_controls(control, temporary):
    randomizer = random.Random(110256)
    values = {0, 1, 2, 9, 10, LIMIT256 - 1, LIMIT256 - 2}
    for exponent in (32, 63, 64, 65, 127, 128, 129, 191, 192, 193, 239, 240, 241, 254, 255):
        values.update((1 << exponent) + delta for delta in (-1, 0, 1))
    values = sorted(values)
    pairs = list(itertools.product(values, repeat=2))
    pairs += [(randomizer.getrandbits(256), randomizer.getrandbits(256)) for _ in range(256)]
    cases = [(op, a, b, 0) for a, b in pairs for op in ("ADD", "ADD_ASSIGN", "SUB", "SUB_ASSIGN", "CMP")]
    unary = values + [randomizer.getrandbits(256) for _ in range(128)]
    for a in unary:
        cases.extend((op, a, 0, 0) for op in ("DEC", "SELFADD", "SELFSUB"))
        for divisor in (0, 1, 2, 3, 10, 65535, 65536, (1 << 31) - 1, 1 << 31, (1 << 32) - 1):
            cases.append(("DIV", a, 0, divisor))
    cases += [("DIV", randomizer.getrandbits(256), 0, randomizer.getrandbits(32)) for _ in range(256)]
    cases += [("CTOR", a, 0, 0) for a in (0, 1, MASK64, MASK64 - 1)]
    source = temporary / "count_control.cpp"
    executable = temporary / "count_control"
    source.write_text(HARNESS)
    compile_run = subprocess.run([control.args.compiler, "-std=c++17", "-O2", "-Wall", "-Wextra",
                                  "-Werror", "-pedantic", "-fsanitize=undefined", "-fno-sanitize-recover=all",
                                  "-I", str(HERE), str(source), "-o", str(executable)],
                                 text=True, capture_output=True, timeout=min(60, control.remaining()))
    if compile_run.returncode:
        raise RuntimeError("count harness compilation failed: " + compile_run.stderr)
    request = "".join(" ".join(map(str, (op, *limbs(a), *limbs(b), divisor))) + "\n"
                      for op, a, b, divisor in cases)
    run = subprocess.run([str(executable)], input=request, text=True, capture_output=True,
                         timeout=min(30, control.remaining()))
    if run.returncode or run.stderr:
        raise RuntimeError("count harness/sanitizer failure: " + run.stderr)
    lines = run.stdout.splitlines()
    if len(lines) != len(cases):
        raise RuntimeError("missing count arithmetic output")
    outcomes = Counter()
    for case, line in zip(cases, lines):
        op, a, b, divisor = case
        tokens = line.split()
        if op == "CMP":
            expected = ["CMP"] + [str(int(x)) for x in (a == b, a != b, a < b, a > b,
                                                        a <= b, a >= b, bool(a), bool(b))]
        else:
            kind, value, remainder = "OK", a, None
            if op in ("ADD", "ADD_ASSIGN", "SELFADD"):
                value = a + (a if op == "SELFADD" else b)
                if value >= LIMIT256:
                    kind, value = "OVERFLOW", a
            elif op in ("SUB", "SUB_ASSIGN", "SELFSUB"):
                value = a - (a if op == "SELFSUB" else b)
                if value < 0:
                    kind, value = "UNDERFLOW", a
            elif op == "DIV":
                if divisor == 0:
                    kind, value = "INVALID", a
                else:
                    kind = "DIV"
                    value, remainder = divmod(a, divisor)
            expected = [kind, str(value)]
            if remainder is not None:
                expected.append(str(remainder))
            expected += list(map(str, limbs(value)))
        if tokens != expected:
            raise RuntimeError(f"Count256 mismatch {case}: {tokens} != {expected}")
        outcomes[tokens[0]] += 1
    return {"cases": len(cases), "operations": dict(Counter(row[0] for row in cases)),
            "outcomes": dict(outcomes), "undefined_behavior_sanitizer": "PASS",
            "header_sha256": hashlib.sha256((HERE / "count256.hpp").read_bytes()).hexdigest()}


def mask(word):
    return sum(int(digit) << t for t, digit in enumerate(word))


def terminal(base, e, g):
    positions = [t for t, digit in enumerate(g) if digit == "1"]
    return mask(e), ((1 << len(g)) - 1) ^ mask(e), tuple((base - 1) * int(e[t]) for t in positions)


def explicit_preimage(base, g, target):
    """Closed coefficient paths, independently of block decomposition/MDDs."""
    p = len(g)
    positions = [t for t, digit in enumerate(g) if digit == "1"]
    index = {t: j for j, t in enumerate(positions)}
    target_l, target_h, target_y = target
    allowed = []
    for t in range(p):
        q, a = target_h >> t & 1, target_l >> t & 1
        table = {}
        for x in range(2 * base - 1):
            if g[t] == "1" and (x + q) % base != target_y[index[t]]:
                continue
            ls = tuple(l for l in (0, 1) if (x + l) // base == a)
            if ls:
                table[x] = ls
        allowed.append(table)
    transitions = []
    for t in range(p):
        q = target_h >> t & 1
        following = allowed[(t + 1) % p]
        table = {}
        for x, ls in allowed[t].items():
            h, digit = divmod(x + q, base)
            options = []
            for l in ls:
                low_digit = (x + l) % base
                if g[t] == "1":
                    options += [(nx, l, h, nx - low_digit) for nx in following if 0 <= nx - low_digit < base]
                elif low_digit + digit in following:
                    options.append((low_digit + digit, l, h, 0))
            table[x] = options
        transitions.append(table)
    result = set()
    ys = [0] * len(positions)
    for initial in allowed[0]:
        viable = [set() for _ in range(p + 1)]
        viable[-1].add(initial)
        for t in range(p - 1, -1, -1):
            viable[t] = {x for x, choices in transitions[t].items()
                         if any(nx in viable[t + 1] for nx, _, _, _ in choices)}
        if initial not in viable[0]:
            continue

        def visit(t, x, old_l, old_h):
            if t == p:
                result.add((old_l, old_h, tuple(ys)))
                return
            for nx, l, h, y in transitions[t][x]:
                if nx in viable[t + 1]:
                    if g[t] == "1":
                        ys[index[t]] = y
                    visit(t + 1, nx, old_l | l << t, old_h | h << t)
        visit(0, initial, 0, 0)
    return result


def replay(witness, base, e, g):
    rows = witness["B_t"]
    p = len(g)
    if witness["base"] != base or witness["e"] != e or witness["g"] != g or len(rows) != p:
        raise RuntimeError("witness driver/period mismatch")
    width = witness["width"]
    if width < 1 or any(len(row) != width or row[0] <= 0 for row in rows):
        raise RuntimeError("invalid common-width positive witness")
    for t, row in enumerate(rows):
        if any(type(x) is not int or not 0 <= x <= 2 * base - 2 for x in row):
            raise RuntimeError("invalid witness coefficient")
        modulus = base ** width
        value = sum(x * base ** j for j, x in enumerate(row))
        carry, low = divmod(value, modulus)
        reverse_value = sum(x * base ** (width - 1 - j) for j, x in enumerate(row)) + 1 - carry
        overflow, high = divmod(reverse_value, modulus)
        a = [(low // base ** j) % base for j in range(width)]
        b = [(high // base ** (width - 1 - j)) % base for j in range(width)]
        if overflow:
            a.append((base - 1) * (1 - carry))
            b.insert(0, 1)
        raw = [x + y for x, y in zip(a, b)]
        if (carry, overflow) != (int(e[t]), int(g[t])) or raw != rows[(t + 1) % p] + [base - 1] * overflow:
            raise RuntimeError(f"whole-integer full-period seam failure at phase {t}")
    if witness["u"] != list(map(int, g)):
        raise RuntimeError("unexpected common-width trims")


def narrow_controls(control):
    randomizer = random.Random(11064)
    cases = [(2, "10", "10"), (2, "01", "01"), (3, "010", "101"),
             (4, "100", "100"), (6, "01", "01"), (6, "0101", "0101"),
             (8, "1000", "1000"), (8, "0001", "0001")]
    frontiers = firsts = preimages = 0
    for base, e, g in cases:
        for depth in (0, 1, 2):
            old = control.states(control.args.old_engine, base, e, g, ["--export-layer", str(depth)])
            new = control.states(control.args.engine, base, e, g, ["--export-layer", str(depth)])
            if old != new:
                raise RuntimeError("old/new complete narrow frontier mismatch")
            frontiers += 1
        if control.states(control.args.old_engine, base, e, g, ["--first"]) != control.states(
                control.args.engine, base, e, g, ["--first"]):
            raise RuntimeError("old/new FIRST mismatch")
        firsts += 1
        targets = {terminal(base, e, g)}
        for _ in range(5):
            targets.add((randomizer.randrange(1 << len(g)), randomizer.randrange(1 << len(g)),
                         tuple(randomizer.randrange(base) for _ in range(g.count("1")))))
        for chosen in [{target} for target in targets] + [targets]:
            expected = set().union(*(explicit_preimage(base, g, target) for target in chosen))
            old = control.states(control.args.old_engine, base, e, g, ["--preimage"], sorted(chosen))
            new = control.states(control.args.engine, base, e, g, ["--preimage"], sorted(chosen))
            if old != expected or new != expected:
                raise RuntimeError("old/new/explicit narrow preimage mismatch")
            preimages += 1
    return {"drivers": len(cases), "complete_frontiers": frontiers,
            "first_sets": firsts, "explicit_preimage_sets": preimages}


def wide_mask_controls(control):
    checked = []
    # Full-period seam fixture: coefficient port at P/2 is 1,
    # while the initial port is 0. Artificially closing either half is wrong.
    for p in (48, 64):
        middle = p // 2
        common = (1 << middle) | (1 << (p - 1))
        target = (common, common, (0,) * p)
        expected = set()
        for a, b in itertools.product((0, 1), repeat=2):
            ys = [0] * p
            ys[middle - 1], ys[p - 2] = 1 - a, 1 - b
            expected.add((common | a << (middle - 1) | b << (p - 2), common, tuple(ys)))
        explicit = explicit_preimage(2, "1" * p, target)
        actual = control.states(control.args.engine, 2, "0" * p, "1" * p, ["--preimage"], [target])
        if actual != expected or explicit != expected:
            raise RuntimeError("wide full-seam four-predecessor control failed")
        control.captures["preimage_controls"].append(
            {"base": 2, "e": "0" * p, "g": "1" * p, "target": target, "predecessors": sorted(actual)})
        checked.append({"period": p, "states": len(actual), "kind": "nonunit_seam"})
    for p in (33, 64):
        all_bits = (1 << p) - 1
        target = (all_bits, all_bits, (0,) * p)
        expected = {(all_bits, all_bits, (1,) * p)}
        actual = control.states(control.args.engine, 2, "0" * p, "1" * p, ["--preimage"], [target])
        if actual != expected or explicit_preimage(2, "1" * p, target) != expected:
            raise RuntimeError("maximum legal mask failed")
        checked.append({"period": p, "states": 1, "kind": "maximum_mask"})
    return checked


def guard_controls(control):
    cases = []
    def reject(name, base, e, g, flags, payload=None, reason=None):
        run = control.run(control.args.engine, base, e, g, flags, payload)
        rows = [json.loads(line) for line in run.stdout.splitlines() if line.strip()]
        final = rows[-1] if rows else {}
        if run.returncode != 2 or final.get("status") != "UNDECIDED" or any(r.get("type") == "WITNESS" for r in rows):
            raise RuntimeError("guard produced a completed decision: " + name + " " + run.stdout[:1000])
        if reason is not None and final.get("reason") != reason:
            raise RuntimeError("wrong guard reason: " + name + " " + str(final))
        cases.append(name)
    reject("P65", 2, "0" * 65, "1" * 65, ["--preimage"], [])
    reject("P33-high-L", 2, "0" * 33, "1" * 33, ["--preimage"], [[1 << 33, 0, [0] * 33]])
    reject("P33-high-H", 2, "0" * 33, "1" * 33, ["--preimage"], [[0, 1 << 33, [0] * 33]])
    reject("P64-overflow-L", 2, "0" * 64, "1" * 64, ["--preimage"], [[1 << 64, 0, [0] * 64]])
    reject("P64-overflow-H", 2, "0" * 64, "1" * 64, ["--preimage"], [[0, 1 << 64, [0] * 64]])
    reject("negative-mask", 2, "0" * 64, "1" * 64, ["--preimage"], [[-1, 0, [0] * 64]])
    reject("bad-lag-count", 2, "0" * 64, "1" * 64, ["--preimage"], [[0, 0, [0] * 63]])
    reject("bad-lag-digit", 2, "0" * 64, "1" * 64, ["--preimage"], [[0, 0, [2] * 64]])
    boundary = "".join("0" if t % 8 == 0 else "1" for t in range(64))
    if 2 * 64 + 2 * boundary.count("1") != 240:
        raise RuntimeError("bad count-space boundary fixture")
    if control.states(control.args.engine, 4, "0" * 64, boundary, ["--preimage"], []) != set():
        raise RuntimeError("exact 240-bit count-space boundary rejected")
    too_wide = "1" + boundary[1:]
    reject("242-bit-count-space", 4, "0" * 64, too_wide, ["--preimage"], [])
    reject("node-cap", 2, "10", "10", ["--layers", "2", "--nodes", "2"], reason="node_cap")
    reject("operation-cap", 2, "10", "10", ["--layers", "2", "--operations", "1"], reason="operation_cap")
    reject("export-cap", 2, "1010", "1010", ["--export-layer", "1", "--export-cap", "1"], reason="export_cap")
    reject("actual-memory-cap", 2, "01" * 32, "01" * 32,
           ["--layers", "0", "--memory-mib", "64", "--seconds", "10", "--operations", "1000000000"],
           reason="memory_cap")
    reject("invalid-memory-cap", 2, "10", "10", ["--preimage", "--memory-mib", "63"], [])
    return {"rejections": len(cases), "cases": cases, "accepted_count_space_bits": 240}


def seam_and_positive_controls(control):
    # Agent105's base6 counterexample requires two laps of its primitive driver.
    one, _ = control.records(6, "01", "01", ["--layers", "100", "--memory-mib", "512"], "EXHAUSTED")
    two, witness = control.records(6, "0101", "0101", ["--layers", "100", "--memory-mib", "512"], "ACCEPT")
    rows = witness[0]["B_t"]
    if rows[0] == rows[2] or rows[1] == rows[3]:
        raise RuntimeError("two-lap positive was incorrectly collapsed to one driver unit")
    wide = []
    for base, word, repeats in ((4, "001", 11), (8, "0001", 16)):
        stream = word * repeats
        result, witnesses = control.records(base, stream, stream,
                                            ["--layers", "4", "--memory-mib", "512"], "ACCEPT")
        if len(witnesses[0]["B_t"]) != len(stream) or stream[-1] != "1":
            raise RuntimeError("wide highest-bit/full-period positive control failed")
        wide.append({"base": base, "period": len(stream), "highest_phase": len(stream) - 1,
                     "width": witnesses[0]["width"], "first_states": result["first_states"]})
    return {"one_lap": {"status": one["status"], "states": one["last_complete_states"]},
            "two_laps": {"status": two["status"], "states": two["last_complete_states"], "width": witness[0]["width"]},
            "wide_positives": wide}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--engine", type=Path, default=Path("/tmp/agent110-wide-reverse-mdd"))
    parser.add_argument("--old-engine", type=Path, default=Path("/tmp/agent110-wide-narrow-baseline"))
    parser.add_argument("--compiler", default="g++")
    parser.add_argument("--seconds", type=float, default=180)
    parser.add_argument("--witnesses", type=Path)
    args = parser.parse_args()
    if not math.isfinite(args.seconds) or not 0 < args.seconds <= 1500:
        parser.error("seconds must be positive and at most 1500")
    control = Controls(args)
    with tempfile.TemporaryDirectory(prefix="agent110-wide-controls-") as temp:
        counts = count_controls(control, Path(temp))
        narrow = narrow_controls(control)
        masks = wide_mask_controls(control)
        seams = seam_and_positive_controls(control)
        guards = guard_controls(control)
    if args.witnesses is not None:
        args.witnesses.write_text(json.dumps(control.captures, sort_keys=True) + "\n")
    print(json.dumps({"status": "PASS", "count256": counts, "narrow": narrow, "wide_masks": masks,
                      "full_seams": seams, "guards": guards,
                      "seconds": time.monotonic() - control.started}, sort_keys=True))


if __name__ == "__main__":
    main()
