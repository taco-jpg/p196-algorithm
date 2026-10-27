#!/usr/bin/env python3
"""Pinned P48 application of Agent108's unchanged nonuniform exterior MDD.

Commands: selftest; run [resource options]; check (read {code,records} JSON
from stdin). Selftest performs parser/dependency/known-source controls only.
It never runs a target search. There is no local MDD reimplementation.

The full repeated e/g words have 48 positions; the 24-step seam is not
closed separately. Completed frontiers are reported exactly. Resource caps,
missing records and invalid records do not establish an all-width negative.
FEASIBLE without a valid extracted witness remains exterior-only evidence.
An extracted witness is coupled to the supplied two-lap center and emitted
as a full Python-checked candidate before the summary. Lean remains required.
Permitted phase cuts rotate both input words; candidate rows are always
restored to the original center phase before the independent full-cycle audit.

Example: python3 calculation/agent-115/two_lap_mdd_run.py run --nodes 6000000
         --operations 1000000000 --seconds 240 --gib 4
"""

from __future__ import annotations

import argparse
import hashlib
import importlib
import importlib.util
import json
import math
import os
from pathlib import Path
import resource
import signal
import subprocess
import sys
import tempfile
import time

import two_lap_oracle as oracle


ROOT = Path(__file__).resolve().parents[2]
ENGINE = ROOT / "calculation/agent-108"
COMMIT = "d2c893c8bdc73529358e926ca5e02d68c5f4d528"
PINS = {
    "exterior_run.py": "4ca26c2a06e9fe676acaaa8a89a31fbdd8cba1c0174b5762dd46ed4ae4060fcd",
    "exterior_mdd.cpp": "8ff554326ce139838cd3894b967778ca21c8c9bb8887f5e0216e15e888fb428e",
    "wide_count.hpp": "e032d490d17a0b1cfde12b863b5effb9bb3a4dcb1981a991057f47f1546a5749",
    "saturation_run.py": "aaf162d2a14a44dd7896d8490512c90d79bf98baa6d7562262f7f23f6afb8281",
}
E48 = "010100110100101011001011" * 2
G48 = "110001001000110001001000" * 2
PHASES = (0, 1, 5, 8)


def require(condition, reason):
    if not condition:
        raise ValueError(reason)


def check_dependencies(expected=None):
    expected = PINS if expected is None else expected
    actual = {name: hashlib.sha256((ENGINE / name).read_bytes()).hexdigest() for name in PINS}
    require(actual == expected, "pinned Agent108 dependency hash mismatch")
    return actual


def runner():
    check_dependencies()
    sys.path.insert(0, str(ENGINE))
    module = importlib.import_module("exterior_run")
    require(Path(module.__file__).resolve() == ENGINE / "exterior_run.py", "wrong engine module")
    require(Path(sys.modules["saturation_run"].__file__).resolve() == ENGINE / "saturation_run.py",
            "wrong bounded runner module")
    return module


def mirror():
    path = ROOT / "calculation/neutral_band_search.py"
    spec = importlib.util.spec_from_file_location("a115_mdd_reference_mirror", path)
    require(spec is not None and spec.loader is not None, "mirror unavailable")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def canonical(word, base):
    word = tuple(word)
    while word and word[-1] == base - 1:
        word = word[:-1]
    return word


def rotate(values, shift):
    require(bool(values), "cannot rotate an empty phase sequence")
    shift %= len(values)
    return values[shift:] + values[:shift]


def input_words(shift):
    require(shift in PHASES, "unsupported phase cut")
    return rotate(E48, shift), rotate(G48, shift)


def restore_rows(rows, shift, period):
    require(isinstance(rows, (list, tuple)) and len(rows) == period, "wrong witness phase count")
    return rotate(rows, -shift)


