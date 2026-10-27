#!/usr/bin/env python3
"""Independent boundary, padding and complete-witness controls for A120 exteriors.

The arithmetic oracle below was fixed from the unchanged neutral_band_search.py
and structure/bauto.cpp before reading either new reverse search implementation.
It uses ordinary carry scans, explicit temporal closure, and complete coefficient
words; it does not import either new search engine. A decimal result is only a
COMPUTED candidate until the registered Lean certificate passes verify.py.

B-only regression fixtures: issue #289, comment 6433052934 (Agent 4), and issue
#314, https://github.com/taco-jpg/p196-algorithm/issues/314. The C24 fixture is the
priority target coordinated in #289. The eight complete positive fixtures are
read from their existing Lean source through the baseline mirror.
"""
from __future__ import annotations

import argparse
from collections import defaultdict
import json
from pathlib import Path
import random
import subprocess
import sys
import time

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import neutral_band_search as mirror

P24_E = "010100110100101011001011"
P24_G = "110001001000110001001000"
P24_V = "100001000000100001000000"
P24_C = [9, 14, 13, 18, 13, 14, 9]
B11 = [18, 14, 0, 2, 10, 10, 6, 0, 7, 8, 18, 9, 1, 5, 9, 6, 4, 3,
       12, 10, 10, 12, 13, 10, 13]
B12 = [10, 4, 6, 6, 7, 12, 9, 16, 16, 13, 0, 2, 10, 17, 7, 0, 18, 6,
       5, 18, 4, 18, 14, 9, 14, 16, 9, 5, 10, 6, 5, 7, 1, 12, 10, 17,
       8, 0, 2, 8, 16, 6, 6, 15, 5, 7, 9, 14, 0, 13, 12]


def require(condition, message):
    if not condition:
        raise ValueError(message)


def nat(value):
    return type(value) is int and value >= 0


def bits(value):
    out = tuple(int(x) for x in value) if isinstance(value, str) else tuple(value)
    require(bool(out) and all(type(x) is int and x in (0, 1) for x in out),
            "expected a nonempty bit stream")
    return out


def word(base, values):
    require(type(base) is int and base >= 2, "invalid base")
    out = list(values)
    require(all(nat(x) and x <= 2 * base - 2 for x in out),
            "coefficient outside the natural A120 domain")
    return out


def normalize(base, values, carry):
    """Literal independent scan; center replay also checks the baseline mirror."""
    ds = []
    for x in values:
        carry, digit = divmod(x + carry, base)
        ds.append(digit)
    return ds, carry


def exterior_step(base, coefficients):
    row = word(base, coefficients)
    require(not row or row[0] > 0, "exterior first coefficient is zero")
    d, e = normalize(base, row, 0)
    dr, g = normalize(base, row[::-1], 1 - e)
    r = dr[::-1]
    raw = [a + b for a, b in zip(d, r)] if not g else [
        a + b for a, b in zip(d + [(base - 1) * (1 - e)], [1] + r)]
    return e, g, raw


def center_step(base, coefficients, e, g, trim):
    row = word(base, coefficients)
    require(e in (0, 1) and g in (0, 1) and nat(trim), "invalid center driver")
    d, c = normalize(base, row, e)
    require((d, c) == mirror.norm(base, row, e), "normalization disagreement")
    require(c == 1 - e, "center carry does not flip")
    if g:
        d = d + [(base - 1) * e]
    raw = [a + b for a, b in zip(d, d[::-1])]
    require(2 * trim <= len(raw), "center trim exceeds width")
    if trim:
        require(raw[:trim] == raw[-trim:] == [base - 1] * trim,
                "nonneutral center trim")
        raw = raw[trim:-trim]
    return raw


def center_cycle(base, e, g, v, initial):
    e, g = bits(e), bits(g)
    require(len(e) == len(g) == len(v), "inconsistent driver lengths")
    rows = [word(base, initial)]
    for et, gt, vt in zip(e, g, v):
        rows.append(center_step(base, rows[-1], et, gt, vt))
    require(rows[-1] == rows[0], "center fails to close")
    return rows[:-1]


