# Recorded Lean runtime

The official Lean 4.19.0 executable and library hashes are recorded in the package verification report. The wrapper and readlink shim source are retained to explain this host-specific executable-path workaround. The shim only replaces the current process path `/proc/<PID>/exe` with `/proc/self/exe`; it does not alter Lean source, proof terms, evaluation, or kernel checking. Normal Linux installations should invoke official `lean` directly.

Author command (exit 0):

```sh
python3 proofs/contributions/agent-107/partition-seam-response/check.py /workspace/scratch/64704429df15/env107/lean --build-dir /workspace/scratch/64704429df15/build107-final
```

The independent reviewer command and empty build directory are recorded under `../review/`. Runtime binaries, compiled shim, objects and copied dependency directories are reproducible infrastructure and are not published. Source snapshots and substantive compiler/audit logs are retained.
