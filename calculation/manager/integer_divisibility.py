#!/usr/bin/env python3
"""Produce bounded integer row-combination divisibility certificates.

Only supplied equality rows participate. An explicit integer combination
whose coefficient gcd does not divide its RHS excludes every integer
assignment. This search is incomplete: no certificate is not feasibility.
Itinerary compilation and independent certificate checking are separate.
"""
from __future__ import annotations

import argparse
import json
from math import gcd
from pathlib import Path

from row_contradiction_check import (
    InvalidInput, UnsupportedInput, integer, read_json, validate_system,
)

MAX_OPERATIONS = 5_000_000
# Below Python's default integer-to-decimal serialization ceiling. The
# independent verifier allows 16384 bits for supplied proof integers.
MAX_INTERMEDIATE_BITS = 12_000


def find_certificate(system, max_operations=MAX_OPERATIONS):
    """Try base-first fraction-free elimination, retaining integer weights.

    Pivot cancellation uses p/g and a/g, where g=gcd(p,a). There is no
    division of an equation by its coefficient gcd: that would in general
    lose the required integer combination of original rows. The first
    intermediate divisibility contradiction is returned, with all weights.
    """
    validate_system(system)
    integer(max_operations, "operation budget", 32)
    if max_operations < 1:
        raise InvalidInput("operation budget must be positive")
    if max_operations > MAX_OPERATIONS:
        raise UnsupportedInput("requested operation budget exceeds producer cap")
    rows, variables = system["equalities"], system["variables"]
    n = len(variables)
    pivots = {}
    operations = rows_started = zero_conflicts = 0

    def charge(count):
        nonlocal operations
        operations += count
        if operations > max_operations:
            raise UnsupportedInput("producer charged-entry budget exceeded")

    def guard(values):
        if any(value.bit_length() > MAX_INTERMEDIATE_BITS for value in values):
            raise UnsupportedInput("producer intermediate integer-bit budget exceeded")

    def summary(status):
        return {"status": status, "operations": operations,
                "rows_started": rows_started, "pivot_count": len(pivots),
                "zero_coefficient_nonzero_rhs_rows_seen": zero_conflicts,
                "method": "base-first-fraction-free-v1"}

    def certificate(work, weights):
        charge(n)
        divisor = 0
        for coefficient in work[:-1]:
            divisor = gcd(divisor, coefficient)
        if divisor < 2 or work[-1] % divisor == 0:
            return None
        result = summary("INTEGER_EQUALITY_DIVISIBILITY_CONTRADICTION")
        result["certificate"] = {
            "format": "p196-integer-row-divisibility-v1",
            "multipliers": [weights.get(i, 0) for i in range(len(rows))],
            "combined_coefficients": work[:-1], "combined_rhs": work[-1],
            "coefficient_gcd": divisor,
        }
        result["nonzero_row_indices"] = sorted(weights)
        result["nonzero_row_labels"] = [rows[i]["label"] for i in sorted(weights)]
        result["scope"] = "No integer solution to the supplied equalities."
        return result

    try:
        order, columns = list(range(len(rows))), list(range(n))
        if "base" in variables:
            base = variables.index("base")
            columns = [base] + [j for j in columns if j != base]
            # This is only an ordering heuristic. The row itself, not its
            # label/origin metadata, must literally say base=target_base.
            for i in reversed(order):
                row = rows[i]
                charge(n)
                unit = row["coefficients"][base]
                if unit in (-1, 1) and row["rhs"] == unit * system["target_base"] and all(
                        not a for j, a in enumerate(row["coefficients"]) if j != base):
                    order = [i] + [j for j in order if j != i]
                    break
        for i in order:
            rows_started += 1
            work = rows[i]["coefficients"][:] + [rows[i]["rhs"]]
            weights = {i: 1}
            guard(work)
            found = certificate(work, weights)
            if found is not None:
                return found
            for column in columns:
                a = work[column]
                if not a:
                    continue
                if column not in pivots:
                    pivots[column] = work, weights
                    break
                pivot, pivot_weights = pivots[column]
                p = pivot[column]
                common = gcd(p, a)
                left, right = p // common, a // common
                charge(n + 1 + len(weights) + len(pivot_weights))
                work = [left * x - right * y for x, y in zip(work, pivot)]
                weights = {j: left * weight for j, weight in weights.items()}
                for j, weight in pivot_weights.items():
                    weights[j] = weights.get(j, 0) - right * weight
                    if not weights[j]:
                        del weights[j]
                guard(work)
                guard(weights.values())
                found = certificate(work, weights)
                if found is not None:
                    return found
            else:
                if work[-1]:
                    # A rational contradiction is intentionally not converted
                    # to this gcd>=2 proof format. Use the rational checker.
                    zero_conflicts += 1
        result = summary("NO_DIVISIBILITY_CERTIFICATE_FOUND")
        result["meaning"] = "No rational, integer, bounded, or center-feasibility conclusion."
        return result
    except UnsupportedInput as error:
        result = summary("RESOURCE_LIMIT_UNDECIDED")
        result["reason"] = str(error)
        return result


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("system", type=Path)
    parser.add_argument("--proof", type=Path, required=True)
    parser.add_argument("--max-operations", type=int, default=MAX_OPERATIONS)
    args = parser.parse_args(argv)
    try:
        if args.system.resolve() == args.proof.resolve() or (
                args.system.exists() and args.proof.exists() and args.system.samefile(args.proof)):
            raise InvalidInput("system and proof paths must differ")
        # Invalidate a previous proof before input parsing or computation.
        args.proof.write_text(json.dumps({"format": "p196-no-divisibility-certificate",
                                         "status": "PENDING_OR_FAILED"}) + "\n")
        result = find_certificate(read_json(args.system), args.max_operations)
        proof = result.pop("certificate", None)
        args.proof.write_text(json.dumps(proof if proof is not None else
            {"format": "p196-no-divisibility-certificate", "status": result["status"]}, indent=2) + "\n")
        result["proof_written"] = proof is not None
        print(json.dumps(result, sort_keys=True))
        return 3 if result["status"] == "RESOURCE_LIMIT_UNDECIDED" else 0
    except UnsupportedInput as error:
        print(json.dumps({"status": "RESOURCE_LIMIT_UNDECIDED", "reason": str(error)}))
        return 3
    except (InvalidInput, OSError, UnicodeError, ValueError, RecursionError) as error:
        print(json.dumps({"status": "INVALID_INPUT", "reason": str(error)}))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
