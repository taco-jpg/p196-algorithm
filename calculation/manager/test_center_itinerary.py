#!/usr/bin/env python3
"""Source positives, separate scalar-row oracle, guards, and optimized controls.

The scalar oracle never uses compiler expressions or elimination. It evaluates
one complete numeric frozen trajectory, retaining every constraint by label.
An affine basis comparison checks every generated matrix coefficient exactly.
Whole-integer normalization separately checks genuine positive center orbits.
"""
from __future__ import annotations

import copy
import json
from pathlib import Path
import random
import subprocess
import sys
import tempfile
from unittest.mock import patch

import center_itinerary as compiler
import row_contradiction_check as checker

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "calculation"))
import neutral_band_search as mirror


def need(condition, message):
    if not condition:
        raise RuntimeError(message)


def value(base, word):
    return sum(coefficient * base**j for j, coefficient in enumerate(word))


def actual_carries(base, word, entering):
    return [(value(base, word[:j]) + entering) // base**j for j in range(len(word) + 1)]


def source_fixtures():
    fixtures = []
    for base, edges in mirror._lean_certs():
        need(mirror.cycleOK(base, edges, edges[0][0], edges[0][1]), "source mirror control")
        phases = []
        for B, C, B2, C2, u, v in edges:
            e = value(base, B) // base**len(B)
            carry = actual_carries(base, C, e)
            g = (value(base, B[::-1]) + carry[-1]) // base**len(B)
            phases.append({"width": len(C), "carry": carry, "overflow": g, "trim": v})
        fixtures.append({"base": base, "itinerary": {"format": "p196-center-itinerary-v1",
                         "symmetry": "required", "phases": phases},
                         "centers": [edge[1] for edge in edges]})
    need(len(fixtures) == 8, "eight established source certificates required")
    for name in ("base20_center_fixture.json", "base10_center_fixture.json"):
        fixtures.append(compiler.load_json(HERE / name))
    return fixtures


def check_positive(fixture):
    base, centers = fixture["base"], fixture["centers"]
    phases = fixture["itinerary"]["phases"]
    need(len(centers) == len(phases), "fixture phase count")
    for t, (C, phase) in enumerate(zip(centers, phases)):
        need(C == C[::-1] and len(C) == phase["width"], "literal symmetric width")
        need(all(type(x) is int and 0 <= x <= 2*base-2 for x in C), "literal coefficient domain")
        e = phase["carry"][0]
        need(actual_carries(base, C, e) == phase["carry"], "actual whole-prefix carries")
        remaining = value(base, C) + e
        digits = []
        for _ in C:
            remaining, d = divmod(remaining, base)
            digits.append(d)
        need(remaining == 1-e, "literal center flip")
        if phase["overflow"]:
            digits.append((base-1)*e)
        raw = [digits[j]+digits[-1-j] for j in range(len(digits))]
        v = phase["trim"]
        if v:
            need(raw[:v] == raw[-v:] == [base-1]*v, "literal neutral boundary")
        target = raw[v:len(raw)-v] if v else raw
        need(target == centers[(t+1) % len(centers)], "literal global seam/closure")
    return len(phases)


def scalar_rows(itinerary, assignment, target_base):
    """Independent matrix-free residuals: equality=0, inequality<=0."""
    phases = itinerary["phases"]
    m0 = phases[0]["width"]
    half, base = assignment[:-1], assignment[-1]
    initial = [half[min(j, m0-1-j)] for j in range(m0)]
    center, result = initial[:], {}
    for t, phase in enumerate(phases):
        k, g, v = phase["carry"], phase["overflow"], phase["trim"]
        normalized = []
        for j, coefficient in enumerate(center):
            digit = coefficient + k[j] - base*k[j+1]
            result[f"p{t}.c{j}.nonnegative"] = -coefficient
            result[f"p{t}.c{j}.bounded"] = coefficient-(2*base-2)
            result[f"p{t}.d{j}.nonnegative"] = -digit
            result[f"p{t}.d{j}.bounded"] = digit-(base-1)
            normalized.append(digit)
        if g:
            normalized.append((base-1)*k[0])
        summed = [normalized[j]+normalized[len(normalized)-j-1] for j in range(len(normalized))]
        for j in range(v):
            result[f"p{t}.trim.left.{j}"] = summed[j]-(base-1)
            right = len(summed)-v+j
            result[f"p{t}.trim.right.{right}"] = summed[right]-(base-1)
        center = summed[v:len(summed)-v] if v else summed
    for j in range(m0):
        result[f"closure.{j}"] = center[j]-initial[j]
    result["target_base"] = base-target_base
    return result


def compare_complete_matrix(system):
    n = len(system["variables"])
    rows = system["equalities"] + system["inequalities"]
    need(len({row["label"] for row in rows}) == len(rows), "unique generated labels")
    zero = scalar_rows(system["itinerary"], [0]*n, system["target_base"])
    need(set(zero) == {row["label"] for row in rows}, "no omitted or extra constraints")
    for row in rows:
        need(-row["rhs"] == zero[row["label"]], "constant term differs from scalar oracle")
    for j in range(n):
        basis = [0]*n
        basis[j] = 1
        direct = scalar_rows(system["itinerary"], basis, system["target_base"])
        for row in rows:
            need(row["coefficients"][j] == direct[row["label"]]-zero[row["label"]],
                 "matrix coefficient differs from scalar oracle")
    return len(rows)*(n+1)


def assignment_satisfies(system, values):
    residual = lambda row: sum(a*b for a,b in zip(row["coefficients"],values))-row["rhs"]
    return (all(residual(row) == 0 for row in system["equalities"]) and
            all(residual(row) <= 0 for row in system["inequalities"]))


def rejects(action, errors=(compiler.InvalidInput, compiler.ResourceLimit)):
    try:
        action()
    except errors:
        return
    raise RuntimeError("malformed/unsupported input was accepted")


def malformed_controls(itinerary):
    mutations = [lambda x: x.update(format="wrong"), lambda x: x.update(symmetry=False),
                 lambda x: x.update(phases=[]), lambda x: x.update(phases=[None]),
                 lambda x: x["phases"][0].update(width=True),
                 lambda x: x["phases"][0].update(width=1.0),
                 lambda x: x["phases"][0].update(width=0),
                 lambda x: x["phases"][0].update(width=511),
                 lambda x: x["phases"][0].update(overflow=True),
                 lambda x: x["phases"][0].update(overflow=2),
                 lambda x: x["phases"][0].update(trim=-1),
                 lambda x: x["phases"][0].update(trim=True),
                 lambda x: x["phases"][0].update(trim=100),
                 lambda x: x["phases"][0].update(carry=[]),
                 lambda x: x["phases"][0]["carry"].__setitem__(1, True),
                 lambda x: x["phases"][0]["carry"].__setitem__(1, 2),
                 lambda x: x["phases"][0]["carry"].__setitem__(-1, x["phases"][0]["carry"][0]),
                 lambda x: x["phases"][0].update(trim=0),
                 lambda x: x.update(phases=x["phases"]*20)]
    for mutate in mutations:
        changed = copy.deepcopy(itinerary)
        mutate(changed)
        rejects(lambda: compiler.compile_system(changed,10))
    for base in (True,10.0,"10",None,1,1<<compiler.MAX_BITS):
        rejects(lambda: compiler.compile_system(itinerary,base))
    return len(mutations)+6


def cli_controls(itinerary):
    with tempfile.TemporaryDirectory() as temp:
        folder = Path(temp)
        inp, system, proof = [folder/name for name in ("in.json","system.json","proof.json")]
        for optimized in ([],["-O"]):
            command=[sys.executable,*optimized,str(Path(compiler.__file__)),str(inp),"--base","10",
                     "--system",str(system),"--proof",str(proof)]
            inp.write_text(json.dumps(itinerary))
            good=subprocess.run(command,capture_output=True,text=True)
            need(good.returncode==0,good.stdout+good.stderr)
            need(checker.verify(checker.read_json(system),checker.read_json(proof)),"CLI proof")
            for bad in ('{}','{"format":"x","format":"y"}','{"x":NaN}'):
                inp.write_text(bad)
                rejected=subprocess.run(command,capture_output=True,text=True)
                need(rejected.returncode==2,"bad CLI did not fail")
                need(json.loads(proof.read_text())["format"]=="p196-no-contradiction-certificate",
                     "early failure left stale proof")
            inp.write_text(json.dumps(itinerary))
            limited=subprocess.run(command+["--max-operations","1"],capture_output=True,text=True)
            need(limited.returncode==3,"resource limit not undecided")
            need(json.loads(proof.read_text())["format"]=="p196-no-contradiction-certificate","stale cap proof")
        with patch.object(compiler,"MAX_FILE_BYTES",2):
            rejects(lambda: compiler.load_json(inp))
    return 10


def worker():
    fixtures=source_fixtures()
    matrix_entries=positive_edges=contradictions=0
    for fixture in fixtures:
        base,it=fixture["base"],fixture["itinerary"]
        positive_edges+=check_positive(fixture)
        system=compiler.compile_system(it,base)
        matrix_entries+=compare_complete_matrix(system)
        initial=fixture["centers"][0]
        values=initial[:(len(initial)+1)//2]+[base]
        need(assignment_satisfies(system,values),"actual positive violates compiled constraints")
        need(compiler.rational_contradiction(system)["status"]=="NO_RATIONAL_EQUALITY_CONTRADICTION",
             "actual positive contradicted")
        if base!=10:
            decimal=compiler.compile_system(it,10)
            result=compiler.rational_contradiction(decimal)
            need(result["status"]=="RATIONAL_EQUALITY_INCONSISTENT","expected frozen decimal contradiction")
            need(checker.verify(decimal,result["certificate"]),"independent multiplier verification")
            contradictions+=1
    rng=random.Random(196)
    for _ in range(50):
        p,m=rng.choice((2,4)),rng.randrange(1,11)
        phases=[]
        for t in range(p):
            e=rng.randrange(2)
            phases.append({"width":m+t,"overflow":1,"trim":p//2 if t==p-1 else 0,
                           "carry":[e]+[rng.randrange(2) for _ in range(m+t-1)]+[1-e]})
        it={"format":"p196-center-itinerary-v1","symmetry":"required","phases":phases}
        matrix_entries+=compare_complete_matrix(compiler.compile_system(it,rng.randrange(2,33)))
    # Equalities have the rational solution C=2b, which violates C<=2b-2.
    # The compiler must not turn absence of an equality contradiction into SAT.
    out_of_domain={"format":"p196-center-itinerary-v1","symmetry":"required",
                   "phases":[{"width":1,"carry":[0,1],"overflow":0,"trim":0}]}
    weak=compiler.compile_system(out_of_domain,10)
    need(compiler.rational_contradiction(weak)["status"]=="NO_RATIONAL_EQUALITY_CONTRADICTION","weak status")
    need(not assignment_satisfies(weak,[20,10]),"domain constraints omitted")
    negatives=malformed_controls(fixtures[-1]["itinerary"])
    cli=cli_controls(fixtures[-2]["itinerary"])
    return {"positive_bases":[f["base"] for f in fixtures],"positive_center_edges":positive_edges,
            "independently_verified_frozen_decimal_contradictions":contradictions,
            "complete_matrix_entries_compared":matrix_entries,"synthetic_itineraries":50,
            "malformed_api_cases":negatives,"normal_optimized_cli_runs":cli,
            "no_equality_contradiction_is_not_feasibility":True}


if __name__=="__main__":
    if "--worker" in sys.argv:
        print(json.dumps(worker(),sort_keys=True))
    else:
        results=[]
        for flags in ([],["-O"]):
            proc=subprocess.run([sys.executable,*flags,__file__,"--worker"],capture_output=True,text=True)
            need(proc.returncode==0,proc.stdout+proc.stderr)
            results.append(proc.stdout)
        need(results[0]==results[1],"normal and optimized results differ")
        print(results[0],end="")
        print("NORMAL_AND_OPTIMIZED_IDENTICAL True")
