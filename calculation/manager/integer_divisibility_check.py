#!/usr/bin/env python3
"""Independently verify an integer row-combination divisibility obstruction.

The input rows use the existing center-affine schema. This module imports only
the independently authored row validator, never the itinerary compiler or proof
producer. It certifies the supplied equalities, not their external provenance.
"""

import argparse
import json
from math import gcd
from pathlib import Path
import sys

from row_contradiction_check import (
    InvalidInput, UnsupportedInput, MAX_ACCUMULATOR_BITS, MAX_ADDITIONS,
    MAX_PROOF_BITS, integer, read_json, validate_system,
)


def verify(system, certificate):
    validate_system(system)
    if type(certificate) is not dict or certificate.get("format") != "p196-integer-row-divisibility-v1":
        raise InvalidInput("unsupported integer divisibility format")
    rows = system["equalities"]
    weights = certificate.get("multipliers")
    if type(weights) is not list or len(weights) != len(rows):
        raise InvalidInput("one integer multiplier is required for every equality")
    for i, weight in enumerate(weights):
        integer(weight, f"multiplier {i}", MAX_PROOF_BITS)
    declared = certificate.get("combined_coefficients")
    n = len(system["variables"])
    if type(declared) is not list or len(declared) != n:
        raise InvalidInput("combined coefficient dimension mismatch")
    for i, coefficient in enumerate(declared):
        integer(coefficient, f"combined coefficient {i}", MAX_PROOF_BITS)
    declared_rhs = integer(certificate.get("combined_rhs"), "combined_rhs", MAX_PROOF_BITS)
    declared_gcd = integer(certificate.get("coefficient_gcd"), "coefficient_gcd", MAX_PROOF_BITS)
    if declared_gcd < 0:
        raise InvalidInput("coefficient_gcd must be nonnegative")
    combined, rhs, additions = [0] * n, 0, 0

    def add(old, weight, coefficient):
        nonlocal additions
        additions += 1
        if additions > MAX_ADDITIONS:
            raise UnsupportedInput("integer row-combination operation budget exceeded")
        value = old + weight * coefficient
        if value.bit_length() > MAX_ACCUMULATOR_BITS:
            raise UnsupportedInput("integer accumulator bit budget exceeded")
        return value

    for row, weight in zip(rows, weights):
        if not weight:
            continue
        for i, coefficient in enumerate(row["coefficients"]):
            if coefficient:
                combined[i] = add(combined[i], weight, coefficient)
        if row["rhs"]:
            rhs = add(rhs, weight, row["rhs"])
    divisor = 0
    for coefficient in combined:
        divisor = gcd(divisor, coefficient)
    if combined != declared or rhs != declared_rhs or divisor != declared_gcd:
        return False
    # gcd=0 is an equality contradiction, handled by the rational checker.
    # gcd=1 supplies no divisibility obstruction for integer assignments.
    return divisor >= 2 and rhs % divisor != 0


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("system", type=Path)
    parser.add_argument("certificate", type=Path)
    args = parser.parse_args(argv)
    try:
        accepted = verify(read_json(args.system), read_json(args.certificate))
    except UnsupportedInput as error:
        print(json.dumps({"status": "UNDECIDED", "reason": str(error)}))
        return 2
    except (InvalidInput, OSError, UnicodeError, json.JSONDecodeError, RecursionError) as error:
        print(json.dumps({"status": "INVALID", "reason": str(error)}))
        return 2
    print(json.dumps({"status": "VERIFIED_INTEGER_DIVISIBILITY" if accepted else "REJECTED",
                      "scope": "supplied integer equalities; itinerary compilation is a separate obligation"}))
    return 0 if accepted else 1


if __name__ == "__main__":
    sys.exit(main())
