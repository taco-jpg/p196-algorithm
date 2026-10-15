# Reproduce the pinned review

Obtain exact source `b2374410d427beb78fc601ee81cf15e34a1ac934` and Agent7 provenance commit `da4a1799b74b98b4199cdb224ea7a694b2657651` from the repository. Keep that source checkout clean; the review output belongs in a separate directory.

## Executed review

The exact executed harness is [executed_harness.py](execution/agent107-outer109-clean-syq1jnqb/executed_harness.py). It does not invoke the author’s build script. The manifest records all commands, source and runtime hashes, individual exit statuses, full stdout/stderr and transitive audits. [POSTFLIGHT_INTEGRITY.json](execution/agent107-outer109-clean-syq1jnqb/POSTFLIGHT_INTEGRITY.json) records the independent postflight checks.

The recorded run used the host-specific wrapper `/workspace/scratch/64704429df15/env107/lean`. Its official native executable was Lean 4.19.0, commit `6caaee842e94`, SHA-256 `92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023`. The readlink-only compatibility shim and wrapper sources are retained in [the earlier environment record](../partition-seam-response/environment/README.md). The shim changes executable-path discovery only. The exact harness deliberately checks this recorded Linux binary and shim; those host checks are not portable runtime discovery.

```sh
python3 proofs/contributions/agent-107/review-agent109-outer/execution/independent_kernel_audit.py --source /workspace/scratch/64704429df15/review109-source107 --output /new/report/path --scratch /workspace/scratch/64704429df15
```

The original evidence is preserved; use a new output path for any replay. No project `.olean`, copied build directory, or toolchain installation is included as a research result. Those are reproducible infrastructure.

## Ordinary Linux replay using official Lean

On an ordinary Linux host, the official compiler can be invoked directly without the host shim. The following alternative command block is a portable reproduction recipe; it was not a second execution during this review. It verifies the pinned source hashes, builds the same nine modules in a new directory, and executes the retained complete axiom audit. Replace the three argument paths.

```sh
python3 - /path/to/review-agent109-outer /path/to/pinned-source /path/to/lean-4.19.0/bin/lean <<'PY'
import hashlib, json, os, pathlib, shutil, subprocess, sys, tempfile
pkg, source, lean = map(pathlib.Path, sys.argv[1:])
scope = json.loads((pkg / 'SCOPE.json').read_text())
assert subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=source, text=True).strip() == scope['reviewed_source_commit']
version = subprocess.check_output([str(lean), '--version'], text=True)
assert '4.19.0' in version and '6caaee842e94' in version
build = pathlib.Path(tempfile.mkdtemp(prefix='outer109-replay-'))
env = dict(os.environ, LEAN_PATH=str(build))
env.pop('LEAN_SYSROOT', None)
env.pop('LD_PRELOAD', None)
for row in scope['dependency_sources']:
    p = source / row['path']
    assert hashlib.sha256(p.read_bytes()).hexdigest() == row['sha256']
    shutil.copyfile(p, build / p.name)
    with (build / (p.stem + '.log')).open('wb') as log:
        subprocess.run([str(lean), '-j1', '-DElab.async=false', '-o', p.stem + '.olean', p.name], cwd=build, env=env, stdout=log, stderr=subprocess.STDOUT, check=True)
audit = pkg / 'execution/agent107-outer109-clean-syq1jnqb/IndependentOuterAxioms.lean'
shutil.copyfile(audit, build / audit.name)
with (build / 'audit.log').open('wb') as log:
    subprocess.run([str(lean), '-j1', '-DElab.async=false', audit.name], cwd=build, env=env, stdout=log, stderr=subprocess.STDOUT, check=True)
print(version.strip(), build)
print((build / 'audit.log').read_text())
PY
```

Every printed target axiom list must be contained in `propext`, `Classical.choice`, `Quot.sound`; all 23 target names are explicitly listed in the audit source. For the exact-integer finite controls and trajectory decompression/hash commands, use [controls/README.md](controls/README.md). Those controls are not a Lean proof.
