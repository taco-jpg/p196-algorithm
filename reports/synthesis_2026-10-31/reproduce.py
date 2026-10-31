#!/usr/bin/env python3
"""Small exact controls for the 2026-10-31 synthesis publication.

No search, third-party dependency, Lean theorem, or decimal existence claim.
Run from any directory: python3 reports/synthesis_2026-10-31/reproduce.py
Checks use explicit exceptions, so python3 -O does not disable validation.
"""
import json
from math import gcd
from pathlib import Path


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def reverse10(n):
    return int(str(n)[::-1])


def y13_check():
    h, k, q = 2, 3, 111
    mh, mk, mg = 10**h - 1, 10**k - 1, 10**gcd(h, k) - 1
    n = mh * q
    require(10**h <= q < 2 * 10**h, "interval")
    require(n % mk == 0, "divisibility")
    require(n != mk and reverse10(n) != n, "counterexample")
    require(mh * (mk // mg) == mk * (mh // mg), "corrected identity")
    return {
        "h": h, "k": k, "q": q, "product": n,
        "quotient": n // mk, "reverse": reverse10(n), "q_mod9": q % 9,
        "scope": "broad interval lemma; not the restricted charge-2 first-exit claim",
    }


def boundary_check():
    b0 = [10,4,6,6,7,12,9,16,16,13,0,2,10,17,7,0,18,6,5,18,4,18,14,9,14,8,12,17,10,4,6,4,0,5]
    b1 = [1,5,10,12,13,10,3,7,14,11,4,2,3,9,15,7,9,15,11,14,13,13,14,5,5,13,11,11,9,5,10,10,4,5]
    w0 = [5,18,4,8,1,15,4,0,5]
    w1 = [10,14,13,12,9,7,10,4,5]
    cut = 79
    half = b0 + w0 * 5 + [10,0,0,0,0]
    pairs = half + half[-2::-1]
    require(pairs == pairs[::-1], "source symmetry")
    digits = [0] * len(pairs)
    for i in range(len(pairs) // 2):
        digits[-1-i] = min(9, pairs[i])
        digits[i] = pairs[i] - digits[-1-i]
    mid = len(pairs) // 2
    require(pairs[mid] % 2 == 0, "midpoint parity")
    digits[mid] = pairs[mid] // 2
    require(digits[-1] > 0 and all(0 <= d <= 9 for d in digits), "canonical source")
    require([x+y for x,y in zip(digits, digits[::-1])] == pairs, "pair realization")
    n = int("".join(map(str, digits[::-1])))
    successor = n + reverse10(n)
    out_digits = list(map(int, str(successor)[::-1]))
    next_pairs = [x+y for x,y in zip(out_digits, out_digits[::-1])]
    carries = [0]
    normalized = []
    for x in pairs:
        value = x + carries[-1]
        normalized.append(value % 10)
        carries.append(value // 10)
    if carries[-1]:
        normalized.append(carries[-1])
    require(normalized == out_digits, "schoolbook versus whole-integer arithmetic")
    require(next_pairs[:cut] == b1 + w1 * 5, "preserved lower prefix")
    require((pairs[cut:cut+2], next_pairs[cut:cut+2]) == ([10,0], [6,1]), "defect edge")
    actual = carries[len(pairs)-cut]
    # The first coefficient above the nominal periodic cut is 5, a carry reset.
    nominal_options = {(w0[0] + incoming) // 10 for incoming in (0,1)}
    require(nominal_options == {0}, "nominal carry reset")
    nominal = next(iter(nominal_options))
    require((actual, nominal) == (1,0), "carry discrepancy")
    for high in (0,1):
        din0 = (pairs[cut+1] + high) // 10
        require((pairs[cut] + din0) // 10 != nominal, "old graph rejects edge")
    require((len(str(n)), len(str(successor))) == (167,168), "lengths")
    return {
        "source_length": 167, "target_length": 168, "cut": cut, "overflow": carries[-1],
        "prefix_exact": True, "defect_before": pairs[cut:cut+2],
        "defect_after": next_pairs[cut:cut+2], "actual_descending_carry": actual,
        "nominal_descending_carry": nominal, "schoolbook_agrees": True,
        "source_integer": str(n), "successor_integer": str(successor),
        "scope": "one omitted physical edge; no stationary cycle",
    }


def primitive_period(word):
    for p in range(1, len(word)+1):
        if len(word) % p == 0 and word == word[:p] * (len(word)//p):
            return p
    raise AssertionError("missing period")


def port_checks():
    ports = {
        "even8a": "010001010100010101000101",
        "even8b": "101110101011101010111010",
        "odd9a": "101010111010101110101011",
        "odd9b": "010101000101010001010100",
        "even6a": "011101111000100001110111100010000111011110001000",
        "even6b": "100010000111011110001000011101111000100001110111",
        "odd7a": "100001110111100010000111011110001000011101111000",
        "odd7b": "011110001000011101111000100001110111100010000111",
    }
    exterior = "101010010101"
    periods = {name: primitive_period(word) for name,word in ports.items()}
    require(primitive_period(exterior) == 12, "exterior primitive period")
    require(set(periods.values()) == {8,16}, "centre primitive periods")
    matches = 0
    for word in ports.values():
        width = len(word) * len(exterior) // gcd(len(word), len(exterior))
        for a in range(len(word)):
            left = (word[a:]+word[:a]) * (width//len(word))
            for b in range(len(exterior)):
                right = (exterior[b:]+exterior[:b]) * (width//len(exterior))
                matches += left == right
    require(matches == 0, "direct attachment unexpectedly matches")
    return {"centre_primitive_periods": periods, "exterior_primitive_period": 12,
            "full_port_matches_over_all_rotations": matches,
            "scope": "eight stored centres versus the known neutral-p12 exterior only"}


def p11_check():
    gamma, ports = "11100010000", "10100110011"
    rotated = [gamma[1:]+gamma[:1], ports[1:]+ports[:1]]
    require(rotated == ["11000100001", "01001100111"], "joint phase rotation")
    return {"left_rotation": 1, "gamma": rotated[0], "ports": rotated[1],
            "scope": "notation comparison; graph certificates not rerun"}


def main():
    actual = {"y13": y13_check(), "boundary": boundary_check(),
              "ports": port_checks(), "p11": p11_check()}
    record = json.loads(Path(__file__).with_name("evidence.json").read_text(encoding="utf-8"))
    require(actual == record["expected"], "recorded evidence mismatch")
    print(json.dumps({"status": "PASS", "checks": actual}, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
