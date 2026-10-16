from pathlib import Path
from hashlib import sha256
from datetime import datetime, timezone
import json, os, subprocess, sys, time

HERE = Path(__file__).resolve().parent
SOURCE = HERE.parents[3] / "Agent105DecodedFiber9df76b.lean"
LEAN = Path("/workspace/scratch/fb513c1676b0/agent102-runtime/lean-4.19.0-linux/bin/lean")
BASE = Path("/workspace/scratch/9df76b503b84/agent105-runtime/base-build")
PREV = Path("/workspace/scratch/9df76b503b84/agent105-decoder-work/proofs/contributions/agent-105/numeric-decoder-9df76b-20261016")
WORD = HERE.parent / "word-fiber/build"
number = int(sys.argv[1])
label = f"attempt{number:03d}"
folder = HERE / label
folder.mkdir(exist_ok=False)
snapshot = folder / "source.lean"
snapshot.write_bytes(SOURCE.read_bytes())
lean_path = ":".join(map(str, [WORD, PREV / "scan/build", PREV / "local/build", BASE]))
argv = [str(LEAN), "--trust=0", "-j1", "-DElab.async=false", "-o", str(HERE / "build/Agent105DecodedFiber9df76b.olean"), str(SOURCE)]
env = dict(os.environ)
env["LEAN_PATH"] = lean_path
started = datetime.now(timezone.utc).isoformat()
t0 = time.monotonic()
result = subprocess.run(argv, env=env, cwd=SOURCE.parent, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
elapsed = time.monotonic() - t0
(folder / "compile.log").write_text(result.stdout)
meta = {"argv": argv, "lean_path": lean_path, "source_sha256": sha256(snapshot.read_bytes()).hexdigest(), "started_utc": started, "elapsed_seconds": elapsed, "exit_code": result.returncode}
(folder / "result.json").write_text(json.dumps(meta, indent=2) + "\n")
print(json.dumps(meta, indent=2))
print(result.stdout)
sys.exit(result.returncode)
