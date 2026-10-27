#!/usr/bin/env python3
"""Finite obstruction to a decimal period-4 scalar quotient modulo 101.

For a fixed weight vector w, put S_w(B) = sum(w[j % 4]*(B[j]-9)) mod101.
Four pairs of legal A120 edges have identical source period-4 moments,
width, e, g and trims, while their target moment differences form an
invertible matrix modulo101. Consequently only w=0 can admit any
deterministic next-charge law on every legal edge with those retained data.
The law need not be affine. Every source also has zero strong R modulo11.

This is a quotient-method obstruction, not a cycle search, a claim about
charges restricted only to actual cycles, or decimal Lychrel nonexistence.
It does not exclude carry-augmented or nonlinear word representations.

Prior scope: Agent51ReciprocalMoment proves symmetric first-moment
redundancy; REPORT_204/214 study spatially periodic bulk maps. Agent112's
separate numerical-step work concerns full positional values. The current
finite collision certificate does not replace any of those results.
Coordination: issue289, Agent107 claim6433557513.

Only the unchanged calculation/neutral_band_search.py mirror is imported.
No assertion is a validation gate: normal and python -O run the same checks.

  python3 calculation/agent-107/period4_quotient.py check
  python3 calculation/agent-107/period4_quotient.py witnesses
"""

import argparse
from functools import lru_cache
import importlib.util
from itertools import permutations
import json
from pathlib import Path
import sys


BASE = 10
MODULUS = 101
PERIOD = 4
WIDTH = 16
NEUTRAL = 9
SCHEMA = "p196-period4-mod101-v1"


def _require(condition, message):
    if not condition:
        raise ValueError(message)


def _integer(value, label):
    _require(type(value) is int, label + " must be an integer, excluding bool")
    return value


def _sequence(value, length, label):
    _require(type(value) in (list, tuple), label + " must be a list or tuple")
    _require(len(value) == length, label + " has the wrong length")
    return value


def _word(word):
    _require(type(word) in (list, tuple), "word must be a list or tuple")
    for coefficient in word:
        _integer(coefficient, "coefficient")
        _require(0 <= coefficient <= 18, "coefficient must lie in [0,18]")
    return tuple(word)


def _vector(vector, label):
    _sequence(vector, PERIOD, label)
    return tuple(_integer(x, label + " entry") for x in vector)


def _matrix(matrix, label):
    _sequence(matrix, PERIOD, label)
    return tuple(_vector(row, label + " row") for row in matrix)


@lru_cache(maxsize=1)
def _mirror():
    path = Path(__file__).resolve().parents[1] / "neutral_band_search.py"
    spec = importlib.util.spec_from_file_location("agent107_period4_mirror", path)
    _require(spec is not None and spec.loader is not None,
             "cannot load the unchanged A120 Python mirror")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def moments(word):
    """Four exact centered coefficient sums; no modular reduction."""
    word = _word(word)
    result = [0] * PERIOD
    for j, coefficient in enumerate(word):
        result[j % PERIOD] += coefficient - NEUTRAL
    return tuple(result)


def charge(word, weights, modulus=MODULUS):
    """S_w; the optional modulus is useful for the old mod11 control."""
    weights = _vector(weights, "weights")
    _integer(modulus, "modulus")
    _require(modulus >= 2, "modulus must be at least 2")
    return sum(w * s for w, s in zip(weights, moments(word))) % modulus


def residual11(word):
    word = _word(word)
    alt = sum((1 if j % 2 == 0 else -1) * x for j, x in enumerate(word))
    return (alt - (1 if len(word) % 2 == 0 else -1)) % 11


def make_pair(j):
    """Return the two source words for j=2,3,4,5, as immutable tuples."""
    _integer(j, "j")
    _require(2 <= j <= 5, "j must be one of 2,3,4,5")
    left = [1] * WIDTH
    left[0] = 2
    left[j] = left[j + 4] = 5
    left[j + 8] = 4
    right = list(left)
    right[j], right[j + 4] = 10, 0
    return tuple(left), tuple(right)


def raw_exterior(word):
    """An actual untrimmed mirror edge, with a compatible one-cell center.

    For e=0 use C=[18], and for e=1 use C=[0]. Either choice gives e2=1-e.
    This helper checks source Hyp and edgeOK; it need not preserve target
    Hyp on arbitrary inputs. The finite certificate checks target Hyp too.
    """
    word = _word(word)
    _require(not word or word[0] != 0, "nonempty exterior must have positive head")
    mirror = _mirror()
    source = list(word)
    e = mirror.e1(BASE, source)
    _require(type(e) is int and e in (0, 1), "non-bit exterior carry")
    center = [18] if e == 0 else [0]
    e2 = mirror.e2(BASE, source, center)
    g = mirror.gam(BASE, source, center)
    _require(e2 == 1 - e and type(g) is int and g in (0, 1),
             "inconsistent complementary carry or overflow")
    target = mirror.nextB(BASE, source, center)
    next_center = mirror.nextC(BASE, source, center)
    _word(target)
    _word(next_center)
    edge = (source, center, target, next_center, 0, 0)
    _require(mirror.hyp(BASE, source, center), "source fails A120 Hyp")
    _require(mirror.edgeOK(BASE, edge), "raw edge fails unchanged A120 edgeOK")
    return {
        "B": source, "C": center, "B2": target, "C2": next_center,
        "e": e, "e2": e2, "g": g, "u": 0, "v": 0,
        "source_R11": residual11(source), "target_R11": residual11(target),
        "source_moments": list(moments(source)),
        "target_moments": list(moments(target)), "mirror_edge_ok": True,
    }