def state(base, g, value):
    require(isinstance(value, (list, tuple)) and len(value) == 3, "invalid cut")
    l, h, y = value
    require(nat(l) and nat(h) and l < 1 << len(g) and h < 1 << len(g),
            "cut carry mask outside period")
    require(isinstance(y, (tuple, list)) and len(y) == sum(g) and
            all(nat(x) and x < base for x in y), "invalid cut partner digits")
    return l, h, tuple(y)


def blocks(g, cut):
    l, h, y = cut
    it = iter(y)
    return tuple(((l >> t) & 1, (h >> t) & 1, next(it) if gt else -1)
                 for t, gt in enumerate(g))


def pack(g, labels):
    l = sum(x[0] << t for t, x in enumerate(labels))
    h = sum(x[1] << t for t, x in enumerate(labels))
    return l, h, tuple(x[2] for x, gt in zip(labels, g) if gt)


def root_and_terminal(base, e, g):
    e, g = bits(e), bits(g)
    require(len(e) == len(g), "inconsistent streams")
    em = sum(x << t for t, x in enumerate(e))
    gm = sum(x << t for t, x in enumerate(g))
    root = (0, gm, (1,) * sum(g))
    terminal = (em, ((1 << len(e)) - 1) ^ em,
                tuple((base - 1) * et for et, gt in zip(e, g) if gt))
    require(root != terminal, "root and terminal must be distinct")
    return root, terminal


def inverse_local(base, overflow, successor, x, xnext, first=False):
    """All predecessor block labels for fixed adjacent temporal ports."""
    if not (0 <= x <= 2 * base - 2 and 0 <= xnext <= 2 * base - 2):
        return ()
    if first and x == 0:
        return ()
    lp, hp, yp = successor
    h, r = divmod(x + hp, base)
    answers = []
    for l in (0, 1):
        actual_lp, d = divmod(x + l, base)
        if actual_lp != lp:
            continue
        if overflow:
            y = xnext - d
            if r == yp and 0 <= y < base:
                answers.append((l, h, y))
        elif xnext == d + r:
            answers.append((l, h, -1))
    return tuple(answers)


def check_column(base, g, source, target, column, first=False):
    g = bits(g)
    source, target = state(base, g, source), state(base, g, target)
    xs = word(base, column)
    require(len(xs) == len(g), "column has wrong period")
    for t, (old, new, gt) in enumerate(zip(blocks(g, source), blocks(g, target), g)):
        require(old in inverse_local(base, gt, new, xs[t], xs[(t + 1) % len(xs)], first),
                f"invalid spatial column at temporal phase {t}")
    return True


def inverse_columns(base, g, target, first=False, cap=1000000):
    """Explicit finite-port oracle; returns one column for every distinct cut.

    The suffix reachability sets are recomputed for each fixed initial port.
    Thus temporal closure is imposed before any projected predecessor is kept.
    This is a small-control oracle, not the research engine.
    """
    g = bits(g)
    labels = blocks(g, state(base, g, target))
    values = range(1 if first else 0, 2 * base - 1)
    arcs = []
    for gt, label in zip(g, labels):
        at_phase = {}
        for x in values:
            candidates = []
            for xn in values:
                candidates.extend((xn, z) for z in inverse_local(base, gt, label, x, xn, first))
            at_phase[x] = candidates
        arcs.append(at_phase)
    answers = {}
    for x0 in values:
        reachable = [set() for _ in range(len(g) + 1)]
        reachable[-1].add(x0)
        for t in range(len(g) - 1, -1, -1):
            reachable[t] = {x for x in values if any(xn in reachable[t + 1]
                                                   for xn, _ in arcs[t][x])}
        if x0 not in reachable[0]:
            continue

        def walk(t, x, previous, column):
            if t == len(g):
                require(x == x0, "open temporal trajectory")
                cut = pack(g, previous)
                if cut not in answers:
                    answers[cut] = tuple(column)
                    require(len(answers) <= cap, "independent inverse control cap")
                return
            for xn, label in arcs[t][x]:
                if xn in reachable[t + 1]:
                    walk(t + 1, xn, previous + [label], column + [x])

        walk(0, x0, [], [])
    return answers


