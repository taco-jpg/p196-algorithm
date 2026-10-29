#!/usr/bin/env python3
"""Independent ordinary Python bigint control for the exact transparent crossing."""
import hashlib


def reverse_add(n: int) -> int:
    return n + int(str(n)[::-1])


def main() -> None:
    for q in (11, 12, 100, 600):
        n = 88 * 10 ** (2 * q + 4) + 78 * 10 ** q + 75
        states = []
        for t in range(14):
            s = str(n)
            assert s != s[::-1], (q, t, "unexpected palindrome")
            states.append(s)
            if t < 13:
                n = reverse_add(n)
        digest = hashlib.sha256("|".join(states).encode()).hexdigest()
        print(f"PY_BIGINT q={q} states=14 initial_digits={len(states[0])} "
              f"final_digits={len(states[-1])} sha256={digest}")
    print("ALL PYTHON BIGINT CONTROLS PASSED")

if __name__ == "__main__":
    main()