def couple(base, phases, centers, vs, e, g):
    """Independently derive each canonical natural trim from raw_B and B2."""
    period = len(e)
    require(period > 0 and len(phases) == len(centers) == len(vs) == len(g) == period,
            "wrong full-cycle phase count")
    phases = [tuple(row) for row in phases]
    for row in phases:
        require(all(type(x) is int and 0 <= x <= 2 * base - 2 for x in row), "bad B coefficient")
        require(canonical(row, base) == row, "B witness is not canonically trimmed")
    edges = []
    for t, row in enumerate(phases):
        following = phases[(t + 1) % period]
        raw, et, gt = oracle.exterior_raw(base, row)
        require((et, gt) == (int(e[t]), int(g[t])), "witness stream mismatch")
        require(canonical(raw, base) == following, "canonical exterior successor mismatch")
        u = len(raw) - len(following)
        require(u >= 0 and raw == following + (base - 1,) * u, "invalid natural exterior trim")
        edge = (list(row), list(centers[t]), list(following),
                list(centers[(t + 1) % period]), u, int(vs[t]))
        oracle.check_edge(base, edge)
        oracle.integer_transition_fixture(base, row, tuple(centers[t]))
        edges.append(edge)
    actual_e, actual_g = oracle.check_cycle(base, edges)
    require(actual_e == tuple(map(int, e)) and actual_g == tuple(map(int, g)), "full-cycle streams")
    require(mirror().cycleOK(base, edges, edges[0][0], edges[0][1]), "mirror cycleOK rejected witness")
    return edges


def natural(value):
    require(type(value) is int or (isinstance(value, str) and value and value.isascii() and value.isdigit()),
            "invalid native nonnegative integer")
    value = int(value)
    require(value >= 0, "negative native count")
    return value


def bounded_native(command, seconds, gib, grace=10):
    """Same native limits as Agent108, retaining complete stdout on wall cap.

    Agent108's limited() discards TimeoutExpired.stdout. It remains suitable
    for the build; this launch preserves potentially decisive witness data.
    """
    def limits():
        resource.setrlimit(resource.RLIMIT_AS, (gib * 1024**3, gib * 1024**3))
        cpu = math.ceil(seconds)
        resource.setrlimit(resource.RLIMIT_CPU, (cpu + 5, cpu + 6))

    started = time.monotonic()
    interrupted = False
    with subprocess.Popen(command, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                          preexec_fn=limits, start_new_session=True) as process:
        try:
            stdout, stderr = process.communicate(timeout=seconds + grace)
        except subprocess.TimeoutExpired:
            interrupted = True
            try:
                os.killpg(process.pid, signal.SIGKILL)
            except ProcessLookupError:
                pass
            stdout, stderr = process.communicate()
        code = process.returncode
    records, malformed = [], False
    for line in stdout.splitlines():
        try:
            item = json.loads(line)
            require(isinstance(item, dict), "native JSON is not an object")
            records.append(item)
        except (ValueError, TypeError):
            malformed = True
            break
    if interrupted or code < 0 or malformed or not any(r.get("type") == "RESULT" for r in records):
        records.append({"type": "PROCESS", "status": "UNDECIDED", "native_exit": code,
                        "reason": "external_wall_cap" if interrupted else "incomplete_native_output",
                        "malformed_tail": malformed, "stderr_tail": stderr[-1000:]})
        code = 3
    records.append({"type": "PROCESS_METRICS", "wall_seconds": time.monotonic() - started,
                    "address_space_limit_GiB": gib, "native_exit": process.returncode})
    return code, records


