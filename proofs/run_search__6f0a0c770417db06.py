#!/usr/bin/env python3
import argparse
import gzip
import hashlib
import json
from pathlib import Path
import subprocess
import time
import shutil
import importlib.util
import sys
from encode import build, verify_candidate

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
REFERENCE = ROOT / "proofs/contributions/2026-10-15-agent8-complementary-bulk/explore.py"


def reference_replay(candidate):
    """Replay against the unchanged pre-existing Agent 8 original exterior map."""
    sys.path.insert(0, str(REFERENCE.parent))
    spec = importlib.util.spec_from_file_location("agent8_original_exterior", REFERENCE)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    states = candidate["states"]
    for i, (c, B) in enumerate(states):
        (cn, Bn), _, gamma = module.outer_step(c, tuple(B))
        cn_expected, Bn_expected = states[(i + 1) % len(states)]
        assert (cn, tuple(Bn)) == (cn_expected, tuple(Bn_expected))
        assert gamma == candidate["overflows"][i]
    candidate.update(reference_map_replay="PASS", reference_source=str(REFERENCE.relative_to(ROOT)),
                     reference_sha256=sha(REFERENCE))


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--solver", required=True)
    p.add_argument("--width", type=int, required=True)
    p.add_argument("--period", type=int, required=True)
    p.add_argument("--phase", type=int, required=True)
    p.add_argument("--overflows", type=int)
    p.add_argument("--seconds", type=int, default=10)
    p.add_argument("--full-width", action="store_true")
    p.add_argument("--name")
    a = p.parse_args()
    name = a.name or f"c{a.phase}-w{a.width}-p{a.period}-h{a.overflows or 'any'}-{a.seconds}s"
    out = HERE / "results" / name
    out.mkdir(parents=True, exist_ok=False)
    started = time.monotonic()
    formula, metadata = build(a.width, a.period, a.phase, a.overflows, a.full_width)
    raw = formula.text().encode()
    cnf = out / "formula.cnf"
    cnf.write_bytes(raw)
    metadata["formula_sha256"] = hashlib.sha256(raw).hexdigest()
    metadata["generator_sha256"] = sha(HERE / "encode.py")
    shutil.copy2(HERE / "encode.py", out / "generator.py")
    metadata["generator_snapshot"] = "generator.py"
    metadata["solver_sha256"] = sha(Path(a.solver))
    metadata["source_model"] = "exact phase-padded cyclic exterior, source width fixed"
    metadata["contains_full_template_certificate"] = False
    metadata["overflow_scope"] = "exterior return only; odd overflow count is allowed"
    (out / "metadata.json").write_text(json.dumps(metadata, indent=2) + "\n")
    cmd = [a.solver, "-t", str(a.seconds), str(cnf)]
    t0 = time.monotonic()
    try:
        proc = subprocess.run(cmd, text=True, stdout=subprocess.PIPE,
                              stderr=subprocess.STDOUT, timeout=a.seconds + 5)
        log, code = proc.stdout, proc.returncode
        timeout = False
    except subprocess.TimeoutExpired as exc:
        log = (exc.stdout or b"").decode() if isinstance(exc.stdout, bytes) else (exc.stdout or "")
        code, timeout = None, True
    (out / "solver.log").write_text(log)
    result = {"status": "UNKNOWN", "exit_code": code, "hard_timeout": timeout,
              "solver_seconds": time.monotonic() - t0, "wall_limit": a.seconds,
              "command": cmd, "metadata": "metadata.json", "proof_certificate": None}
    if code == 10 and "s SATISFIABLE" in log:
        positive = {int(x) for line in log.splitlines() if line.startswith("v ")
                    for x in line[2:].split() if int(x) > 0}
        # First replay every CNF clause against the returned total model.
        assigned = {abs(int(x)): int(x) > 0 for line in log.splitlines() if line.startswith("v ")
                    for x in line[2:].split() if int(x)}
        assert all(any(assigned.get(abs(x)) == (x > 0) for x in clause) for clause in formula.clauses)
        candidate = verify_candidate(metadata, positive)
        reference_replay(candidate)
        (out / "candidate.json").write_text(json.dumps(candidate, indent=2) + "\n")
        result.update(status="SAT_ORIGINAL_MAP_VERIFIED", candidate="candidate.json")
    elif code == 20 and "s UNSATISFIABLE" in log:
        result["status"] = "SOLVER_UNSAT_UNCERTIFIED"
    result["total_seconds"] = time.monotonic() - started
    (out / "result.json").write_text(json.dumps(result, indent=2) + "\n")
    with gzip.GzipFile(out / "formula.cnf.gz", "wb", mtime=0) as f:
        f.write(raw)
    cnf.unlink()
    print(json.dumps({"name": name, **{k: result[k] for k in
          ("status", "solver_seconds", "exit_code")}, "variables": metadata["variables"],
          "clauses": metadata["clauses"]}), flush=True)


if __name__ == "__main__":
    main()
