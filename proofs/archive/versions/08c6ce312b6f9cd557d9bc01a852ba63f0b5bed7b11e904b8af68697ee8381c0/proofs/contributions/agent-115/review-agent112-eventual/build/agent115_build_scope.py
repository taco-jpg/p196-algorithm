#!/usr/bin/env python3
"""Agent #115 independent fresh build (generic, SCOPE-driven mapping).

Written independently of Agent #103's verify_*.py drivers. Only the
module-name -> source-file mapping is taken from the package layout
(it is data: where each imported module lives in the pinned tree).

Usage: agent115_build.py <exported-tree-root> <empty-build-dir> <lean-binary> [workers]

* copies every source into <build>/src/<Module>.lean and records SHA-256
* rejects sorry/admit/native_decide/axiom/sorryAx tokens outside comments
  (the pinned base LychrelDigitSums.lean is checked by hash instead)
* compiles in topological order from an empty object directory, at most
  `workers` concurrent `lean` processes, each with -DElab.async=false
* records wall time, exit status and peak RSS of every compilation
"""
import hashlib, json, os, re, subprocess, sys, time, resource
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, FIRST_COMPLETED, wait

SCOPE = "proofs/contributions/agent-112/eventual-realizability/SCOPE.json"
BASE_SHA256 = "ca5f46523b7cff02c00918b6466a97963087b499fb5f184232b8b3d806dc0b57"


def sha(b):
    return hashlib.sha256(b).hexdigest()


def strip_comments(text):
    out, i, depth = [], 0, 0
    while i < len(text):
        if text.startswith("/-", i):
            depth += 1; i += 2
        elif depth and text.startswith("-/", i):
            depth -= 1; i += 2
        elif depth:
            i += 1
        elif text.startswith("--", i):
            j = text.find("\n", i); i = len(text) if j < 0 else j
        else:
            out.append(text[i]); i += 1
    if depth:
        raise SystemExit("unterminated comment")
    return "".join(out)


def mapping(root):
    """Module -> source path, taken only from the package's SCOPE.json data.
    Hashes are re-checked independently below."""
    scope = json.loads((root / SCOPE).read_text())
    m = {}
    for e in scope["modules"]:
        p = root / e["path"]
        assert sha(p.read_bytes()) == e["sha256"], ("SCOPE hash mismatch", e["module"])
        m[e["module"]] = p
    return m


def closure(m, targets):
    order, imports, seen, stack = [], {}, set(), set()
    forbidden = re.compile(r"\b(sorry|admit|native_decide|axiom|sorryAx|ofReduceBool|implemented_by|extern)\b")

    def visit(n):
        if n in seen:
            return
        if n in stack:
            raise SystemExit("import cycle at " + n)
        stack.add(n)
        blob = m[n].read_bytes()
        code = strip_comments(blob.decode())
        if n == "LychrelDigitSums":
            assert sha(blob) == BASE_SHA256, "base hash mismatch"
        else:
            hit = forbidden.search(code)
            assert not hit, (n, hit.group(0))
        deps = [t for line in re.findall(r"^import\s+([^\n]+)", code, re.M) for t in line.split()]
        for d in deps:
            assert d in m or d.split(".")[0] in ("Init", "Std", "Lean"), (n, d)
        imports[n] = [d for d in deps if d in m]
        for d in imports[n]:
            visit(d)
        stack.discard(n); seen.add(n); order.append(n)

    for t in targets:
        visit(t)
    return order, imports


def compile_one(lean, build, name, env):
    src = build / "src" / (name + ".lean")
    olean = build / "obj" / (name + ".olean")
    ilean = build / "obj" / (name + ".ilean")
    log = build / "logs" / (name + ".log")
    t0 = time.time()
    cmd = [str(lean), "-DElab.async=false", "--root=" + str(build / "src"),
           "-o", str(olean), "-i", str(ilean), str(src)]
    runner = ("import resource,subprocess,sys;"
              "r=subprocess.run(sys.argv[2:],stdout=open(sys.argv[1],'w'),stderr=subprocess.STDOUT);"
              "print(r.returncode, resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss)")
    out = subprocess.run([sys.executable, "-I", "-c", runner, str(log)] + cmd,
                         env=env, capture_output=True, text=True)
    rc, rss = (int(x) for x in out.stdout.split())
    return {"module": name, "exit": rc, "seconds": round(time.time() - t0, 1),
            "peak_rss_kb": rss, "log_sha256": sha(log.read_bytes()),
            "olean_sha256": sha(olean.read_bytes()) if olean.exists() else None}


def main():
    root, build, lean = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve(), Path(sys.argv[3]).resolve()
    workers = int(sys.argv[4]) if len(sys.argv) > 4 else 2
    targets = sys.argv[5].split(",") if len(sys.argv) > 5 else ["EventualCompat"]
    if build.exists() and any(build.iterdir()):
        raise SystemExit("build directory must be empty")
    for sub in ("src", "obj", "logs"):
        (build / sub).mkdir(parents=True)
    m = mapping(root)
    order, imports = closure(m, targets)
    sources = {}
    for n in order:
        blob = m[n].read_bytes()
        (build / "src" / (n + ".lean")).write_bytes(blob)
        sources[n] = {"path": str(m[n].relative_to(root)), "sha256": sha(blob), "imports": imports[n]}
    libdir = subprocess.run([str(lean), "--print-libdir"], capture_output=True, text=True).stdout.strip()
    env = {"PATH": "/usr/bin:/bin", "LEAN_PATH": str(build / "obj") + ":" + libdir, "HOME": str(build)}
    report = {"schema": 1, "driver": "agent115_build.py", "driver_sha256": sha(Path(__file__).read_bytes()),
              "lean": str(lean), "lean_sha256": sha(lean.read_bytes()),
              "lean_version": subprocess.run([str(lean), "--version"], capture_output=True, text=True).stdout.strip(),
              "targets": targets, "workers": workers, "order": order, "sources": sources,
              "results": [], "started": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
    rpath = build / "build_report.json"
    done, failed, running = set(), set(), {}
    with ThreadPoolExecutor(workers) as pool:
        while len(done) + len(failed) < len(order):
            for n in order:
                if n in done or n in failed or n in running.values():
                    continue
                if len(running) >= workers:
                    break
                if any(d in failed for d in imports[n]):
                    failed.add(n); report["results"].append({"module": n, "exit": None, "skipped": "dependency failed"})
                    continue
                if all(d in done for d in imports[n]):
                    running[pool.submit(compile_one, lean, build, n, env)] = n
            if not running:
                break
            fin, _ = wait(list(running), return_when=FIRST_COMPLETED)
            for f in fin:
                n = running.pop(f)
                r = f.result()
                report["results"].append(r)
                (done if r["exit"] == 0 else failed).add(n)
                print(json.dumps(r), flush=True)
                rpath.write_text(json.dumps(report, indent=1) + "\n")
    report["finished"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    report["status"] = "PASS" if not failed and len(done) == len(order) else "FAIL"
    rpath.write_text(json.dumps(report, indent=1) + "\n")
    print(report["status"], len(done), "modules")


if __name__ == "__main__":
    main()
