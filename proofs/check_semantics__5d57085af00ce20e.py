#!/usr/bin/env python3
"""Small exact arithmetic review controls; not Lean verification."""
from fractions import Fraction
from pathlib import Path
import hashlib
import json
import subprocess

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[4]


def reverse(n):
    return int(str(n)[::-1])


def step(n):
    return n + reverse(n)


def safe(n):
    return n > 0 and n != reverse(n) and step(n) != reverse(step(n))


def target(m):
    return 10**(2*m) + 99*10**(m-1) - 1


def main():
    pins = json.loads((HERE / "source-pins.json").read_text())
    for path, pin in pins.items():
        data = subprocess.check_output(
            ["git", "show", pin["source_commit"] + ":" + path], cwd=REPO)
        assert hashlib.sha256(data).hexdigest() == pin["sha256"]
        if "prior_family_source_commit" in pin:
            old = subprocess.check_output(
                ["git", "show", pin["prior_family_source_commit"] + ":" + path], cwd=REPO)
            assert data == old

    y = target(2)
    full_fiber = [n for n in range(y+1) if safe(n) and step(n) == y]
    expected = [1998,2997,3996,4995,5994,6993,7992,8991,9990]
    assert y == 10989 and safe(y) and full_fiber == expected
    weight_controls = []
    for label, w in [
            ("one_on_Safe_negative_outside", lambda n: Fraction(1) if safe(n) else Fraction(-17)),
            ("reciprocal_on_Safe_negative_outside", lambda n: Fraction(1,n+1) if safe(n) else Fraction(-17))]:
        total = sum((w(n) for n in full_fiber), Fraction(0))
        assert w(y) > 0 and total >= 9*w(y)
        for n in full_fiber:
            assert n < y and w(n) >= w(y)
        weight_controls.append({"label":label,"target_weight":str(w(y)),
                                "full_incoming_sum":str(total),"ratio":str(total/w(y))})
    negative_constants = [-3,-1,0,1,8]
    assert all(Fraction(C) < len(full_fiber) for C in negative_constants)

    exact_size_controls = []
    for m in range(2,13):
        yy, count = target(m), 9*10**(m-2)
        assert 10*yy < 11*10**(2*m)
        assert Fraction(count) == Fraction(9,100)*10**m
        # All quantities are nonnegative: squaring verifies the exact
        # numerical coefficient in the strict square-root comparison.
        square_of_reference = Fraction(81,10000)*Fraction(10,11)*yy
        assert square_of_reference < count*count
        exact_size_controls.append({"m":m,"target":yy,"family_size":count,
                                    "strict_integral_margin":11*10**(2*m)-10*yy,
                                    "squared_reference":str(square_of_reference)})
    assert not 10*target(1) < 11*10**2
    report={"status":"PASS_FINITE_DIAGNOSTICS_ONLY",
            "source_pins_verified":len(pins),"prior_family_sources_byte_identical":True,
            "full_fiber_at_m2":full_fiber,"safe_target":y,
            "weight_controls":weight_controls,"tested_uniform_constants":negative_constants,
            "exact_size_controls":exact_size_controls,
            "excluded_m1_size_bound_fails":True,
            "lean_executed":False,"universal_weight_or_fiber_theorem_proved_by_script":False}
    (HERE/"diagnostics.json").write_text(json.dumps(report,indent=2)+"\n")
    print(json.dumps({"status":report["status"],"complete_m2_safe_fiber_size":len(full_fiber),
                      "exact_size_parameters":[2,12],"float_arithmetic_used":False}))


if __name__ == "__main__":
    main()
