# PR #177 retained verification package

This package preserves exact-source evidence and independent reviews for
`taco-jpg/p196-algorithm` PR #177 at source H
`6f48ca108dee4c07588f8c5582bcfef55388537f`, against frozen main B
`74a1c3922eb7af438fe40b23d2105ad07556e3f5`. H contains B, so H is the
combined source tree for that frozen base. Later source or base changes require
the responsible integration workflow to assess the affected evidence.

## Results and preserved failures

The original `canonical-run-001` compiled all 19 selected modules but failed
before its theorem audit because its endpoint regex rejected the legal `?` in
`stateIndex?_stateAt`. Its commands did not explicitly specify `--trust=0`.
It remains FAIL. The independently reviewed three-line repair accepts `?` only
in identifier tails and adds `--trust=0` to both Lean invocation sites.

`trust0-run-001` records 19 clean module compilations and the generated theorem
audit, all 20 commands exiting zero under `--trust=0 -j1 -DElab.async=false`.
It audits 1,453 theorem constants. `supplement-001` retains a successful safe
declaration audit and a failed literal audit caused by an invalid optional
`pp.width` setting. `supplement-002` reuses only that successful safe audit under
the runner's exact report/source/object/compiler pins, then freshly runs the
corrected literal audit to exit zero. The failed attempt remains FAIL.

The supplemental PASS covers 1,453 theorems, 414 safe definitions, no safe
opaque declarations, actual `#print axioms` for all 115 theorem constants from
the seven new modules, and all nine endpoints. Those seven modules also contain
50 audited safe definitions. The transitive axiom union is exactly
`Classical.choice`, `Quot.sound`, and `propext`. The separately enumerated 3,940
unsafe compiler implementation declarations are described in the independent
review; they are not silently counted as safe mathematical declarations.

These are generic conditional checker and closure results. They do not supply
a concrete safe invariant, prove a seed belongs to one, resolve P196, or establish
a repository-wide PASS. The unretained historical report of 20 modules / 1,445
theorems / 128 new theorems was not reused or recovered.

## Layout and preservation

- `evidence/`: every input evidence file except `.olean` and `__pycache__`,
  including original/repaired verifiers, both supplemental runner revisions,
  patches, all original failures, successful reports, command logs and source
  snapshots.
- `reviews/`: complete independent source, verifier-repair and supplemental
  reviews, the 75-file source/hash review inventory, and the complete connector
  patch. Reviews contain their actual historical statements; pre-execution
  approval sections do not by themselves claim a subsequent PASS.
- `source-at-H/`: exact Git bytes for all 75 PR-added files, every one of the 19
  selected original source paths, both original registries, repository AGENTS,
  original verifier files, and the four reviewed algorithm-provenance scripts.
  All author failed and successful attempts in the PR are included.
- `runtime/`: retained official-runtime provenance and saved official release
  metadata. The archive SHA256 is a locally recorded official-download-stream
  hash; the upstream release metadata's digest field is null. Runtime binaries
  and standard-library objects are not bundled.
- `SOURCE.json`: exact scope, input identities and measured retained counts.
- `FILES.json`: current per-file byte counts and SHA256 values, excluding itself
  to avoid a circular hash. The external package manifest additionally hashes it.

The original absolute paths are provenance, not requirements to recreate those
directories. The historical `evidence/PRELIMINARY_FILES.json` describes an earlier
supplement-runner draft. It is deliberately unchanged; consult `FILES.json` for
the final packaged bytes. Original source language and all evidence bytes are
preserved. This package makes no ownership transfer or publication claim.

## Recover and verify the transport package

Place `recover.py`, `package-manifest.json`, and the `parts/` directory together.
Use a new output directory whose parent already exists:

```bash
python3 /path/to/package/recover.py /path/to/package /path/to/new-recovered-bundle
```

For stronger transport checking, provide the archive SHA256 received through
the accompanying delivery record using `--expected-archive-sha256 HASH`.
The standalone standard-library recovery script checks every encoded part,
every decoded part, the complete archive, and every member before writing any
member. It rejects traversal, absolute/noncanonical names, duplicates, symlinks,
hardlinks, devices, unexpected members, and existing output paths. It does not
run any archived script or Lean program. Hashes detect corruption; by themselves
they do not authenticate the publisher.

## Reproduce the 19-module build from exact H

