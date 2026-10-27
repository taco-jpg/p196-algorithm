#!/usr/bin/env python3
"""Neutral-A120 exterior alternating charge and exact residue counts.

R_b(B) = alt(B) - (-1)**len(B), interpreted modulo b+1.
Every legal suffix trim preserves R modulo b+1. A raw exterior step
doubles R if gamma=0 and resets R to zero if gamma=1. Thus every closed
legal exterior cycle has zero R. This is a necessary filter, not a
cycle-existence decision.

Q_b(B) = 2*alt(B) + (b-1)*(-1)**len(B) is preserved exactly by a neutral
suffix trim. The strong cycle condition is Q == b+1 (mod 2*(b+1)),
equivalent to R == 0 (mod b+1). Q == 0 (mod b+1) alone is weaker when
the base is odd; it is checked only as a control, not used to filter.

Prior alternating-moment algebra is credited to
Drafts/D20261015Agent2ComplementarySearchAlternatingCharge/AlternatingCharge.lean,
Core/OuterCharge.lean, Core/OuterOrbit.lean and
Agent5EvenBaseAbsorption/GeneralMomentAbsorption.lean.
Those files treat the different, nonneutral exterior map. The present
code applies the charge to the fixed-neutral A120 complement-carry map.

Commands:
  python3 calculation/agent-107/exterior_charge.py selftest
  python3 calculation/agent-107/exterior_charge.py count --base 10 --maxlen 12 --include-empty
"""

import argparse
import ast
from collections import Counter
from itertools import product
import json
from math import gcd
from pathlib import Path
import random
import re


ROOT = Path(__file__).resolve().parents[2]


def sign(n):
    return 1 if n % 2 == 0 else -1


def alternating(word):
    return sum(sign(i) * x for i, x in enumerate(word))


def validate(base, word=()):
    if type(base) is not int or base < 2:
        raise ValueError("base must be an integer at least 2")
    if any(type(x) is not int or x < 0 or x > 2 * (base - 1) for x in word):
        raise ValueError("coefficients must be integers in [0, 2*(base-1)]")


def charge(base, word):
    """The integer Q, exactly invariant under neutral suffix padding."""
    validate(base, word)
    return 2 * alternating(word) + (base - 1) * sign(len(word))


def residual(base, word):
    """The integer R; its residue modulo b+1 is the strong cycle filter."""
    validate(base, word)
    return alternating(word) - sign(len(word))


def effective_modulus(base):
    """Full modulus for the strong R cycle condition, in every base."""
    validate(base)
    return base + 1


def charge_only_modulus(base):
    """Weaker modulus obtained from Q == 0 mod b+1 alone."""
    validate(base)
    return (base + 1) // gcd(2, base + 1)


def eligible(base, word):
    """Necessary strong cycle condition; it does not assert a cycle exists."""
    return residual(base, word) % effective_modulus(base) == 0


def normalize(base, word, carry):
    digits = []
    for coefficient in word:
        carry, digit = divmod(coefficient + carry, base)
        digits.append(digit)
    return tuple(digits), carry


def normalize_integer(base, word, entry):
    """Independent whole-integer arithmetic, with explicit fixed width."""
    value = 0
    for coefficient in reversed(word):
        value = value * base + coefficient
    value += entry
    digits = []
    for _ in word:
        value, digit = divmod(value, base)
        digits.append(digit)
    return tuple(digits), value


def raw_exterior(base, word, normalizer=normalize):
    """Autonomous A120 B map with complementary reverse-entry carry 1-e."""
    word = tuple(word)
    validate(base, word)
    left, e = normalizer(base, word, 0)
    right, gamma = normalizer(base, word[::-1], 1 - e)
    if gamma:
        left = left + ((base - 1) * (1 - e),)
        right = (1,) + right[::-1]
    else:
        right = right[::-1]
    return tuple(x + y for x, y in zip(left, right)), e, gamma


def suffix_trims(base, raw):
    """All literal neutral suffix trims, including zero and full trimming."""
    raw = tuple(raw)
    yield raw, 0
    for k in range(1, len(raw) + 1):
        if raw[-k] != base - 1:
            break
        yield raw[:-k], k


