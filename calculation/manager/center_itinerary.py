#!/usr/bin/env python3
"""Compile a frozen symmetric A120 center itinerary to exact affine constraints.

The external entry/overflow bits and center trims are supplied, not realized
by this tool. All phases share one symbolic initial center and one base, so
every temporal seam is joined. Equalities may yield a rational contradiction;
absence of that contradiction says nothing about bounded integer feasibility.
"""
from __future__ import annotations

import argparse
from fractions import Fraction
import json
from pathlib import Path
import time

MAX_PHASES = 128
MAX_WIDTH = 510
MAX_TOTAL_WIDTH = 4096
MAX_VARIABLES = 256
MAX_ROWS = 20000
MAX_BITS = 4096
# Below Python's default 4300-decimal-digit serialization ceiling. The
# independent checker accepts the larger schema budget of 16384 bits.
MAX_PROOF_BITS = 12000
MAX_FILE_BYTES = 64 * 1024**2


class InvalidInput(ValueError):
    pass


class ResourceLimit(RuntimeError):
    pass


def require(condition, message):
    if not condition:
        raise InvalidInput(message)


def integer(value, label, minimum=None):
    require(type(value) is int, label + " must be an integer, not bool/float")
    require(minimum is None or value >= minimum, label + " below allowed minimum")
    if value.bit_length() > MAX_BITS:
        raise ResourceLimit(label + " exceeds integer-bit budget")
    return value


def validate_itinerary(itinerary):
    require(type(itinerary) is dict, "itinerary must be an object")
    require(itinerary.get("format") == "p196-center-itinerary-v1", "itinerary format")
    require(itinerary.get("symmetry") == "required", "symmetric centers required")
    phases = itinerary.get("phases")
    require(type(phases) is list and phases, "nonempty phase list required")
    if len(phases) > MAX_PHASES:
        raise ResourceLimit("phase limit")
    total = 0
    for t, phase in enumerate(phases):
        require(type(phase) is dict, "phase must be an object")
        m = integer(phase.get("width"), "width", 1)
        g = integer(phase.get("overflow"), "overflow", 0)
        v = integer(phase.get("trim"), "trim", 0)
        require(g in (0, 1), "overflow must be binary")
        require(2 * v < m + g, "trim must leave a nonempty center")
        if m > MAX_WIDTH:
            raise ResourceLimit("width limit")
        total += m
        carry = phase.get("carry")
        require(type(carry) is list and len(carry) == m + 1, "carry word width")
        require(all(type(c) is int and c in (0, 1) for c in carry), "binary carry word required")
        require(carry[-1] == 1 - carry[0], "center entering/exiting carry must flip")
    if total > MAX_TOTAL_WIDTH:
        raise ResourceLimit("total center-width limit")
    for t, phase in enumerate(phases):
        require(phase["width"] + phase["overflow"] - 2 * phase["trim"] ==
                phases[(t + 1) % len(phases)]["width"], "cyclic width/trim mismatch")
    return phases


