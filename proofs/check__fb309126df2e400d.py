"""Fresh Lean 4.19.0 rebuild; all generated files remain in this directory."""
from pathlib import Path
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import time

here = Path(__file__).resolve().parent
project = here.parents[2]
compiler = Path(sys.argv[1]).resolve()
build = here / "build"
build.mkdir(exist_ok=True)
sources = [project / "continuation/LychrelDigitSums.lean", here / "FiniteAncestry.lean"]
hashes = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in sources}
version = subprocess.run([str(compiler), "--version"], capture_output=True,
                         text=True, check=True).stdout.strip()
assert "version 4.19.0" in version, version
env = dict(os.environ, LEAN_PATH=str(build))
records, logs = [], [version + "\n"]
for source in sources:
    shutil.copy2(source, build / source.name)
    start = time.monotonic()
    proc = subprocess.run([str(compiler), "-o", source.stem + ".olean", source.name],
                          cwd=build, env=env, capture_output=True, text=True)
    rec = {"module": source.stem, "exit_code": proc.returncode,
           "seconds": time.monotonic() - start}
    records.append(rec)
    logs.append(json.dumps(rec) + "\n" + proc.stdout + proc.stderr)
    (here / "compile.log").write_text("\n".join(logs))
    print(json.dumps(rec), flush=True)
    if proc.returncode:
        raise SystemExit(proc.returncode)
    for names in re.findall(r"depends on axioms:\s*\[([^\]]*)\]", proc.stdout, re.S):
        assert {name.strip() for name in names.split(",")} <= {
            "propext", "Classical.choice", "Quot.sound"}, names
assert hashes == {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in sources}
(here / "verification.json").write_text(json.dumps({"status": "PASS",
    "compiler": version, "modules": records, "source_sha256": hashes,
    "conditional_growth_assumption": False, "decimal_lychrel_existence_proved": False,
    "axioms_allowed": ["propext", "Classical.choice", "Quot.sound"]}, indent=2) + "\n")