def summarize(code, records, phase_shift=0, trusted_driver=False):
    """Check record consistency; pinned #423 retains #405's exact arithmetic."""
    output = {"classification": "COMPUTED", "period": 48, "e": E48, "g": G48,
              "dependency_commit": COMMIT, "status": "UNDECIDED", "candidate": False,
              "scope": "prescribed full-P48 exterior completion of the supplied C24 squared"}
    try:
        wanted_e, wanted_g = input_words(phase_shift)
        output.update(e=wanted_e, g=wanted_g, phase_shift=phase_shift, original_e=E48, original_g=G48)
        require(type(code) is int and isinstance(records, list), "bad runner envelope")
        layers, terminals, witnesses, failures, metrics = [], [], [], [], []
        ended = False
        for record in records:
            require(isinstance(record, dict), "native record is not an object")
            kind = record.get("type")
            if kind == "LAYER":
                require(not ended, "layer after terminal record")
                depth, states, accepts = (natural(record[key]) for key in ("depth", "states", "accepts"))
                require(depth == len(layers) and accepts <= states, "nonconsecutive or inconsistent frontier")
                layers.append({"width": depth, "states": str(states), "accepts": str(accepts),
                               "root": natural(record["root"])})
            elif kind == "RESULT":
                ended = True
                terminals.append(record)
            elif kind == "WITNESS":
                require(not ended, "witness after terminal record")
                witnesses.append(record)
            elif kind == "PROCESS":
                require(record.get("status") == "UNDECIDED", "unexpected process status")
                failures.append(record)
            elif kind == "PROCESS_METRICS":
                metrics.append(record)
            else:
                raise ValueError("unknown native record kind")
        require(len(terminals) <= 1 and len(witnesses) <= 1, "duplicate native terminal or witness")
        output.update(completed_frontiers=layers, completed_through=layers[-1]["width"] if layers else None,
                      native_exit=code, process_metrics=metrics)
        zero_prefix = -1
        for layer in layers:
            if int(layer["accepts"]):
                break
            zero_prefix = layer["width"]
        output["zero_accept_prefix_through"] = zero_prefix
        metadata_ok = bool(terminals and terminals[0].get("g") == wanted_g
                           and terminals[0].get("requested_e") == wanted_e
                           and terminals[0].get("period") == 48 and terminals[0].get("G") == 16
                           and terminals[0].get("phase_rotation") == 0)
        if witnesses:
            # A self-contained checked certificate survives a lost terminal
            # record or a later process failure; no engine status proves it.
            witness = witnesses[0]
            require(witness.get("e") == wanted_e and witness.get("g") == wanted_g, "wrong witness streams")
            center = oracle.target_center(2)
            phases = restore_rows(witness["B_t"], phase_shift, 48)
            edges = couple(10, phases, center["C"], center["v"], E48, G48)
            output.update(status="CANDIDATE", candidate=True, candidate_status="PYTHON_CYCLEOK",
                          edges=edges, cycleOK10=True, lean_verified=False,
                          reason="independently_checked_full_witness")
            if (terminals and not metadata_ok) or (not terminals and not trusted_driver):
                for key in ("completed_frontiers", "zero_accept_prefix_through", "completed_through"):
                    output.pop(key, None)
            return output
        if not terminals:
            output["reason"] = "missing_terminal_record"
            output["process_failures"] = failures
            if not trusted_driver:
                for key in ("completed_frontiers", "zero_accept_prefix_through", "completed_through"):
                    output.pop(key, None)
            return output
        final = terminals[0]
        require(metadata_ok, "wrong target streams or full-P48 seam")
        status, reason = final.get("status"), final.get("reason")
        require(status in ("FEASIBLE", "EXHAUSTED_NO_B_FOR_E", "UNDECIDED"), "unexpected engine status")
        depth = natural(final["depth"])
        require(not layers or depth == layers[-1]["width"], "terminal depth disagrees with completed frontier")
        output.update(status=status, reason=reason, terminal_record=final)
        if status == "EXHAUSTED_NO_B_FOR_E":
            require(code == 0 and not failures and layers and zero_prefix == depth, "incomplete negative result")
            if reason == "empty_layer":
                require(int(layers[-1]["states"]) == 0 and layers[-1]["root"] == 0, "nonempty negative frontier")
            elif reason == "exact_layer_repeat":
                start = natural(final["cycle_start"])
                require(1 <= start < depth and layers[start]["root"] == layers[-1]["root"]
                        and layers[start]["states"] == layers[-1]["states"], "invalid exact layer repeat")
            else:
                raise ValueError("resource cap cannot establish an all-width negative")
            output["all_width_exclusion"] = True
        elif status == "FEASIBLE":
            require(layers and int(layers[-1]["accepts"]) > 0, "feasible result lacks accepting frontier")
            output["candidate_status"] = "UNDECIDED"
            output["candidate_reason"] = "exterior feasible; witness missing or extraction capped"
        return output
    except (KeyError, TypeError, ValueError) as error:
        output.update(status="UNDECIDED", candidate=False, reason="invalid_or_failed_audit: " + str(error))
        output.pop("all_width_exclusion", None)
        output.pop("edges", None)
        for key in ("completed_frontiers", "zero_accept_prefix_through", "completed_through", "terminal_record"):
            output.pop(key, None)
        return output


