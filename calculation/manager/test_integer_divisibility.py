#!/usr/bin/env python3
"""Source positives, short Q-consistent obstructions, caps, and -O controls."""
from __future__ import annotations

import copy
from fractions import Fraction
import json
from pathlib import Path
import random
import subprocess
import sys
import tempfile
from unittest.mock import patch

import center_itinerary as compiler
import integer_divisibility as producer
import integer_divisibility_check as checker
from test_center_itinerary import (
    assignment_satisfies, check_positive, need, source_fixtures,
)


def abstract_system(coefficients, rhs):
    n = len(coefficients[0])
    return {"format": "p196-center-affine-v1", "variables": [f"x{i}" for i in range(n)],
            "target_base": 10, "itinerary": {}, "inequalities": [],
            "equalities": [{"label": f"row{i}", "coefficients": row[:], "rhs": value, "origin": {}}
                           for i, (row, value) in enumerate(zip(coefficients, rhs))]}


def satisfies_equalities(system, values):
    return all(sum(a*x for a, x in zip(row["coefficients"], values)) == row["rhs"]
               for row in system["equalities"])


def rejects(action, errors=(producer.InvalidInput, producer.UnsupportedInput)):
    try:
        action()
    except errors:
        return
    raise RuntimeError("malformed/unsupported input was accepted")


def short_subsystem_controls(fixtures):
    details = []
    for base in (20, 26):
        fixture = next(f for f in fixtures if f["base"] == base)
        full = compiler.compile_system(fixture["itinerary"], 10)
        result = producer.find_certificate(full)
        proof = result["certificate"]
        need(checker.verify(full, proof), "independent full-system integer proof")
        indices = result["nonzero_row_indices"]
        # The selected original rows alone are rationally consistent. The
        # extension therefore proves more than a disguised rational identity.
        subsystem = copy.deepcopy(full)
        subsystem["equalities"] = [full["equalities"][i] for i in indices]
        subsystem["inequalities"] = []
        short_proof = copy.deepcopy(proof)
        short_proof["multipliers"] = [proof["multipliers"][i] for i in indices]
        need(checker.verify(subsystem, short_proof), "short-subsystem independent proof")
        values = [Fraction(0)] * len(full["variables"])
        values[-1] = Fraction(10)
        if base == 20:
            values[0] = Fraction(431, 32)
            need(indices == [0, 28] and short_proof["multipliers"] == [1, 93], "base20 row support")
            need(proof["combined_coefficients"] == [64] + [0]*13 and
                 proof["combined_rhs"] == 862 and proof["coefficient_gcd"] == 64, "base20 identity")
        else:
            values[0], values[1] = Fraction(12), Fraction(76, 11)
            need(indices == [0, 3, 6] and short_proof["multipliers"] == [-1, 1, 9], "base26 row support")
            need(proof["combined_coefficients"] == [0, 11, 0] and
                 proof["combined_rhs"] == 76 and proof["coefficient_gcd"] == 11, "base26 identity")
        need(satisfies_equalities(subsystem, values), "explicit rational subsystem solution")
        need(compiler.rational_contradiction(subsystem)["status"] == "NO_RATIONAL_EQUALITY_CONTRADICTION",
             "short subsystem unexpectedly inconsistent over Q")
        details.append({"source_base": base, "row_indices": indices,
                        "gcd": proof["coefficient_gcd"], "rhs": proof["combined_rhs"]})
    return details


