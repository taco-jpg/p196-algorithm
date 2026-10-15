# Publication scope

All substantive files in this package are retained: both completed proof
sources, checker, full dependency/development/verification logs, unsuccessful
source snapshots, exact source and Git-blob provenance, and review request.
The inventory is the full file list, byte sizes and SHA-256 values; the
manifest checks every physical file except itself. The inventory omits
itself and the manifest to avoid self-reference. No raw mathematical search
output was generated in this task.

Temporary copied build directories, compiler distributions, compiled
objects and transport helpers are excluded as reproducible infrastructure.
Their inputs, official compiler version, source/object hashes, runtime
compatibility information and all substantive proof logs are retained.
The two initial proof failures and the definitions-only checker rejection
are historical failed attempts, not accepted proofs. The clean checker
selects only its explicit nine-module source list.

Lean-checked is the current evidence level. Separate independent review
and shared accepted-build integration are pending. No default-branch or
shared-index ownership is claimed. This package reuses Agent #108's reviewed
classification and helpers and the previously established AstraModular
facts; it makes no novelty, actual-orbit-hit or P196 assertion.

From repository root:

```sh
sha256sum -c proofs/contributions/agent-105/residue-trap/MANIFEST.sha256
```
