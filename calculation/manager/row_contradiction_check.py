#!/usr/bin/env python3
"""Independently check a rational contradiction between supplied integer rows.

This checker does not import the itinerary compiler. Acceptance proves that
the supplied equalities are inconsistent over the rationals. The association
between those rows and a reverse-add itinerary is a separate proof obligation.
Inequalities are validated but are not used in this certificate format.
"""

from __future__ import annotations

import argparse
import json
import sys
from fractions import Fraction
from pathlib import Path


MAX_VARIABLES = 256
MAX_ROWS = 20_000
MAX_ROW_BITS = 4_096
MAX_PROOF_BITS = 16_384
MAX_ACCUMULATOR_BITS = 1_048_576
MAX_ADDITIONS = 2_000_000
MAX_FILE_BYTES = 64 * 1024 * 1024
MAX_INTEGER_DIGITS = 5_000


class InvalidInput(ValueError):
    """Malformed input, independently of the truth of any research claim."""


class UnsupportedInput(ValueError):
    """A resource or numeric limit was exceeded; no decision was made."""


def integer(value, name, bits):
    if type(value) is not int:
        raise InvalidInput(f"{name} must be a JSON integer, not a bool or float")
    if value.bit_length() > bits:
        raise UnsupportedInput(f"{name} exceeds the {bits}-bit limit")
    return value


def text_field(value, name, limit=1024):
    if type(value) is not str or not value or len(value) > limit:
        raise InvalidInput(f"{name} must be a nonempty string of at most {limit} characters")


def validate_system(system):
    if type(system) is not dict or system.get("format") != "p196-center-affine-v1":
        raise InvalidInput("unsupported system format")
    variables = system.get("variables")
    if type(variables) is not list or not variables:
        raise InvalidInput("variables must be a nonempty list")
    if len(variables) > MAX_VARIABLES:
        raise UnsupportedInput("too many variables")
    for name in variables:
        text_field(name, "variable name", 512)
    if len(set(variables)) != len(variables):
        raise InvalidInput("variable names must be unique")
    base = integer(system.get("target_base"), "target_base", MAX_ROW_BITS)
    if base < 2 or type(system.get("itinerary")) is not dict:
        raise InvalidInput("target_base must be at least two and itinerary must be an object")
    for kind in ("equalities", "inequalities"):
        rows = system.get(kind)
        if type(rows) is not list:
            raise InvalidInput(f"{kind} must be a list")
        if len(rows) > MAX_ROWS:
            raise UnsupportedInput(f"too many {kind}")
        for i, row in enumerate(rows):
            if type(row) is not dict:
                raise InvalidInput(f"{kind}[{i}] must be an object")
            text_field(row.get("label"), f"{kind}[{i}].label")
            coeffs = row.get("coefficients")
            if type(coeffs) is not list or len(coeffs) != len(variables):
                raise InvalidInput(f"{kind}[{i}] has the wrong coefficient dimension")
            for j, value in enumerate(coeffs):
                integer(value, f"{kind}[{i}].coefficients[{j}]", MAX_ROW_BITS)
            integer(row.get("rhs"), f"{kind}[{i}].rhs", MAX_ROW_BITS)
            if type(row.get("origin")) is not dict:
                raise InvalidInput(f"{kind}[{i}].origin must be an object")


def checked_sum(old, multiplier, coefficient):
    value = old + multiplier * coefficient
    if max(value.numerator.bit_length(), value.denominator.bit_length()) > MAX_ACCUMULATOR_BITS:
        raise UnsupportedInput("rational accumulator exceeds its bit budget")
    return value


def verify(system, certificate):
    """Return True exactly when the supplied multiplier identity is contradictory.

    Explicit exceptions distinguish malformed/unsupported inputs from a validly
    formed certificate that fails its claimed arithmetic identity. No assertion
    participates in acceptance, including under optimized Python.
    """
    validate_system(system)
    if type(certificate) is not dict or certificate.get("format") != "p196-rational-row-contradiction-v1":
        raise InvalidInput("unsupported contradiction format")
    multipliers = certificate.get("multipliers")
    rows = system["equalities"]
    if type(multipliers) is not list or len(multipliers) != len(rows):
        raise InvalidInput("one rational multiplier is required for every equality")
    rational_multipliers = []
    for i, pair in enumerate(multipliers):
        if type(pair) is not list or len(pair) != 2:
            raise InvalidInput(f"multiplier {i} must be [numerator, denominator]")
        numerator = integer(pair[0], f"multiplier {i} numerator", MAX_PROOF_BITS)
        denominator = integer(pair[1], f"multiplier {i} denominator", MAX_PROOF_BITS)
        if denominator <= 0:
            raise InvalidInput("rational denominators must be positive")
        rational_multipliers.append(Fraction(numerator, denominator))
    combined = [Fraction(0) for _ in system["variables"]]
    rhs = Fraction(0)
    additions = 0
    for row, multiplier in zip(rows, rational_multipliers):
        if not multiplier:
            continue
        for j, coefficient in enumerate(row["coefficients"]):
            if coefficient:
                additions += 1
                if additions > MAX_ADDITIONS:
                    raise UnsupportedInput("weighted-sum operation budget exceeded")
                combined[j] = checked_sum(combined[j], multiplier, coefficient)
        if row["rhs"]:
            additions += 1
            if additions > MAX_ADDITIONS:
                raise UnsupportedInput("weighted-sum operation budget exceeded")
            rhs = checked_sum(rhs, multiplier, row["rhs"])
    return all(value == 0 for value in combined) and rhs != 0


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise InvalidInput(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def parse_integer(token):
    # Parse in small chunks, avoiding global changes to Python's integer parser.
    negative = token.startswith("-")
    digits = token[1:] if negative else token
    if len(digits) > MAX_INTEGER_DIGITS:
        raise UnsupportedInput("JSON integer literal exceeds its digit budget")
    number = 0
    for i in range(0, len(digits), 9):
        chunk = digits[i:i + 9]
        number = number * (10 ** len(chunk)) + int(chunk)
    return -number if negative else number


def reject_constant(value):
    raise InvalidInput(f"nonfinite JSON constant: {value}")


def read_json(path):
    with Path(path).open("rb") as handle:
        data = handle.read(MAX_FILE_BYTES + 1)
    if len(data) > MAX_FILE_BYTES:
        raise UnsupportedInput("JSON file exceeds its byte budget")
    return json.loads(data.decode("utf-8"), object_pairs_hook=unique_object,
                      parse_int=parse_integer, parse_constant=reject_constant)


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
    print(json.dumps({"status": "VERIFIED_ROW_CONTRADICTION" if accepted else "REJECTED",
                      "scope": "supplied integer equalities; itinerary compilation is a separate obligation"}))
    return 0 if accepted else 1


if __name__ == "__main__":
    sys.exit(main())
