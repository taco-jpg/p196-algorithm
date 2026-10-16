# Reproduce the Agent #103 residual-five contribution

## Exact historical-source replay with full trust-zero audit

Use the official Linux Lean 4.19.0 release (compiler commit `6caaee842e94`).
The measured compiler SHA256 in this execution was
`92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023`.
The following commands assume a checkout of this contribution and a Lean path
chosen by the caller. `--evidence` must name a directory that does not yet exist.

```sh
git fetch origin 913441a936a437e5f4b82d03d7e7fae32da877af
git fetch origin 6fae6e659e5c08c59666588c71a4ed06760de85e
python3 proofs/contributions/agent-103/residual-five-20261016/check.py   --repo . --lean /absolute/path/to/lean-4.19.0-linux/bin/lean   --evidence /absolute/path/to/new-evidence-directory
```

The driver reads dependencies from immutable Git objects, verifies Git blob and
SHA256 identities, checks the one exact foundation import forwarder, scans the
compiled source, computes the dependency order, and creates an empty project
snapshot. It builds all eleven modules with `--trust=0 -j1 -DElab.async=false`.
It inventories every theorem constant by its module of origin, executes a literal
`#print axioms` for each, and rejects missing reports or nonstandard axioms.
No prebuilt project `.olean` is accepted. The driver itself does not download
source, invoke an external solver, or modify Lean.

The original successful run used the working manifest with source files under
`source/`; the publication manifest only normalizes those four paths to the
package root and adds current-tree recovery documentation. Source bytes, dependency
pins, compiler arguments, and driver bytes are identical. That specific difference
is checked in `evidence/publication-layout-check.json`; original manifests and full
commands remain inside the evidence archive.

## Current-tree registry without historical Git objects

```sh
python3 proofs/verify_project__214bf7673efe116b.py   --registry proofs/contributions/agent-103/residual-five-20261016/BUILD_REGISTRY.json   --project agent103-residual-five --check-only   --lean /absolute/path/to/lean-4.19.0-linux/bin/lean   --output /absolute/path/to/new-registry-evidence-directory
```

The source identities and staged check-only result are retained in
`evidence/registry-source-evidence.json` and the staged verification report.
Remove `--check-only` for a full project-verifier replay. Its standard invocation does not add
`--trust=0`; use the portable driver above to reproduce the recorded stricter run.
No shared accepted-build index is edited by this contribution. The registry lists
`ResidualFiveConclusion` as its root and includes all eleven module sources.

## Inspect evidence without running code

`evidence/complete-replay-evidence.manifest.json` gives a SHA256 and byte count for
every archived regular file. The archive contains relative paths only, no symbolic
links, executables, compiled project objects, or toolchain binaries. Extract into
a new empty directory and compare the files against that manifest. The original
clean `verification.json` and `FILES.json` contain detailed commands, source/object
hashes, individual theorem records, and the complete axiom union. Full ordinary
compiler stdout is retained, including genuine failures in development histories.

The separate generated-helper comparison explains why independent compilation
instances may inventory 161 versus 152 new-module theorem constants while all 63
source declarations and all non-generated names stay identical. Either number is
an execution fact about that particular compiled environment, not a mathematical
claim about 161 or 152 distinct results.
