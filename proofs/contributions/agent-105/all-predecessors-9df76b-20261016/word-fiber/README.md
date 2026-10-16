# Agent105WordFiber9df76b

## Checked result

Frozen source: `proofs/Agent105WordFiber9df76b.lean`.

SHA-256: `c24bbb0a91f0c524f857d20b623a38704a278e909b2385621875f70561cf7ba3`.

Namespace `Agent105WordFiber9df76b` supplies three executable definitions and five theorems:

- `half qs`: take the first `qs.length / 2` coefficients.
- `center qs`: no center at even length; the original middle coefficient at odd length.
- `wordFiber qs`: original `Agent101.numericFiber (half qs) (center qs)`.
- `half_coefficientWord h c` and `center_coefficientWord h c`: computational projections on the already defined coefficient word.
- `coefficientWord_roundtrip qs hrev`: reconstruct a reverse-symmetric finite list by consuming `Agent101.exists_coefficientWord_of_reverse`.
- `mem_wordFiber qs n hrev hb`: membership iff `Agent101.decimalWidth n qs.length ∧ Lychrel196.step n = Agent101.natValue qs`, assuming reverse symmetry and coefficient bound 18.
- `wordFiber_nodup qs`: unconditional duplicate freedom.

All public theorem arguments are explicit in the displayed order. No target decoder, symmetric-list existence proof, digit-split enumeration, sharp maximum, or initial-palindrome count is reproved here. The optional center is a coefficient, not its half.

## Dependency provenance

`Agent101ProfileExtraction.lean` is reused byte for byte from commit
`9bf1b2c35129500da39388727e17523f55fae80e`,
Git blob `5a5ef0e2d0355362abb84ef48b82ca8d39cd156f`,
SHA-256 `fff6917b100aeec40e353abe4a3f8d27f6561d6859a1feeac9135c22cd8c836b`.

The shared foundational cache is
`/workspace/scratch/9df76b503b84/agent105-runtime/base-build`.
Only the newly published extraction dependency and the new WordFiber module were compiled in this author run. No fresh full foundational replay is claimed here.

The preceding read-only scope report and complete source/task evidence are retained in `enumeration-scope-scout.md`, `enumeration-scope-scout.json`, and `retrieved/`.

## Actual author execution

Compiler:
`/workspace/scratch/fb513c1676b0/agent102-runtime/lean-4.19.0-linux/bin/lean`.

Actual version: Lean 4.19.0, x86_64-unknown-linux-gnu, commit 6caaee842e94, Release.

Both commands used `--trust=0 -j1 -DElab.async=false` through the platform's formally approved execution path. The existing compiler was not modified.

| Retained run | Result | Meaning |
|---|---|---|
| `dependency-ProfileExtraction-001/` | exit 0; about 0.790 s | Exact published Agent101 dependency, seven literal axiom reports |
| `attempt-001/` | exit 1; about 0.424 s | `List.take_length` was incorrectly applied to an explicit argument; Lean inserted error-recovery axioms in this failed elaboration. This run is not an accepted proof |
| `attempt-002/` | exit 0; about 0.450 s | Frozen source, all five theorem and three definition axiom reports |

The successful theorem axiom union is exactly `propext`, `Classical.choice`, `Quot.sound`. All three executable definitions report no axioms. The first three projection/roundtrip theorems use only `propext` and `Quot.sound`; numeric membership and Nodup inherit the standard three from Agent101.

Each run retains its exact input snapshot, full stdout/stderr, compiler version stdout/stderr, argv, environment import path, source hash, exit code and elapsed time in `receipt.json`. Successful cache copies are placed in `build/`; a failed run never replaces a successful cache entry.

## Repeat the scoped author build

From an environment authorized to execute this installed Lean:

```sh
python /workspace/scratch/9df76b503b84/agent105-predecessors-work/proofs/contributions/agent-105/all-predecessors-9df76b-20261016/word-fiber/compile.py --dependency
python /workspace/scratch/9df76b503b84/agent105-predecessors-work/proofs/contributions/agent-105/all-predecessors-9df76b-20261016/word-fiber/compile.py
```

The driver creates a new numbered evidence directory on every invocation. The import path for consumers is:

```text
/workspace/scratch/9df76b503b84/agent105-predecessors-work/proofs/contributions/agent-105/all-predecessors-9df76b-20261016/word-fiber/build:/workspace/scratch/9df76b503b84/agent105-runtime/base-build
```

This is an author build and literal-export audit. Independent semantic review and the complete project rebuild are assigned to other specialists; this module's author does not independently review their own source.
