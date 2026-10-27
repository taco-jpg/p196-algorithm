#!/usr/bin/env python3
"""Independent bigint audit of finite central-core projection counterexamples.

No import from the mirror or center_core_projection.py.  Every edge is an
actual center transition; equality of projected states does not assert equality
of the complete center words.  This verifies a limitation of the abstraction,
not existence of a closed center or a Lychrel certificate.

Run from the repository root:
    python3 calculation/agent-114/verify_center_core.py
"""

import argparse
from itertools import product


SHELLS = {
    # key: (incoming e, overflow g, maximal trim v, target e)
    (0, 0, 0, 0): (15, 5),
    (0, 0, 0, 1): (10, 0),
    (1, 0, 0, 0): (5, 6),
    (1, 0, 0, 1): (0, 1),
    (0, 0, 1, 0): (14, 15, 0),
    (0, 0, 1, 1): (14, 10, 6),
    (1, 0, 1, 0): (4, 5, 0),
    (1, 0, 1, 1): (4, 0, 6),
    (0, 1, 0, 1): (10, 0),
    (1, 1, 0, 0): (0, 1),
}


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def normalize(word, incoming):
    """Normalize via a whole bigint; recover carries from raw prefix values."""
    require(incoming in (0, 1), "nonbinary incoming carry")
    require(all(0 <= x <= 18 for x in word), "coefficient out of bounds")
    value = incoming
    place = 1
    carries = [incoming]
    for coefficient in word:
        value += coefficient * place
        place *= 10
        carries.append(value // place)
    outgoing, remainder = divmod(value, place)
    digits = tuple(int(c) for c in str(remainder).zfill(len(word))[::-1])
    require(len(digits) == len(word), "incorrect normalized width")
    require(all(c in (0, 1) for c in carries), "nonbinary prefix carry")
    return digits, outgoing, tuple(carries)


def alternating(word):
    return sum(x if i % 2 == 0 else -x for i, x in enumerate(word)) % 11


def advance(word, e, g):
    digits, outgoing, _ = normalize(word, e)
    require(outgoing == 1 - e, "source flip fails")
    paired = digits + ((9 * e,) if g else ())
    raw = tuple(a + b for a, b in zip(paired, reversed(paired)))
    v = 0
    while len(raw) >= 2 and raw[0] == raw[-1] == 9:
        raw = raw[1:-1]
        v += 1
    return raw, v


def construct(shell, d, zero_count):
    require(0 <= d <= 8 and zero_count > 0, "bad filler parameters")
    filler = (0, d, d, 0)
    outside = shell + filler
    return outside + (0,) * zero_count + outside[::-1]


def projection(word, e, radius):
    require(word == word[::-1], "nonsymmetric center")
    require(bool(word) and word[0] != 9, "center is not normalized")
    digits, outgoing, carries = normalize(word, e)
    require(outgoing == 1 - e, "projected center flip fails")
    width = 2 * radius + len(word) % 2
    require(len(word) > width, "core consumes the full word")
    offset = (len(word) - width) // 2
    core = word[offset:offset + width]
    core_digits = digits[offset:offset + width]
    core_carries = carries[offset:offset + width + 1]
    require(core == (0,) * width, "nonzero core coefficient")
    require(core_digits == (0,) * width, "nonzero core digit")
    require(core_carries == (0,) * (width + 1), "nonzero core carry")
    alt = alternating(word)
    require(alt == (9 if len(word) % 2 else 0), "alternating residue fails")
    if len(word) % 2:
        require(word[len(word) // 2] % 2 == 0, "odd midpoint is not even")
    return (e, len(word), core, core_digits, core_carries, sum(word) % 9, alt)


def check_edge(word, mode, radius):
    e, g, expected_v, next_e = mode
    before = projection(word, e, radius)
    target, v = advance(word, e, g)
    require(v == expected_v, "maximal trim differs from the shell mode")
    require(len(target) == len(word) + g - 2 * v, "length equation fails")
    after = projection(target, next_e, radius)
    require(after[-2] == (2 * before[-2] + 4 * e - 2) % 9,
            "digit-sum recurrence fails")
    return before, after


def check_shells(max_radius):
    count = 0
    for radius, parity, d, mode in product(
            range(1, max_radius + 1), (0, 1), range(9), SHELLS):
        shell = SHELLS[mode]
        word = construct(shell, d, 2 * radius + 4 + parity)
        require(sum(word) % 9 == (2 * sum(shell) + 4 * d) % 9,
                "filler sum differs from 4d")
        check_edge(word, mode, radius)
        count += 1
    return count


def closed_residues(e):
    result = []
    for start in range(9):
        current = start
        for bit in e:
            current = (2 * current + 4 * bit - 2) % 9
        if current == start:
            result.append(start)
    return result


def check_loop(e, g, radius, initial_parity, start_residue):
    require(len(e) == len(g) and sum(g) % 2 == 0, "bad closed itinerary")
    nongrowth = [i for i, bit in enumerate(g) if bit == 0]
    require(len(nongrowth) >= sum(g) // 2, "insufficient trimming slots")
    trims = [0] * len(e)
    for i in nongrowth[:sum(g) // 2]:
        trims[i] = 1
    offsets = [0]
    for bit, v in zip(g, trims):
        offsets.append(offsets[-1] + bit - 2 * v)
    require(offsets[-1] == 0, "nonclosing exact lengths")
    initial_length = 2 * radius + 18 - min(offsets)
    initial_length += (initial_parity - initial_length) % 2
    residue = start_residue
    first = previous_target = None
    for t, (bit, growth, v) in enumerate(zip(e, g, trims)):
        next_e = e[(t + 1) % len(e)]
        mode = (bit, growth, v, next_e)
        require(mode in SHELLS, "unsupported overflow carry transition")
        shell = SHELLS[mode]
        length = initial_length + offsets[t]
        zero_count = length - 2 * len(shell) - 8
        d = (7 * (residue - 2 * sum(shell))) % 9
        word = construct(shell, d, zero_count)
        before, after = check_edge(word, mode, radius)
        require(before[-2] == residue, "chosen filler has incorrect residue")
        require(len(word) == length, "source exact length differs")
        if previous_target is not None:
            require(before == previous_target, "projected edges do not concatenate")
        else:
            first = before
        previous_target = after
        residue = (2 * residue + 4 * bit - 2) % 9
    require(previous_target == first, "projected cycle fails closure")
    return len(e)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--max-radius", type=int, default=12)
    args = parser.parse_args()
    require(1 <= args.max_radius <= 100, "radius outside audit range 1..100")
    shell_checks = check_shells(args.max_radius)
    cases = [("p11", "10100110011", "11100010000", k) for k in (1, 2, 3, 4)]
    cases += [("p12", "101010010101", "100010001000", k) for k in (2, 4, 6)]
    loops = edge_checks = 0
    for name, estr, gstr, k in cases:
        e = tuple(map(int, estr * k))
        g = tuple(map(int, gstr * k))
        residues = closed_residues(e)
        require(residues, "itinerary has no closed mod-9 residue")
        for radius, parity, residue in product(
                range(1, args.max_radius + 1), (0, 1), residues):
            edge_checks += check_loop(e, g, radius, parity, residue)
            loops += 1
        print(f"{name} k={k} period={len(e)} residues={','.join(map(str, residues))}")
    print(f"shell_checks={shell_checks} projected_loops={loops} "
          f"loop_edge_checks={edge_checks}")
    print("PASS: bigint center arithmetic, maximal trims, core coefficients/digits/"
          "carries, mod9, odd mod11, exact lengths, projected closure")
    print("Scope: existential projection cycles only; no actual center-cycle claim.")


if __name__ == "__main__":
    main()