def residue_counts(base, maxlen, include_empty=False):
    """Exact DP for all words with nonzero first coefficient and length<=M.

    These are combinatorial state counts only. No state graph is built.
    Coefficients range from 0 to 2(b-1); the first ranges from 1 to 2(b-1).
    Every base uses the full modulus b+1 on R, including odd bases.
    The zero_charge output field counts zero R (equivalently centered
    Q-(b+1) modulo 2*(b+1)); it does not use the weaker Q-only condition.
    Empty B is counted in the universe only when requested; it never
    satisfies the necessary cycle condition.
    """
    if type(maxlen) is not int or maxlen < 0:
        raise ValueError("maxlen must be a nonnegative integer")
    modulus = effective_modulus(base)
    rows = []
    cumulative = int(include_empty)
    surviving = 0
    if include_empty:
        rows.append({"length": 0, "total": 1, "zero_charge": 0,
                     "cumulative_total": 1, "cumulative_zero_charge": 0})
    distribution = [0] * modulus
    distribution[0] = 1
    alphabet = 2 * base - 1
    for length in range(1, maxlen + 1):
        low = 1 if length == 1 else 0
        weights = Counter(sign(length - 1) * x % modulus
                          for x in range(low, alphabet))
        following = [0] * modulus
        for residue, count in enumerate(distribution):
            for offset, multiplicity in weights.items():
                following[(residue + offset) % modulus] += count * multiplicity
        distribution = following
        total = (alphabet - 1) * alphabet ** (length - 1)
        kept = distribution[sign(length) % modulus]
        if sum(distribution) != total:
            raise ArithmeticError("DP total does not match word count")
        cumulative += total
        surviving += kept
        rows.append({"length": length, "total": total, "zero_charge": kept,
                     "cumulative_total": cumulative,
                     "cumulative_zero_charge": surviving})
    return {"base": base, "maxlen": maxlen, "include_empty": include_empty,
            "criterion": "R=alt(B)-(-1)^len(B) is zero modulo b+1",
            "charge_modulus": 2 * (base + 1), "charge_target": base + 1,
            "effective_modulus": modulus,
            "weaker_charge_modulus": charge_only_modulus(base),
            "rows": rows, "total": cumulative, "zero_charge": surviving}


def source_certificates():
    """Read the eight concrete certificates from their existing Lean files."""
    files = [ROOT / "lean/P196/Drafts/Agent120NeutralBandCalibration/A120PowerTwo.lean",
             ROOT / "lean/P196/Agent213KnownBaseMechanisms/KnownBases.lean"]
    result = []
    for path in files:
        source = path.read_text(encoding="utf-8")
        words = {name: tuple(ast.literal_eval(literal)) for name, literal in
                 re.findall(r"^def (\w+)\s*:\s*List Nat\s*:=\s*(\[[^\]]*\])",
                            source, re.M)}
        declarations = re.finditer(
            r"^def cert(\d+)\s*:\s*List Edge\s*:=\s*\n(.*?)(?=^\s*$)",
            source, re.M | re.S)
        for declaration in declarations:
            edges = []
            for row in re.findall(r"⟨([^⟩]+)⟩", declaration[2]):
                tokens = re.findall(r"\[[^\]]*\]|[A-Za-z_]\w*|\d+", row)
                if len(tokens) != 6:
                    raise ValueError("source certificate syntax changed")
                def word(token):
                    return tuple(ast.literal_eval(token)) if token.startswith("[") else words[token]
                edges.append(tuple(word(x) for x in tokens[:4]) +
                             tuple(int(x) for x in tokens[4:]))
            if not edges:
                raise ValueError("empty source certificate")
            result.append((int(declaration[1]), edges))
    if sorted(base for base, _ in result) != [2, 4, 8, 11, 16, 17, 26, 32]:
        raise ValueError("expected eight known source certificates")
    return sorted(result)


