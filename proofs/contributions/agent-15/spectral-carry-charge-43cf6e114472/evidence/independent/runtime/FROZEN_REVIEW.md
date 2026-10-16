# Independent review: U/S spectral carry charge

**Verdict: ACCEPT_EXACT_US_CHARGE_TARGET.** The exact reserved binary-word charge equivalence has passed independent semantic review and a fresh complete five-module Lean build with declaration and axiom auditing.

Reviewer: **runtime_scout**, an independent agent that authored no target Lean declaration and changed no target Lean source. The parent authored the coding, symmetry, formula-bridge, and control modules; coverage_scout authored the weight module. This report is an attributed agent review. It does not represent a separate human reviewer or a different GitHub account's APPROVE action.

The accepted mathematical source is frozen at commit [`e8d706dc8a67248e1531b0b828fbe05ff50052ed`](https://github.com/taco-jpg/p196-algorithm/commit/e8d706dc8a67248e1531b0b828fbe05ff50052ed), tree `2d447634e0ff42b4275d34bfb169101bba0ed130`, under `proofs/contributions/agent-15/spectral-carry-charge-43cf6e114472`. The parent supplied this commit after remote readback and exact fetch. The reviewer independently resolved the immutable local Git commit/tree, compared all five source blobs with committed bytes, and established byte identity with the copies used for the earlier semantic reading. The Git commands were read-only and disabled lazy fetching and optional locks. See [the freeze manifest](freeze-inputs-001/manifest.json) and [the executed gate report](frozen-e8d706dc-attempt-001/verification.json).

The mechanical checker's `semantic_acceptance` field intentionally remains `SEPARATE_REVIEW_REQUIRED`. This report supplies that separate nonauthor semantic verdict; the original execution receipt remains unchanged.

## 1. Exact source claim and accepted statement

The task is `SPECTRAL-CARRY-CHARGE-ZERO`, reserved as `agent15-spectral-carry-charge-43cf6e114472` in coordination commit `9ff01fb85383833abe440d7f41bc7c249c332070`, task-record blob `70340af5e48d1c965d012180c04bc6ea01f90b21`. The task record is retained in [claim-record.json](claim-record.json).

The original mathematical note and companion implementation come from repository snapshot `5ff4f607535587d572fbc9e95ba9501d1fbe5fc5`:

- [Original note](original-note.md): `creative_global_spectral_notes.md`, Git blob `cb1c355fa05916a770816a4d5ef680e54079cccb`.
- [Original script](original-script.py): `creative_global_spectral.py`, Git blob `730acd722bf017b6bf1e51e5a0411169a7804da4`.

The reviewer recomputed both original Git blob identifiers directly from the retained bytes. The note fixes the dominance argument and the zero-charge/reflection claim. The script fixes the signs, recurrence seeds, parity formulas, and outgoing-carry indexing through `qstep` and `carry_coordinates`.

Let `c` be the finite list of outgoing binary carries, ordered from the least significant column first. Its final entry is the outgoing carry `h`, including when `h = 0`. The initial incoming zero is not inserted into the list. Reversal always uses the full list length, without trimming a zero endpoint.

The integer recurrences are

```text
U(0) = 0,  U(1) = 1,
S(0) = 1,  S(1) = 21,
X(k + 2) = 20 * X(k + 1) - X(k).
```

The odd weights are `U(k + 1)` and the even weights are `S(k)`. For a word of length `2m + 1`, the accepted charge is

```text
J(c) = sum(i = 0, ..., m - 1) (c[2m - i] - c[i]) * U(m - i).
```

For a word of length `2m`, it is

```text
J(c) = sum(i = 0, ..., m - 1) (c[2m - 1 - i] - c[i]) * S(m - 1 - i).
```

Both carry entries are cast to `Int` before subtraction. The odd center is unconstrained and absent from the sum. Under the sole substantive premise that all entries are zero or one, the universal conclusion is

```lean
carryCharge_zero_iff {cs : List Nat} (hc : Binary cs) :
  carryCharge cs = 0 ↔ cs.reverse = cs
```

All package declarations live in `P196.Agent15.SpectralCarry`. The actual executed kernel-environment signature for this endpoint confirms the displayed premise and conclusion; it is retained with all 69 signatures in [exact-public-signatures.txt](exact-public-signatures.txt).

The original note's fixed-length polynomial reflection is read coefficientwise in the reserved list-level target. The package directly proves the original finite integer sums and the list-reversal equivalence. It does not add a polynomial datatype or claim a separate spectral-field interpretation.

## 2. Semantic assessment of the proof

The proof preserves the original claim through four explicit steps.

First, `SpectralWeights` defines the exact `Int` recurrence and proves positivity and growth of the two used weight sequences. `oddWeight_superincreasing` and `evenWeight_superincreasing` assert the strict inequality `weightSum w n < w n`, where `weightSum w n` contains exactly weights zero through `n - 1`. The U shift is essential: the first used odd weight is `U(1) = 1`, and the first even weight is `S(0) = 1`.

Second, `BinaryCode` defines a highest-weight-first code for a list. Its injectivity theorem has explicit binary premises for both inputs, equality of their lengths, and equality of their integer codes. Those hypotheses are sufficient and appropriately scoped: without equal lengths, the leading-zero example `[1]` and `[0, 1]` would have the same unit-weight code. The actual final charge proof compares two halves extracted from one list, so their lengths agree.

Third, `ChargeSymmetry` compares the first half of the full reverse with the first half of the original list. Its general `reverse_take_half_iff` lemma proves that equality of those halves is equivalent to full reversal equality, including the free center of an odd word. Subtracting the two integer codes defines `halfCharge`; the parity-selected `carryCharge` uses the exact odd/even weights. The final theorem has no desired-conclusion premise, symmetry assumption, length bound, center restriction, or fixed outgoing-bit premise.

Fourth, `SourceFormula` proves the representation bridge. `sumFirst_eq_range_sum` identifies its recursive summation with the ordinary mapped `List.range` sum. The weighted/take/reverse lemmas yield the mirrored signed coefficient formula. The two `carryCharge_eq_*_source_sum` theorems match the original odd and even indices and signs exactly. The endpoints `odd_source_charge_zero_iff` and `even_source_charge_zero_iff` state the equivalence directly for those sums, under their explicit parity length and binary hypotheses. Option defaults do not introduce a semantic relaxation: every index used in a nonempty active summation range is in bounds; the zero-length range is empty.

The nine `ChargeControls` theorems are additional kernel-computed boundary and convention checks using ordinary `decide`. They cover the empty word, singleton words, both two-entry signs, a free odd center, even symmetry, the original 419-valued example, and three assumption/convention distinctions:

- `[1, 0, 21, 0]` has zero charge but is not symmetric, confirming the need for the binary premise.
- `[1, 1]` has zero charge while prepending the incoming zero gives charge one.
- `[0, 1, 0]` has zero charge while deleting its final outgoing zero gives charge one.

These finite controls supplement the universal proof. The empty list is an explicitly documented algebraic extension of the original positive-width setting.

### Contract findings

| Obligation | Finding |
|---|---|
| Exact U/S seeds and recurrence | PASS: integer recurrence and exact initial values. |
| Strict dominance of all preceding used weights | PASS: universal strict inequalities with the intended prefix. |
| Binary hypothesis | PASS: every Nat entry equals zero or one; no hidden realizability premise. |
| Full outgoing-carry word | PASS: `h` remains present, including zero; no incoming zero is inserted. |
| Odd/even signs and indices | PASS: both original formulas are formally bridged and restated as final equivalences. |
| Integer signed difference | PASS: both casts precede `Int` subtraction. |
| Universal zero-charge/reflection claim | PASS: arbitrary finite binary list, with exact full reversal equality. |
| Forbidden shortcuts or added mathematical assumptions | PASS: source scan and complete transitive axiom inventory agree. |

## 3. Fresh build and exact command

The reviewer ran a new isolated build directory, `frozen-e8d706dc-attempt-001/source`. It initially contained only copied committed Lean source. `LEAN_PATH` pointed exclusively to this new directory. No author `.olean`, prior reviewer fixture object, decimal baseline object, or other project cache was reused.

All five project modules were compiled in dependency order:

```text
SpectralWeights → BinaryCode → ChargeSymmetry → SourceFormula → ChargeControls
```

Every compiler invocation used `-j1 -DElab.async=false --trust=0`. All five source builds exited zero and produced empty diagnostic logs. The complete origin audit and the separate 69-export audit also exited zero. The first frozen mathematical-source attempt passed; the previously failed attempts were unrelated reviewer infrastructure preparation.

The actual outer invocation is recorded below. It is historical: a rerun must select a new nonexistent `--evidence` directory because the helper refuses to overwrite an earlier attempt. Machine-readable exact arguments, interpreter identity, start/end times, and exit code are in [gate-invocation-001.json](gate-invocation-001.json). Each individual compiler command, working directory, minimal environment, elapsed time, output log, and hash is in the gate receipt.

```sh
/opt/codex/runtimes/codex-primary-runtime/dependencies/python/bin/python \
  /dev/shm/p196-agent15-43cf6e114472/runtime-review/clean_review.py \
  --lean \
  /tmp/p196-agent5-lean/lean-4.19.0-linux/bin/lean \
  --repo-root \
  /dev/shm/p196-agent15-43cf6e114472/repo \
  --source-root \
  /dev/shm/p196-agent15-43cf6e114472/repo/proofs/contributions/agent-15/spectral-carry-charge-43cf6e114472 \
  --source-commit \
  e8d706dc8a67248e1531b0b828fbe05ff50052ed \
  --evidence \
  /dev/shm/p196-agent15-43cf6e114472/runtime-review/frozen-e8d706dc-attempt-001 \
  --module \
  ChargeControls \
  --exact-module \
  SpectralWeights \
  --exact-module \
  BinaryCode \
  --exact-module \
  ChargeSymmetry \
  --exact-module \
  SourceFormula \
  --exact-module \
  ChargeControls \
  --required-declaration \
  P196.Agent15.SpectralCarry.carryCharge_zero_iff \
  --required-declaration \
  P196.Agent15.SpectralCarry.odd_source_charge_zero_iff \
  --required-declaration \
  P196.Agent15.SpectralCarry.even_source_charge_zero_iff \
  --public-exports \
  /dev/shm/p196-agent15-43cf6e114472/runtime-review/expected-public-exports.txt \
  --expected-public-export-count \
  69
```

The independent checker source is [clean_review.py](clean_review.py), SHA256 `3c5beaea129575dd335bebf6f31994613c3f706cee13711a3aaf60bacaa768ef`. The helper was validated on a separate small fixture before target execution; it was not substituted for Lean or used to bypass an execution restriction.

### Runtime and external dependency boundary

The actual compiler was

```text
/tmp/p196-agent5-lean/lean-4.19.0-linux/bin/lean
Lean (version 4.19.0, x86_64-unknown-linux-gnu, commit 6caaee842e94, Release)
```

Its SHA256 was `92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023`. The compiler executable, four top-level Lean shared-library files, and the directly imported official `Std.olean` were hashed and checked again after the gate. Their recorded identities remained unchanged. `Std.olean` SHA256 was `7d3771da25b893da62564bf8198487ff28f01af5cbd410be88d493a4921b2bb1`.

This is a clean build of the complete five-module **project** dependency closure. The sole direct external project import is official `Std`; its prebuilt Init/Std runtime dependencies were reused from the pinned Lean distribution. The introspection harness additionally imports official `Lean`. This review does not claim a fresh build of Lean or its standard library, a new download verification, or an independent toolchain implementation. The historical installation record names the official Lean release; its archived checksum is retained as local provenance rather than presented as an independently authenticated release signature.

The authorized executor mode was `require_escalated`: ordinary execution could not use this distribution correctly, and the full overlay later prevented normal process startup. The memory-backed reviewer directory was explicitly authorized. No wrapper or distribution mutation was used.

## 4. Complete declaration and axiom coverage

The expected public list was extracted independently from the source. It exactly matches the author's list, including order: 69 entries comprising 13 definitions and 56 theorems. Every entry received an actual literal `#print` and `#print axioms` command in the separate export pass. The complete output, including printed declaration bodies, is [public-exports.log](frozen-e8d706dc-attempt-001/logs/public-exports.log).

The origin-based pass enumerated every environment constant attributed to the five modules, required presence in the checked environment, emitted its signature, collected transitive axioms, and executed an actual `#print axioms`. It found:

| Module | Explicit exports | All origin declarations | Safe declarations | Safe private declarations | Compiler implementation declarations |
|---|---:|---:|---:|---:|---:|
| SpectralWeights | 29 | 58 | 38 | 5 | 20 |
| BinaryCode | 7 | 36 | 25 | 6 | 11 |
| ChargeSymmetry | 11 | 28 | 17 | 0 | 11 |
| SourceFormula | 13 | 43 | 34 | 3 | 9 |
| ChargeControls | 9 | 9 | 9 | 0 | 0 |
| **Total** | **69** | **174** | **123** | **14** | **51** |

The 123 safe declarations include 109 public declarations, including generated declarations, and 14 private helpers/generated declarations. The 51 implementation entries are Lean-generated unsafe/partial compilation artifacts such as `_cstage1`, `_cstage2`, and `_unsafe_rec`. Their names, flags, signatures, and axiom outputs were retained too. All 51 reported an empty axiom list; they do not enlarge the mathematical axiom allowance.

The safe declaration axiom distribution is:

| Transitive axioms | Safe declarations |
|---|---:|
| none | 68 |
| `propext` | 1 |
| `propext`, `Quot.sound` | 43 |
| `propext`, `Classical.choice`, `Quot.sound` | 11 |

All three principal zero-charge equivalence endpoints use exactly `propext`, `Classical.choice`, and `Quot.sound`. The odd/even dominance endpoints use `propext` and `Quot.sound`. No audited declaration introduces a new safe axiom, and no audited transitive axiom list contains `sorryAx`, `Lean.ofReduceBool`, or any name outside the allowed foundational set. The source scan rejects live `sorry`, `admit`, `axiom`, `native_decide`, `skipKernelTC`, and explicit unsafe/partial constructs while correctly masking comments and strings.

The two coverage passes are deliberately distinguished: 174 origin-based `#print axioms` commands and 69 further public-export `#print axioms` commands, together with 69 public `#print` commands. The machine inventory is [declarations.json](frozen-e8d706dc-attempt-001/declarations.json), the tabular inventory is [declaration-coverage.tsv](declaration-coverage.tsv), and complete signature/axiom output is [all-declarations.log](frozen-e8d706dc-attempt-001/logs/all-declarations.log).

## 5. Accepted source identities

| Committed file | Bytes | SHA256 |
|---|---:|---|
| SpectralWeights.lean | 4445 | `07b3831f17a0d2e43a7e27cfd8a63d364a98ccbbcef87362a20cfbf24fb49db1` |
| BinaryCode.lean | 2655 | `8db88d52e00dddbd32610dc09b7f8833f1ec1dc623b82236060b67bd2c9171f9` |
| ChargeSymmetry.lean | 3240 | `28d11217cf147750ec2d07e64dbc6dabeee7deec7e543987817da611201b60a3` |
| SourceFormula.lean | 5059 | `be165a538963922f6096e63934e5f3c1010d760cabc9e08baa96a0bb43c105d8` |
| ChargeControls.lean | 1104 | `bb23522ad6792dcf6b30ef010837eb1703f7eba59f4448e355282f8eb27f668c` |

The corresponding committed Git blobs, import edges, copied source paths, and before/after checks are recorded in the freeze manifest and execution receipt. Future documentation-only changes can retain this verdict only while these mathematical source bytes remain identical. A changed Lean source requires a new relevant review and gate.

## 6. Preserved history and limits

All failed reviewer infrastructure sources and logs remain in `infrastructure-001` and `infrastructure-002`. Attempt 001 exposed an unsupported pretty-printer option and an overbroad template substitution; attempt 002 exposed compiler-generated unsafe implementation declarations. The revised fixture audit in `infrastructure-003` passed and retained all 22 fixture declarations. None of these attempts was a failed U/S mathematical source build. Two read-only metadata presentation errors are separately recorded in [metadata-inspection-failures.json](metadata-inspection-failures.json); they changed neither mathematics nor successful gate evidence.

The earlier `LychrelDigitSums` build is preserved as environment-only evidence under [environment-history](environment-history/copy-manifest.json), including its source, command, logs, and endpoint audits. It is not a target dependency and was never on the independent gate's search path. Historical generated objects were omitted from this evidence copy with their identities recorded; no original object was deleted during packaging.

The historical cleanup receipt reported removal of five regenerable objects. A subsequent read found all five original paths again present with their original hashes and modification times. Both observations are preserved; this review makes no claim that deletion or reclaimed space persisted. [cleanup-observation-correction.json](cleanup-observation-correction.json) records the discrepancy. Its cause was not determined, and no further deletion was attempted. The discrepancy does not affect the fresh target gate, whose separate directory and import path excluded those objects.

This verdict covers the reserved U/S integer charge equivalence and its exact finite-sum representation. It does not assert the separately reserved T/R result, a square-root spectral embedding, any four-case evolution law, a decimal orbit invariant, eventual symmetry of carries, a palindrome result for 196, or repository-wide verification. Those claims require their own statements and proofs. The review closes no unrelated issue and performs no GitHub publication action.

## 7. Reproducible evidence entry points

- [review-summary.json](review-summary.json): machine-readable semantic verdict, source identities, runtime boundary, endpoint signatures, axiom sets, and coverage counts.
- [review-manifest.json](review-manifest.json): hashes and sizes of the complete reviewer evidence tree, excluding the manifest itself and its delivery archive.
- [gate-invocation-001.json](gate-invocation-001.json) and [gate-invocation-001.log](gate-invocation-001.log): exact independent helper invocation and complete progress log.
- [verification.json](frozen-e8d706dc-attempt-001/verification.json): full per-command evidence and artifact inventory for the successful frozen gate.
- [source directory](frozen-e8d706dc-attempt-001/source): all five exact mathematical source copies, both generated audit sources, and their freshly generated objects.