def determinant4(matrix):
    """Exact integer determinant by the 24-term permutation formula."""
    matrix = _matrix(matrix, "matrix")
    result = 0
    for permutation in permutations(range(PERIOD)):
        inversions = sum(permutation[i] > permutation[j]
                         for i in range(PERIOD) for j in range(i + 1, PERIOD))
        term = -1 if inversions % 2 else 1
        for i, j in enumerate(permutation):
            term *= matrix[i][j]
        result += term
    return result


def inverse4_mod101(matrix):
    """Gauss-Jordan construction; validation separately multiplies the inverse."""
    matrix = _matrix(matrix, "matrix")
    rows = [[x % MODULUS for x in row] + [int(i == j) for j in range(PERIOD)]
            for i, row in enumerate(matrix)]
    for column in range(PERIOD):
        pivot = next((i for i in range(column, PERIOD) if rows[i][column]), None)
        _require(pivot is not None, "matrix is singular modulo101")
        rows[column], rows[pivot] = rows[pivot], rows[column]
        scale = pow(rows[column][column], -1, MODULUS)
        rows[column] = [(x * scale) % MODULUS for x in rows[column]]
        for i in range(PERIOD):
            if i != column:
                factor = rows[i][column]
                rows[i] = [(x - factor * y) % MODULUS
                           for x, y in zip(rows[i], rows[column])]
    _require(all(rows[i][j] == int(i == j)
                 for i in range(PERIOD) for j in range(PERIOD)),
             "Gauss-Jordan reduction did not produce an identity")
    return [row[PERIOD:] for row in rows]


def _validate_edge(edge, label):
    _require(type(edge) is dict, label + " must be an object")
    required = {"B", "C", "B2", "C2", "e", "e2", "g", "u", "v",
                "source_R11", "target_R11", "source_moments", "target_moments",
                "mirror_edge_ok"}
    _require(set(edge) == required, label + " has missing or unknown fields")
    for name in ("B", "C", "B2", "C2"):
        _word(edge[name])
    for name in ("e", "e2", "g", "u", "v", "source_R11", "target_R11"):
        _integer(edge[name], label + "." + name)
    _vector(edge["source_moments"], label + ".source_moments")
    _vector(edge["target_moments"], label + ".target_moments")
    _require(edge["mirror_edge_ok"] is True, label + " lacks the positive edge flag")
    _require(len(edge["B"]) == WIDTH and len(edge["B2"]) == WIDTH,
             label + " must have width16 at both ends")
    _require(edge["B"][0] > 0 and edge["B2"][0] > 0,
             label + " has a zero head")
    _require(edge["C"] == [18] and edge["C2"] == [16],
             label + " has the wrong concrete center edge")
    _require((edge["e"], edge["e2"], edge["g"], edge["u"], edge["v"])
             == (0, 1, 0, 0, 0), label + " changes the retained edge data")
    _require(edge["source_R11"] == 0 and edge["target_R11"] == 0,
             label + " fails the strong alternating residue filter")
    expected = raw_exterior(edge["B"])
    for name in required:
        _require(edge[name] == expected[name], label + "." + name + " fails replay")
    _require(_mirror().hyp(BASE, edge["B2"], edge["C2"]),
             label + " target fails A120 Hyp")


