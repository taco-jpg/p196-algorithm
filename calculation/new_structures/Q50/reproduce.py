#!/usr/bin/env python3
"""Repository fixtures for Q50's all-parameter symbolic edge checker.

Run: python3 calculation/new_structures/Q50/reproduce.py
Controls are actual published repository certificates, not new discoveries.
No decimal all-time candidate is currently encoded as a closed phase cycle.
"""
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
spec = importlib.util.spec_from_file_location("universal_edge_verifier", ROOT / "tools/universal_edge_verifier.py")
v = importlib.util.module_from_spec(spec)
spec.loader.exec_module(v)

POSITIVE = [
    "calculation/decimal_frontier/lattice_formats/cert_b9_rec0.json",
    "calculation/decimal_frontier/lattice_formats/cert_b9_rec1.json",
    "calculation/neutral_band/agent10_base50/cert_b50.json",
    "calculation/neutral_band/agent10_base146/cert_b146.json",
]
SLOW = ["calculation/neutral_band/agent10_base1286/cert_b1286.json"]
UNSUPPORTED = [
    "calculation/new_structures/agent-X18/candidate.json",
    "calculation/new_structures/agent-W26/boundary_cocycle_expected.json",
    "calculation/decimal_frontier/lattice_kinks/agent3_cubic_parity/graph_certificate.json",
    "calculation/decimal_frontier/lattice_kinks/agent3_full_boolean/graph_certificate.json",
    "calculation/decimal_frontier/lattice_kinks/agent3_perturbation_radius/graph_certificate.json",
]

def main():
    import sys
    fixtures = POSITIVE + (SLOW if "--slow" in sys.argv else [])
    for rel in fixtures:
        data = v.normalize_json(json.loads((ROOT / rel).read_text()))
        result = v.validate_cycle(data, bigint_widths=(20,40,80,160,200), bigint_cycles=2)
        print("PASS symbolic + actual big integers", rel,
              "phases", result["phases"], "gain", result["gain"],
              "bounds", [x["finite_bound"] for x in result["checks"]])
    # Mutation test on the published base-50 cycle.
    data = v.normalize_json(json.loads((ROOT/POSITIVE[2]).read_text()))
    data["phases"][1]["word"][0]["lit"][7] += 1
    try:
        v.validate_cycle(data,bigint_cycles=0)
    except AssertionError as e:
        assert "WRONG EDGE" in str(e), str(e)
        print("PASS false-edge negative control: reject damaged base50")
    else:
        raise AssertionError("unsound verifier: accepted corrupt template")
    for rel in UNSUPPORTED:
        data=json.loads((ROOT / rel).read_text())
        try:
            v.normalize_json(data)
        except (ValueError, KeyError, AssertionError):
            print("UNSUPPORTED (not a closed symbolic phase-cycle JSON):", rel)
        else:
            raise AssertionError("unexpected phase-cycle in unsupported object: "+rel)
    print("NO BASE-10 CLOSED CERTIFICATE CHECKED: UNDECIDED")

if __name__=="__main__": main()