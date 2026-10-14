"""Exact two-step classification of variable-exterior overlap gates.

Every affine run calculation covers all r=k+5, k>=0.  The exceptional
spacers r=1,...,4 are evaluated independently by ordinary integer arithmetic.
There is no claim of an infinite safe orbit or an unbounded search horizon.
"""
from __future__ import annotations

import csv
from collections import Counter, defaultdict
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[3]
sys.path[:0] = [str(ROOT / "main_existence_attempt/smart_pass/collision"),
               str(ROOT / "main_existence_attempt/correlation_pass/constructive")]
import orthant_runs as run
from seam_overlap import canonical, literal_step, realize
from variable_overlap import shifted_double

HERE = Path(__file__).resolve().parent
ONE = run.Length((0,), 1)
GAP = run.Length((1,), 5)


def size(q):
    return run.Length((sum(n.coefficients[0] for _, n in q),),
                      sum(n.constant for _, n in q))


def phi(q, shift):
    assert shift >= 0
    z = (0, run.Length((0,), shift))
    return run.add_runs(run.canon(q+[z]), run.canon([z]+q))



def component(p, u, v):
    return run.canon([(p, ONE), (0, GAP), (u, ONE),
                      (v, run.Length((0,), 2)), (u, ONE), (0, GAP), (p, ONE)])


def safe(q):
    present = [x for x, length in q if length.positive()]
    assert len(present) == len(q)
    return not (all(x <= 9 for x in present)
                or (q[0][0] == 11 and all(x in (0, 11) for x in present)))


def classify(p, u, v):
    a, q = component(p, u, v), phi(component(p, u, v), 1)
    all_a, all_q = [a], [q]
    clocks_a, clocks_q, closed, shifts, safety = [], [], [], [], []
    for t in range(2):
        safety.append(safe(q))
        a, ha = run.step(a)
        q, hq = run.step(q)
        clocks_a.append(ha)
        clocks_q.append(hq)
        delta = size(q)-size(a)
        assert delta.coefficients == (0,)
        shift = delta.constant
        shifts.append(shift)
        closed.append(shift >= 0 and q == phi(a, shift))
        all_a.append(a)
        all_q.append(q)
    return {
        "p": p, "u": u, "v": v,
        "clock_a": "".join(map(str, clocks_a)),
        "clock_q": "".join(map(str, clocks_q)),
        "closed_1": int(closed[0]), "closed_2": int(closed[1]),
        "shift_1": shifts[0], "shift_2": shifts[1],
        "safe_1": int(safety[0]), "safe_2": int(safety[1]),
    }, all_a, all_q


def finite_classify(p, u, v, r):
    a = (p,)+(0,)*r+(u,v,v,u)+(0,)*r+(p,)
    q = shifted_double(a, 1)
    assert canonical(a) and canonical(q)
    clocks_a, clocks_q, closed, shifts, safety = [], [], [], [], []
    for _ in range(2):
        n = realize(q)
        out = n + int(str(n)[::-1])
        safety.append(str(out) != str(out)[::-1])
        na, nq = literal_step(a), literal_step(q)
        clocks_a.append(len(na)-len(a))
        clocks_q.append(len(nq)-len(q))
        a, q = na, nq
        shift = len(q)-len(a)
        shifts.append(shift)
        closed.append(shift >= 0 and q == shifted_double(a, shift))
    return {
        "p": p, "u": u, "v": v,
        "clock_a": "".join(map(str, clocks_a)),
        "clock_q": "".join(map(str, clocks_q)),
        "closed_1": int(closed[0]), "closed_2": int(closed[1]),
        "shift_1": shifts[0], "shift_2": shifts[1],
        "safe_1": int(safety[0]), "safe_2": int(safety[1]),
    }


def main():
    rows = []
    exceptions = []
    examples = {}
    controls = 0
    late_returns = defaultdict(list)
    all_returns = defaultdict(list)
    for p in range(1, 19):
        for u in range(1, 19):
            for v in range(10):
                if u+v > 18:
                    continue
                row, aa, qq = classify(p, u, v)
                rows.append(row)
                signature = tuple(row[k] for k in row if k not in ("p","u","v"))
                if signature not in examples:
                    examples[signature] = {"case": [p,u,v],
                        "A": [run.as_json(a) for a in aa],
                        "Q": [run.as_json(q) for q in qq], "summary": row}
                for r in (1, 2, 3, 4, 5, 9):
                    literal = finite_classify(p,u,v,r)
                    controls += 1
                    if r >= 5:
                        assert literal == row, (p,u,v,r,row,literal)
                        for t in range(3):
                            a = tuple(run.expand(aa[t], (r-5,)))
                            q = tuple(run.expand(qq[t], (r-5,)))
                            assert canonical(a) and canonical(q)
                            if t:
                                assert literal_step(tuple(run.expand(aa[t-1], (r-5,)))) == a
                                assert literal_step(tuple(run.expand(qq[t-1], (r-5,)))) == q
                    elif literal != row:
                        exceptions.append({"r": r, "bulk": row, "exception": literal})
                if row["closed_2"]:
                    all_returns[p].append([u,v])
                    if not row["closed_1"]:
                        late_returns[p].append([u,v])

    with (HERE / "padded_core_cases.csv").open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    result = {
        "status": "complete exact two-step class; no infinite recurrence asserted",
        "parameter_domain": {"p": "1..18", "u": "1..18", "v": "0..9",
                             "constraint": "u+v<=18", "r": "every integer >=1"},
        "affine_domain": "r=5+k for every k>=0",
        "exact_affine_cases": len(rows),
        "independent_literal_parameter_instances": controls,
        "small_spacer_exceptions": exceptions,
        "number_of_small_spacer_exceptions": len(exceptions),
        "two_step_returns_by_p": dict(all_returns),
        "genuine_delayed_returns_by_p": dict(late_returns),
        "genuine_delayed_returns_safe_through_return": [r for r in rows
            if r["closed_2"] and not r["closed_1"] and r["safe_1"] and r["safe_2"]],
        "signature_examples": list(examples.values()),
        "case_table_sha256": hashlib.sha256((HERE/"padded_core_cases.csv").read_bytes()).hexdigest(),
        "affine_engine_sha256": hashlib.sha256(Path(run.__file__).read_bytes()).hexdigest(),
        "infinite_safety": False,
    }
    (HERE / "padded_core_classification.json").write_text(json.dumps(result, indent=2)+'\n')
    compact = {k: result[k] for k in ("status","exact_affine_cases",
               "independent_literal_parameter_instances","number_of_small_spacer_exceptions",
               "genuine_delayed_returns_by_p","case_table_sha256")}
    print(json.dumps(compact, indent=2))


if __name__ == '__main__':
    main()