def incompleteness_controls():
    # Forward elimination does not revisit the x pivot after introducing y.
    # This system is integer-inconsistent, but this producer does not find it.
    system = abstract_system([[2, 1], [0, 1]], [0, 1])
    result = producer.find_certificate(system)
    need(result["status"] == "NO_DIVISIBILITY_CERTIFICATE_FOUND", "honest incomplete status")
    missed = {"format": "p196-integer-row-divisibility-v1", "multipliers": [1, -1],
              "combined_coefficients": [2, 0], "combined_rhs": -1, "coefficient_gcd": 2}
    need(checker.verify(system, missed), "independent proof of deliberately missed integer conflict")
    need(satisfies_equalities(system, [Fraction(-1, 2), 1]), "missed-system rational solution")
    # Integer equality feasibility also says nothing about domain inequalities.
    out_of_domain = {"format": "p196-center-itinerary-v1", "symmetry": "required",
                     "phases": [{"width": 1, "carry": [0, 1], "overflow": 0, "trim": 0}]}
    system = compiler.compile_system(out_of_domain, 10)
    need(producer.find_certificate(system)["status"] == "NO_DIVISIBILITY_CERTIFICATE_FOUND",
         "domain case status")
    need(satisfies_equalities(system, [20, 10]) and not assignment_satisfies(system, [20, 10]),
         "integer equality solution must still violate a digit/coefficient constraint")
    # gcd=0 conflicts remain the separate rational certificate format.
    system = abstract_system([[0, 0]], [1])
    result = producer.find_certificate(system)
    need(result["status"] == "NO_DIVISIBILITY_CERTIFICATE_FOUND" and
         result["zero_coefficient_nonzero_rhs_rows_seen"] == 1, "zero-gcd format separation")
    return 3


def producer_guards(system):
    mutations = [lambda s: s.update(format="wrong"), lambda s: s.update(target_base=True),
                 lambda s: s.update(target_base=1), lambda s: s.update(itinerary=[]),
                 lambda s: s.update(variables=["same"]*len(s["variables"])),
                 lambda s: s["equalities"][0].update(coefficients=[]),
                 lambda s: s["equalities"][0]["coefficients"].__setitem__(0, True),
                 lambda s: s["equalities"][0]["coefficients"].__setitem__(0, 64.0),
                 lambda s: s["equalities"][0].update(rhs="-68"),
                 lambda s: s["equalities"][0].update(origin=None)]
    for mutate in mutations:
        changed = copy.deepcopy(system)
        mutate(changed)
        rejects(lambda: producer.find_certificate(changed))
    for cap in (True, 1.0, 0, -1, producer.MAX_OPERATIONS+1):
        rejects(lambda: producer.find_certificate(system, cap))
    need(producer.find_certificate(system, 1)["status"] == "RESOURCE_LIMIT_UNDECIDED", "operation cap")
    with patch.object(producer, "MAX_INTERMEDIATE_BITS", 1):
        need(producer.find_certificate(system)["status"] == "RESOURCE_LIMIT_UNDECIDED", "bit cap")
    return len(mutations)+5


def cli_controls(negative, positive):
    runs = 0
    with tempfile.TemporaryDirectory() as temp:
        directory = Path(temp)
        source, proof = directory/"system.json", directory/"proof.json"
        for flags in ([], ["-O"]):
            command = [sys.executable, *flags, str(Path(producer.__file__)), str(source), "--proof", str(proof)]
            source.write_text(json.dumps(negative))
            good = subprocess.run(command, capture_output=True, text=True)
            need(good.returncode == 0 and checker.verify(negative, json.loads(proof.read_text())),
                 "negative CLI proof: "+good.stdout+good.stderr)
            accepted_proof = proof.read_text()
            runs += 1
            for bad in ('{}', '{"format":"x","format":"y"}', '{"x":NaN}', '['*1200+'0'+']'*1200):
                source.write_text(bad)
                proof.write_text(accepted_proof)
                rejected = subprocess.run(command, capture_output=True, text=True)
                need(rejected.returncode == 2, "malformed CLI failure")
                need(json.loads(proof.read_text())["format"] == "p196-no-divisibility-certificate",
                     "invalid input left a stale proof")
                runs += 1
            source.write_text(json.dumps(negative))
            proof.write_text(accepted_proof)
            limited = subprocess.run(command+["--max-operations", "1"], capture_output=True, text=True)
            need(limited.returncode == 3 and json.loads(limited.stdout)["status"] == "RESOURCE_LIMIT_UNDECIDED",
                 "CLI operation cap")
            need(json.loads(proof.read_text())["format"] == "p196-no-divisibility-certificate", "cap stale proof")
            runs += 1
            source.write_text(json.dumps(positive))
            proof.write_text(accepted_proof)
            clean = subprocess.run(command, capture_output=True, text=True)
            need(clean.returncode == 0 and json.loads(clean.stdout)["status"] == "NO_DIVISIBILITY_CERTIFICATE_FOUND",
                 "positive CLI status")
            need(json.loads(proof.read_text())["format"] == "p196-no-divisibility-certificate", "positive stale proof")
            runs += 1
        original = source.read_bytes()
        same = subprocess.run([sys.executable, str(Path(producer.__file__)), str(source), "--proof", str(source)],
                              capture_output=True, text=True)
        need(same.returncode == 2 and source.read_bytes() == original, "same path corrupted source")
        linked = directory/"hardlink.json"
        linked.hardlink_to(source)
        alias = subprocess.run([sys.executable, str(Path(producer.__file__)), str(source), "--proof", str(linked)],
                               capture_output=True, text=True)
        need(alias.returncode == 2 and source.read_bytes() == original, "hardlink alias corrupted source")
    return runs+2


