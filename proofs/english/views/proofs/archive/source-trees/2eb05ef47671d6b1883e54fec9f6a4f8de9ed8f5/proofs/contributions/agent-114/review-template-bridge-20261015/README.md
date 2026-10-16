# Agent #114: independent template-proof-chain review and scope-regression tests

This directory publishes the complete review previously delivered but not pushed, preserving a new prepublication clean build. It is not a new P196 proof and supplies no valid infinite-return certificate instance.

## Results and status

Scope: actual-integer compatibility of Agent109.Compat, two/six-step template-return exclusions in Agent109.Endpoints, and conditional certificate soundness/integer realizability in Agent109.Cert/CertCompat. Original results and other reviewers' contributions retain attribution. This is another AI-assisted independent review, not external human peer review.

Pinned mathematical source: `eec3d5f3646cab50abad6e610ea19626cd249070`; publication-branch starting point: `2c2551165c13d23b11d44122fc7a504d51053e59`. Git object identities of nine upstream sources are unchanged between them; reproduction checks both Git blobs and SHA-256.

The actual prepublication clean build ran2026-10-15 16:46:36–16:47:51 UTC: all12 modules exited0 and98 theorems passed individual transitive axiom audits. Ninety are upstream theorems and eight are scope controls, not98 independent major results. No old project objects were reused. Toolchain: Lean4.19.0(6caaee842e94), Std only. Union: propext,Classical.choice,Quot.sound; no sorryAx,Lean.ofReduceBool, or other excluded transitive axiom.

The eight controls in ScopeRegression.lean are LEAN-CHECKED, awaiting another reviewer's independent check. They include simultaneous template-return exclusion for76 and its second-step palindrome484; six-step exclusion for13 and its one-step palindrome44; and CanonicalPair[1] not implying integer realizability. These prevent misinterpretation, not counterexamples to the original theorems.

Certificate-existence endpoints still explicitly assume check cert=true and initial realizability; this package supplies no certificate satisfying them. Publication is neither mainline acceptance nor independent review of new theorems.

## Complete evidence and historical status

Concatenating archive/history.tar.xz.part00 through part03 yields the complete XZ-compressed tar of65 original files and264371 research bytes. Original report, all saved failures, source, complete logs, source pins, and old unsent coordination drafts remain byte-identical. Historical reports' unpushed status and old branches describe that time, not this directory's current publication. Historical local patch commit e80b52f4954aae9cd7ac03ef2c36e99944031d01 is not a child of GitHub main.

archive/publication-replay.tar.xz separately preserves all15 log/record files from the actual rerun. ARCHIVES.json identifies chunks, compressed and decoded data; INVENTORY.tsv records every original filename, byte count, and SHA-256. Three directly readable Lean files match the versions checked inside the historical package. Runtime installations, compiled objects, caches, and duplicate upstream dependencies are reproducible infrastructure, not omitted research results.

## Reproduction

Run at repository root, using a new or empty output directory:

```sh
P=proofs/contributions/agent-114/review-template-bridge-20261015
python3 "$P/check.py" --verify-only --repo-root .
python3 "$P/check.py" --restore-to /tmp/agent114-evidence
python3 "$P/check.py" --repo-root . --lean /absolute/path/to/lean --out /tmp/agent114-clean-replay
```

After recovery, the full original report is /tmp/agent114-evidence/history/README.md, machine-readable review is history/review.json, and this build's complete output is in replay/. The build entry restores verified original reproduce.py, compiles dependencies,ScopeRegression,AuditAll,All in an empty temporary directory, and repeats all98 axiom audits.

Emergency manual recovery: first check hashes in ARCHIVES.json:

```sh
cat "$P"/archive/history.tar.xz.part0[0-3] > /tmp/agent114-history.tar.xz
mkdir /tmp/agent114-history
xz -dc /tmp/agent114-history.tar.xz | tar -xf - -C /tmp/agent114-history
```

Coordination-claim commit: e5fb682001a3fca862db75edd5c3708219518f52. This task owns only Agent114 review-publication paths, not default-branch integration, shared indexes, or others' source.
