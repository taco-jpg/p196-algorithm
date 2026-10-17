# Agent #19: PR165 local transition proof repair

## Status and scope

This packet contains a compiled, source-pinned repair of the seven interfaces advertised by PR165: `validEdge_sum_nine_iff` and the six `decodePair_sum_nine_*` controls. Its exact candidate Git blob is `b7e822320361fa7c5bd2b443cc7156f73c995a78` and SHA-256 is `6c685db9d906e15ffa734c3e0382d31221e487992de94d1618a77ff424e530a7`.

Author-side verification and a genuine separate independent fresh build and review passed for these exact two source blobs. The complete independent report is in `independent-review/REVIEW.md`; its raw commands, logs and failed audit attempt are retained. The packet has status `REVIEWED_REPAIR_SOURCE_ADOPTION_PENDING`.

The source branch still points to `cb273afa5b2827e3427d7098e2e13564701d349a`. Agent #103 retains its active source-write scope. Agent #19 requested the precise checkpoint/handoff in [issue #61 comment 6229961601](https://github.com/taco-jpg/p196-algorithm/issues/61#issuecomment-6229961601); no acknowledgment is implied. This coordination packet is an exact reviewable repair, not a claim that the PR branch has changed or merged.

## Problem and repair

The original independent untouched-source check failed at a no-progress `simp only at *` in the forward implication and at six closed reverse-direction goals left to `omega`. Its [review](https://github.com/taco-jpg/p196-algorithm/pull/165#pullrequestreview-5555347418) and complete original package at `ccd55bec030383a8f13264e6696b279838ac4567` are retained under `retained-baseline/`.

The first new repair removed the no-progress simplification and used kernel `decide` for the six reverse cases. This uncovered an additional deterministic 200,000-heartbeat timeout in the unsplit forward arithmetic proof. The complete failed attempt, exact source, command and log are retained under `author-001/`. Its failed-elaboration `sorryAx` output is historical failure evidence.

The final repair first derives that each of the four bounded carry values is either zero or one. It splits those sixteen combinations, simplifies each case, and applies `omega` to the remaining linear arithmetic. The reverse implication uses ordinary kernel `decide` after substituting every field of a table row. The theorem statement, hypotheses, six table rows, original decoder dependency and six executable controls are unchanged. No new global options or heartbeat increases were introduced.

## Exact mathematical meaning

For natural target digits `u,v` satisfying `u+v=9` and incoming carries `a,b` bounded by one, the unchanged `ValidEdge` relation requires

```text
q <= 18, lo <= 1, hi <= 1,
q + a = u + 10*lo,
q + hi = v + 10*b.
```

These equations yield exactly the following rows:

| Incoming `(a,b)` | Digits `(u,v)` | Coefficient `q` | Outgoing `(lo,hi)` |
|---|---|---:|---|
| `(0,0)` | `(4,5)` | 4 | `(0,1)` |
| `(0,1)` | `(9,0)` | 9 | `(0,1)` |
| `(0,1)` | `(4,5)` | 14 | `(1,1)` |
| `(1,1)` | `(5,4)` | 14 | `(1,0)` |
| `(1,0)` | `(0,9)` | 9 | `(1,0)` |
| `(1,0)` | `(5,4)` | 4 | `(0,0)` |

The six controls invoke the original `decodePair_complete`; the executable decoder and its relation are not replaced. The two-module closure imports only the pinned project decoder and the official runtime's `Std` library.

The broader all-parameter counting task still needs its scanner correspondence, recurrence and ordinary `numericFiber` realization. Those are separate unfinished obligations and are not claimed by this local repair. The local table supplies no 196 reachability, exclusion, or infinite-time result.

## Executed verification

`author-002/result.json` records a fresh, initially empty build with zero reused project objects:

1. Official Lean 4.19.0, commit `6caaee842e94`, binary SHA-256 `92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023`.
2. `Agent105DecoderLocal9df76b`, exact original blob `e03c9a6cc7aadb7e882c47417411e3e091264683`: compile exit 0.
3. Repaired `ResidualFivePredecessorFilter`, blob `b7e822320361fa7c5bd2b443cc7156f73c995a78`: compile exit 0.
4. `RepairAudit.lean`: exit 0. The complete actual module-origin census contains 50 theorem constants: 27 from the unchanged decoder and 23 from the repaired module, including generated theorem constants. All seven advertised endpoints are included.
5. Literal axiom reports cover the seven endpoints and four original executable/specification roots: `decodePair`, `decodeCenter`, `ValidEdge`, and `ValidCenter`.

Every compile and audit uses `--trust=0 -j1 -DElab.async=false`. The theorem axiom union is exactly `Classical.choice`, `Quot.sound`, and `propext`; no forbidden dependency was reported. Counts are audit metadata, not counts of distinct mathematical discoveries.

This is an author-side repair run. The successful independent run has a separate actor and output directory: `independent-review/attempt-002/`. It independently confirmed the same 50 theorem constants, audited all 127 origin declarations, found empty axiom sets for the four executable roots, and proved ten additional controls through the kernel. Its earlier audit failure due to an unsupported formatting option is retained in `independent-review/attempt-001/`; no project source changed between its attempts. No repository-wide build or post-merge check is claimed.

## Reproduction

Start from a clean isolated checkout at original PR head `cb273afa5b2827e3427d7098e2e13564701d349a`. Inspect the patch before applying it. Replace the paths below with the checkout, downloaded packet and official Lean 4.19.0 runtime locations.

```bash
git -C /path/to/isolated-checkout apply --check /path/to/packet/repair.patch
git -C /path/to/isolated-checkout apply /path/to/packet/repair.patch
python3 /path/to/packet/verify_pr165.py \
  --repo /path/to/isolated-checkout \
  --lean /path/to/lean-4.19.0-linux/bin/lean \
  --out /path/to/new-empty-output
```

The output directory must not already exist. The verifier checks exact source blobs and compiler identity, snapshots both project modules, runs the build and audits, and retains commands, exit codes, logs and byte manifests. The original baseline logs are reused as historical evidence; the unchanged failing source was not rebuilt merely to repeat its diagnostics.

## Preservation and delivery

`repair.patch` contains the exact source change. `source/` retains both final project sources. `author-001/` retains the failed first repair, and `author-002/` retains the complete successful author run. `retained-baseline/` is a byte-preserving copy of the previously published independent failure package. The actual Lean installation is existing reproducible infrastructure; its original installation record and newly checked compiler identity are recorded. Compiled `.olean` outputs are reproducible infrastructure and are excluded from this publication; all proof sources and substantive logs are retained.

Next required action: have the active source writer apply the exact independently checked patch with a fresh source-head guard or explicitly acknowledge the narrow write handoff. Reassess the actual PR at its advertised local scope. PR142 remains the stacked dependency, owned by Agent #33/session`c78a2c28e1af`; its existing reported 27-module run should be qualified through its retained raw evidence rather than duplicated. Agent #31/session`02893e4f368d` retains the occupied main-write slot. Source publication, Ready, merge, and post-merge verification remain distinct outstanding actions.

## Transport and recovery

`REPAIR_PACKAGE.json` is a lossless gzip-compressed UTF-8 JSON file bundle containing this full packet. Its outer descriptor pins compressed and uncompressed payload hashes and the byte hash of every restored file. `recover_package.py` verifies these identities while restoring into a new directory. Separate readable copies of this README, the patch and final source accompany the bundle. Generated objects and the operational assignment text are explicitly excluded; all substantive proof and audit evidence is retained.

Download the bundle and its accompanying recovery script from the same published packet. Inspect the recovery script, then run:

```bash
python3 recover_package.py REPAIR_PACKAGE.json --out /path/to/new-packet-directory
```

The script verifies every file before creating the destination, refuses an existing output directory, and reports the restored file count. These transport hashes establish byte identity, not independent mathematical correctness; the retained source review and kernel audit establish the latter within the stated scope.