def compile_system(itinerary, target_base):
    """Return rows with dot(coefficients, variables)=rhs (or <= for bounds).

    Initial symmetric half-center variables are followed by symbolic base.
    An expression is a dense variable vector followed by its constant term.
    The explicit base row fixes the requested base. This parameterization is
    exact for integer centers, including zero coefficients and nonmaximal trims.
    """
    phases = validate_itinerary(itinerary)
    integer(target_base, "target base", 2)
    m0 = phases[0]["width"]
    half = (m0 + 1) // 2
    count = half + 1
    if count > MAX_VARIABLES:
        raise ResourceLimit("variable limit")
    variables = [f"C0_{j}" for j in range(half)] + ["base"]
    equalities, inequalities = [], []

    def row(expression, label, origin, inequality=False):
        if any(abs(x).bit_length() > MAX_BITS for x in expression):
            raise ResourceLimit("compiled row bit budget")
        collection = inequalities if inequality else equalities
        if len(collection) >= MAX_ROWS:
            raise ResourceLimit("compiled row count")
        origin = dict(origin)
        origin["frozen_prefix_length"] = (origin["phase"] + 1 if "phase" in origin else
                                          0 if origin["kind"] == "target_base" else len(phases))
        collection.append({"label": label, "coefficients": expression[:-1],
                           "rhs": -expression[-1], "origin": origin})

    initial = []
    for j in range(m0):
        expression = [0] * (count + 1)
        expression[min(j, m0 - 1 - j)] = 1
        initial.append(expression)
    center = [x[:] for x in initial]
    # Integer coefficient bounds plus normalized digit bounds make the chosen
    # carry words actual base-b normalization, not unguarded affine substitutions.
    for t, phase in enumerate(phases):
        carry = phase["carry"]
        digits = []
        for j, coefficient in enumerate(center):
            row([-x for x in coefficient], f"p{t}.c{j}.nonnegative",
                {"kind": "coefficient_lower", "phase": t, "index": j}, True)
            upper = coefficient[:]
            upper[half] -= 2
            upper[-1] += 2
            row(upper, f"p{t}.c{j}.bounded",
                {"kind": "coefficient_upper", "phase": t, "index": j}, True)
            digit = coefficient[:]
            digit[half] -= carry[j + 1]
            digit[-1] += carry[j]
            row([-x for x in digit], f"p{t}.d{j}.nonnegative",
                {"kind": "digit_lower", "phase": t, "index": j}, True)
            upper = digit[:]
            upper[half] -= 1
            upper[-1] += 1
            row(upper, f"p{t}.d{j}.bounded",
                {"kind": "digit_upper", "phase": t, "index": j}, True)
            digits.append(digit)
        if phase["overflow"]:
            digit = [0] * (count + 1)
            digit[half], digit[-1] = carry[0], -carry[0]
            digits.append(digit)
        raw = [[a + b for a, b in zip(x, y)] for x, y in zip(digits, digits[::-1])]
        trim = phase["trim"]
        for side, indices in (("left", range(trim)), ("right", range(len(raw) - trim, len(raw)))):
            for j in indices:
                neutral = raw[j][:]
                neutral[half] -= 1
                neutral[-1] += 1
                row(neutral, f"p{t}.trim.{side}.{j}",
                    {"kind": "neutral_trim", "phase": t, "side": side, "index": j})
        center = raw[trim:len(raw) - trim] if trim else raw
    for j, (final, start) in enumerate(zip(center, initial)):
        row([a - b for a, b in zip(final, start)], f"closure.{j}",
            {"kind": "cycle_closure", "index": j})
    base_row = [0] * (count + 1)
    base_row[half], base_row[-1] = 1, -target_base
    row(base_row, "target_base", {"kind": "target_base"})
    frozen = {"format": "p196-center-itinerary-v1", "symmetry": "required",
              "phases": [{key: (list(p[key]) if key == "carry" else p[key])
                          for key in ("width", "carry", "overflow", "trim")} for p in phases]}
    return {"format": "p196-center-affine-v1", "variables": variables,
            "equalities": equalities, "inequalities": inequalities,
            "itinerary": frozen, "target_base": target_base}


