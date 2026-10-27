#!/usr/bin/env python3
"""Guarded runner for Agent116's exterior regular-language review.

Examples (from the repository root):
  python3 calculation/agent-116/p24_regular_run.py run --seconds 60
  python3 calculation/agent-116/p24_regular_run.py run --finite-k 1 --nfa-bisim
  python3 calculation/agent-116/p24_regular_run.py guards

The default compiles the local engine into a temporary directory, which is
removed on exit. No result file is created unless --output is supplied.
Limits, signals, malformed output, and failed independent witness replay
are UNDECIDED. Finite-k negatives retain their exact repetition scope.
Peak RSS comes only from the engine's own measurement, never compiler or
cumulative RUSAGE_CHILDREN data. Engine self-check flags are not trusted
instead of the separately authored positional-integer witness replay.
"""
import argparse
from contextlib import contextmanager
from hashlib import sha256
import importlib.util
import json
import math
import os
from pathlib import Path
import re
import resource
import signal
import subprocess
import sys
import tempfile
import time

from p24_regular_controls import (P24_E, P24_G, ROOT, replay_certificate,
                                  replay_fixed_width, replay_p24_center, require)


COMPLETE = {"EXHAUSTED", "REPEATED_LANGUAGE", "TARGET_HIT", "DIAGNOSTIC_ONLY"}
SOURCE = Path(__file__).with_name("exterior_regular.cpp")


class Parser(argparse.ArgumentParser):
    def error(self, message):
        raise ValueError(message)


def reject_constant(text):
    raise ValueError(f"nonfinite JSON number: {text}")


def limits(memory_mib, seconds):
    def install():
        memory = memory_mib * 1024 * 1024
        resource.setrlimit(resource.RLIMIT_AS, (memory, memory))
        cpu = max(1, math.ceil(seconds) + 5)
        resource.setrlimit(resource.RLIMIT_CPU, (cpu, cpu + 1))
    return install


