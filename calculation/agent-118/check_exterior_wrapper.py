#!/usr/bin/env python3
"""Reproduce the 13 protocol fixtures for the exterior resource wrapper.

These are synthetic completion-message controls, not mathematical search
results.  The wrapper's subprocess call is replaced only inside this process;
no executable is launched and no resource-limit callback is applied.
"""
from __future__ import annotations

import contextlib
import importlib.util
import io
import json
from pathlib import Path
import subprocess
import sys


def main() -> None:
    path = Path(__file__).with_name("run_exterior_regular.py")
    spec = importlib.util.spec_from_file_location("wrapper_guard_control", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load exterior wrapper")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    valid = ("BREG_DONE status=known_drivers_only mode=forward "
             "scope=all_G_all_widths cycle_start=6 period=1 "
             "terminal_checks=8 known_seen=1\n")
    back = ("BREG_DONE status=known_drivers_only mode=backward "
            "scope=all_G_all_widths fixed_at=6 final_index=7 "
            "first_intersection_empty=1 terminal_seed_excludes_known=1 "
            "residue_seed=0\n")
    new = ("BREG_DONE status=new_driver mode=forward scope=all_G_all_widths "
           "width=53 blocks=3 verified=1\n")
    witness = "BREG_WITNESS verified=1 width=53 blocks=3 period=12\n"
    # name, wrapper flags, stdout, stderr, simulated process exit, expected wrapper exit
    cases = [
        ("valid_protocol", [], valid, "", 0, 0),
        ("bad_scope", [], valid.replace("all_G_all_widths", "fixed_G_control"), "", 0, 2),
        ("bad_mode", [], valid.replace("mode=forward", "mode=backward"), "", 0, 2),
        ("missing_checks", [], valid.replace("terminal_checks=8", "terminal_checks=7"), "", 0, 2),
        ("missing_witness", [], new, "", 0, 2),
        ("mismatched_witness", [], witness.replace("width=53", "width=52") + new, "", 0, 2),
        ("valid_witness_protocol", [], witness + new, "", 0, 0),
        ("completion_plus_cap", [], valid, "UNDECIDED cap\n", 2, 2),
        ("duplicate_completion", [], valid + valid, "", 0, 2),
        ("valid_backward_protocol", ["--backward"], back, "", 0, 0),
        ("bad_backward_index", ["--backward"], back.replace("final_index=7", "final_index=6"), "", 0, 2),
        ("missing_residue_flag", ["--backward", "--residue-seed"], back, "", 0, 2),
        ("fixed_control_promoted", ["--fixed-blocks", "3"], valid, "", 0, 2),
    ]
    original_run = module.subprocess.run
    original_argv = sys.argv[:]
    try:
        for name, args, stdout, stderr, returncode, expected in cases:
            module.subprocess.run = lambda *a, **k: subprocess.CompletedProcess(
                a[0], returncode, stdout, stderr)
            sys.argv = ["wrapper", "/tmp/protocol-fixture", *args]
            captured = io.StringIO()
            with contextlib.redirect_stdout(captured):
                actual = module.main()
            result = json.loads(captured.getvalue())
            if actual != expected:
                raise AssertionError((name, result))
            if expected == 2 and result["status"] != "UNDECIDED":
                raise AssertionError((name, result))
        print(json.dumps({
            "wrapper_protocol_cases": len(cases),
            "valid_fixture_controls": sum(case[-1] == 0 for case in cases),
            "rejected_incomplete_or_wrong_scope": sum(case[-1] == 2 for case in cases),
            "status": "PASS",
        }))
    finally:
        module.subprocess.run = original_run
        sys.argv = original_argv


if __name__ == "__main__":
    main()
