#!/usr/bin/env python3
"""Verify the whole repository in one command:  python3 tools/verify.py

1. Repository rules: every .lean file under lean/P196 is a module of at least
   one registered project, no two files have identical content, the registry
   lists no missing module, and no source (outside comments and strings) uses
   sorry, admit, native_decide or declares an axiom.
2. `lake build` of every module (Lean 4.19.0, pinned in lean/lean-toolchain).
3. `#print axioms` for every registered endpoint; only propext,
   Classical.choice and Quot.sound are allowed (so no sorry, no custom axiom,
   no native_decide).
Exit status 0 means everything passed.

Faster check of only what changed (what agents run before pushing):

    python3 tools/verify.py --changed            # compared with origin/main
    python3 tools/verify.py --changed <commit>   # compared with any commit

Step 1 still checks the whole repository (it takes seconds). Step 2 builds only the
Lean files that are new or changed, plus every file that imports them (Lake also builds
whatever they import). Step 3 audits only the projects that contain those files or whose
registry entry changed.
"""
import collections, hashlib, json, os, re, subprocess, sys, tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LEAN = os.path.join(ROOT, "lean")
REG = json.load(open(os.path.join(LEAN, "registry.json")))
ALLOWED = set(REG["allowed_axioms"])
fail = []

CHANGED = "--changed" in sys.argv
BASE = None
if CHANGED:
    i = sys.argv.index("--changed")
    BASE = sys.argv[i + 1] if len(sys.argv) > i + 1 and not sys.argv[i + 1].startswith("-") else "origin/main"
    def git(*a):
        return subprocess.run(["git", "-C", ROOT, *a], capture_output=True, text=True)
    if git("rev-parse", "--verify", "-q", BASE + "^{commit}").returncode != 0:
        sys.exit(f"--changed: unknown base commit {BASE!r} (run git fetch first)")

# 1. repository rules
files = {}
for dp, _, fns in os.walk(os.path.join(LEAN, "P196")):
    for fn in fns:
        if fn.endswith(".lean"):
            p = os.path.join(dp, fn)
            mod = os.path.relpath(p, LEAN)[:-5].replace(os.sep, ".")
            files[mod] = hashlib.sha256(open(p, "rb").read()).hexdigest()
registered = {m for p in REG["projects"].values() for m in p["modules"]}
for m in sorted(set(files) - registered):
    fail.append(f"unregistered Lean file: {m} (add it to a project in lean/registry.json or remove it)")
for m in sorted(registered - set(files)):
    fail.append(f"registered module has no file: {m}")
seen = {}
for m, h in files.items():
    if h in seen:
        fail.append(f"duplicate content: {m} == {seen[h]}")
    seen[h] = m
def strip(src):
    out, i, n, depth = [], 0, len(src), 0
    while i < n:
        c = src[i]
        if depth == 0 and c == '"':
            j = i + 1
            while j < n and src[j] != '"': j += 2 if src[j] == "\\" else 1
            out.append('""'); i = j + 1; continue
        if src.startswith("/-", i): depth += 1; i += 2; continue
        if depth and src.startswith("-/", i): depth -= 1; i += 2; continue
        if depth: out.append("\n" if c == "\n" else ""); i += 1; continue
        if src.startswith("--", i):
            j = src.find("\n", i); i = n if j < 0 else j; continue
        out.append(c); i += 1
    return "".join(out)
BANNED = re.compile(r"(?<![\w.'])(sorry|admit|native_decide)(?![\w'])|^\s*(?:@\[[^\]]*\]\s*)*(?:private\s+|protected\s+)?axiom\s", re.M)
for m in sorted(files):
    src = strip(open(os.path.join(LEAN, *m.split(".")) + ".lean", encoding="utf-8").read())
    for hit in BANNED.finditer(src):
        line = src.count("\n", 0, hit.start()) + 1
        fail.append(f"{m}:{line}: forbidden '{hit.group(0).strip()}'")
print(f"[rules] {len(files)} Lean files, {len(REG['projects'])} projects, "
      f"{'OK' if not fail else str(len(fail)) + ' problem(s)'}", flush=True)

