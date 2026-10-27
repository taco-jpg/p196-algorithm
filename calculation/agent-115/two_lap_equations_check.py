#!/usr/bin/env python3
"""Independent arithmetic controls for the fixed-width exterior equations.

This is not a solver. It checks integer-derived digits/carry equations against
the exact repository mirror, every permissible trim of small exterior words,
and all eight actual Lean-source certificates after padding and phase retiming.
No assertion is used for acceptance, so the checks remain active under -O.
"""

from __future__ import annotations

import argparse
import ast
import importlib.util
import itertools
import json
from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parents[2]
TARGET_E = "010100110100101011001011" * 2
TARGET_G = "110001001000110001001000" * 2


class CheckFailure(Exception):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise CheckFailure(message)


def valid(base: int, word: tuple[int, ...]) -> bool:
    return base >= 2 and all(0 <= x <= 2 * base - 2 for x in word) and (
        not word or word[0] != 0)


def column_trace(base: int, word: tuple[int, ...]) -> dict:
    """Digits use positional integers; carries use separately checked columns.

    f[j] enters column j from below. r[j+1] enters it from above, and r[j]
    leaves toward column j-1. Consequently f[0]=0,f[W]=e,r[W]=1-e,r[0]=g.
    """
    require(valid(base, word), "invalid exterior source")
    width = len(word)
    value = sum(x * base ** j for j, x in enumerate(word))
    e = value // base ** width
    reversed_value = sum(x * base ** (width - 1 - j) for j, x in enumerate(word)) + 1 - e
    g = reversed_value // base ** width
    digits = tuple(value // base ** j % base for j in range(width))
    reverse_digits = tuple(reversed_value // base ** (width - 1 - j) % base
                           for j in range(width))
    forward = [0]
    for x in word:
        forward.append((x + forward[-1]) // base)
    reverse = [0] * width + [1 - e]
    for j in range(width - 1, -1, -1):
        reverse[j] = (word[j] + reverse[j + 1]) // base
    require(e in (0, 1) and g in (0, 1), "stream must consist of bits")
    require(forward[-1] == e and reverse[0] == g, "boundary carries")
    require(all(x in (0, 1) for x in forward + reverse), "carry bound")
    for j, x in enumerate(word):
        require(x + forward[j] == digits[j] + base * forward[j + 1],
                "forward column equation")
        require(x + reverse[j + 1] == reverse_digits[j] + base * reverse[j],
                "reverse column equation")
    if g:
        raw = tuple(a + b for a, b in zip(
            digits + ((base - 1) * (1 - e),), (1,) + reverse_digits))
    else:
        raw = tuple(a + b for a, b in zip(digits, reverse_digits))
    return {"e": e, "g": g, "D": digits, "R": reverse_digits,
            "f": tuple(forward), "r": tuple(reverse), "raw": raw}


def fixed_edge(base: int, source: tuple[int, ...], target: tuple[int, ...],
               e: int, g: int) -> bool:
    """Exact constant-width, u=g equation predicate, with all boundaries."""
    if not source or len(source) != len(target) or not valid(base, target):
        return False
    t = column_trace(base, source)
    if t["e"] != e or t["g"] != g:
        return False
    if not g:
        return all(target[j] == t["D"][j] + t["R"][j] for j in range(len(source)))
    return (target[0] == t["D"][0] + 1
            and all(target[j] == t["D"][j] + t["R"][j - 1]
                    for j in range(1, len(source)))
            and t["R"][-1] == (base - 1) * e)


def padding(base: int, word: tuple[int, ...], width: int) -> tuple[int, ...]:
    require(len(word) <= width, "padding width too small")
    return word + (base - 1,) * (width - len(word))


def load_mirror():
    spec = importlib.util.spec_from_file_location("a115_reference_mirror", ROOT / "calculation/neutral_band_search.py")
    require(spec is not None and spec.loader is not None, "mirror import")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def split_fields(text: str) -> list[str]:
    depth = 0
    fields = []
    begin = 0
    for i, character in enumerate(text):
        if character == "[":
            depth += 1
        elif character == "]":
            depth -= 1
        elif character == "," and depth == 0:
            fields.append(text[begin:i].strip())
            begin = i + 1
    fields.append(text[begin:].strip())
    require(depth == 0 and len(fields) == 6, "Lean edge field parsing")
    return fields


def source_certificates() -> dict:
    result = {}
    for relative in (
        "lean/P196/Drafts/Agent120NeutralBandCalibration/A120PowerTwo.lean",
        "lean/P196/Agent213KnownBaseMechanisms/KnownBases.lean",
    ):
        text = (ROOT / relative).read_text()
        definitions = {name: ast.literal_eval(value) for name, value in re.findall(
            r"def\s+(\w+)\s*:\s*List Nat\s*:=\s*(\[[^\]]*\])", text)}
        for base, body in re.findall(
                r"def\s+cert(\d+)\s*:\s*List Edge\s*:=\s*\[(.*?)\]\s*\n\n", text, re.S):
            edges = []
            for raw in re.findall(r"⟨(.*?)⟩", body, re.S):
                fields = split_fields(raw)
                words = [ast.literal_eval(s) if s.startswith("[") else definitions[s]
                         for s in fields[:4]]
                edges.append((*words, int(fields[4]), int(fields[5])))
            require(edges and int(base) not in result, "Lean certificate parsing")
            result[int(base)] = edges
    require(set(result) == {2, 4, 8, 11, 16, 17, 26, 32}, "eight known source bases")
    return result


def small_word_checks(mirror) -> dict:
    counts = {"small_words": 0, "padding_identities": 0,
              "all_trim_padding_edges": 0, "fixed_edge_equivalences": 0,
              "rejected_overflow_boundaries": 0}
    for base in (2, 3, 4, 10):
        for size in range(4):
            for source in itertools.product(range(2 * base - 1), repeat=size):
                if not valid(base, source):
                    continue
                counts["small_words"] += 1
                trace = column_trace(base, source)
                center = [base] if trace["e"] == 0 else [0]
                require(mirror.hyp(base, list(source), center), "synthetic flip center")
                require(tuple(mirror.nextB(base, list(source), center)) == trace["raw"],
                        "exact mirror exterior image")
                require(mirror.e1(base, list(source)) == trace["e"]
                        and mirror.gam(base, list(source), center) == trace["g"],
                        "exact mirror carry streams")
                for extra in range(4):
                    padded = source + (base - 1,) * extra
                    new = column_trace(base, padded)
                    require((new["e"], new["g"]) == (trace["e"], trace["g"]),
                            "padding must preserve both streams")
                    require(new["raw"] == trace["raw"] + (base - 1,) * extra,
                            "padding must commute with raw image")
                    counts["padding_identities"] += 1
                if source:
                    target = trace["raw"][:size]
                    exact = trace["raw"] == target + (base - 1,) * trace["g"]
                    require(fixed_edge(base, source, target, trace["e"], trace["g"]) == exact,
                            "constant-width equation equivalence")
                    counts["fixed_edge_equivalences"] += 1
                    if trace["g"]:
                        require(exact == (source[-1] == base - 1), "overflow top coefficient")
                        counts["rejected_overflow_boundaries"] += not exact
                raw = trace["raw"]
                for trim in range(len(raw) + 1):
                    if trim and raw[-trim:] != (base - 1,) * trim:
                        continue
                    target = raw[:len(raw) - trim] if trim else raw
                    require(valid(base, target), "trimmed target validity")
                    for extra in range(3):
                        width = max(len(source), len(target), 1) + extra
                        left, right = padding(base, source, width), padding(base, target, width)
                        require(fixed_edge(base, left, right, trace["e"], trace["g"]),
                                "arbitrary trim must become fixed-width u=g")
                        counts["all_trim_padding_edges"] += 1
    require(not valid(10, (0,)) and not valid(10, (0, 9)), "zero-head rejection")
    require(valid(10, ()) and valid(10, (9, 9)), "empty and neutral-word allowance")
    require(column_trace(10, ())["raw"] == (10,), "empty exterior boundary")
    return counts


def known_source_checks(mirror) -> dict:
    summaries = []
    total_cycles = total_edges = source_edges = 0
    for base, edges in sorted(source_certificates().items()):
        require(mirror.cycleOK(base, edges, edges[0][0], edges[0][1]), "original source cycle")
        period = len(edges)
        source_edges += period
        minimum_width = max(len(edge[0]) for edge in edges)
        for phase in range(period):
            rotated = edges[phase:] + edges[:phase]
            for repetitions in (1, 2):
                timed = rotated * repetitions
                for width in (minimum_width, minimum_width + 2):
                    padded_edges = []
                    for B, C, B2, C2, original_u, v in timed:
                        source, target = tuple(B), tuple(B2)
                        t = column_trace(base, source)
                        require(t["raw"] == target + (base - 1,) * original_u,
                                "original source trim")
                        left, right = padding(base, source, width), padding(base, target, width)
                        require(fixed_edge(base, left, right, t["e"], t["g"]),
                                "retimed fixed-width source equations")
                        padded_edges.append((list(left), C, list(right), C2, t["g"], v))
                        total_edges += 1
                    require(mirror.cycleOK(base, padded_edges, padded_edges[0][0], padded_edges[0][1]),
                            "retimed padded full mirror cycle")
                    total_cycles += 1
        summaries.append({"base": base, "source_period": period, "minimum_padded_width": minimum_width})
    return {"source_certificates": summaries, "source_edges": source_edges,
            "retimed_padded_cycles": total_cycles, "retimed_padded_edges": total_edges}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    try:
        mirror = load_mirror()
        result = {"small": small_word_checks(mirror), "known": known_source_checks(mirror),
                  "target": {"base": 10, "period": len(TARGET_E), "e": TARGET_E, "g": TARGET_G,
                             "overflows": TARGET_G.count("1")}}
        require(len(TARGET_E) == len(TARGET_G) == 48, "target two-lap length")
    except (CheckFailure, KeyError, ValueError) as error:
        print(f"CHECK FAILED: {error}", file=sys.stderr)
        return 1
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(" ".join(f"{k}={v}" for k, v in result["small"].items()))
        print("known_bases=" + ",".join(str(x["base"]) for x in result["known"]["source_certificates"]))
        print(" ".join(f"{k}={v}" for k, v in result["known"].items() if k != "source_certificates"))
        print("target_base=10 period=48 overflow_count=" + str(result["target"]["overflows"]))
        print("ALL CHECKS PASSED")
        print("COMPUTED equation controls only; no target-stream feasibility or decimal certificate claim.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