def selftest():
    check_dependencies()
    wrong = dict(PINS, **{"exterior_run.py": "0" * 64})
    try:
        check_dependencies(wrong)
    except ValueError:
        pass
    else:
        raise ValueError("dependency corruption was accepted")
    edge_count = rotated_edges = 0
    for base, source in oracle.load_lean_certificates().items():
        e, g = oracle.check_cycle(base, source)
        phases = [canonical(edge[0], base) for edge in source]
        centers, vs = [edge[1] for edge in source], [edge[5] for edge in source]
        edges = couple(base, phases, centers, vs, e, g)
        edge_count += len(edges)
        for shift in PHASES:
            shifted = rotate(phases, shift)
            require(restore_rows(shifted, shift, len(e)) == phases, "inverse witness phase cut")
            shifted_edges = couple(base, shifted, rotate(centers, shift), rotate(vs, shift),
                                   rotate(e, shift), rotate(g, shift))
            require(rotate(shifted_edges, -shift) == edges, "rotated full-cycle coupling mismatch")
            rotated_edges += len(shifted_edges)
    layer0 = {"type": "LAYER", "depth": 0, "root": 2, "states": "1", "accepts": "0"}
    final = {"type": "RESULT", "g": G48, "requested_e": E48, "period": 48, "G": 16,
             "phase_rotation": 0, "depth": 0, "status": "UNDECIDED", "reason": "node_cap"}
    cases = [
        (3, [layer0, final], "UNDECIDED"),
        (3, [layer0], "UNDECIDED"),
        (0, [layer0, dict(final, period=24)], "UNDECIDED"),
        (0, [layer0, dict(final, requested_e=E48[:24])], "UNDECIDED"),
        (3, [dict(layer0, states="corrupt"), final], "UNDECIDED"),
        (3, [layer0, dict(layer0, depth=2), final], "UNDECIDED"),
        (0, [layer0, final, final], "UNDECIDED"),
        (0, [layer0, dict(final, status="EXHAUSTED_NO_B_FOR_E")], "UNDECIDED"),
        (0, [layer0, dict(layer0, depth=1, root=0, states="0"),
             dict(final, depth=1, status="EXHAUSTED_NO_B_FOR_E", reason="empty_layer")], "EXHAUSTED_NO_B_FOR_E"),
        (0, [layer0, dict(layer0, depth=1, accepts="1"),
             dict(final, depth=1, status="FEASIBLE", reason="operation_cap")], "FEASIBLE"),
        (0, [layer0, {"type": "WITNESS", "e": E48, "g": G48, "B_t": [[]] * 48}], "UNDECIDED"),
        (0, [layer0, {"type": "WITNESS", "e": E48[:24], "g": G48, "B_t": [[]] * 48}], "UNDECIDED"),
        (0, [layer0, dict(layer0, depth=1, root=3, states="2"),
             dict(layer0, depth=2, root=3, states="2"),
             dict(final, depth=2, status="EXHAUSTED_NO_B_FOR_E", reason="exact_layer_repeat", cycle_start=1)],
         "EXHAUSTED_NO_B_FOR_E"),
        (0, [layer0, dict(layer0, depth=1),
             dict(final, depth=1, status="EXHAUSTED_NO_B_FOR_E", reason="exact_layer_repeat", cycle_start=0)],
         "UNDECIDED"),
    ]
    for code, records, wanted in cases:
        result = summarize(code, records)
        require(result["status"] == wanted and not result["candidate"], "parser control failed")
    unscoped = summarize(3, [layer0])
    scoped = summarize(3, [layer0], trusted_driver=True)
    require("completed_through" not in unscoped and scoped.get("completed_through") == 0,
            "missing terminal driver scope")
    for shift in PHASES:
        wanted_e, wanted_g = input_words(shift)
        shifted_final = dict(final, requested_e=wanted_e, g=wanted_g)
        result = summarize(3, [layer0, shifted_final], shift)
        require(result["status"] == "UNDECIDED" and result.get("completed_through") == 0,
                "rotated input metadata control")
    wrong_second_lap = E48[:24] + ("1" if E48[24] == "0" else "0") + E48[25:]
    for records, shift in (([layer0, dict(final, requested_e=wrong_second_lap)], 0),
                           ([layer0, dict(final, g=rotate(G48, 1))], 1)):
        result = summarize(3, records, shift)
        require(result["status"] == "UNDECIDED" and "completed_through" not in result
                and "zero_accept_prefix_through" not in result, "invalid driver retained a width bound")
    # Synthetic, deliberately non-certificate data: a complete witness-shaped
    # record followed by a truncated record must survive a real wall timeout.
    probe = ("import sys,time; print('{\"type\":\"WITNESS\",\"control\":true}',flush=True);"
             "sys.stdout.write('{');sys.stdout.flush();time.sleep(2)")
    code, records = bounded_native([sys.executable, "-c", probe], 0.1, 1, grace=0.1)
    require(code == 3 and any(r.get("type") == "WITNESS" for r in records)
            and any(r.get("reason") == "external_wall_cap" for r in records),
            "timeout discarded a complete witness record")
    return {"status": "SELFTEST_PASSED", "known_bases": 8, "canonical_coupled_edges": edge_count,
            "rotation_coupling_controls": 8 * len(PHASES), "rotated_coupled_edges": rotated_edges,
            "parser_controls": len(cases) + len(PHASES) + 3, "dependency_controls": 2,
            "timeout_capture_controls": 1, "engine_searches": 0,
            "scope": "synthetic parser controls and existing nondecimal certificate audits only"}


