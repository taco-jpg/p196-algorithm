#!/usr/bin/env python3
"""Independent coverage for the decimal period-20 exterior review.

Generate every binary necklace, including imprimitive words, by the standard
recursive necklace algorithm. Apply the sound 18-state first-coefficient
projection. A surviving overflow word is only a candidate for the full B
automaton; it is not a B cycle or a certificate.

The recurrence is credited to Agent 4 (#290/#323); this implementation and
its coverage/arithmetic checks do not import that implementation or a mirror.
"""
import argparse
from collections import Counter
from functools import lru_cache
from hashlib import sha256
from itertools import product
import json
from math import comb, gcd
from pathlib import Path
import time


def require(condition, message):
    if not condition:
        raise ValueError(message)


def necklaces(n):
    """Lexicographically least rotations; do not discard shorter periods."""
    a = [0] * (n + 1)

    def visit(t, period):
        if t > n:
            if n % period == 0:
                yield tuple(a[1:])
            return
        a[t] = a[t - period]
        yield from visit(t + 1, period)
        for symbol in range(a[t - period] + 1, 2):
            a[t] = symbol
            yield from visit(t + 1, t)

    yield from visit(1, 1)


def totient(n):
    return sum(gcd(k, n) == 1 for k in range(1, n + 1))


def necklace_weight_count(n, k):
    """Burnside count, independently of the recursive generator."""
    numerator = sum(totient(d) * comb(n // d, k // d)
                    for d in range(1, gcd(n, k) + 1) if gcd(n, k) % d == 0)
    require(numerator % n == 0, "Burnside count is not integral")
    return numerator // n


def head_table():
    table = [[0] * 18 for _ in range(2)]
    for x in range(1, 19):
        for inward in (0, 1):
            overflow = (x + inward) // 10
            following = x % 10 + 1 if overflow else 2 * x + inward
            require(1 <= following <= 18, "head recurrence left its state space")
            table[overflow][x - 1] |= 1 << (following - 1)
    return table


HEAD = head_table()


@lru_cache(maxsize=None)
def image(bits, overflow):
    following = 0
    while bits:
        least = bits & -bits
        following |= HEAD[overflow][least.bit_length() - 1]
        bits -= least
    return following


def surviving_heads(word):
    survivors = []
    for x in range(1, 19):
        singleton = 1 << (x - 1)
        bits = singleton
        for overflow in word:
            bits = image(bits, overflow)
            if not bits:
                break
        if bits & singleton:
            survivors.append(x)
    return survivors


def normalize(word, carry):
    result = []
    for coefficient in word:
        carry, digit = divmod(coefficient + carry, 10)
        result.append(digit)
    return result, carry


def full_b_successors(word):
    """Literal independent arithmetic, branching over every legal suffix trim."""
    low, carry = normalize(word, 0)
    high, overflow = normalize(word[::-1], 1 - carry)
    if overflow:
        low = low + [9 * (1 - carry)]
        high = [1] + high[::-1]
    else:
        high.reverse()
    raw = tuple(x + y for x, y in zip(low, high))
    while True:
        yield overflow, raw
        if not raw or raw[-1] != 9:
            return
        raw = raw[:-1]


def selftest():
    necklace_cases = 0
    for n in range(1, 11):
        generated = list(necklaces(n))
        brute = [w for w in product((0, 1), repeat=n)
                 if all(w <= w[j:] + w[:j] for j in range(1, n))]
        require(generated == brute, f"necklace mismatch at period {n}")
        counts = Counter(map(sum, generated))
        require(all(counts[k] == necklace_weight_count(n, k) for k in range(n + 1)),
                f"Burnside mismatch at period {n}")
        necklace_cases += len(generated)

    states = edges = 0
    for width in range(4):
        for word in product(range(19), repeat=width):
            if word and word[0] == 0:
                continue
            first = word[0] if word else 9
            states += 1
            for overflow, following in full_b_successors(word):
                target = following[0] if following else 9
                require(HEAD[overflow][first - 1] & (1 << (target - 1)),
                        f"direct arithmetic projection failed: {word}, {following}")
                edges += 1
    for text in ("11100010000", "100010001000"):
        word = tuple(map(int, text))
        require(surviving_heads(word), "known positive B driver rejected")
        require(all(surviving_heads(word[j:] + word[:j]) for j in range(len(word))),
                "rotation of known positive driver rejected")
    require(not surviving_heads((0,) * 20), "all-zero clock unexpectedly survives")
    require(not surviving_heads((1,) * 20), "all-one clock unexpectedly survives")
    return {"status": "PASS", "necklaces_compared_to_brute": necklace_cases,
            "direct_B_states": states, "all_trim_edges": edges,
            "max_direct_width": 3, "known_positive_drivers": 2}


def census(n):
    all_words, selected = [], []
    all_weights, selected_weights = Counter(), Counter()
    for word in necklaces(n):
        text = "".join(map(str, word))
        all_words.append(text)
        all_weights[sum(word)] += 1
        if surviving_heads(word):
            selected.append(text)
            selected_weights[sum(word)] += 1
    formula = {k: necklace_weight_count(n, k) for k in range(n + 1)}
    require(dict(all_weights) == formula, "full necklace coverage disagrees with Burnside")
    require(all_words == sorted(set(all_words)), "necklaces are not unique and ordered")
    require(all(w <= w[j:] + w[:j] for w in all_words for j in range(1, n)),
            "a generated word is not its least cyclic rotation")
    payload = "".join(word + "\n" for word in selected)
    result = {"status": "COMPUTED_NECESSARY_PROJECTION", "base": 10, "period": n,
              "all_necklaces": len(all_words), "surviving_necklaces": len(selected),
              "all_counts_by_weight": dict(sorted(all_weights.items())),
              "surviving_counts_by_weight": dict(sorted(selected_weights.items())),
              "selected_lexicographic_lf_sha256": sha256(payload.encode()).hexdigest(),
              "every_necklace_rotation_checked": True,
              "imprimitive_words_included": True}
    if n == 20:
        result["agrees_with_Agent4_report"] = (
            len(all_words) == 52488 and
            dict(selected_weights) == {5: 1, 6: 23, 7: 164, 8: 219, 9: 41, 10: 1})
    return result, all_words, selected


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--period", type=int, default=20)
    parser.add_argument("--selftest", action="store_true")
    parser.add_argument("--output", type=Path, help="write surviving g words, one per line")
    parser.add_argument("--all-output", type=Path, help="write every necklace, one per line")
    args = parser.parse_args()
    if not 1 <= args.period <= 24:
        parser.error("period must lie between 1 and 24")
    begin = time.monotonic()
    tests = selftest() if args.selftest else None
    result, all_words, selected = census(args.period)
    if args.output is not None:
        args.output.write_text("".join(w + "\n" for w in selected))
    if args.all_output is not None:
        args.all_output.write_text("".join(w + "\n" for w in all_words))
    if tests is not None:
        result["selftest"] = tests
    result["elapsed_seconds"] = round(time.monotonic() - begin, 6)
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
