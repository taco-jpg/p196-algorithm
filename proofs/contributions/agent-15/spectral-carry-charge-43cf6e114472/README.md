# Spectral carry-charge symmetry — Agent 15

Status: **LEAN_CHECKED**. A complete fresh author build and public axiom audit passed. Frozen-source independent semantic review, independent full-closure rebuild and repository integration are pending at this source checkpoint.

This package proves the exact original claim: the integer antisymmetric charge J vanishes if and only if the complete binary outgoing-carry word equals its reversal. Both length parities, the unrestricted binary odd center, zero final overflow, and all boundary lengths are retained. The empty word is an explicit algebraic extension. No incoming zero is prepended.

## Exact coverage

All declarations are in `P196.Agent15.SpectralCarry`.

| Source obligation | Covering declarations |
| --- | --- |
| U/S recurrence and domination over all smaller weights | `U_step`, `S_step`, `oddWeight_superincreasing`, `evenWeight_superincreasing` |
| Equal-length binary weighted-code injectivity | `weighted_injective_binary` |
| Outer-half equality detects complete reversal symmetry | `reverse_take_half_iff` |
| Original parity-selected integer charge vanishes exactly on symmetric binary words | `carryCharge_zero_iff` |
| Exact finite-sum interpretation | `sumFirst_eq_range_sum`, `carryCharge_eq_odd_source_sum`, `carryCharge_eq_even_source_sum` |
| The original displayed odd/even sums themselves equal zero exactly on symmetric words | `odd_source_charge_zero_iff`, `even_source_charge_zero_iff` |

Read [CONTRACT.md](CONTRACT.md) for the exact source statement, quantifiers, definitions, hypotheses and provenance. Five local modules are compiled in dependency order: `SpectralWeights`, `BinaryCode`, `ChargeSymmetry`, `SourceFormula`, `ChargeControls`. The only external mathematical dependency is the standard library shipped with Lean 4.19.0. The decimal baseline is environment evidence only.

## Reproduce

Run from this directory with the official Lean 4.19.0 executable:

```bash
python3 check.py --lean /absolute/path/to/lean-4.19.0/bin/lean --output /absolute/new/directory
```

The output directory must not exist. The checker copies every selected source, compiles all five modules using `--trust=0 -j1 -DElab.async=false`, prints all 69 explicit public declarations and their transitive axioms, and records the exact source/compiler hashes, commands, complete logs and exit codes. It imports no prior project objects. Its public export scan is supplemented by a separate nonauthor module-origin audit before final acceptance.

Author attempt 006 passed all seven commands, including the public audit. Every public result uses only the permitted foundational axioms `propext`, `Classical.choice`, `Quot.sound` (or none). The nine finite kernel controls supplement the universal proof and exercise boundary lengths, both signs, a nonzero odd charge, the original +419 example, the initial-zero convention, the retained zero overflow, and a nonbinary cancellation counterexample.

The full author and environment history, including failed source attempts, is preserved in [evidence/development-evidence.tar.gz](evidence/development-evidence.tar.gz) with a file-by-file SHA256 manifest. Original logs and historical manifests are unchanged; regenerable compiler objects are omitted explicitly. The weights author's separate source/audit history is in `development/weights/`.

The shared overlay became full during development. A small isolated copy of the checkout and fresh build directories were moved to a separately approved temporary memory filesystem. The original checkout, every source attempt and every substantive log were retained. Five baseline/fixture compiler objects were removed only after their hashes were recorded; this did not change the source or proof acceptance policy.

## Scope, provenance and status

Original source snapshot: `5ff4f607535587d572fbc9e95ba9501d1fbe5fc5`. Protected task claim: `9ff01fb85383833abe440d7f41bc7c249c332070`, task `agent15-spectral-carry-charge-43cf6e114472`. The accompanying coverage census records its inspected corpus and unresolved claims; it does not claim exhaustive repository coverage.

Agent 14 owns the complementary T/R coordinate and fixed-width injectivity. The current contribution does not establish the real quadratic interpretation, H, the four transition laws, persistent nonzero charge, or any all-time conclusion about 196. Existing research and Lean results retain their original authorship.

The root agent authored `BinaryCode`, `ChargeSymmetry`, `SourceFormula`, `ChargeControls`, and the canonical checker. The genuine coverage specialist authored `SpectralWeights`. Genuine nonauthor ownership and runtime specialists perform the semantic and execution reviews. All technical artifacts are English; coordination is on issue #61. Main integration and shared build-registry changes remain with the designated integration owner.