def cuts_from_rows(base, e, g, rows):
    """Reconstruct every carry cut from actual whole exterior words."""
    e, g = bits(e), bits(g)
    require(len(e) == len(g) == len(rows), "row/driver count mismatch")
    rows = [word(base, row) for row in rows]
    width = len(rows[0])
    require(width > 0 and all(len(row) == width and row[0] > 0 for row in rows),
            "expected nonempty equal-width positive-FIRST exteriors")
    left, high, reverse_digits = [], [], []
    for t, row in enumerate(rows):
        ls = [0]
        for x in row:
            ls.append((x + ls[-1]) // base)
        hs, rs = [0] * (width + 1), [0] * width
        hs[-1] = 1 - e[t]
        for j in range(width - 1, -1, -1):
            hs[j], rs[j] = divmod(row[j] + hs[j + 1], base)
        require(ls[-1] == e[t] and hs[0] == g[t], "wrong exterior driver")
        et, gt, raw = exterior_step(base, row)
        require((et, gt) == (e[t], g[t]) and
                raw == rows[(t + 1) % len(rows)] + [base - 1] * g[t],
                "whole-word exterior edge mismatch")
        left.append(ls)
        high.append(hs)
        reverse_digits.append(rs)
    cuts = []
    for j in range(width + 1):
        cuts.append((sum(left[t][j] << t for t in range(len(g))),
                     sum(high[t][j] << t for t in range(len(g))),
                     tuple(1 if j == 0 else reverse_digits[t][j - 1]
                           for t, gt in enumerate(g) if gt)))
    root, terminal = root_and_terminal(base, e, g)
    require((cuts[0], cuts[-1]) == (root, terminal), "wrong spatial endpoints")
    columns = list(zip(*rows))
    for j, column in enumerate(columns):
        check_column(base, g, cuts[j], cuts[j + 1], column, first=j == 0)
    check_column(base, g, terminal, terminal, [base - 1] * len(g))
    return cuts, columns


def strict_cycle(base, edges):
    require(bool(edges), "empty certificate")
    for edge in edges:
        require(isinstance(edge, (tuple, list)) and len(edge) == 6, "malformed edge")
        for coefficients in edge[:4]:
            word(base, coefficients)
        require(nat(edge[4]) and nat(edge[5]), "trim is not natural")
    require(mirror.cycleOK(base, edges, edges[0][0], edges[0][1]), "mirror cycleOK rejected")
    return True


def join_center(base, e, g, rows, centers, trims):
    cuts_from_rows(base, e, g, rows)
    period = len(rows)
    require(period == len(centers) == len(trims), "join period mismatch")
    edges = [(list(rows[t]), list(centers[t]), list(rows[(t + 1) % period]),
              list(centers[(t + 1) % period]), int(g[t]), int(trims[t]))
             for t in range(period)]
    strict_cycle(base, edges)
    return edges


def padded_rows(base, original, extra=0):
    require(nat(extra), "negative padding")
    width = max(1, max(map(len, original))) + extra
    return [list(row) + [base - 1] * (width - len(row)) for row in original]


def canonical_exterior(base, initial, period):
    rows, es, gs, us = [], [], [], []
    row = word(base, initial)
    for _ in range(period):
        rows.append(row)
        e, g, nxt = exterior_step(base, row)
        u = 0
        while nxt and nxt[-1] == base - 1:
            nxt.pop()
            u += 1
        es.append(e)
        gs.append(g)
        us.append(u)
        row = nxt
    require(row == list(initial), "canonical exterior fails to close")
    return tuple(es), tuple(gs), rows, us


def baseline_controls():
    summaries, fixtures = [], []
    known = mirror._lean_certs()
    require({b for b, _ in known} == {2, 4, 8, 11, 16, 17, 26, 32},
            "known positive fixture set changed")
    column_checks = 0
    for base, edges in known:
        strict_cycle(base, edges)
        e = tuple(mirror.e1(base, edge[0]) for edge in edges)
        g = tuple(mirror.gam(base, edge[0], edge[1]) for edge in edges)
        centers = [edge[1] for edge in edges]
        trims = [edge[5] for edge in edges]
        require(center_cycle(base, e, g, trims, centers[0]) == centers,
                "known center replay mismatch")
        for extra in (0, 1, 3):
            rows = padded_rows(base, [edge[0] for edge in edges], extra)
            cuts, columns = cuts_from_rows(base, e, g, rows)
            join_center(base, e, g, rows, centers, trims)
            column_checks += len(columns)
            if extra == 0:
                fixtures.append((base, e, g, rows, cuts, columns))
        summaries.append({"base": base, "period": len(edges),
                          "width": len(fixtures[-1][3][0]), "padded_cycles": 3})
    decimal = []
    for initial, period, estr, gstr in (
            (B11, 11, "10100110011", "11100010000"),
            (B12, 12, "100101011010", "100010001000")):
        e, g, rows, us = canonical_exterior(10, initial, period)
        require((e, g) == (bits(estr), bits(gstr)), "decimal exterior stream mismatch")
        for extra in (0, 1, 3):
            padded = padded_rows(10, rows, extra)
            cuts, columns = cuts_from_rows(10, e, g, padded)
            column_checks += len(columns)
            if extra == 0:
                fixtures.append((10, e, g, padded, cuts, columns))
        decimal.append({"period": period, "widths": list(map(len, rows)),
                        "natural_trims": us, "fixed_width": len(fixtures[-1][3][0]),
                        "status": "EXTERIOR_ONLY"})
    centers = center_cycle(10, P24_E, P24_G, bits(P24_V), P24_C)
    require(all(centers[t + 12] == [18 - x for x in centers[t]] for t in range(12)),
            "C24 half-period complement mismatch")
    return {"known_complete_certificates": summaries, "decimal_exteriors": decimal,
            "spatial_columns_checked": column_checks,
            "priority_center": {"period": 24, "sum_g": 8, "sum_v": 4,
                                "widths": list(map(len, centers)),
                                "status": "CENTER_ONLY"}}, fixtures


def boundary_controls():
    count = 0
    # Complete local forward/inverse equivalence, including coefficient 0 and 2b-2.
    for base in range(2, 13):
        for overflow in (0, 1):
            expected = defaultdict(set)
            for l in (0, 1):
                for hp in (0, 1):
                    for x in range(2 * base - 1):
                        lp, d = divmod(x + l, base)
                        h, r = divmod(x + hp, base)
                        for y in (range(base) if overflow else (-1,)):
                            xn = d + (y if overflow else r)
                            target = (lp, hp, r if overflow else -1)
                            expected[(target, x, xn)].add((l, h, y))
            for (target, x, xn), predecessors in expected.items():
                require(set(inverse_local(base, overflow, target, x, xn)) == predecessors,
                        "local inverse mismatch")
                first = set(inverse_local(base, overflow, target, x, xn, first=True))
                require(first == (predecessors if x else set()), "FIRST mismatch")
                count += 1
    # A g=0 all-zero temporal column is valid inside, but cannot be FIRST.
    check_column(10, (0,), (0, 0, ()), (0, 0, ()), (0,))
    try:
        check_column(10, (0,), (0, 0, ()), (0, 0, ()), (0,), first=True)
    except ValueError:
        pass
    else:
        raise AssertionError("zero FIRST was admitted")
    # An open local step x=1 -> 2 must not become a period-one column.
    require(inverse_local(10, 0, (0, 0, -1), 1, 2), "open-path control is invalid")
    require((0, 0, ()) not in inverse_columns(10, (0,), (0, 0, ()), first=True),
            "temporal closure was dropped")
    invalid = 0
    for coeff in (-1, 19, True, 1.5):
        try:
            word(10, [coeff])
        except ValueError:
            invalid += 1
    require(invalid == 4, "strict coefficient guards failed")
    rng = random.Random(1102424)
    padding_checks = 0
    for base in range(2, 33):
        for length in range(17):
            row = [rng.randrange(2 * base - 1) for _ in range(length)]
            if row:
                row[0] = rng.randrange(1, 2 * base - 1)
            e, g, raw = exterior_step(base, row)
            for amount in (0, 1, 2, 7):
                ep, gp, padded_raw = exterior_step(base, row + [base - 1] * amount)
                require((ep, gp) == (e, g) and padded_raw == raw + [base - 1] * amount,
                        "neutral suffix covariance failed")
                padding_checks += 1
    return {"local_inverse_cases": count, "boundary_counterexamples": 3,
            "strict_bad_coefficient_rejections": invalid,
            "suffix_padding_covariance_checks": padding_checks}


def candidate_from_witness(witness):
    require(isinstance(witness, dict), "witness is not an object")
    base = witness.get("base")
    e, g = bits(witness.get("e", "")), bits(witness.get("g", ""))
    rows = witness.get("B_t", witness.get("B"))
    require(isinstance(rows, list), "missing full exterior rows")
    cuts, _ = cuts_from_rows(base, e, g, rows)
    if "width" in witness:
        require(type(witness["width"]) is int and witness["width"] == len(rows[0]),
                "witness width mismatch")
    if "u" in witness:
        require(witness["u"] == list(g) and all(type(x) is int for x in witness["u"]),
                "witness does not use fixed-width u=g")
    result = {"status": "EXTERIOR_ONLY", "base": base, "period": len(e),
              "width": len(rows[0]), "cuts": len(cuts)}
    if base == 10 and len(e) % 24 == 0:
        repetitions = len(e) // 24
        if e == bits(P24_E * repetitions) and g == bits(P24_G * repetitions):
            v = bits(P24_V * repetitions)
            centers = center_cycle(base, e, g, v, P24_C)
            edges = join_center(base, e, g, rows, centers, v)
            result = {"status": "CANDIDATE", "verification": "COMPUTED_PYTHON_MIRROR_ONLY",
                      "base": 10, "edges": edges, "B": rows[0], "C": P24_C}
    return result


def search_output(stdout, returncode, base, e, g):
    """A valid full positive survives a later cap or damaged terminal record.

    Absence of a complete terminal record, nonzero exit, malformed output, or
    incomplete image is never classified as an exhaustion result.
    """
    records, malformed = [], False
    for line in stdout.splitlines():
        if not line.strip():
            continue
        try:
            record = json.loads(line)
            require(isinstance(record, dict), "search output is not an object")
            records.append(record)
        except (ValueError, TypeError):
            malformed = True
    positive = []
    for record in records:
        if "B_t" not in record and "B" not in record:
            continue
        try:
            require(record.get("base") == base and bits(record.get("e", "")) == bits(e)
                    and bits(record.get("g", "")) == bits(g), "witness driver mismatch")
            result = candidate_from_witness(record)
        except (ValueError, TypeError):
            malformed = True
            continue
        positive.append((record, result))
    if positive:
        record, result = next((p for p in positive if p[1]["status"] == "CANDIDATE"), positive[0])
        return {"status": "CANDIDATE" if result["status"] == "CANDIDATE" else "EXTERIOR_ACCEPT",
                "witness": record, "replay": result,
                "complete_output": not malformed and returncode == 0}
    if records and not malformed and returncode == 0:
        final = records[-1]
        complete = final.get("image_complete", final.get("complete", False)) is True
        try:
            if (final.get("status") == "EXHAUSTED" and complete and final.get("base") == base
                    and bits(final.get("e", "")) == bits(e) and bits(final.get("g", "")) == bits(g)):
                return {"status": "EXHAUSTED", "terminal": final}
        except (ValueError, TypeError):
            malformed = True
    return {"status": "UNDECIDED", "malformed": malformed, "returncode": returncode}


def command_prefix(program):
    program = Path(program).resolve()
    return [sys.executable, str(program)] if program.suffix == ".py" else [str(program)]


def engine_run(program, base, e, g, flags, seconds, targets=None):
    estr, gstr = "".join(map(str, e)), "".join(map(str, g))
    command = command_prefix(program) + [str(base), estr, gstr] + list(flags) + ["--seconds", str(seconds)]
    return subprocess.run(command, input=None if targets is None else json.dumps(targets),
                          text=True, capture_output=True, timeout=seconds + 5, check=False)


def engine_controls(programs, fixtures, seconds):
    inverse_queries = inverse_states_count = memberships = positive_words = full_cycles = 0
    summaries = []
    source_certificates = {base: edges for base, edges in mirror._lean_certs()}
    for base, e, g, rows, cuts, columns in fixtures:
        targets = sorted(set(cuts[1:]))
        expected = {target: inverse_columns(base, g, target) for target in targets}
        for j, column in enumerate(columns):
            require(cuts[j] in expected[cuts[j + 1]], "known path missing from inverse oracle")
            check_column(base, g, cuts[j], cuts[j + 1], column, first=j == 0)
            memberships += 1
        for program in programs:
            for target in targets:
                process = engine_run(program, base, e, g, ["--preimage"], seconds, [target])
                require(process.returncode == 0, "incomplete inverse export: " + process.stdout[:300])
                exported = json.loads(process.stdout)
                require(isinstance(exported, list), "inverse export is not a complete array")
                actual = {state(base, g, row) for row in exported}
                require(len(actual) == len(exported), "duplicate inverse export")
                require(actual == set(expected[target]), "complete singleton-preimage mismatch")
                inverse_queries += 1
                inverse_states_count += len(actual)
        # The symbolic engine can reach every supplied known witness width.
        # The explicit oracle's small positive search is checked separately.
        if programs:
            process = engine_run(programs[0], base, e, g,
                                 ["--layers", str(len(columns) - 1)], seconds)
            checked = search_output(process.stdout, process.returncode, base, e, g)
            require(checked["status"] == "EXTERIOR_ACCEPT", "known positive search failed: " + process.stdout[-500:])
            witness_rows = checked["witness"].get("B_t", checked["witness"].get("B"))
            positive_words += 1
            if base in source_certificates:
                edges = source_certificates[base]
                join_center(base, e, g, witness_rows, [edge[1] for edge in edges],
                            [edge[5] for edge in edges])
                full_cycles += 1
            summaries.append({"base": base, "period": len(e),
                              "witness_width": len(witness_rows[0]), "inverse_targets": len(targets)})
    return {"engine_singleton_preimage_queries": inverse_queries,
            "engine_inverse_states_compared": inverse_states_count,
            "known_path_memberships": memberships,
            "engine_positive_exterior_witnesses": positive_words,
            "engine_witnesses_joined_to_known_centers": full_cycles,
            "engine_positive_details": summaries}


def parser_controls(fixtures):
    base, e, g, rows, _, _ = fixtures[0]
    witness = {"type": "WITNESS", "base": base, "e": "".join(map(str, e)),
               "g": "".join(map(str, g)), "B_t": rows, "width": len(rows[0]), "u": list(g)}
    cap = {"type": "RESULT", "status": "UNDECIDED", "reason": "node_cap"}
    count = 0
    for tail, code in ((cap, 2), (None, 0), ("truncated {", -9)):
        suffix = "" if tail is None else "\n" + (json.dumps(tail) if isinstance(tail, dict) else tail)
        result = search_output(json.dumps(witness) + suffix, code, base, e, g)
        require(result["status"] == "EXTERIOR_ACCEPT", "valid partial positive lost")
        count += 1
    complete = {"type": "RESULT", "status": "EXHAUSTED", "base": base,
                "e": witness["e"], "g": witness["g"], "image_complete": True}
    for output, code in (("", 0), (json.dumps(cap), 2), (json.dumps(complete), -9),
                         (json.dumps(dict(complete, image_complete=False)), 0),
                         (json.dumps(complete) + "\ntruncated {", 0)):
        require(search_output(output, code, base, e, g)["status"] == "UNDECIDED",
                "incomplete or failed search misclassified as negative")
        count += 1
    damaged = json.loads(json.dumps(witness))
    damaged["B_t"][0][0] = -1
    require(search_output(json.dumps(damaged), 0, base, e, g)["status"] == "UNDECIDED",
            "invalid witness admitted")
    require(search_output(json.dumps(complete), 0, base, e, g)["status"] == "EXHAUSTED",
            "well-formed complete terminal misclassified")
    return {"search_status_controls": count + 2}


def guard_controls(program, seconds):
    e, g = bits(P24_E), bits(P24_G)
    probes = []
    for flags, targets, cap_seconds in ((["--layers", "0"], None, seconds),
                                        (["--operations", "1"], None, seconds),
                                        (["--nodes", "2"], None, seconds),
                                        ([], None, 1),
                                        (["--memory-mib", "64"], None, seconds),
                                        (["--export-layer", "1", "--export-cap", "1"], None, seconds),
                                        (["--preimage"], [[0, 0, [-1] * sum(g)]], seconds)):
        process = engine_run(program, 10, e, g, flags, cap_seconds, targets)
        result = search_output(process.stdout, process.returncode, 10, e, g)
        require(process.returncode == 2 and result["status"] == "UNDECIDED",
                "cap or malformed input reported as completed search")
        terminal = json.loads(process.stdout.splitlines()[-1])
        probes.append({"flags": flags, "seconds_cap": cap_seconds,
                       "reason": terminal.get("reason"), "returncode": process.returncode})
    return {"engine_guard_probes": probes}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--witness-json", type=Path,
                        help="independently replay one complete JSON WITNESS object")
    parser.add_argument("--search-output", type=Path, help="inspect P24 JSON-lines output, preserving partial positives")
    parser.add_argument("--search-returncode", type=int, default=0)
    parser.add_argument("--mdd", type=Path, help="primary reverse MDD executable")
    parser.add_argument("--reference", type=Path, help="optional independent explicit inverse program")
    parser.add_argument("--seconds", type=int, default=45, help="maximum seconds for each engine subprocess")
    parser.add_argument("--guards", action="store_true")
    args = parser.parse_args()
    require(1 <= args.seconds <= 1500, "invalid subprocess time budget")
    require(not args.reference or args.mdd, "reference comparison requires primary --mdd")
    if args.witness_json:
        result = candidate_from_witness(json.loads(args.witness_json.read_text()))
        print(json.dumps(result, separators=(",", ":")), flush=True)
        return 0
    if args.search_output:
        result = search_output(args.search_output.read_text(), args.search_returncode, 10, P24_E, P24_G)
        print(json.dumps(result, separators=(",", ":")), flush=True)
        return 2 if result["status"] == "UNDECIDED" else 0
    start = time.monotonic()
    result, fixtures = baseline_controls()
    result.update(boundary_controls())
    result.update(parser_controls(fixtures))
    if args.mdd:
        programs = [args.mdd] + ([args.reference] if args.reference else [])
        result.update(engine_controls(programs, fixtures, args.seconds))
        if args.guards:
            result.update(guard_controls(args.mdd, args.seconds))
    result.update(status="PASS", seconds=time.monotonic() - start)
    print(json.dumps(result, sort_keys=True), flush=True)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (ValueError, TypeError, AssertionError, OSError, subprocess.SubprocessError) as exc:
        print(json.dumps({"status": "ERROR", "reason": str(exc)}), flush=True)
        raise SystemExit(2)
