# Agent #105 publication scope

This isolated contribution retains all substantive research files from both
owned high-return tasks: eight completed Lean modules, dependency-aware
fresh-build checkers, source and axiom records, all available failed proof
attempts and compiler logs, separate statement and execution reviews, and
both complete finite-control outputs. `INVENTORY.json` is the file list and
byte inventory; `MANIFEST.sha256` checks the published bytes. The manifest
excludes itself only. The inventory excludes itself and the manifest to
avoid self-reference. `RAW_OUTPUTS.json` records original and stored sizes,
hashes, compression, and exact recovery commands for both raw outputs.

The 124,333,689 decoded raw bytes are retained losslessly in two gzip files;
the readable finite summaries are supplementary. These experiments remain
finite controls and do not substitute for Lean proofs. Source commits
`167eed51bc2ae014450626b9e5c0d3302a5ae5c4` and
`8f846def03ec368d1de0fe20965f5e47f6172bc5` pin the two mathematical packages.
The later publication adds verification evidence without changing those
Lean theorem sources.

The first package is INDEPENDENTLY-REVIEWED. The second is LEAN-CHECKED and
READY_FOR_REVIEW; its independent final source review and separate rebuild
remain outstanding after the reviewer's execution quota ended. Both are
awaiting shared integration. No background execution or integration ownership
is claimed.

The two root-level initial compiler logs are byte-identical duplicates of
retained package logs and are inventoried as such. Temporary copied build
directories, `.olean` products, runtime distributions, download/extraction
files, and publishing transport helpers are reproducible infrastructure;
they are excluded. Exact sources, compiler identity, startup shim source and
provenance, command exit statuses, build/object hashes, and substantive logs
needed to replay the accepted checks are retained. The independent parser
failure and rejected second build are preserved and explicitly labelled.
No substantive proof-development or finite-search output is omitted.

The parent shared README/FINDINGS/inventory are owned by the default-branch
integration process. This branch supplies scoped replacements in the Agent
#105 directory rather than editing another owner's shared records. Its PR
asks the integration owner to include the reviewed modules and update shared
indexes, after checking the newest main head and rebuilding there.

Verify from the repository root:

```sh
sha256sum -c proofs/contributions/agent-105/MANIFEST.sha256
```

The per-package README files give Lean reproduction commands. The runtime
compatibility shim is only needed in the original sandbox; standard systems
can invoke the pinned official Lean directly. Neither package establishes
P196 or an infinite palindrome-avoiding orbit.
