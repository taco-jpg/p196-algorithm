#!/usr/bin/env python3
"""Fresh-directory rebuild and exhaustive axiom audit for Agent #124's prefix kernel.

Usage (from anywhere):
  python3 check.py --lean /path/to/lean-4.19.0/bin/lean --evidence /new/empty/dir [--jobs 2]
                   [--certs k5,k6]

The evidence directory must not exist.  Every source is copied from the
repository checkout into EVIDENCE/src and hashed before compilation; objects
are written only to EVIDENCE/out, so no pre-existing .olean is imported.
After a successful build, a generated audit module enumerates every theorem
constant defined in an Agent #124 module (names Agent124* and A124*) and
computes its transitive axioms with a memoized traversal of types and values.
Any axiom outside propext, Classical.choice, Quot.sound, any axiom declared in
those modules, or any forbidden token in their code fails the run.
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
import time
from concurrent.futures import FIRST_COMPLETED, ThreadPoolExecutor, wait
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]
CORE = REPO / "proofs/research/continuation/LychrelDigitSums.lean"
CORE_PIN = "ca5f46523b7cff02c00918b6466a97963087b499fb5f184232b8b3d806dc0b57"
A104 = REPO / "proofs/contributions/agent-104/seven-column-kernel"
BASE = [CORE,
        A104 / "PrefixInverse.lean", A104 / "FastInverse.lean", A104 / "ActualPrefix.lean",
        A104 / "PrefixCertificate.lean", A104 / "PalindromeBridge.lean",
        A104 / "ShortBoundary.lean",
        A104 / "certificate/LongRowsBase.lean", A104 / "certificate/FastRowsBase.lean"]
MINE = ["Agent124PrefixK", "Agent124FastPred", "Agent124PrefixR", "Agent124CodeCert",
        "Agent124LeadOne"]
ALLOWED = {"propext", "Classical.choice", "Quot.sound"}
FORBIDDEN = re.compile(r"(?<![\w.'])(sorry|admit|native_decide|sorryAx|implemented_by|extern|"
                       r"decide\s*\+native|ofReduceBool)(?![\w'])")
AXIOM_DECL = re.compile(r"^\s*(?:private\s+|protected\s+)?axiom\s", re.M)


def sha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def code_only(text: str) -> str:
    """Blank out nested block comments, line comments and strings."""
    out, i, depth, in_str = [], 0, 0, False
    n = len(text)
    while i < n:
        two = text[i:i + 2]
        ch = text[i]
        if depth:
            if two == "/-":
                depth += 1; out.append("  "); i += 2
            elif two == "-/":
                depth -= 1; out.append("  "); i += 2
            else:
                out.append("\n" if ch == "\n" else " "); i += 1
        elif in_str:
            if ch == "\\":
                out.append("  "); i += 2
            else:
                in_str = ch != '"'
                out.append("\n" if ch == "\n" else " "); i += 1
        elif two == "/-":
            depth = 1; out.append("  "); i += 2
        elif two == "--":
            j = text.find("\n", i)
            j = n if j < 0 else j
            out.append(" " * (j - i)); i = j
        elif ch == '"':
            in_str = True; out.append(" "); i += 1
        else:
            out.append(ch); i += 1
    return "".join(out)


def imports_of(path: Path) -> list[str]:
    deps = []
    for line in path.read_text().splitlines():
        m = re.match(r"import\s+(\S+)", line)
        if m:
            deps.append(m.group(1))
        elif line.strip() and not line.startswith("import"):
            break
    return deps


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--lean", required=True)
    ap.add_argument("--evidence", required=True)
    ap.add_argument("--jobs", type=int, default=2)
    ap.add_argument("--certs", default="k5,k6")
    args = ap.parse_args()
    lean = Path(args.lean).resolve()
    ev = Path(args.evidence).resolve()
    if ev.exists():
        sys.exit(f"evidence directory {ev} already exists")
    src, out, logs = ev / "src", ev / "out", ev / "logs"
    for d in (src, out, logs):
        d.mkdir(parents=True)
    t_start = time.time()
    report: dict = {"tool": "agent124 check.py", "lean": str(lean), "repo": str(REPO)}
    ver = subprocess.run([str(lean), "--version"], capture_output=True, text=True)
    report["lean_version"] = ver.stdout.strip()
    try:
        report["lean_binary_sha256"] = sha(lean)
    except OSError:
        report["lean_binary_sha256"] = None
    if sha(CORE) != CORE_PIN:
        sys.exit("base LychrelDigitSums.lean does not match its pin")

    files: list[Path] = list(BASE) + [HERE / f"{m}.lean" for m in MINE]
    cert_mods: list[str] = []
    for c in [x for x in args.certs.split(",") if x]:
        cdir = HERE / "certificate" / c
        order = (cdir / "order.txt").read_text().split()
        extra = sorted(p.stem for p in cdir.glob("*.lean") if p.stem not in order)
        for m in order + extra:
            files.append(cdir / f"{m}.lean")
            cert_mods.append(m)
    summary = HERE / "Agent124PrefixSummary.lean"
    if summary.exists():
        files.append(summary)
    sources = {}
    for f in files:
        dest = src / f.name
        if dest.exists():
            sys.exit(f"duplicate module name {f.name}")
        shutil.copy2(f, dest)
        sources[f.stem] = {"path": str(f.relative_to(REPO)), "sha256": sha(dest)}
    report["sources"] = sources

    # token scan of every Agent #124 source (code only, comments/strings masked)
    scan = {}
    for name in sources:
        if name.startswith(("Agent124", "A124")):
            text = code_only((src / f"{name}.lean").read_text())
            bad = sorted(set(m.group(0) for m in FORBIDDEN.finditer(text)))
            if AXIOM_DECL.search(text):
                bad.append("axiom-declaration")
            if bad:
                scan[name] = bad
    report["token_scan_failures"] = scan
    if scan:
        report["status"] = "FAIL_TOKENS"
        (ev / "verification.json").write_text(json.dumps(report, indent=1))
        print("FAIL token scan", scan)
        return 1

    env = dict(os.environ, LEAN_PATH=f"{out}:{lean.parent.parent / 'lib' / 'lean'}")
    mods = list(sources)
    deps = {m: set(imports_of(src / f"{m}.lean")) & set(mods) for m in mods}
    builds = {}

    def build(m: str) -> int:
        t0 = time.time()
        with (logs / f"{m}.log").open("w") as log:
            p = subprocess.Popen([str(lean), "-o", str(out / f"{m}.olean"),
                                  "-i", str(out / f"{m}.ilean"), str(src / f"{m}.lean")],
                                 stdout=log, stderr=subprocess.STDOUT, env=env)
            _, status, ru = os.wait4(p.pid, 0)
        rc = os.waitstatus_to_exitcode(status)
        builds[m] = {"rc": rc, "wall": round(time.time() - t0, 2),
                     "user": round(ru.ru_utime, 2), "maxrss_mb": round(ru.ru_maxrss / 1024)}
        print(("OK " if rc == 0 else "FAIL ") + m, builds[m], flush=True)
        return rc

    done, running, failed = set(), {}, None
    with ThreadPoolExecutor(args.jobs) as ex:
        while len(done) < len(mods) and failed is None:
            ready = [m for m in mods if m not in done and m not in running and deps[m] <= done]
            while ready and len(running) < args.jobs:
                m = ready.pop(0)
                running[m] = ex.submit(build, m)
            if not running:
                failed = "dependency deadlock"
                break
            fin, _ = wait(list(running.values()), return_when=FIRST_COMPLETED)
            for m, fut in list(running.items()):
                if fut in fin:
                    del running[m]
                    if fut.result() != 0:
                        failed = m
                    done.add(m)
    report["builds"] = builds
    if failed is not None:
        report["status"] = f"FAIL_BUILD {failed}"
        (ev / "verification.json").write_text(json.dumps(report, indent=1))
        return 1

    # exhaustive transitive axiom audit of every Agent #124 theorem constant
    finals = [m for m in mods if not any(m in deps[o] for o in mods)]
    audit = src / "Agent124Audit.lean"
    audit.write_text("\n".join(f"import {m}" for m in finals) + "\nimport Lean\n" + AUDIT_BODY)
    t0 = time.time()
    res = subprocess.run([str(lean), str(audit)], capture_output=True, text=True, env=env)
    (logs / "Agent124Audit.log").write_text(res.stdout + res.stderr)
    lines = (res.stdout + res.stderr).splitlines()
    theorems, custom, bad, unsafe_impl = [], [], [], []
    for line in lines:
        if line.startswith("AUDIT_THM\t"):
            _, mod, name, axs = line.split("\t", 3)
            ax = [a for a in axs.split(",") if a]
            theorems.append({"module": mod, "name": name, "axioms": ax})
            if not set(ax) <= ALLOWED:
                bad.append(name)
        elif line.startswith("AUDIT_AXIOM_DECL\t"):
            custom.append(line)
        elif line.startswith("AUDIT_UNSAFE_IMPL\t"):
            unsafe_impl.append(line.split("\t", 2)[2])
    report["audit"] = {"returncode": res.returncode, "seconds": round(time.time() - t0, 1),
                       "theorem_count": len(theorems), "custom_axioms": custom,
                       "unsafe_compiler_implementation_decls": len(unsafe_impl),
                       "disallowed": bad,
                       "axiom_union": sorted(set(a for t in theorems for a in t["axioms"]))}
    (ev / "theorem_axioms.json").write_text(json.dumps(theorems, indent=0))
    ok = res.returncode == 0 and not custom and not bad and len(theorems) > 0
    report["status"] = "PASS" if ok else "FAIL_AUDIT"
    report["total_seconds"] = round(time.time() - t_start, 1)
    (ev / "verification.json").write_text(json.dumps(report, indent=1))
    print(report["status"], report["audit"])
    return 0 if ok else 1


AUDIT_BODY = r'''
open Lean Elab Command

partial def axDeps (env : Environment) (n : Name) :
    StateT (Std.HashMap Name (Array Name)) Id (Array Name) := do
  if let some r := (← get).get? n then return r
  modify (·.insert n #[])
  let some ci := env.find? n | return #[]
  let mut acc : Array Name := #[]
  match ci with
  | .axiomInfo _ => acc := #[n]
  | _ =>
    let mut deps := ci.type.getUsedConstants
    if let some v := ci.value? (allowOpaque := true) then
      deps := deps ++ v.getUsedConstants
    match ci with
    | .inductInfo v => deps := deps ++ v.ctors.toArray
    | _ => pure ()
    for d in deps do
      for a in (← axDeps env d) do
        if !acc.contains a then acc := acc.push a
  modify (·.insert n acc)
  return acc

run_cmd do
  let env ← getEnv
  let mut cache : Std.HashMap Name (Array Name) := {}
  let mut count := 0
  for (name, info) in env.constants.toList do
    if let some idx := env.getModuleIdxFor? name then
      let mod := (env.allImportedModuleNames[idx.toNat]!).toString
      if mod.startsWith "Agent124" || mod.startsWith "A124" then
        match info with
        | .axiomInfo v =>
          if v.isUnsafe then IO.println s!"AUDIT_UNSAFE_IMPL\t{mod}\t{name}"
          else IO.println s!"AUDIT_AXIOM_DECL\t{mod}\t{name}"
        | .thmInfo _ =>
          let (axs, c') := (axDeps env name).run cache
          cache := c'
          let s := ",".intercalate (axs.toList.map toString)
          IO.println s!"AUDIT_THM\t{mod}\t{name}\t{s}"
          count := count + 1
        | _ => pure ()
  IO.println s!"AUDIT_COUNT\t{count}"
'''

if __name__ == "__main__":
    sys.exit(main())
