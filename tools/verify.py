#!/usr/bin/env python3
"""Verify the whole repository in one command:  python3 tools/verify.py

1. Repository rules: every .lean file under lean/P196 is a module of at least
   one registered project, no two files have identical content, the registry
   lists no missing module, and no source (outside comments and strings) uses
   sorry, admit, native_decide or declares an axiom, and none uses meta-programming that
   can bypass the kernel (debug options, run_cmd/run_elab, addDecl, implemented_by, unsafe, #eval, ...).
2. `lake build` of every module (Lean 4.19.0, pinned in lean/lean-toolchain), then
   lean4checker on every built module: the kernel re-checks every stored declaration
   (modules whose build output is unchanged since lean4checker last accepted them are
   skipped; see lean/.lake/kernel-replay-ok.json).
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

# Registry fragments: lean/registry.d/<Name>.json holds {"<Name>": {project entry}}.  New results go there, so that
# parallel contributors never edit the same file (lean/registry.json is the frozen legacy part).
def load_fragments(read_text, names):
    out = {}
    for n in names:
        stem = os.path.basename(n)[:-5]
        try:
            frag = json.loads(read_text(n))
        except Exception as e:
            fail.append(f"{n}: not valid JSON ({e})"); continue
        if list(frag) != [stem]:
            fail.append(f"{n}: must contain exactly one project named {stem!r}"); continue
        out[stem] = frag[stem]
    return out
_rd = os.path.join(LEAN, "registry.d")
_names = sorted(os.path.join(_rd, f) for f in os.listdir(_rd) if f.endswith(".json")) if os.path.isdir(_rd) else []
for _k, _v in load_fragments(lambda n: open(n, encoding="utf-8").read(), _names).items():
    if _k in REG["projects"]:
        fail.append(f"project {_k!r} is in both lean/registry.json and lean/registry.d/")
    REG["projects"][_k] = _v

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
# Meta-programming that can put declarations into the environment without the kernel checking them
# (e.g. `set_option debug.skipKernelTC true` + `addDecl`), or replace code at run time. Step 2b
# (lean4checker) is the real guard; this catches the obvious forms early and with a line number.
META = re.compile(r"set_option\s+debug\.|(?<![\w.'])(run_cmd|run_elab|run_meta|addDecl|addAndCompile|"
                  r"implemented_by|unsafe|modifyEnv|setEnv|initialize|builtin_initialize|elab_rules|elab|#eval)"
                  r"(?![\w'])|@\[\s*extern", re.M)
for m in sorted(files):
    src = strip(open(os.path.join(LEAN, *m.split(".")) + ".lean", encoding="utf-8").read())
    for hit in BANNED.finditer(src):
        line = src.count("\n", 0, hit.start()) + 1
        fail.append(f"{m}:{line}: forbidden '{hit.group(0).strip()}'")
    for hit in META.finditer(src):
        line = src.count("\n", 0, hit.start()) + 1
        fail.append(f"{m}:{line}: forbidden meta-programming '{hit.group(0).strip()}'")
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
    _old = [x for x in git("ls-tree", "-r", "--name-only", BASE, "lean/registry.d").stdout.split() if x.endswith(".json")]
    _fail_before = len(fail)
    old_reg.update(load_fragments(lambda n: git("show", f"{BASE}:{n}").stdout, _old))
    del fail[_fail_before:]
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

# 2b. kernel replay: lean4checker re-checks every declaration stored in each built module with the
# kernel, so a declaration that was added without kernel checking (a meta-programming trick that
# `#print axioms` does not see) is rejected. Built once from the tag matching lean/lean-toolchain.
def lean4checker():
    """Command prefix that runs lean4checker on module names, or None if it cannot run here.
    Uses the compiled binary; if that cannot start (e.g. new macOS rejects binaries linked by the
    toolchain's linker: 'dyld: __DATA_CONST segment missing SG_READ_ONLY flag'), runs the same
    program in Lean's interpreter (`lean --run`), which needs no linking. LEAN4CHECKER overrides."""
    if os.environ.get("LEAN4CHECKER"): return ["lake", "env", os.environ["LEAN4CHECKER"]], {}
    tag = open(os.path.join(LEAN, "lean-toolchain")).read().strip().split(":")[-1]
    d = os.path.join(LEAN, ".lake", "lean4checker")
    if not os.path.isdir(d):
        subprocess.run(["git", "-c", "advice.detachedHead=false", "clone", "-q", "--depth", "1", "--branch", tag,
                        "https://github.com/leanprover/lean4checker", d], check=True)
    subprocess.run(["lake", "build", "Lean4Checker"], cwd=d, check=True, capture_output=True)
    subprocess.run(["lake", "build", "lean4checker"], cwd=d, capture_output=True)
    exe = os.path.join(d, ".lake", "build", "bin", "lean4checker")
    # smoke test on a small core module (no arguments would mean "check the whole project")
    if os.path.exists(exe) and subprocess.run(["lake", "env", exe, "Init.Prelude"], cwd=LEAN,
                                              capture_output=True).returncode == 0:
        return ["lake", "env", exe], {}
    lp = subprocess.run(["lake", "env", "printenv", "LEAN_PATH"], cwd=LEAN, capture_output=True, text=True).stdout.strip()
    env = dict(os.environ, LEAN_PATH=lp + os.pathsep + os.path.join(d, ".lake", "build", "lib", "lean"))
    cmd = ["lean", "--run", os.path.join(d, "Main.lean")]
    if subprocess.run(cmd + ["Init.Prelude"], cwd=LEAN, env=env, capture_output=True).returncode == 0:
        print("[kernel replay] compiled lean4checker cannot start here; using the interpreter (lean --run)", flush=True)
        return cmd, env
    return None, None
check_mods = sorted(targets) if targets is not None else sorted(files)
# Replay ledger: a module whose .olean and Lake trace (which covers its source and all its imports)
# are byte-identical to the last time lean4checker accepted it is not replayed again. The ledger lives
# in lean/.lake, which CI caches even after a timeout, so a full replay that does not fit in one run
# continues where the previous run stopped instead of starting over.
LEDGER = os.path.join(LEAN, ".lake", "kernel-replay-ok.json")
TOOLCHAIN = open(os.path.join(LEAN, "lean-toolchain")).read().strip()
def replay_key(m):
    base = os.path.join(LEAN, ".lake", "build", "lib", "lean", *m.split("."))
    try:
        h = hashlib.sha256(TOOLCHAIN.encode())
        with open(base + ".olean", "rb") as f:
            for block in iter(lambda: f.read(1 << 20), b""): h.update(block)
        if os.path.exists(base + ".trace"):
            h.update(open(base + ".trace", "rb").read())
        return h.hexdigest()
    except OSError:
        return None
try:
    ledger = json.load(open(LEDGER))
except Exception:
    ledger = {}
keys = {m: replay_key(m) for m in check_mods}
todo_mods = [m for m in check_mods if keys[m] is None or ledger.get(m) != keys[m]]
replay_incomplete = 0
if check_mods:
    print(f"[kernel replay] {len(check_mods)} module(s); {len(check_mods) - len(todo_mods)} unchanged since "
          f"lean4checker last accepted them; {len(todo_mods)} to re-check", flush=True)
if todo_mods:
    import concurrent.futures, time
    cmd, env = lean4checker()
    if cmd is None:
        fail.append("lean4checker could not be started on this machine (neither compiled nor interpreted); "
                    "kernel replay NOT done")
    else:
        # lean4checker is one single-threaded process per chunk; run several at once (default: one per
        # core, at most one per 4 GB of RAM; KERNEL_REPLAY_JOBS overrides).
        jobs = int(os.environ.get("KERNEL_REPLAY_JOBS") or max(1, min(os.cpu_count() or 1, int(ram_gb() // 4))))
        # KERNEL_REPLAY_BUDGET_MIN: stop starting new chunks after this many minutes, so the run ends
        # (and saves the ledger) before an outer timeout kills it. Unset = no limit.
        budget = float(os.environ.get("KERNEL_REPLAY_BUDGET_MIN") or 0) * 60
        t0 = time.time()
        def save_ledger():
            tmp = LEDGER + ".tmp"
            json.dump(ledger, open(tmp, "w"), sort_keys=True); os.replace(tmp, LEDGER)
        def replay(mods):
            if budget and time.time() - t0 > budget: return mods, None, "skipped: time budget used up"
            out = subprocess.run(cmd + mods, cwd=LEAN, env=env or None, capture_output=True, text=True)
            return mods, out.returncode, (out.stdout + out.stderr).strip()
        chunks = [todo_mods[i:i + 25] for i in range(0, len(todo_mods), 25)]
        bad_chunks, done, last = [], 0, 0.0
        print(f"[kernel replay] {len(chunks)} chunk(s) of up to 25 modules, {jobs} at a time"
              + (f", budget {budget / 60:g} min" if budget else ""), flush=True)
        with concurrent.futures.ThreadPoolExecutor(jobs) as ex:
            for fut in concurrent.futures.as_completed([ex.submit(replay, c) for c in chunks]):
                mods, rc, text = fut.result()
                if rc is None: replay_incomplete += len(mods); continue
                if rc != 0: bad_chunks.append(mods)
                else:
                    for m in mods:
                        if keys[m]: ledger[m] = keys[m]
                    save_ledger()
                done += len(mods)
                if time.time() - last > 60 or done == len(todo_mods):
                    last = time.time()
                    print(f"[kernel replay] {done}/{len(todo_mods)} re-checked, {(last - t0) / 60:.1f} min", flush=True)
        # a failing chunk stops at its first problem: re-check its modules one by one to list all of them
        with concurrent.futures.ThreadPoolExecutor(jobs) as ex:
            for mods, rc, text in ex.map(lambda m: replay([m]), [m for c in bad_chunks for m in c]):
                if rc is None: replay_incomplete += 1
                elif rc != 0: fail.append(f"lean4checker rejects {mods[0]}: {text[-300:]}")
                elif keys[mods[0]]: ledger[mods[0]] = keys[mods[0]]
        save_ledger()
        if replay_incomplete:
            fail.append(f"kernel replay incomplete: {replay_incomplete} module(s) not re-checked within the "
                        f"{budget / 60:g}-minute budget; progress is saved in lean/.lake and the next run continues")
        print(f"[kernel replay] {len(todo_mods) - replay_incomplete} module(s) re-checked by lean4checker "
              f"in {(time.time() - t0) / 60:.1f} min", flush=True)

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