Use Python 3, Git, and the official Lean 4.19.0 Linux distribution, commit
`6caaee842e94`. The recorded official archive SHA256 is
`6fe3ce97a58f44e2b3567d455b994eacec5bfe9ae7774f2a573444480ba813fe`.
Its URL is
`https://github.com/leanprover/lean4/releases/download/v4.19.0/lean-4.19.0-linux.tar.zst`.
Verify the distribution's origin and bytes using the retained provenance and
your download procedure. The runtime's Std/Lean/Init libraries are required;
no Mathlib dependency is used by this selected closure.

Review the scripts and repository instructions before executing them. Define
task-specific absolute paths; do not reuse existing output directories:

```bash
P196_BUNDLE=/absolute/path/to/new-recovered-bundle
P196_WORK=/absolute/path/to/new-isolated-checkout
P196_LEAN=/absolute/path/to/lean-4.19.0-linux/bin/lean
P196_RUN=/absolute/path/to/new-trust0-output
P196_SUPPLEMENT=/absolute/path/to/new-supplement-output
P196_HEAD=6f48ca108dee4c07588f8c5582bcfef55388537f

git init "$P196_WORK"
git -C "$P196_WORK" remote add origin https://github.com/taco-jpg/p196-algorithm.git
git -C "$P196_WORK" fetch --no-tags origin "$P196_HEAD"
git -C "$P196_WORK" checkout --detach "$P196_HEAD"
git -C "$P196_WORK" rev-parse HEAD

cp "$P196_BUNDLE/evidence/verify_project.repaired.py"   "$P196_WORK/proofs/verify_project_pr177_reviewed.py"
python3 "$P196_WORK/proofs/verify_project_pr177_reviewed.py"   --lean "$P196_LEAN"   --project agent107-dfa-horn-closure   --registry "$P196_WORK/proofs/contributions/agent-107/dfa-horn-closure-20261016/verification/Agent107DFAHorn.verify-registry.json"   --output "$P196_RUN"

python3 "$P196_BUNDLE/evidence/run_supplement.py"   "$P196_RUN" "$P196_LEAN" "$P196_SUPPLEMENT"
```

**Verifier placement matters:** its ROOT is computed from its own path. Copy it
into the checkout's `proofs/` directory exactly as shown. Running it directly
from `evidence/` would point ROOT at the wrong tree. The runnable registry is the
complete 19-module `verification/Agent107DFAHorn.verify-registry.json`, not the
older seven-new-module public `proofs/Agent107DFAHorn.registry.json`. The latter
has a separate endpoint typo preserved in `registry-original.json`; the exact
one-line proposed correction is in `registry-endpoint.patch` and
`registry-corrected.json`. No registry patch is needed for the command above.

The preserved `source-at-H/` files provide every source byte required by this
selected closure in its original repository path. The retained run snapshots
also include all 19 module-name `.lean` files. Use the exact Git checkout for the
documented verifier procedure because it records Git HEAD and tracked-tree
status. This source subset is not a fabricated full Git history.

The compiler must run normally in the host environment. In the original hosted
environment, default sandbox Lean execution failed to locate its application;
the ordinary approved execution permission was used. No compiler shim, kernel
change, trust shortcut, or environment bypass is part of this procedure.

## Supplemental audit paths and optional reuse

The supplemental interface is:

```text
run_supplement.py TRUST_ZERO_OUTPUT LEAN NEW_OUTPUT [REUSE_SAFE_AUDIT_OUTPUT]
```

On a fresh reproduction, omit the final argument as above: both supplemental
audits run against that reproduction's 19 freshly built objects. The script
binds the compiler, source snapshots, exact prior report, and all 19 objects.
All retained `.olean` files are excluded from this package and must be rebuilt.

The historical successful retry used `trust0-run-001` and reused the successful
safe stage from `supplement-001`. That reuse is permitted only when the runner
verifies the exact same prior-report hash, sources, object hashes, compiler map,
generated safe-audit source, log hash, exit zero and trust-zero command. Merely
extracting this archive does not satisfy that optional reuse gate. Do not alter
the gate or copy old report hashes into a new run. Preserve a fresh run's own
reports and paths even if reproducible objects happen to hash identically.

## Packaging validation boundary

The packager checked exact Git/source identities, selected retained report and
log hashes, complete transport recovery, and byte-for-byte equality of every
recovered member. It did not rebuild the proofs or conduct a replacement
mathematical review. Compilation and audit PASS refer to the retained executions
reviewed in `reviews/`, with the distinct failures preserved alongside them.