# which modules and projects to build and audit
targets, audit_projects = None, None
if CHANGED:
    paths = set(git("diff", "--name-only", "--diff-filter=ACMR", BASE, "--", "lean/P196").stdout.split())
    paths |= set(git("ls-files", "--others", "--exclude-standard", "lean/P196").stdout.split())
    changed = {p[len("lean/"):-5].replace("/", ".") for p in paths if p.endswith(".lean")} & set(files)
    importers = collections.defaultdict(set)
    IMP = re.compile(r"^\s*import\s+(.+)$", re.M)
    for m in files:
        src = strip(open(os.path.join(LEAN, *m.split(".")) + ".lean", encoding="utf-8").read())
        for line in IMP.findall(src):
            for dep in line.split():
                importers[dep].add(m)
    targets, todo = set(), list(changed)
    while todo:
        m = todo.pop()
        if m in targets: continue
        targets.add(m); todo.extend(importers[m])
    try:
        old_reg = json.loads(git("show", f"{BASE}:lean/registry.json").stdout)["projects"]
    except Exception:
        old_reg = {}
    audit_projects = {n for n, p in REG["projects"].items()
                      if set(p["modules"]) & targets or old_reg.get(n) != p}
    print(f"[changed] against {BASE}: {len(changed)} new/changed Lean file(s); building {len(targets)} module(s); "
          f"auditing {len(audit_projects)} project(s)", flush=True)

# 2. build
# Lake runs one lean process per thread of LEAN_NUM_THREADS (default: every core). A single file may
# need several GB, so by default run at most one file per 8 GB of RAM (set LEAN_NUM_THREADS to override).
def ram_gb():
    try:
        if sys.platform == "darwin":
            return int(subprocess.run(["sysctl", "-n", "hw.memsize"], capture_output=True, text=True).stdout) / 2**30
        return os.sysconf("SC_PAGE_SIZE") * os.sysconf("SC_PHYS_PAGES") / 2**30
    except Exception:
        return 8
os.environ.setdefault("LEAN_NUM_THREADS", str(max(1, min(os.cpu_count() or 1, int(ram_gb() // 8)))))
print(f"[build] up to {os.environ['LEAN_NUM_THREADS']} Lean file(s) at a time", flush=True)
if targets is not None and not targets:
    r = subprocess.CompletedProcess([], 0, "", "")
else:
    r = subprocess.run(["lake", "build", *sorted(targets or [])], cwd=LEAN, capture_output=True, text=True)
sys.stdout.write(r.stdout[-4000:]); sys.stderr.write(r.stderr[-4000:])
if "declaration uses 'sorry'" in r.stdout + r.stderr:
    fail.append("build reports a declaration that uses sorry")
if r.returncode != 0:
    fail.append("lake build failed")
    print("\n".join(fail)); sys.exit(1)
print("[build] OK", flush=True)

# 3. axiom audit
# names may contain ' (e.g. value_lt'), so match up to the last "' depends" / "' does not" on the line
AX = re.compile(r"^'(.+)' (?:depends on axioms: \[([^\]]*)\]|does not depend on any axioms)", re.M)
total = 0
with tempfile.TemporaryDirectory() as td:
    for name, p in sorted(REG["projects"].items()):
        if audit_projects is not None and name not in audit_projects: continue
        eps = p["endpoints"]
        if not eps: continue
        # one audit file per root set; drafts audit each module on its own (versions may clash if imported together)
        batches = collections.defaultdict(list)
        if p.get("endpoint_modules"):
            for e in eps: batches[(p["endpoint_modules"][e],)].append(e)
        else:
            batches[tuple(p["roots"])] = eps
        got = {}
        for i, (roots, bes) in enumerate(sorted(batches.items())):
            src = "".join(f"import {m}\n" for m in roots) + "".join(f"#print axioms {e}\n" for e in bes)
            f = os.path.join(td, f"Audit{name.replace('.', '_')}_{i}.lean")
            open(f, "w").write(src)
            out = subprocess.run(["lake", "env", "lean", f], cwd=LEAN, capture_output=True, text=True)
            text = (out.stdout + out.stderr).replace("\n ", " ")
            for m in AX.finditer(text):
                got[m.group(1)] = [a.strip() for a in (m.group(2) or "").split(",") if a.strip()]
        for e in eps:
            if e not in got:
                fail.append(f"{name}: endpoint {e} not found"); continue
            bad = [a for a in got[e] if a not in ALLOWED]
            if bad: fail.append(f"{name}: {e} uses {bad}")
        total += len(eps)
print(f"[axioms] {total} endpoints checked", flush=True)

if fail:
    print("FAILED:\n  " + "\n  ".join(fail)); sys.exit(1)
print("ALL CHECKS PASSED" + (f" (changed files only, against {BASE})" if CHANGED else ""))
