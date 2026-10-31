#!/usr/bin/env python3
"""Independent integer-arithmetic replay of Agent 116 B/C search witnesses.

The arithmetic below does not call the repository mirror.  It normalizes an
entire coefficient word by division of its integer value, then checks literal
edge identities.  The mirror is imported only as a separate comparison oracle
and to read existing positive-control certificate data from Lean sources.
This is a COMPUTED cross-check, not Lean verification or an exclusion search.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path
import sys

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[2]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def value(base: int, word: list[int]) -> int:
    total = 0
    for coefficient in reversed(word):
        total = total * base + coefficient
    return total


def normalized(base: int, word: list[int], entering: int) -> tuple[list[int], int]:
    carry, residue = divmod(value(base, word) + entering, base ** len(word))
    digits = []
    for _ in word:
        residue, digit = divmod(residue, base)
        digits.append(digit)
    require(residue == 0, "normalization residue did not fit its width")
    return digits, carry


def bounded(base: int, word: list[int]) -> bool:
    return all(type(x) is int and 0 <= x <= 2 * base - 2 for x in word)


def exterior(base: int, B: list[int]) -> tuple[int, int, list[int]]:
    require(base >= 2 and bounded(base, B), "invalid base or B coefficients")
    require(not B or B[0] != 0, "B has zero first coefficient")
    low, e = normalized(base, B, 0)
    high, g = normalized(base, list(reversed(B)), 1 - e)
    require(e in (0, 1) and g in (0, 1), "nonbinary exterior carry")
    if g:
        low = low + [(base - 1) * (1 - e)]
        high = list(reversed(high))
        high.insert(0, 1)
    else:
        high.reverse()
    require(len(low) == len(high), "exterior summands have different widths")
    return e, g, [a + b for a, b in zip(low, high)]


def center(base: int, C: list[int], e: int, g: int) -> list[int]:
    require(bounded(base, C) and C == C[::-1], "invalid or asymmetric C")
    digits, outgoing = normalized(base, C, e)
    require(outgoing == 1 - e, "center carry does not complement exterior carry")
    if g:
        digits.append((base - 1) * e)
    return [a + b for a, b in zip(digits, reversed(digits))]


def suffix_trim(base: int, raw: list[int], target: list[int]) -> int:
    u = len(raw) - len(target)
    require(u >= 0 and raw == target + [base - 1] * u,
            "exterior successor is not the claimed literal neutral trim")
    return u


def symmetric_trim(base: int, raw: list[int], target: list[int]) -> int:
    difference = len(raw) - len(target)
    require(difference >= 0 and difference % 2 == 0, "invalid center trim length")
    v = difference // 2
    require(raw == [base - 1] * v + target + [base - 1] * v,
            "center successor is not the claimed literal neutral trim")
    return v


def reverse_add(base: int, number: int) -> int:
    reverse, remainder = 0, number
    while remainder:
        remainder, digit = divmod(remainder, base)
        reverse = base * reverse + digit
    return number + reverse


def digits_lsf(base: int, number: int) -> list[int]:
    result = []
    while number:
        number, digit = divmod(number, base)
        result.append(digit)
    return result


def template(base: int, B: list[int], C: list[int], gap: int) -> int:
    return value(base, B + [base - 1] * gap + C + [base - 1] * gap + B[::-1])


def load_mirror():
    path = ROOT / "calculation/neutral_band_search.py"
    spec = importlib.util.spec_from_file_location("a116_mirror_oracle", path)
    require(spec is not None and spec.loader is not None, "mirror import failed")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def audit_b(base: int, Bs: list[list[int]], es: str, gs: str, mirror) -> dict:
    period = len(Bs)
    require(period > 0 and len(es) == len(gs) == period, "B stream length mismatch")
    require(set(es + gs) <= {"0", "1"}, "B stream is not binary")
    trims = []
    for t, B in enumerate(Bs):
        e, g, raw = exterior(base, B)
        require((e, g) == (int(es[t]), int(gs[t])), f"B carry mismatch at phase {t}")
        u = suffix_trim(base, raw, Bs[(t + 1) % period])
        # One coefficient forces exactly the required center carry.
        synthetic_C = [base] if e == 0 else [0]
        require(mirror.nextB(base, B, synthetic_C) == raw,
                f"independent/mirror B mismatch at phase {t}")
        trims.append(u)
    require(sum(trims) == gs.count("1"), "B length-balance identity failed")
    return {"period": period, "sum_g": gs.count("1"), "sum_u": sum(trims),
            "max_B_width": max(map(len, Bs)), "u": trims}


def audit_cycle(base: int, Bs: list[list[int]], Cs: list[list[int]],
                es: str, gs: str, mirror, expected_v: str | None = None) -> tuple[dict, list]:
    Bresult = audit_b(base, Bs, es, gs, mirror)
    period = len(Bs)
    require(len(Cs) == period, "center phase count mismatch")
    if expected_v is not None:
        require(len(expected_v) == period and set(expected_v) <= {"0", "1"},
                "invalid cauto binary trim pattern")
    edges = []
    for t, (B, C) in enumerate(zip(Bs, Cs)):
        e, g, _ = exterior(base, B)
        rawC = center(base, C, e, g)
        B2, C2 = Bs[(t + 1) % period], Cs[(t + 1) % period]
        u, v = Bresult["u"][t], symmetric_trim(base, rawC, C2)
        if expected_v is not None:
            require(v == int(expected_v[t]), "center trim differs from printed pattern")
        edge = [B, C, B2, C2, u, v]
        require(mirror.nextC(base, B, C) == rawC and mirror.edgeOK(base, edge),
                f"independent/mirror C or edge mismatch at phase {t}")
        for gap in (2, 3, 5):
            actual = reverse_add(base, template(base, B, C, gap))
            expected = template(base, B2, C2, gap - g + u + v)
            require(actual == expected, f"ordinary integer step mismatch at phase {t}")
        edges.append(edge)
    sum_v = sum(edge[5] for edge in edges)
    require(2 * sum_v == Bresult["sum_g"], "center length-balance identity failed")
    require(mirror.cycleOK(base, edges, Bs[0], Cs[0]), "mirror cycleOK rejected cycle")
    return ({**Bresult, "sum_v": sum_v, "max_C_width": max(map(len, Cs)),
             "integer_step_checks": 3 * period, "mirror_cycleOK": True}, edges)


def selftest(mirror) -> dict:
    summaries = []
    for base, edges in mirror._lean_certs():
        Bs, Cs = [edge[0] for edge in edges], [edge[1] for edge in edges]
        es = "".join(str(exterior(base, B)[0]) for B in Bs)
        gs = "".join(str(exterior(base, B)[1]) for B in Bs)
        result, replayed = audit_cycle(base, Bs, Cs, es, gs, mirror)
        require([list(edge) for edge in edges] == replayed, "source certificate edges changed")
        summaries.append({"base": base, **result})
    require(len(summaries) == 8, "expected eight source positive controls")
    return {"source_controls": summaries, "source_edges": sum(r["period"] for r in summaries),
            "integer_step_checks": sum(r["integer_step_checks"] for r in summaries)}


def records_audit(path: Path, mirror) -> tuple[dict, list]:
    records = json.loads(path.read_text())
    bases = {batch["base"] for batch in records["B"]}
    require(len(bases) == 1, "expected exactly one base in search records")
    base = next(iter(bases))
    summaries, cycles = [], []
    for batch in records["B"]:
        for stream in batch["streams"]:
            require(stream["b"] == base, "printed B base mismatch")
            require(stream["p"] == batch["period"], "printed B period mismatch")
            summaries.append(audit_b(base, stream["B"], stream["e"], stream["g"], mirror))
    for record in records["C"]:
        for hit in record.get("hits", []):
            result, edges = audit_cycle(base, record["B"], hit["C"],
                                       record["e"], record["g"], mirror, hit["v"])
            cycles.append({"base": base, "e": record["e"], "g": record["g"],
                           "summary": result, "edges": edges})
    return ({"base": base, "last_recorded_period": records["B"][-1]["period"],
             "accepted_B_streams_replayed": len(summaries),
             "B_edges_replayed": sum(r["period"] for r in summaries),
             "center_cycles_replayed": len(cycles),
             "cycle_edges_replayed": sum(c["summary"]["period"] for c in cycles)}, cycles)


def certificate_audit(path: Path, mirror, steps: int) -> tuple[dict, list]:
    record = json.loads(path.read_text())
    base, submitted = record["base"], record["edges"]
    Bs, Cs = [edge[0] for edge in submitted], [edge[1] for edge in submitted]
    es = "".join(str(exterior(base, B)[0]) for B in Bs)
    gs = "".join(str(exterior(base, B)[1]) for B in Bs)
    result, edges = audit_cycle(base, Bs, Cs, es, gs, mirror)
    require(edges == submitted, "literal submitted edges differ from reconstructed edges")
    gap = 2 + gs.count("1")
    initial_gap = gap
    initial = number = template(base, Bs[0], Cs[0], gap)
    initial_digits = digits_lsf(base, initial)
    for t in range(steps + 1):
        phase = t % len(edges)
        B, C, B2, C2, u, v = edges[phase]
        require(gap >= 2, "template orbit lost the two-digit neutral gap")
        require(number == template(base, B, C, gap), f"orbit/template mismatch at step {t}")
        digits = digits_lsf(base, number)
        require(digits and digits != digits[::-1], f"ordinary palindrome at step {t}")
        if t < steps:
            number = reverse_add(base, number)
            gap += u + v - int(gs[phase])
    alphabet = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    seed = "".join(alphabet[x] for x in reversed(initial_digits)) if base <= 36 else initial_digits[::-1]
    result.update({"base": base, "e": es, "g": gs, "seed_base_digits": seed,
                   "initial_digits": len(initial_digits), "final_digits": len(digits),
                   "initial_gap": initial_gap, "final_gap": gap,
                   "ordinary_orbit_steps": steps, "orbit_template_matches": steps + 1,
                   "palindromes_in_checked_orbit": 0})
    return result, edges


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--selftest", action="store_true")
    parser.add_argument("--records", type=Path)
    parser.add_argument("--certificate", type=Path)
    parser.add_argument("--orbit-steps", type=int, default=1000)
    parser.add_argument("--certificates-output", type=Path)
    args = parser.parse_args()
    require(args.selftest or args.records or args.certificate,
            "provide --selftest, --records and/or --certificate")
    require(args.orbit_steps >= 0, "orbit steps must be nonnegative")
    mirror, result, cycles = load_mirror(), {}, []
    if args.selftest:
        result["selftest"] = selftest(mirror)
    if args.records:
        result["records"], cycles = records_audit(args.records, mirror)
    if args.certificate:
        result["certificate"], edges = certificate_audit(args.certificate, mirror, args.orbit_steps)
        cycles.append({"base": result["certificate"]["base"],
                       "summary": result["certificate"], "edges": edges})
    if args.certificates_output:
        args.certificates_output.write_text(json.dumps(cycles, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
