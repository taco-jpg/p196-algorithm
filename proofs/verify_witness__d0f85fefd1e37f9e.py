#!/usr/bin/env python3
"""Two exact implementations of the safe three-return witness. Stdlib only."""
from __future__ import annotations
import json
from pathlib import Path

SEED = 809999999
EXPECTED = (
    809999999, 1809999907, 8909998988, 17808998086, 85898978957,
    161886968815, 680756656976, 1360413314062, 3964546454693,
)


def digits(n: int) -> tuple[int, ...]:
    """Canonical decimal digits, least significant first."""
    if n <= 0:
        raise ValueError("A positive integer is required")
    return tuple(map(int, reversed(str(n))))


def pair_word(n: int) -> tuple[int, ...]:
    d = digits(n)
    return tuple(x + y for x, y in zip(d, reversed(d)))


def high(q: tuple[int, ...]) -> bool:
    return bool(q) and q[0] >= 10 and all(9 <= x <= 18 for x in q)


def coefficient_step(q: tuple[int, ...]) -> tuple[tuple[int, ...], tuple[int, ...]]:
    """Normalize coefficients with actual carries; then reflect actual width."""
    if not q or q != q[::-1] or q[0] == 0 or not all(0 <= x <= 18 for x in q):
        raise ValueError("A canonical symmetric pair word is required")
    if len(q) % 2 and q[len(q)//2] % 2:
        raise ValueError("An odd-width center must be even")
    output: list[int] = []
    carry = 0
    for x in q:
        carry, digit = divmod(x + carry, 10)
        output.append(digit)
    if carry:
        output.append(carry)
    assert output[-1] != 0
    d = tuple(output)
    return tuple(x + y for x, y in zip(d, reversed(d))), d


def verify() -> dict:
    n = SEED
    q = pair_word(n)
    trace = []
    for t, expected in enumerate(EXPECTED):
        assert n == expected, (t, n, expected)
        assert q == pair_word(n), (t, q, pair_word(n))
        is_palindrome = str(n) == str(n)[::-1]
        trace.append({"time": t, "n": str(n), "pair_word": list(q),
                      "in_high_region": high(q), "palindrome": is_palindrome})
        if t < 7:
            assert not is_palindrome, ("unsafe witness", t)
        if t in (0, 2, 4, 6):
            assert high(q), ("missed return", t)
        if t + 1 < len(EXPECTED):
            q_next, actual_digits = coefficient_step(q)
            n_next = n + int(str(n)[::-1])
            assert actual_digits == digits(n_next), ("implementation disagreement", t)
            n, q = n_next, q_next
    assert all(not row["palindrome"] for row in trace[:8])
    assert trace[8]["palindrome"]
    return {"status": "checked finite witness; not a Lychrel seed",
            "seed": str(SEED), "safe_high_returns": 3,
            "first_positive_palindrome_time": 8, "trace": trace}


def main() -> None:
    result = verify()
    target = Path(__file__).with_name("witness.json")
    data = json.dumps(result, indent=2) + "\n"
    if target.exists():
        assert json.loads(target.read_text()) == result, "Stored evidence differs"
    else:
        target.write_text(data)
    print(data, end="")


if __name__ == "__main__":
    main()