def worker():
    fixtures = source_fixtures()
    positive_edges = negatives = 0
    systems = {}
    for fixture in fixtures:
        base = fixture["base"]
        positive_edges += check_positive(fixture)
        system = compiler.compile_system(fixture["itinerary"], base)
        before = copy.deepcopy(system)
        initial = fixture["centers"][0]
        need(assignment_satisfies(system, initial[:(len(initial)+1)//2]+[base]), "source positive assignment")
        need(producer.find_certificate(system)["status"] == "NO_DIVISIBILITY_CERTIFICATE_FOUND", "positive contradicted")
        need(system == before, "producer mutated its input")
        systems[base] = system
        if base != 10:
            frozen = compiler.compile_system(fixture["itinerary"], 10)
            proof = producer.find_certificate(frozen)["certificate"]
            need(checker.verify(frozen, proof), "independent frozen-to-decimal certificate")
            negatives += 1
    # Distinct signed/unit pivots on systems with a known integer solution.
    rng = random.Random(196)
    for _ in range(60):
        n, count = rng.randrange(1, 7), rng.randrange(1, 10)
        values = [rng.randrange(-4, 5) for _ in range(n)]
        coefficients = [[rng.randrange(-4, 5) for _ in range(n)] for _ in range(count)]
        system = abstract_system(coefficients, [sum(a*x for a, x in zip(row, values)) for row in coefficients])
        need(producer.find_certificate(system)["status"] == "NO_DIVISIBILITY_CERTIFICATE_FOUND",
             "known integer solution contradicted")
    negative = compiler.compile_system(next(f["itinerary"] for f in fixtures if f["base"] == 20), 10)
    return {"positive_bases": [f["base"] for f in fixtures], "positive_center_edges": positive_edges,
            "independently_verified_frozen_decimal_divisibility_proofs": negatives,
            "rationally_consistent_short_subsystems": short_subsystem_controls(fixtures),
            "no_conclusion_controls": incompleteness_controls(), "generated_integer_solution_controls": 60,
            "malformed_api_cases": producer_guards(negative), "normal_optimized_cli_runs": cli_controls(negative, systems[10])}


if __name__ == "__main__":
    if "--worker" in sys.argv:
        print(json.dumps(worker(), sort_keys=True))
    else:
        results = []
        for flags in ([], ["-O"]):
            run = subprocess.run([sys.executable, *flags, __file__, "--worker"], capture_output=True, text=True)
            need(run.returncode == 0, run.stdout+run.stderr)
            results.append(run.stdout)
        need(results[0] == results[1], "normal/optimized producer results differ")
        print(results[0], end="")
        print("NORMAL_AND_OPTIMIZED_IDENTICAL True")