def validate_certificate(data):
    """Validate supplied evidence in full; malformed/corrupt data raise ValueError.

    This checks the submitted outputs, collision rows, determinant and both
    inverse products. It does not replace them with freshly generated data.
    """
    _require(type(data) is dict, "certificate must be an object")
    required = {"schema", "base", "modulus", "width", "period", "pairs",
                "matrix", "determinant", "determinant_mod", "inverse_mod", "rank"}
    _require(set(data) == required, "certificate has missing or unknown fields")
    _require(data["schema"] == SCHEMA, "unsupported certificate schema")
    for name, expected in (("base", BASE), ("modulus", MODULUS),
                           ("width", WIDTH), ("period", PERIOD), ("rank", PERIOD)):
        _require(_integer(data[name], name) == expected, "wrong " + name)
    _sequence(data["pairs"], PERIOD, "pairs")
    rows = []
    natural_differences = []
    alternating_differences = []
    for j, pair in zip(range(2, 6), data["pairs"]):
        _require(type(pair) is dict, "pair must be an object")
        _require(set(pair) == {"j", "left", "right", "input_moments", "difference"},
                 "pair has missing or unknown fields")
        _require(_integer(pair["j"], "j") == j, "pair indices must be 2,3,4,5")
        _validate_edge(pair["left"], "pair%d.left" % j)
        _validate_edge(pair["right"], "pair%d.right" % j)
        left, right = pair["left"], pair["right"]
        generated = make_pair(j)
        _require(tuple(left["B"]) == generated[0] and tuple(right["B"]) == generated[1],
                 "source pair is not the stated finite witness")
        common = _vector(pair["input_moments"], "input_moments")
        _require(common == moments(left["B"]) == moments(right["B"]),
                 "source moments do not agree")
        difference = tuple(y - x for x, y in
                           zip(moments(left["B2"]), moments(right["B2"])))
        _require(_vector(pair["difference"], "difference") == difference,
                 "stored target difference is incorrect")
        expected = [0] * PERIOD
        expected[(j - 1) % PERIOD] += 1
        expected[j % PERIOD] -= 20
        expected[(j + 1) % PERIOD] += 1
        _require(difference == tuple(expected), "local carry-defect formula failed")
        rows.append(difference)
        natural_differences.append(sum(x * y for x, y in
                                       zip(difference, (1, 10, 100, 91))) % MODULUS)
        alternating_differences.append(sum(x * y for x, y in
                                           zip(difference, (1, -1, 1, -1))) % 11)

    matrix = _matrix(data["matrix"], "matrix")
    _require(matrix == tuple(rows), "matrix is not the checked collision matrix")
    determinant = determinant4(matrix)
    _require(_integer(data["determinant"], "determinant") == determinant == 158400,
             "wrong exact determinant")
    _require(_integer(data["determinant_mod"], "determinant_mod")
             == determinant % MODULUS == 32, "wrong determinant residue")
    inverse = _matrix(data["inverse_mod"], "inverse_mod")
    _require(all(0 <= x < MODULUS for row in inverse for x in row),
             "inverse entries must be canonical residues modulo101")
    for first, second in ((matrix, inverse), (inverse, matrix)):
        for i in range(PERIOD):
            for j in range(PERIOD):
                product = sum(first[i][k] * second[k][j] for k in range(PERIOD))
                _require(product % MODULUS == int(i == j),
                         "submitted inverse fails a matrix product")
    _require(natural_differences == [20, 99, 81, 2],
             "natural mod101 weight control failed")
    _require(alternating_differences == [0, 0, 0, 0],
             "old alternating mod11 control failed")
    return {
        "schema": SCHEMA, "base": BASE, "modulus": MODULUS,
        "width": WIDTH, "period": PERIOD, "matrix": [list(row) for row in matrix],
        "determinant": determinant, "determinant_mod": determinant % MODULUS,
        "inverse_mod": [list(row) for row in inverse], "rank": PERIOD,
        "natural_weight": [1, 10, 100, 91],
        "natural_output_differences": natural_differences,
        "alternating_mod11_output_differences": alternating_differences,
        "checks": {"pairs": PERIOD, "mirror_edges": 2 * PERIOD,
                   "source_target_hyp": 4 * PERIOD, "strong_R11": 4 * PERIOD,
                   "equal_input_moments": PERIOD, "target_difference_rows": PERIOD,
                   "inverse_product_entries": 2 * PERIOD * PERIOD},
        "scope": "Only zero fixed period-4 linear scalar charge modulo101 has a "
                 "deterministic next-charge law on all legal decimal exterior edges "
                 "when width, e, g and trims are retained; not a cycle-existence result.",
    }


verify_certificate = validate_certificate


def build_certificate():
    pairs = []
    for j in range(2, 6):
        left_source, right_source = make_pair(j)
        left, right = raw_exterior(left_source), raw_exterior(right_source)
        pairs.append({
            "j": j, "left": left, "right": right,
            "input_moments": list(moments(left_source)),
            "difference": [y - x for x, y in
                           zip(left["target_moments"], right["target_moments"])],
        })
    matrix = [pair["difference"][:] for pair in pairs]
    determinant = determinant4(matrix)
    result = {
        "schema": SCHEMA, "base": BASE, "modulus": MODULUS,
        "width": WIDTH, "period": PERIOD, "pairs": pairs, "matrix": matrix,
        "determinant": determinant, "determinant_mod": determinant % MODULUS,
        "inverse_mod": inverse4_mod101(matrix), "rank": PERIOD,
    }
    validate_certificate(result)
    return result


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("check", "witnesses"))
    args = parser.parse_args(argv)
    try:
        certificate = build_certificate()
        summary = validate_certificate(certificate)
        if args.command == "check":
            result = {"status": "PASS", **summary}
        else:
            result = {"status": "PASS", "certificate": certificate,
                      "checks": summary["checks"], "scope": summary["scope"]}
        print(json.dumps(result, sort_keys=True, separators=(",", ":")))
        return 0
    except (ValueError, OSError) as error:
        print(json.dumps({"status": "ERROR", "error": str(error)}, sort_keys=True))
        return 2


if __name__ == "__main__":
    sys.exit(main())
