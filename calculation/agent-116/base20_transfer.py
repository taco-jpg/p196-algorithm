#!/usr/bin/env python3
"""Exact frozen-itinerary transfer audit for Agent 116's base-20 certificate.

The seven boundary transitions alone force 64*x + 68 = 93*b. Thus b must
equal 20 modulo 64; base 10 cannot realize this particular carry itinerary.
This is not an obstruction to other base-10 centers or certificates.
No imports from the repository mirror and no third-party dependencies.
"""
import argparse
from fractions import Fraction
import json
from pathlib import Path


def require(condition, message):
    if not condition:
        raise ValueError(message)


def carries(base, word, initial):
    require(base >= 2, "invalid base")
    require(initial in (0, 1), "nonbinary initial carry")
    result = [initial]
    for coefficient in word:
        require(type(coefficient) is int and 0 <= coefficient <= 2 * base - 2,
                "invalid coefficient")
        result.append((coefficient + result[-1]) // base)
    return result


def driver(base, edge):
    B, C, B2, C2, u, v = edge
    require(C and C == C[::-1], "center must be nonempty and symmetric")
    e = carries(base, B, 0)[-1]
    k = carries(base, C, e)
    require(k[-1] == 1 - e, "center carry must flip")
    g = carries(base, B[::-1], k[-1])[-1]
    return e, g, k


def boundary_audit(certificate):
    base, edges = certificate["base"], certificate["edges"]
    require(len(edges) == 8, "expected the recovered eight-phase certificate")
    # Each triple means raw_head = a*old_head + beta*base + constant.
    expected = [(2, -2, 1), (2, 0, 1), (2, -2, 1), (1, -1, 0),
                (2, 0, 2), (2, -2, 1), (2, 0, 1)]
    affine = [1, 0, 0]
    initial = edges[0][1][0]
    heads, laws = [], []
    for t, edge in enumerate(edges[:7]):
        e, g, k = driver(base, edge)
        C, C2, v = edge[1], edge[3], edge[5]
        require(v == (1 if t == 6 else 0), "the frozen trim itinerary changed")
        law = (1, e - k[1], 0) if g else (2, -k[1] - k[-1], e + k[-2])
        require(law == expected[t], "the frozen boundary carry itinerary changed")
        a, beta, constant = law
        raw_head = a * C[0] + beta * base + constant
        require(raw_head == (base - 1 if v else C2[0]), "boundary equality failed")
        affine = [a * affine[0], a * affine[1] + beta,
                  a * affine[2] + constant]
        require(affine[0] * initial + affine[1] * base + affine[2] == raw_head,
                "affine composition failed")
        heads.append(C[0])
        laws.append(list(law))
    require(affine == [64, -92, 67], "unexpected seven-step composition")
    require(64 * initial + 68 == 93 * base, "derived equality failed")
    residue = (68 * pow(93, -1, 64)) % 64
    require(residue == 20, "unexpected necessary base residue")
    return {"status": "COMPUTED", "base": base, "initial_head": initial,
            "phase_heads": heads, "boundary_laws": laws,
            "raw_trim_head_affine": affine, "equation": "64*x + 68 = 93*b",
            "necessary_base_modulus": 64, "necessary_base_residue": residue,
            "base10_rhs_remainder_mod64": (93 * 10 - 68) % 64,
            "base10_frozen_boundary_itinerary": "IMPOSSIBLE",
            "scope": "Only the displayed seven boundary carry cases and trim; not all centers."}


def full_center_system(certificate):
    """Propagate symbolic initial center entries through the fixed carry words."""
    base, edges = certificate["base"], certificate["edges"]
    initial = edges[0][1]
    n = (len(initial) + 1) // 2
    dimension = n + 2  # n symmetric coefficients, symbolic base, constant.
    unit = lambda j: [int(k == j) for k in range(dimension)]
    center = [unit(min(j, len(initial) - 1 - j)) for j in range(len(initial))]
    rows, labels = [], []
    for t, edge in enumerate(edges):
        e, g, k = driver(base, edge)
        require(len(center) == len(edge[1]), "center phase width changed")
        digits = []
        for j, coefficient in enumerate(center):
            digit = coefficient.copy()
            digit[n] -= k[j + 1]
            digit[-1] += k[j]
            digits.append(digit)
        y = [0] * dimension
        y[n], y[-1] = e, -e
        if g:
            digits.append(y)
        raw = [[a + b for a, b in zip(x, z)]
               for x, z in zip(digits, reversed(digits))]
        v = edge[5]
        for j in range(v):
            row = raw[j].copy()
            row[n] -= 1
            row[-1] += 1
            rows.append(row)
            labels.append(f"trim_{t}_{j}")
        center = raw[v:len(raw) - v] if v else raw
        require(len(center) == len(edge[3]), "trimmed center width mismatch")
        evaluated = [sum(row[j] * initial[j] for j in range(n)) + row[n] * base + row[-1]
                     for row in center]
        require(evaluated == edge[3], "symbolic center propagation failed")
    require(len(center) == len(initial), "center does not return to its width")
    for j in range(n):
        row = center[j].copy()
        row[j] -= 1
        rows.append(row)
        labels.append(f"closure_{j}")

    pivots = {}
    for row in rows:
        residual = list(map(Fraction, row))
        for j, pivot in pivots.items():
            factor = residual[j]
            if factor:
                residual = [a - factor * b for a, b in zip(residual, pivot)]
        column = next((j for j, value in enumerate(residual[:-1]) if value), None)
        if column is None:
            require(residual[-1] == 0, "inconsistent symbolic system")
            continue
        factor = residual[column]
        pivots[column] = [value / factor for value in residual]
    require(n in pivots, "the fixed full itinerary did not force a base")
    forced = -pivots[n][-1]
    require(forced == base, "forced base differs from supplied certificate")
    return {"status": "COMPUTED_EXACT_RATIONAL_ELIMINATION", "equations": len(rows),
            "unknowns": n + 1, "rank": len(pivots), "forced_base": str(forced),
            "column_order": [f"x{j}" for j in range(n)] + ["base", "constant"],
            "rows": [{"label": label, "coefficients": row}
                     for label, row in zip(labels, rows)],
            "scope": "Only the frozen full center carry words, phase widths and trims."}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("certificate", nargs="?", type=Path,
                        default=Path(__file__).with_name("cert20.json"))
    parser.add_argument("--full-system", action="store_true")
    parser.add_argument("--emit-equations", action="store_true")
    args = parser.parse_args()
    certificate = json.loads(args.certificate.read_text())
    result = boundary_audit(certificate)
    if args.full_system or args.emit_equations:
        full = full_center_system(certificate)
        if not args.emit_equations:
            full.pop("rows")
            full.pop("column_order")
        result["full_center_system"] = full
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