def rational_contradiction(system, max_operations=5000000):
    """Exact elimination, tracking explicit rational combinations of input rows.

    Only equalities participate. A missing contradiction is deliberately not
    called SAT. Time/bit/operation guards return an undecided resource status.
    """
    integer(max_operations, "operation budget", 1)
    rows = system["equalities"]
    n = len(system["variables"])
    pivots = {}
    operations = 0
    started = time.monotonic()

    def guard(values):
        nonlocal operations
        operations += len(values)
        if operations > max_operations:
            raise ResourceLimit("elimination operation budget")
        if any(max(x.numerator.bit_length(), x.denominator.bit_length()) > MAX_PROOF_BITS
               for x in values):
            raise ResourceLimit("elimination fraction-bit budget")

    try:
        for i, row in enumerate(rows):
            work = list(map(Fraction, row["coefficients"] + [row["rhs"]]))
            combination = {i: Fraction(1)}
            for col in range(n):
                factor = work[col]
                if not factor:
                    continue
                if col not in pivots:
                    work = [x / factor for x in work]
                    combination = {j: x / factor for j, x in combination.items()}
                    guard(work + list(combination.values()))
                    pivots[col] = work, combination
                    break
                pivot, weights = pivots[col]
                work = [a - factor * b for a, b in zip(work, pivot)]
                for j, weight in weights.items():
                    combination[j] = combination.get(j, Fraction(0)) - factor * weight
                    if not combination[j]:
                        del combination[j]
                guard(work + list(combination.values()))
            else:
                if work[-1]:
                    weights = [combination.get(j, Fraction(0)) / work[-1] for j in range(len(rows))]
                    guard(weights)
                    proof = {"format": "p196-rational-row-contradiction-v1",
                             "multipliers": [[w.numerator, w.denominator] for w in weights]}
                    return {"status": "RATIONAL_EQUALITY_INCONSISTENT", "rank_so_far": len(pivots),
                            "operations": operations, "seconds": time.monotonic() - started,
                            "certificate": proof,
                            "nonzero_row_labels": [rows[j]["label"] for j, w in enumerate(weights) if w]}
        return {"status": "NO_RATIONAL_EQUALITY_CONTRADICTION", "rank": len(pivots),
                "operations": operations, "seconds": time.monotonic() - started,
                "meaning": "No bounded/integer feasibility or center existence conclusion."}
    except ResourceLimit as exc:
        return {"status": "RESOURCE_LIMIT_UNDECIDED", "reason": str(exc),
                "operations": operations, "seconds": time.monotonic() - started}


def load_json(path):
    with Path(path).open("rb") as stream:
        data = stream.read(MAX_FILE_BYTES + 1)
    if len(data) > MAX_FILE_BYTES:
        raise ResourceLimit("input file budget")
    def invalid_constant(text):
        raise InvalidInput("non-JSON constant: " + text)
    def unique_keys(pairs):
        result = {}
        for key, value in pairs:
            require(key not in result, "duplicate JSON key: " + key)
            result[key] = value
        return result
    return json.loads(data, parse_constant=invalid_constant, object_pairs_hook=unique_keys)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("itinerary", type=Path)
    parser.add_argument("--base", type=int, required=True)
    parser.add_argument("--system", type=Path, required=True)
    parser.add_argument("--proof", type=Path)
    parser.add_argument("--max-operations", type=int, default=5000000)
    args = parser.parse_args()
    try:
        input_path = args.itinerary.resolve()
        system_path = args.system.resolve()
        proof_path = args.proof.resolve() if args.proof is not None else None
        require(input_path != system_path, "input and system paths must differ")
        require(proof_path not in (input_path, system_path), "proof path must be separate")
        if args.proof is not None:
            # Invalidate any prior proof before parsing/compilation. Even an
            # early malformed-input/resource exit must not leave a stale proof.
            args.proof.write_text(json.dumps({"format": "p196-no-contradiction-certificate",
                "status": "PENDING_OR_FAILED"}) + "\n")
        data = load_json(args.itinerary)
        itinerary = data.get("itinerary", data) if type(data) is dict else data
        system = compile_system(itinerary, args.base)
        result = rational_contradiction(system, args.max_operations)
        args.system.write_text(json.dumps(system, indent=2) + "\n")
        proof = result.pop("certificate", None)
        if args.proof is not None:
            # Always replace a previous artifact, including a non-proof marker
            # when this run has no certificate. Never leave a stale proof behind.
            args.proof.write_text(json.dumps(proof if proof is not None else
                {"format": "p196-no-contradiction-certificate", "status": result["status"]}, indent=2) + "\n")
        result["proof_written"] = proof is not None and args.proof is not None
        print(json.dumps(result, sort_keys=True))
        return 3 if result["status"] == "RESOURCE_LIMIT_UNDECIDED" else 0
    except ResourceLimit as exc:
        print(json.dumps({"status": "RESOURCE_LIMIT_UNDECIDED", "reason": str(exc)}))
        return 3
    except (InvalidInput, ValueError, TypeError, KeyError, OSError) as exc:
        print(json.dumps({"status": "INVALID_INPUT", "reason": str(exc)}))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
