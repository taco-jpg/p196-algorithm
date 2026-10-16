#!/usr/bin/env python3
"""Rebuild Agent #9's exact inverse-fiber package without stale Lean objects."""
from __future__ import annotations
import argparse, datetime, hashlib, json, os, pathlib, re, shutil, subprocess, sys

MODULES = ["InverseFibers", "PathCounts", "WordBridge", "ActualWords", "SharpMaximum"]
DEP_SHA256 = "83102a949036799a929ba72d74ce9d76bc2a11cb3adf61e0bc06b6013b22991a"
DEP_BLOB = "a89dda20e9a9b3452f7d0272b4fbd28f7d6ce119"
NAMESPACE = "P196.Agent9.InverseFibers."

def sha256(path: pathlib.Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def git_blob(path: pathlib.Path) -> str:
    raw = path.read_bytes()
    return hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--lean", required=True, type=pathlib.Path)
    ap.add_argument("--dependency", required=True, type=pathlib.Path,
                    help="Unmodified Agent8 PeriodObstructions.lean from the pinned repository snapshot")
    ap.add_argument("--output", required=True, type=pathlib.Path)
    args = ap.parse_args()
    root = pathlib.Path(__file__).resolve().parent
    out = args.output.resolve()
    lean = args.lean.resolve()
    dep = args.dependency.resolve()
    if out.exists():
        ap.error("Output directory already exists; use a fresh directory.")
    if sha256(dep) != DEP_SHA256 or git_blob(dep) != DEP_BLOB:
        ap.error("Dependency differs from the pinned, attributed Agent8 source.")
    version = subprocess.run([str(lean), "--version"], check=True, text=True, capture_output=True).stdout.strip()
    if "version 4.19.0," not in version or "6caaee842e94" not in version:
        raise RuntimeError("Expected official Lean 4.19.0, commit 6caaee842e94")
    out.mkdir(parents=True)
    shutil.copyfile(dep, out / "PeriodObstructions.lean")
    names, sources = [], {}
    for module in MODULES:
        source = root / (module + ".lean")
        text = source.read_text()
        clean = re.sub(r"/-.*?-/", "", text, flags=re.S)
        clean = re.sub(r"--[^\n]*", "", clean)
        if re.search(r"\b(sorry|admit|native_decide|axiom)\b", clean):
            raise RuntimeError("Excluded mechanism in " + module)
        names += re.findall(r"^(?:@\[[^\n]*\]\s*)?theorem\s+(\w+)", text, re.M)
        sources[source.name] = {"sha256":sha256(source), "git_blob":git_blob(source)}
        shutil.copyfile(source, out / source.name)
    if len(names) != len(set(names)):
        raise RuntimeError("Duplicate exported theorem names")
    audit = out / "Audit.lean"
    audit.write_text("import SharpMaximum\n" + "".join("#print axioms "+NAMESPACE+n+"\n" for n in names))
    env = dict(os.environ, LEAN_PATH=str(out))
    commands = []
    for module in ["PeriodObstructions"] + MODULES + ["Audit"]:
        command = [str(lean), "-o", str(out / (module+".olean")), str(out / (module+".lean"))]
        proc = subprocess.run(command, cwd=out, env=env, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        (out / (module+".log")).write_text(proc.stdout)
        commands.append({"command":command, "exit_code":proc.returncode})
        if proc.returncode or re.search(r"\b(error|warning):", proc.stdout):
            print(proc.stdout, end="")
            raise RuntimeError(module + " build was not clean")
    report = (out / "Audit.log").read_text()
    observed = set()
    groups = re.findall(r"depends on axioms: \[([^]]*)\]", report)
    for group in groups:
        observed.update(x.strip() for x in group.split(",") if x.strip())
    if observed - {"propext", "Classical.choice", "Quot.sound"}:
        raise RuntimeError("Excluded or unrecognized transitive axioms: " + repr(observed))
    if len(groups) + report.count("does not depend on any axioms") != len(names):
        raise RuntimeError("Incomplete export audit")
    result = {"agent":"Agent #9", "status":"LEAN-CHECKED", "toolchain":version,
      "sources":sources, "dependency":{"file":"PeriodObstructions.lean", "original_agent":"Agent #8",
      "source_commit":"2eb05ef47671d6b1883e54fec9f6a4f8de9ed8f5", "git_blob":DEP_BLOB, "sha256":DEP_SHA256},
      "theorems":names, "axioms":sorted(observed), "commands":commands,
      "time_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),
      "scope":"Exact duplicate-free canonical even-width no-overflow pair-word fibers for Agent8.stepWord; sharp maximum max(1,F_(m-1)) for every m>=1; maximizing targets avoid palindromes at their next normalization for m>=2.",
      "not_claimed":["individual integer inverse-fiber cardinalities", "overflow-branch bound", "infinite avoidance", "196 resolution"],
      "independent_review":False, "integrated":False}
    (out / "verification.json").write_text(json.dumps(result, indent=2)+"\n")
    print(json.dumps({"status":result["status"], "theorem_count":len(names),
        "axioms":result["axioms"], "time_utc":result["time_utc"], "sources":sources}, indent=2))
    return 0
if __name__ == "__main__":
    sys.exit(main())
