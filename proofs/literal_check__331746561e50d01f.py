#!/usr/bin/env python3
"""Independent ordinary-integer replay of the finite witness, not a search."""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
EXPECTED = [(6, [13]), (12, [4, 10]), (6, [9, 1]),
            (12, [18, 2]), (6, [9, 11, 5]), (12, [10, 1, 7, 11])]
EXPECTED_GAMMA = [1, 0, 0, 1, 1]


def digits(n):
    return list(map(int, str(n)[::-1]))


def pairword(n):
    d = digits(n)
    return [a + b for a, b in zip(d, reversed(d))]


def realize(q):
    d = [0] * len(q)
    for i in range((len(q) + 1) // 2):
        j = len(q) - 1 - i
        d[i], d[j] = q[i] // 2, q[i] - q[i] // 2
    n = int("".join(map(str, reversed(d))))
    assert pairword(n) == q
    return n


def z(c, B):
    return 9 * sum(a * 10**i for i, a in enumerate(B)) - c * (10**len(B) - 1)


def main():
    traces = []
    for initial_core in [12, 24, 41]:
        c, B = EXPECTED[0]
        n = realize(B + [c] * initial_core + B[::-1])
        core = initial_core
        states = []
        for t, (c, B) in enumerate(EXPECTED):
            q = pairword(n)
            assert q == B + [c] * core + B[::-1]
            assert B[0] > 0 and B[-1] != c and max(B) <= 18
            states.append({"time": t, "n": str(n), "phase": c, "B": B,
                           "core_length": core, "radix_defect": z(c, B)})
            if t < len(EXPECTED) - 1:
                new_n = n + int(str(n)[::-1])
                gamma = len(str(new_n)) - len(str(n))
                assert gamma == EXPECTED_GAMMA[t]
                next_B = EXPECTED[t + 1][1]
                core += gamma + 2 * len(B) - 2 * len(next_B)
                assert core >= 2
                states[-1]["actual_overflow"] = gamma
                n = new_n
        assert states[2]["radix_defect"] == states[4]["radix_defect"] == -423
        assert states[3]["radix_defect"] == -846
        assert states[5]["radix_defect"] == -14508
        traces.append({"initial_core": initial_core, "states": states})
    out = {"status": "PASS", "scope": "three finite literal-integer witness replays",
           "additions": 15, "traces": traces}
    (HERE / "evidence/literal_controls.json").write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps({"status": "PASS", "additions": 15}))


if __name__ == "__main__":
    main()
