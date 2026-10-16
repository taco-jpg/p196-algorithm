from pathlib import Path
import subprocess, os, json, time, hashlib
repo = Path(__file__).resolve().parents[5]
ev = Path(__file__).resolve().parent
src = repo / "proofs/Agent101PalindromeFibers.lean"
attempts = ev / "attempts"
attempts.mkdir(exist_ok=True)
i = len(list(attempts.glob("attempt-*.lean"))) + 1
(attempts / f"attempt-{i:03}.lean").write_bytes(src.read_bytes())
build = ev / "build"
build.mkdir(exist_ok=True)
env = os.environ.copy()
env["LEAN_PATH"] = "/workspace/scratch/2a8a87fd78df/agent101-numeric-build"
cmd = ["/workspace/scratch/2a8a87fd78df/agent101-runtime/toolchain/lean-4.19.0-linux/bin/lean", "-o", str(build / "Agent101PalindromeFibers.olean"), str(src)]
t = time.time()
r = subprocess.run(cmd, cwd=repo, env=env, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
(attempts / f"attempt-{i:03}.log").write_text(r.stdout)
meta = {"attempt": i, "command": cmd, "lean_path": env["LEAN_PATH"], "returncode": r.returncode, "seconds": time.time()-t, "source_sha256": hashlib.sha256(src.read_bytes()).hexdigest()}
(attempts / f"attempt-{i:03}.json").write_text(json.dumps(meta,indent=2)+"\n")
print(json.dumps(meta))
print(r.stdout)