def selftest():
    checks = Counter()

    def require(condition, message):
        if not condition:
            raise AssertionError(message)

    def one(base, word, padding):
        word = tuple(word)
        raw, e, gamma = raw_exterior(base, word)
        require((raw, e, gamma) == raw_exterior(base, word, normalize_integer),
                ("independent arithmetic", base, word))
        require(e in (0, 1) and gamma in (0, 1), ("carry range", base, word))
        require(len(raw) == len(word) + gamma, ("raw length", base, word))
        expected = 0 if gamma else 2 * charge(base, word)
        require((charge(base, raw) - expected) % (base + 1) == 0,
                ("charge law", base, word))
        expected_r = 0 if gamma else 2 * residual(base, word)
        require((residual(base, raw) - expected_r) % (base + 1) == 0,
                ("strong R law", base, word))
        expected_q = base + 1 if gamma else 2 * charge(base, word) - (base + 1)
        require((charge(base, raw) - expected_q) % (2 * (base + 1)) == 0,
                ("strong Q law", base, word))
        require(eligible(base, word) == ((charge(base, word) - (base + 1)) % (2 * (base + 1)) == 0),
                ("strong charge equivalence", base, word))
        require((charge(base, word) % (base + 1) == 0) ==
                (residual(base, word) % charge_only_modulus(base) == 0),
                ("weaker charge equivalence", base, word))
        checks["strong_residual_laws"] += 1
        for entry in (0, 1):
            digits, exit_carry = normalize(base, word, entry)
            norm_defect = alternating(digits) + sign(len(word)) * exit_carry - alternating(word) - entry
            require(norm_defect % (base + 1) == 0, ("normalization identity", base, word, entry))
            checks["normalization_identities"] += 1
        for trimmed, _ in suffix_trims(base, raw):
            require(charge(base, trimmed) == charge(base, raw), ("integer trim identity", base, raw))
            require((residual(base, trimmed) - residual(base, raw)) % (base + 1) == 0,
                    ("strong trim residue", base, raw))
            checks["all_legal_raw_trims"] += 1
        for k in padding:
            padded = word + (base - 1,) * k
            require(charge(base, padded) == charge(base, word), ("integer padding identity", base, word, k))
            padded_raw, ep, gp = raw_exterior(base, padded)
            require((ep, gp) == (e, gamma) and padded_raw == raw + (base - 1,) * k,
                    ("padding transition control", base, word, k))
            checks["padding_controls"] += 1
        checks["one_step_cases"] += 1
        checks[f"gamma_{gamma}"] += 1

    for base, maximum in [(2, 4), (3, 4), (4, 4), (5, 4), (10, 3)]:
        for length in range(maximum + 1):
            for word in product(range(2 * base - 1), repeat=length):
                one(base, word, (0, 1, 2))
                checks["exhaustive_words"] += 1

    rng = random.Random(107)
    bases = (2, 3, 4, 8, 10, 11, 16, 17, 26, 32, 63, 257, 65536)
    for _ in range(5000):
        base = rng.choice(bases)
        word = tuple(rng.randrange(2 * base - 1) for _ in range(rng.randrange(257)))
        one(base, word, (rng.randrange(9),))
        checks["random_words"] += 1

    for base, edges in source_certificates():
        for i, (B, _C, B2, _C2, u, _v) in enumerate(edges):
            raw, _, _ = raw_exterior(base, B)
            require(raw == B2 + (base - 1,) * u, ("source exterior edge", base, i))
            require(B2 == edges[(i + 1) % len(edges)][0], ("source exterior closure", base, i))
            require(B and eligible(base, B), ("source charge condition", base, i))
            one(base, B, (0, 1, 4))
            checks["source_certificate_edges"] += 1
        checks["source_certificates"] += 1

    for base in range(2, 7):
        rows = residue_counts(base, 4, include_empty=True)["rows"]
        for row in rows:
            length = row["length"]
            kept = total = 0
            for word in product(range(2 * base - 1), repeat=length):
                if word and word[0] == 0:
                    continue
                total += 1
                kept += eligible(base, word)
            require((total, kept) == (row["total"], row["zero_charge"]),
                    ("DP enumeration", base, length))
            checks["dp_bruteforce_rows"] += 1

    for base in range(2, 201):
        require(not eligible(base, ()), ("empty B obstruction", base))
    require(charge(3, (1,)) % 4 == 0 and not eligible(3, (1,)),
            "odd-base weak-Q false positive")
    checks["empty_base_cases"] = 199
    checks["odd_base_counterexample"] = 1
    print(json.dumps({"status": "PASS", "checks": dict(sorted(checks.items()))}, sort_keys=True))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("selftest")
    counts = sub.add_parser("count")
    counts.add_argument("--base", type=int, default=10)
    counts.add_argument("--maxlen", type=int, default=12)
    counts.add_argument("--include-empty", action="store_true")
    args = parser.parse_args()
    if args.command == "selftest":
        selftest()
    else:
        try:
            result = residue_counts(args.base, args.maxlen, args.include_empty)
        except ValueError as error:
            parser.error(str(error))
        print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
