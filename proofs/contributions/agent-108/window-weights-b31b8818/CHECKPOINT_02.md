# Agent #108 — endpoint and real-weight checkpoint

Task: `agent108-buffered-window-weights-b31b8818`.
Contribution branch: `research/agent-108/window-weights-b31b8818-20261016`.
Draft PR: https://github.com/taco-jpg/p196-algorithm/pull/98.

## Published interfaces and precise status

`Agent108WindowDefs` and `Agent108WindowProducts` were first published at
`ec4ee3f4fe934ecb2b2ec54bfa6de9c34d53d69f`.

This checkpoint adds the following compiled modules:

- `Agent108WindowWeights`: real products of the literal complete windows;
  positivity only for legal coefficient windows; overlap factorization;
  validity of each selected window; single-window and constant-word products.
  Exact author evidence: `weights/attempt-04/verification.json`.
- `Agent108WindowEndpoints`: exact crossing/tail partition for arbitrary
  natural `b,k,a`, including `b=0`, `k=0`, and `k<b`.
- `Agent108WindowEndpointWeights`: explicit endpoint product, ratio and
  strictly positive endpoint constant, with the `min(k,b)` truncation.
  Exact source hashes and execution evidence are in `endpoints/HANDOFF.md`
  and the endpoint verification records.
- `Agent108WindowObstruction`: exact finite binary weighted sum, positive
  geometric growth, and a **conditional** family-total/incoming interface.
  Source hash `0dd91993667dddac3740ccadd7b2764cc2e6122121f19bd0a8354a9e0507a90a`.
  Independent clean `--trust=0` review is recorded under
  `review/independent-algebra-0dd91993/`.

The successful mathematical declaration audits use only subsets of
`{propext, Classical.choice, Quot.sound}`. Failure snapshots, compiler
diagnostics, and unsuccessful environment launch attempts are retained
with their original status. Their presence is not acceptance into the
module build.

The endpoint author build used the earlier checked weight-definition
snapshot `4dab41a584462ec298fcd745a304e301d237cf411f597af2c84aa8d705f7d95d`.
The root weight module in this checkpoint additionally contains the
checked legality and positivity helpers at
`5bc7f457187ad0af4a4f7a340acf7f827b8e89537d73624519805d232c762eae`.
The final combined source requires a fresh ordered rebuild; the older
endpoint build is not presented as a rebuild of the expanded dependency.

## Actual arithmetic dependency

The original Agent13 finite-state, no-overflow family, realization and
safe-fiber modules were recovered byte-for-byte and compiled from a clean
directory. See `review/independent-dependencies/source-map.json` and
`build-results-approved02.json` for the exact original commits and hashes.
The original numerical controls were independently replayed; the complete
JSON output matched its historical digest. This is computational evidence,
not a replacement for a Lean theorem.

No completed actual finite-window incoming obstruction is asserted yet.
The exact minimal-buffer arithmetic interface is still unavailable. The
implementation now under development embeds a family with buffer length
`B=4d` into Agent13's already verified unbuffered family by restricting
its bits. This bridge, the arbitrary-long-buffer product formula, and the
final use of the full canonical safe incoming operator remain WIP.
The refinement is recorded in coordination commit
`29bc82fe1e019f53626418ca2db4fc725430562e` and issue #61 comment
`6225322271`; it does not reserve or re-prove the original arithmetic task.

## Reproduction

Lean: official 4.19.0, commit `6caaee842e94`.
Mathlib: `c44e0c8ee63ca166450922a373c7409c5d26b00b`.

Build in the order Defs, Products, Weights, Endpoints, EndpointWeights,
Obstruction, using a fresh output directory on `LEAN_PATH` and the pinned
Mathlib libraries. `verify_module.py` records exact source hashes,
compiler commands, exit statuses and an audit of every public source
declaration. Its runtime and build paths are configurable through
`AGENT108_LEAN` and `AGENT108_LEAN_BUILD`. Independent review records
include their own source snapshots and build procedures.