def child(command, seconds, memory_mib, outer_timeout=None):
    """One isolated process group; communicate always has a finite timeout."""
    outer = seconds + 15 if outer_timeout is None else outer_timeout
    require(0 < outer <= seconds + 15, "invalid outer timeout")
    started = time.monotonic()
    try:
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                   text=True, start_new_session=True,
                                   preexec_fn=limits(memory_mib, seconds))
    except OSError as error:
        return {"exit_code": None, "stdout": "", "stderr": str(error),
                "wall_seconds": time.monotonic() - started, "stop": "LAUNCH_UNDECIDED"}
    stop = None
    try:
        stdout, stderr = process.communicate(timeout=outer)
    except subprocess.TimeoutExpired:
        stop = "OUTER_TIMEOUT_UNDECIDED"
        try:
            os.killpg(process.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
        stdout, stderr = process.communicate(timeout=5)
    except BaseException:
        try:
            os.killpg(process.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
        process.communicate(timeout=5)
        raise
    if stop is None and process.returncode < 0:
        stop = "PROCESS_SIGNAL_UNDECIDED"
    return {"exit_code": process.returncode, "stdout": stdout, "stderr": stderr,
            "wall_seconds": time.monotonic() - started, "stop": stop}


def source_hashes():
    pending, found = [SOURCE], {}
    while pending:
        path = pending.pop().resolve()
        if path in found:
            continue
        data = path.read_bytes()
        found[path] = sha256(data).hexdigest()
        pending.extend(path.parent / name for name in re.findall(
            r'^\s*#include\s+"([^"]+)"', data.decode(), re.M))
    return {str(path.relative_to(ROOT)): digest for path, digest in sorted(found.items())}


@contextmanager
def engine_binary(existing=None, compiler="c++"):
    if existing is not None:
        path = existing.resolve()
        yield path, {"status": "EXISTING_BINARY", "binary_sha256": sha256(path.read_bytes()).hexdigest()}
        return
    with tempfile.TemporaryDirectory(prefix="agent116-regular-") as directory:
        binary = Path(directory) / "exterior_regular"
        before = source_hashes()
        flags = ["-O3", "-std=c++17", "-Wall", "-Wextra", "-pedantic"]
        built = child([compiler, *flags, str(SOURCE), "-o", str(binary)], 120, 8192)
        metadata = {"status": "PASS", "compiler": compiler, "flags": flags,
                    "source_sha256": before, "wall_seconds": round(built["wall_seconds"], 6),
                    "compiler_stderr_lines": len(built["stderr"].splitlines())}
        if built["stop"] or built["exit_code"] != 0:
            metadata.update(status="COMPILATION_UNDECIDED", exit_code=built["exit_code"],
                            reason=built["stop"] or built["stderr"].splitlines()[:1])
            yield None, metadata
        elif source_hashes() != before:
            metadata["status"] = "SOURCE_CHANGED_DURING_COMPILE_UNDECIDED"
            yield None, metadata
        else:
            metadata["binary_sha256"] = sha256(binary.read_bytes()).hexdigest()
            yield binary, metadata


def independent_witness(record, scope):
    require(scope is not None, "witness received without an exact requested scope")
    base, e, g, B = record["base"], record["e"], record["g"], record["B"]
    require(base == scope["base"] and isinstance(e, str) and isinstance(g, str),
            "witness base or stream type mismatch")
    require(len(e) == len(g) and len(e) % len(scope["e"]) == 0, "witness repetition mismatch")
    repetitions = len(e) // len(scope["e"])
    require(repetitions >= 1 and e == scope["e"] * repetitions and g == scope["g"] * repetitions,
            "witness does not belong to the requested typed driver language")
    require(scope["finite_k"] in (0, repetitions), "witness escaped the finite-k restriction")
    require(record["repetitions"] == repetitions and isinstance(B, list) and
            all(isinstance(word, list) and all(type(x) is int for x in word) for word in B),
            "malformed witness coefficient data")
    width = replay_fixed_width(base, e, g, B)
    require(record["width"] == width and record.get("u") == list(map(int, g)),
            "witness width or fixed-width trim schedule mismatch")
    verified = {"base": base, "width": width, "repetitions": repetitions,
                "phases": len(B), "independent_whole_integer_replay": True}
    candidate = None
    if base == 10 and scope["e"] == P24_E and scope["g"] == P24_G:
        centers = replay_p24_center()["edges"]
        edges = [[word, centers[t % 24]["C"], B[(t + 1) % len(B)],
                  centers[t % 24]["C2"], int(g[t]), centers[t % 24]["v"]]
                 for t, word in enumerate(B)]
        replay_certificate({"base": 10, "edges": edges, "source": "engine witness + PR381 center",
                            "pin": "runtime candidate; not Lean verified"})
        specification = importlib.util.spec_from_file_location(
            "agent116_candidate_mirror", ROOT / "calculation/neutral_band_search.py")
        mirror = importlib.util.module_from_spec(specification)
        specification.loader.exec_module(mirror)
        require(mirror.cycleOK(10, edges, edges[0][0], edges[0][1]),
                "decimal candidate failed the unchanged cycleOK mirror")
        candidate = {"classification": "CANDIDATE_NOT_LEAN_VERIFIED", "base": 10,
                     "mirror_cycleOK": True, "edges": edges}
    return verified, candidate


def summarize(raw, scope=None, ignore_target=False):
    summary = {"status": raw["stop"] or "OUTPUT_UNDECIDED", "scope": scope,
               "exit_code": raw["exit_code"], "wall_seconds": round(raw["wall_seconds"], 6),
               "engine_peak_rss_mib": None, "records": [], "witness_replays": []}
    try:
        records = summary["records"]
        for line in raw["stdout"].splitlines():
            if line.strip():
                item = json.loads(line, parse_constant=reject_constant)
                require(isinstance(item, dict) and isinstance(item.get("event"), str),
                        "engine output record lacks an event type")
                records.append(item)
        peaks = [row["peak_rss_mib"] for row in records if "peak_rss_mib" in row]
        require(all(type(x) in (int, float) and math.isfinite(x) and x >= 0 for x in peaks),
                "invalid engine peak RSS measurement")
        if peaks:
            summary["engine_peak_rss_mib"] = max(peaks)
        results = [row for row in records if row["event"] == "result"]
        require(len(results) == 1, "engine must emit exactly one terminal result")
        result = results[0]
        status = result["status"]
        require(isinstance(status, str) and (status in COMPLETE or status.endswith("UNDECIDED")),
                "unrecognized terminal status")
        summary["engine_status"], summary["result"] = status, result
        if raw["stop"]:
            return summary
        if status in COMPLETE and raw["exit_code"] != 0:
            summary["status"] = "NONZERO_EXIT_UNDECIDED"
            return summary
        if scope is not None and "finite_k" in result:
            require(result["finite_k"] == scope["finite_k"], "terminal result changed repetition scope")
        for record in records:
            if record["event"] == "witness":
                try:
                    verified, candidate = independent_witness(record, scope)
                except (ValueError, KeyError, TypeError, IndexError) as error:
                    summary.update(status="WITNESS_REPLAY_UNDECIDED", reason=str(error))
                    return summary
                summary["witness_replays"].append(verified)
                if candidate is not None:
                    summary["candidate"] = candidate
        if status == "TARGET_HIT" and not summary["witness_replays"]:
            summary["status"] = "TARGET_HIT_WITNESS_MISSING_UNDECIDED"
            return summary
        if status in {"EXHAUSTED", "REPEATED_LANGUAGE"}:
            require(not ignore_target and not summary["witness_replays"] and
                    not any(row.get("target_hit_k") for row in records),
                    "negative terminal status conflicts with diagnostic mode or an earlier target")
            summary["conclusion"] = "NO_B_LIFT_IN_REQUESTED_REPETITION_SCOPE"
        elif status == "DIAGNOSTIC_ONLY":
            summary["conclusion"] = "DIAGNOSTIC_ONLY_NO_NEGATIVE_INFERENCE"
        elif status == "TARGET_HIT":
            summary["conclusion"] = "COMPUTED_B_WITNESS_INDEPENDENTLY_REPLAYED"
        summary["status"] = status
    except (ValueError, KeyError, TypeError, IndexError) as error:
        summary.update(status=raw["stop"] or "OUTPUT_PROTOCOL_UNDECIDED", reason=str(error))
    if raw["stderr"] and "reason" not in summary:
        summary["diagnostic"] = raw["stderr"].splitlines()[0][:500]
    return summary


def invoke(binary, arguments, scope, seconds=5, memory_mib=512, ignore_target=False):
    raw = child([str(binary), *arguments], seconds, memory_mib)
    return summarize(raw, scope, ignore_target)


def run_arguments(args):
    require(2 <= args.base <= 32 and 1 <= len(args.e) == len(args.g) <= 256 and
            set(args.e + args.g) <= {"0", "1"} and args.g[0] == "1", "invalid base or typed E/G")
    require(math.isfinite(args.seconds) and 0 < args.seconds <= 1190, "seconds must lie in (0,1190]")
    require(64 <= args.memory_mib <= 8192 and 1 <= args.layers <= 10000, "invalid memory or depth bound")
    require(args.finite_k is None or 1 <= args.finite_k <= 1000, "finite-k must be1..1000 when supplied")
    require(1 <= args.nfa_cap < 2 ** 32 - 1 and 1 <= args.dfa_cap < 2 ** 32 - 1 and
            1 <= args.edge_cap < 2 ** 64 and 1 <= args.ops_cap < 2 ** 64, "invalid operation/state cap")
    scope = {"base": args.base, "e": args.e, "g": args.g, "finite_k": args.finite_k or 0,
             "repetition_scope": f"exactly {args.finite_k}" if args.finite_k else "every positive integer"}
    command = [str(args.base), args.e, args.g]
    for name in ("seconds", "memory_mib", "layers", "nfa_cap", "dfa_cap", "edge_cap", "ops_cap"):
        command += ["--" + name.replace("_", "-"), str(getattr(args, name))]
    if args.finite_k is not None:
        command += ["--finite-k", str(args.finite_k)]
    for name in ("stream_anchors", "nfa_bisim", "ignore_target"):
        if getattr(args, name):
            command.append("--" + name.replace("_", "-"))
    return command, scope


def guards(binary):
    results = []
    common = ["--seconds", "5", "--memory-mib", "512", "--layers", "30",
              "--nfa-cap", "500000", "--dfa-cap", "500000",
              "--edge-cap", "5000000", "--ops-cap", "20000000"]
    scope = {"base": 2, "e": "10", "g": "10", "finite_k": 0,
             "repetition_scope": "every positive integer"}

    def check(name, arguments, expected, expected_scope=scope, diagnostic=False, seconds=5):
        result = invoke(binary, arguments, expected_scope, seconds=seconds, ignore_target=diagnostic)
        expected_statuses = {expected} if isinstance(expected, str) else set(expected)
        require(result["status"] in expected_statuses,
                {"guard": name, "expected": expected, "actual": result})
        results.append({"guard": name, "status": result["status"], "exit_code": result["exit_code"],
                        "independently_replayed_witnesses": len(result["witness_replays"])})
        return result

    malformed = [
        ("base", ["1", "10", "10"]), ("unequal_streams", ["2", "1", "10"]),
        ("leading_overflow", ["2", "01", "01"]), ("gap6", ["32", "100000", "100000"]),
        ("unknown_flag", ["2", "10", "10", "--unknown", "1"]),
        ("missing_value", ["2", "10", "10", "--seconds"]),
        ("nonfinite_time", ["2", "10", "10", "--seconds", "nan"]),
        ("excess_time", ["2", "10", "10", "--seconds", "1191"]),
        ("excess_memory", ["2", "10", "10", "--memory-mib", "8193"]),
        ("zero_state_cap", ["2", "10", "10", "--nfa-cap", "0"]),
        ("zero_finite_k", ["2", "10", "10", "--finite-k", "0"]),
    ]
    for name, arguments in malformed:
        check(name, arguments, "ERROR_UNDECIDED")
    for name, extra, status in [
        ("nfa_cap", ["--nfa-cap", "1"], "NFA_CAP_UNDECIDED"),
        ("dfa_cap", ["--dfa-cap", "1"], "DFA_CAP_UNDECIDED"),
        ("edge_cap", ["--edge-cap", "1"], "EDGE_CAP_UNDECIDED"),
        ("ops_cap", ["--ops-cap", "1"], "OPERATION_CAP_UNDECIDED"),
        ("depth_cap", ["--layers", "1"], "DEPTH_CAP_UNDECIDED"),
        ("time_cap", ["--seconds", "0.000000000001"], "TIMEOUT_UNDECIDED"),
    ]:
        check(name, ["2", "10", "10", *common, *extra], status)
    for base, e, g in [(2, "10", "10"), (4, "100", "100"),
                       (16, "10000", "10000"), (20, "10", "10")]:
        for k in (1, 2, 3):
            fixed = {"base": base, "e": e, "g": g, "finite_k": k, "repetition_scope": f"exactly {k}"}
            check(f"positive_base{base}_k{k}",
                  [str(base), e, g, *common, "--finite-k", str(k)], "TARGET_HIT", fixed)
    fixed = {**scope, "finite_k": 1, "repetition_scope": "exactly 1"}
    check("diagnostic_no_negative", ["2", "10", "10", *common, "--finite-k", "1", "--ignore-target"],
          "DIAGNOSTIC_ONLY", fixed, True)
    for flags in (["--stream-anchors"], ["--nfa-bisim"], ["--stream-anchors", "--nfa-bisim"]):
        check("positive_" + "_".join(flags), ["2", "10", "10", *common, *flags], "TARGET_HIT")
    decimal = {"base": 10, "e": "10", "g": "10", "finite_k": 1, "repetition_scope": "exactly 1"}
    check("fixed_k_negative_scope", ["10", "10", "10", *common, "--finite-k", "1"], "EXHAUSTED", decimal)
    # Agent105's physical two-lap example is a control, not our discovery.
    base6 = {"base": 6, "e": "10", "g": "10", "finite_k": 0,
             "repetition_scope": "every positive integer"}
    multi = check("agent105_base6_all_laps", ["6", "10", "10", *common, "--seconds", "10"],
                  "TARGET_HIT", base6, seconds=10)
    require(multi["witness_replays"][0]["repetitions"] == 2,
            "base6 physical control did not recover its genuine two-lap witness")
    check("agent105_base6_one_lap", ["6", "10", "10", *common, "--finite-k", "1"],
          {"EXHAUSTED", "REPEATED_LANGUAGE"},
          {**base6, "finite_k": 1, "repetition_scope": "exactly 1"})
    check("agent105_base6_two_laps", ["6", "10", "10", *common, "--finite-k", "2"],
          "TARGET_HIT", {**base6, "finite_k": 2, "repetition_scope": "exactly 2"})

    synthetic = [
        ("malformed_json", "print('not JSON')", "OUTPUT_PROTOCOL_UNDECIDED", None),
        ("missing_result", "print('{\"event\":\"layer\",\"depth\":0}')", "OUTPUT_PROTOCOL_UNDECIDED", None),
        ("nonzero_false_negative", "import sys; print('{\"event\":\"result\",\"status\":\"EXHAUSTED\"}'); sys.exit(2)",
         "NONZERO_EXIT_UNDECIDED", None),
        ("unreplayed_positive", "print('{\"event\":\"result\",\"status\":\"TARGET_HIT\"}')",
         "TARGET_HIT_WITNESS_MISSING_UNDECIDED", None),
        ("corrupt_witness", "import json; print(json.dumps({'event':'witness','base':2,'e':'10','g':'10',"
         "'B':[[2,0],[1,0]],'u':[1,0],'width':2,'repetitions':1})); "
         "print(json.dumps({'event':'result','status':'TARGET_HIT'}))", "WITNESS_REPLAY_UNDECIDED", None),
        ("outer_timeout", "while True: pass", "OUTER_TIMEOUT_UNDECIDED", 0.05),
    ]
    for name, program, expected, timeout in synthetic:
        raw = child([sys.executable, "-c", program], 1, 128, timeout)
        result = summarize(raw, scope)
        require(result["status"] == expected, {"guard": name, "expected": expected, "actual": result})
        results.append({"guard": name, "status": result["status"], "exit_code": result["exit_code"]})
    return {"status": "PASS", "guard_count": len(results), "guards": results,
            "independently_replayed_witnesses": sum(row.get("independently_replayed_witnesses", 0)
                                                    for row in results)}


def main():
    parser = Parser(description=__doc__)
    modes = parser.add_subparsers(dest="mode", required=True, parser_class=Parser)
    run = modes.add_parser("run", help="run the exact P24 driver, or an explicitly supplied control")
    guard = modes.add_parser("guards", aliases=["guard"], help="check parser, resource, scope, and replay guards")
    for subparser in (run, guard):
        subparser.add_argument("--engine", type=Path, help="reuse a supplied executable instead of compiling")
        subparser.add_argument("--compiler", default="c++")
        subparser.add_argument("--output", type=Path, help="optional JSON result file")
    run.add_argument("--base", type=int, default=10)
    run.add_argument("--e", default=P24_E)
    run.add_argument("--g", default=P24_G)
    run.add_argument("--seconds", type=float, default=60)
    run.add_argument("--memory-mib", type=int, default=2048)
    run.add_argument("--layers", type=int, default=80)
    run.add_argument("--finite-k", type=int)
    run.add_argument("--nfa-cap", type=int, default=500000)
    run.add_argument("--dfa-cap", type=int, default=500000)
    run.add_argument("--edge-cap", type=int, default=20000000)
    run.add_argument("--ops-cap", type=int, default=150000000)
    run.add_argument("--stream-anchors", action="store_true")
    run.add_argument("--nfa-bisim", action="store_true")
    run.add_argument("--ignore-target", action="store_true", help="diagnostic mode; never infer a negative")
    args = parser.parse_args()
    command, scope = run_arguments(args) if args.mode == "run" else (None, None)
    with engine_binary(args.engine, args.compiler) as (binary, build):
        if binary is None:
            result = {"status": build["status"]}
        elif args.mode == "run":
            result = invoke(binary, command, scope, args.seconds, args.memory_mib, args.ignore_target)
        else:
            result = guards(binary)
        result["build"] = build
    payload = json.dumps(result, sort_keys=True, allow_nan=False) + "\n"
    if args.output is not None:
        args.output.write_text(payload)
    print(payload, end="")
    return 2 if "UNDECIDED" in result["status"] else 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (ValueError, KeyError, OSError, TypeError) as error:
        print(json.dumps({"status": "RUNNER_ERROR_UNDECIDED", "reason": str(error)}, sort_keys=True))
        raise SystemExit(2) from error
