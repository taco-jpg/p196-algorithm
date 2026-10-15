#!/usr/bin/env python3
"""Fresh clean build and exhaustive transitive axiom audit for the
Agent #119 eight-family package (EightFamilies.lean).

Usage:
  python3 check.py /absolute/path/to/lean --evidence /new/empty/dir [--jobs 2]

* The evidence directory must not exist.  Every source in the import closure is
  copied into a fresh flat snapshot and hashed before compilation; no previously
  compiled project object is used.
* Reused sources (base module and Agent #104's accepted structural modules) are
  pinned to the SHA256 values of Agent #104's integrated source pins.
* Every theorem constant (including private and generated ones) that belongs to
  an Agent #119 module is discovered from the compiled environment and audited
  with an actual `#print axioms`; the union must lie within
  {propext, Classical.choice, Quot.sound}.  Any declared axiom in those modules
  fails the run.  Selected reused-module endpoints are audited as well.
* Agent #119 sources are scanned (comments and strings masked) for the tokens
  sorry/admit/axiom/native_decide/sorryAx/ofReduceBool.

The report states build and axiom facts only; the mathematical meaning comes
from the theorem statements (see README.md).
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import threading
import time
from concurrent.futures import FIRST_COMPLETED, ThreadPoolExecutor, wait
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]
K104 = REPO / "proofs/contributions/agent-104/seven-column-kernel"

# module -> (path relative to repository root, required SHA256 or None)
REUSED = {
    "LychrelDigitSums": ("proofs/research/continuation/LychrelDigitSums.lean",
                         "ca5f46523b7cff02c00918b6466a97963087b499fb5f184232b8b3d806dc0b57"),
    "PrefixInverse": ("proofs/contributions/agent-104/seven-column-kernel/PrefixInverse.lean",
                      "0a93622752fa22cf6c8de2efc8500dc313498d59831bb0e5381b3b351e0ab03e"),
    "ActualPrefix": ("proofs/contributions/agent-104/seven-column-kernel/ActualPrefix.lean",
                     "c136216ed9c4100a268643be9a471b6746320f63d0af2030b6418429e5551e76"),
    "PalindromeBridge": ("proofs/contributions/agent-104/seven-column-kernel/PalindromeBridge.lean",
                         "6c1de8cf02ec9381e80388e6b4915db6cfa4d1189d3e47c273400f0d37948093"),
}
OWN_DIR = "proofs/contributions/agent-119/eight-families"
ALLOWED = {"propext", "Classical.choice", "Quot.sound"}
FORBIDDEN = re.compile(r"(?<![\w'.])(?:sorry|admit|axiom|native_decide|sorryAx|ofReduceBool)(?![\w'])")
TOP = "EightFamilies"
REUSED_ENDPOINTS = [
    "SevenColumnProjection.actual_mem_prefixPredecessors",
    "SevenColumnProjection.actual_noOverflow",
    "SevenColumn.NoOverflow.mem_noOverflowPred",
    "SevenColumnKernel.PalindromeBridge.canonical_unique",
    "Lychrel196.step_mod9",
    "AstraModular.orbit_preserves_dvd11",
    "DecimalDigits.step_palindrome_iff_overflow",
    "DecimalCarry.no_overflow_palindrome_has_no_carries",
    "OverflowCarryNormalization.iterPairs_representation",
]


def sha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def code_only(text: str) -> str:
    """Mask (nested) block comments, line comments and string literals."""
    out, i, depth, string = [], 0, 0, False
    while i < len(text):
        pair = text[i:i + 2]
        if depth:
            if pair == "/-":
                depth, i = depth + 1, i + 2
                out.append("  ")
            elif pair == "-/":
                depth, i = depth - 1, i + 2
                out.append("  ")
            else:
                out.append("\n" if text[i] == "\n" else " ")
                i += 1
        elif string:
            if text[i] == "\\":
                out.append("  ")
                i += 2
            else:
                string = text[i] != '"'
                out.append(" ")
                i += 1
        elif pair == "/-":
            depth, i = 1, i + 2
            out.append("  ")
        elif pair == "--":
            j = text.find("\n", i)
            j = len(text) if j < 0 else j
            out.append(" " * (j - i))
            i = j
        elif text[i] == '"':
            string = True
            out.append(" ")
            i += 1
        else:
            out.append(text[i])
            i += 1
    return "".join(out)


def own_sources() -> dict[str, Path]:
    found = {}
    for p in sorted((REPO / OWN_DIR).glob("*.lean")):
        found[p.stem] = p
    return found


def imports_of(text: str) -> list[str]:
    return re.findall(r"^import\s+(\S+)", text, re.MULTILINE)


def write_json(path: Path, obj) -> None:
    tmp = path.with_suffix(".tmp")
    tmp.write_text(json.dumps(obj, indent=1, sort_keys=True) + "\n")
    tmp.replace(path)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("lean")
    ap.add_argument("--evidence", required=True, type=Path)
    ap.add_argument("--jobs", type=int, default=2)
    args = ap.parse_args()
    evidence = args.evidence.resolve()
    evidence.mkdir(parents=True, exist_ok=False)
    snap = evidence / "snapshot"
    logs = evidence / "logs"
    snap.mkdir()
    logs.mkdir()
    report_path = evidence / "verification.json"
    report = {"status": "IN_PROGRESS", "allowed_axioms": sorted(ALLOWED), "jobs": args.jobs,
              "fresh_snapshot": True, "sources": {}, "builds": [], "theorems": {},
              "scope": "Build and transitive-axiom facts only; see README.md for theorem meaning."}
    try:
        report["source_commit"] = subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=REPO, text=True).strip()
        report["worktree_clean_for_package"] = subprocess.run(
            ["git", "diff", "--quiet", "HEAD", "--", OWN_DIR], cwd=REPO).returncode == 0
    except Exception:  # pragma: no cover - outside git
        report["source_commit"] = None
    write_json(report_path, report)
    env = {k: v for k, v in os.environ.items() if k not in ("LEAN_PATH", "LEAN_SRC_PATH", "LEAN_SYSROOT")}
    env["LEAN_PATH"] = str(snap)
    lock = threading.Lock()

    def run(label: str, cmd: list[str]) -> str:
        log = logs / f"{label}.log"
        t0 = time.monotonic()
        with log.open("w") as out:
            proc = subprocess.Popen(cmd, cwd=snap, env=env, stdout=out, stderr=subprocess.STDOUT)
            _, status, usage = os.wait4(proc.pid, 0)
        code = os.waitstatus_to_exitcode(status)
        rec = {"label": label, "command": cmd, "exit_code": code,
               "seconds": round(time.monotonic() - t0, 3), "max_rss_kib": usage.ru_maxrss,
               "log": str(log.relative_to(evidence)), "log_sha256": sha(log)}
        with lock:
            report["builds"].append(rec)
            write_json(report_path, report)
        print(json.dumps(rec), flush=True)
        if code:
            raise RuntimeError(f"{label} failed with exit {code}; see {log}")
        return log.read_text()

    try:
        lean = str(Path(shutil.which(args.lean) or args.lean).resolve())
        version = run("version", [lean, "--version"]).strip()
        if not re.search(r"version 4\.19\.0, .*commit 6caaee842e94, Release", version):
            raise ValueError(f"unexpected Lean: {version}")
        report["lean"] = {"path": lean, "version": version, "sha256": sha(Path(lean))}
        own = own_sources()
        modules: dict[str, tuple[Path, str | None, str]] = {}
        for m, (rel, pin) in REUSED.items():
            modules[m] = (REPO / rel, pin, "reused")
        for m, p in own.items():
            if m in modules:
                raise ValueError(f"module name clash: {m}")
            modules[m] = (p, None, "agent-119")
        # Import closure of the top module.
        order, seen, active = [], set(), set()

        def visit(m: str) -> None:
            if m in seen:
                return
            if m in active:
                raise ValueError(f"import cycle at {m}")
            if m not in modules:
                return  # Std / Lean / Init
            active.add(m)
            path, pin, origin = modules[m]
            text = path.read_text()
            for dep in imports_of(text):
                visit(dep)
            digest = sha(path)
            if pin is not None and digest != pin:
                raise ValueError(f"pin mismatch for {m}: {digest} != {pin}")
            dest = snap / f"{m}.lean"
            shutil.copyfile(path, dest)
            if sha(dest) != digest:
                raise ValueError(f"copy changed {m}")
            local = [d for d in imports_of(text) if d in modules]
            report["sources"][m] = {"origin": origin, "path": str(path.relative_to(REPO)),
                                    "sha256": digest, "imports": local, "pinned": pin is not None}
            if origin == "agent-119":
                hits = [(n + 1, line.strip()) for n, line in enumerate(code_only(text).splitlines())
                        if FORBIDDEN.search(line)]
                report["sources"][m]["forbidden_token_hits"] = hits
                if hits:
                    raise ValueError(f"forbidden token in {m}: {hits[:3]}")
            active.discard(m)
            seen.add(m)
            order.append(m)

        visit(TOP)
        unused = sorted(set(own) - seen)
        report["agent119_sources_outside_build"] = unused
        report["build_order"] = order
        write_json(report_path, report)
        deps = {m: set(report["sources"][m]["imports"]) for m in order}
        remaining, done, running = list(order), set(), {}
        with ThreadPoolExecutor(max_workers=args.jobs) as pool:
            while remaining or running:
                ready = [m for m in remaining if deps[m] <= done]
                for m in ready[: max(0, args.jobs - len(running))]:
                    remaining.remove(m)
                    running[pool.submit(run, m, [lean, "-j1", "-DElab.async=false",
                                                 "-o", f"{m}.olean", f"{m}.lean"])] = m
                if not running:
                    raise RuntimeError("no buildable module")
                fin, _ = wait(running, return_when=FIRST_COMPLETED)
                for f in fin:
                    m = running.pop(f)
                    f.result()
                    done.add(m)
                    report["sources"][m]["object_sha256"] = sha(snap / f"{m}.olean")
        own_mods = [m for m in order if report["sources"][m]["origin"] == "agent-119"]
        names = ", ".join(json.dumps(m) for m in own_mods)
        reused = "\n".join(f"#print axioms {n}" for n in REUSED_ENDPOINTS)
        audit = (f"import {TOP}\nimport Lean\nopen Lean Elab Command\n"
                 "set_option maxRecDepth 100000\nset_option maxHeartbeats 0\n"
                 "run_cmd do\n  let env ← getEnv\n"
                 f"  let selected : List String := [{names}]\n"
                 "  for (name, info) in env.constants.toList do\n"
                 "    if let some idx := env.getModuleIdxFor? name then\n"
                 "      let mod := env.allImportedModuleNames[idx.toNat]!\n"
                 "      if selected.contains mod.toString then\n"
                 "        match info with\n"
                 "        | .axiomInfo v =>\n"
                 "          if v.isUnsafe then logInfo m!\"UNSAFE_IMPL {mod} {name}\"\n"
                 "          else throwError m!\"CUSTOM_AXIOM {mod} {name}\"\n"
                 "        | .thmInfo _ =>\n"
                 "          logInfo m!\"AUDIT_THEOREM {mod} {name}\"\n"
                 "          elabCommand (← `(command| #print axioms $(mkIdent name)))\n"
                 "        | _ => pure ()\n"
                 f"{reused}\n")
        (snap / "AuditAgent119.lean").write_text(audit)
        report["audit_source_sha256"] = sha(snap / "AuditAgent119.lean")
        out = run("AuditAgent119", [lean, "-j1", "-DElab.async=false", "AuditAgent119.lean"])
        thms = re.findall(r"AUDIT_THEOREM (\S+) (\S+)", out)
        names_mod = {n: m for m, n in thms}
        if not names_mod or len(names_mod) != len(thms):
            raise ValueError("empty or duplicate theorem inventory")
        audited = {}
        for n, ax in re.findall(r"'([^']+)' depends on axioms: \[([^\]]*)\]", out):
            audited[n] = sorted(a.strip() for a in ax.split(",") if a.strip())
        for n in re.findall(r"'([^']+)' does not depend on any axioms", out):
            audited[n] = []
        missing = set(names_mod) - set(audited)
        if missing:
            raise ValueError(f"unaudited theorems: {sorted(missing)[:5]}")
        for n, ax in audited.items():
            if not set(ax) <= ALLOWED:
                raise ValueError(f"disallowed axioms for {n}: {ax}")
        report["theorems"] = {n: {"module": names_mod[n], "axioms": audited[n]} for n in sorted(names_mod)}
        report["reused_endpoints"] = {n: audited.get(n) for n in REUSED_ENDPOINTS}
        if any(v is None for v in report["reused_endpoints"].values()):
            raise ValueError("reused endpoint audit missing")
        report["theorem_count"] = len(names_mod)
        report["unsafe_implementation_constants"] = re.findall(r"UNSAFE_IMPL (\S+) (\S+)", out)
        report["axiom_union"] = sorted(set().union(*audited.values()))
        for m, rec in report["sources"].items():
            if sha(snap / f"{m}.lean") != rec["sha256"]:
                raise ValueError(f"snapshot changed: {m}")
        report["status"] = "PASS"
        write_json(report_path, report)
        print(f"PASS: {len(order)} modules freshly compiled; {len(names_mod)} Agent #119 theorem "
              f"constants audited; axiom union {report['axiom_union']}", flush=True)
        return 0
    except Exception as exc:
        report["status"] = "FAIL"
        report["failure"] = str(exc)
        write_json(report_path, report)
        print(f"FAIL: {exc}", file=sys.stderr, flush=True)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