def run(args):
    began = time.monotonic()
    deadline = began + args.seconds
    native = runner()
    wanted_e, wanted_g = input_words(args.phase_shift)
    with tempfile.TemporaryDirectory(prefix="p196-agent115-p48-mdd-") as temporary:
        binary = Path(temporary) / "exterior_mdd"
        build_seconds = min(60, int(deadline - time.monotonic()) - 10)
        if build_seconds < 1:
            return {"status": "UNDECIDED", "reason": "insufficient build time budget", "candidate": False}
        py = [sys.executable] + (["-O"] if sys.flags.optimize else [])
        build_started = time.monotonic()
        code, records = native.limited(py + [str(Path(__file__).resolve()), "--build", str(binary)],
                                       build_seconds, args.gib)
        build_wall = time.monotonic() - build_started
        require(code == 0 and any(r.get("status") == "BINARY_BUILT" for r in records), "bounded engine build failed")
        check_dependencies()
        seconds = int(deadline - time.monotonic()) - 10
        if seconds < 1:
            return {"status": "UNDECIDED", "reason": "build consumed run budget", "candidate": False}
        command = [str(binary), wanted_g, str(args.nodes), str(args.operations), str(args.depth), str(seconds),
                   "--e", wanted_e, "--witness"]
        if args.live:
            command.append("--live")
        native_started = time.monotonic()
        code, records = bounded_native(command, seconds, args.gib)
        native_wall = time.monotonic() - native_started
        output = summarize(code, records, args.phase_shift, trusted_driver=True)
        peak = resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss
        output.update(total_seconds=round(time.monotonic() - began, 6), native_seconds_budget=seconds,
                      build_wall_seconds=round(build_wall, 6), native_wall_seconds=round(native_wall, 6),
                      peak_child_KiB=peak // (1024 if sys.platform == "darwin" else 1),
                      wall_budget_seconds=args.seconds, address_space_limit_GiB=args.gib,
                      node_cap=args.nodes, operation_cap=args.operations, depth_cap=args.depth, live=args.live)
        return output


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=("run", "selftest", "check"))
    parser.add_argument("--nodes", type=int, default=1500000)
    parser.add_argument("--operations", type=int, default=300000000)
    parser.add_argument("--depth", type=int, default=1000)
    parser.add_argument("--seconds", type=int, default=120)
    parser.add_argument("--gib", type=int, default=4)
    parser.add_argument("--phase-shift", type=int, choices=PHASES, default=0)
    parser.add_argument("--live", action="store_true", help="use Agent108's live-node collection mode")
    args = parser.parse_args()
    if (not 1 <= args.seconds <= 1200 or not 1 <= args.gib <= 8 or not 2 <= args.nodes < 2**32
            or not 1 <= args.operations < 2**64 or not 0 <= args.depth <= 1000000):
        parser.error("invalid resource limits (maximum 1200 seconds and 8 GiB)")
    try:
        check_dependencies()
        if args.mode == "selftest":
            result = selftest()
        elif args.mode == "check":
            envelope = json.load(sys.stdin)
            result = summarize(envelope["code"], envelope["records"], args.phase_shift)
            result["input_mode"] = "supplied native records; no new engine run"
        else:
            result = run(args)
    except (OSError, RuntimeError, ValueError, KeyError, TypeError, MemoryError, subprocess.SubprocessError) as error:
        result = {"status": "UNDECIDED", "candidate": False, "reason": str(error)}
    if result.get("candidate"):
        print(json.dumps({"type": "CANDIDATE", "base": 10, "edges": result.pop("edges"),
                          "e": E48, "g": G48, "source_phase_shift": args.phase_shift,
                          "cycleOK10": True, "lean_verified": False}), flush=True)
    print(json.dumps({"type": "SUMMARY", **result}, sort_keys=True), flush=True)
    return 3 if result["status"] == "UNDECIDED" else 0


if __name__ == "__main__":
    if len(sys.argv) == 3 and sys.argv[1] == "--build":
        runner().build(Path(sys.argv[2]))
        print(json.dumps({"type": "RESULT", "status": "BINARY_BUILT"}), flush=True)
    else:
        raise SystemExit(main())
