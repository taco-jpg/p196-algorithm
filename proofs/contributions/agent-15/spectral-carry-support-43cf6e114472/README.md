# Actual spectral carry support at coefficient nine

Status: **INDEPENDENTLY_REVIEWED; not yet integrated into main.** The exact source contract, the author canonical checker, independent semantic review, and independent execution/axiom/public-print gates have passed. Integration and the final publication records remain with the coordinator.

The mathematical source is unchanged from checkpoint `5d02e88f13f59f6fcd09cf75d8c7f188c6645727`: Git blob `c0e5562e1661570546bced3dca82dd4fb459fa5f`, SHA256 `4c06522efae7aa254b6281003d042e49f6b60162d01d00881d50052c7a73c646`. The four spectral dependencies retain PR145's pin `e8d706dc8a67248e1531b0b828fbe05ff50052ed`; the three decimal dependencies retain original snapshot `5ff4f607535587d572fbc9e95ba9501d1fbe5fc5`.

Protected task: `agent15-spectral-carry-support-43cf6e114472`, claim `3de89d0bd03534c92f65886a29b7996525571ff5`, task blob `2707332dbc4dc1274bb8470b15e17f6350618bba`. [CONTRACT.md](CONTRACT.md) records the original source provenance and full quantifiers.

## Exact contract and endpoints

All new declarations are in `P196.Agent15.SpectralSupport`. The definitions use the existing decimal recurrence and exact integer charge:

```lean
outgoing q L = (List.range L).map (fun i => DecimalDigits.carry q (i + 1))
actualCharge q L = P196.Agent15.SpectralCarry.carryCharge (outgoing q L)
```

For `q : Nat → Nat` and `L : Nat`, write `hb` for `∀ i, i < L → q i ≤ 18` and `hs` for `∀ i, i < L → q i = q (L - 1 - i)`. The main equivalences are:

```lean
-- Under hb alone:
actualCharge q L = 0 ↔
  ∀ i, i < L → DecimalDigits.carry q (i + 1) = DecimalDigits.carry q (L - i)

-- Under hb and hs:
actualCharge q L ≠ 0 ↔
  ∃ i, i < L ∧ q i = 9 ∧
    DecimalDigits.carry q (i + 1) ≠ DecimalDigits.carry q (L - i)
```

| Endpoint group | Exact declarations | Scope |
| --- | --- | --- |
| Actual word | `outgoing_length`, `outgoing_getElem`, `outgoing_getElem?`, `outgoing_last`, `outgoing_binary` | Exactly L entries; entry i is `carry q (i+1)`. Binary membership uses hb; the last-entry theorem only requires L>0. |
| Reflection adapter | `outgoing_reverse_iff` | List reversal equality iff every in-range reflected outgoing pair agrees, without coefficient assumptions. |
| Charge-zero adapter | `actualCharge_zero_iff` | The first equivalence above; coefficient symmetry is not required. |
| Local support | `outgoing_reflected_eq_of_nonnine` | Under hb and hs, `i<L` and `q i ≠ 9` imply equality of the reflected outgoing carries. Reuses `RawSymmetryObstruction.nonnine_binary_div`. |
| Nonzero support | `actualCharge_nonzero_iff_nine_asymmetry` | The second equivalence above, including both the nine coefficient and actual carry inequality. |
| No-nine consequence | `actualCharge_zero_of_no_nine` | Under hb and hs, absence of nine in the original width implies zero charge. |

The canonical endpoints take the existing `DecimalDigits.Canonical n d L` directly and use `q = DecimalDigits.columnSum d L`:

| Canonical endpoint | Conclusion |
| --- | --- |
| `canonical_actualCharge_zero_iff` | Zero charge iff all reflected computed outgoing carries agree. |
| `canonical_outgoing_reflected_eq_of_nonnine` | A paired coefficient different from nine has equal reflected outgoing carries. |
| `canonical_actualCharge_nonzero_iff_nine_asymmetry` | Nonzero charge iff a paired coefficient nine has unequal reflected outgoing carries. |
| `canonical_actualCharge_zero_of_no_nine` | Absence of paired coefficient nine implies zero charge. |

These wrappers use the existing `columnSum_bounded` and `columnSum_symmetric` theorems. The word retains `carry q L`, including when it is zero, and excludes the initial `carry q 0`. Both parities and overflow values are covered; the odd central carry remains free. General statements include L=0 and L=1 and assume no orbit premise or outer positivity. Named boundary theorems and four kernel controls include `[9,9]` with outgoing `[0,0]` and charge zero, so the mere presence of nine does not imply nonzero charge.

## Complete mathematical import closure

`ActualCarrySupport` is the root and only new mathematical module. [BUILD.json](BUILD.json) records the exact repository paths, byte counts, SHA256 hashes, Git blobs, and imports of all eight modules.

| Module | Direct imports |
| --- | --- |
| `LychrelDigitSums` | `Std` |
| `IncomingCarrySensitivity` | `LychrelDigitSums` |
| `RawSymmetryObstruction` | `IncomingCarrySensitivity` |
| `SpectralWeights` | `Std` |
| `BinaryCode` | `SpectralWeights` |
| `ChargeSymmetry` | `BinaryCode` |
| `SourceFormula` | `ChargeSymmetry` |
| `ActualCarrySupport` | `SourceFormula`, `RawSymmetryObstruction` |

The exact charge preserves the original odd/even U/S source formulas. No decimal foundation, local division arithmetic, or carry recurrence is replaced.

## Reproduction

Use the exact source paths and pins in BUILD.json and the official **Lean 4.19.0 Linux x64** runtime (`x86_64-unknown-linux-gnu`, compiler commit `6caaee842e94`). From the repository root:

```text
python3 proofs/contributions/agent-15/spectral-carry-support-43cf6e114472/check.py --lean /absolute/path/to/lean-4.19.0-linux/bin/lean --output /absolute/path/to/new-support-build
```

The output directory must not exist. [check.py](check.py), [BUILD.json](BUILD.json), and [lean-toolchain](lean-toolchain) remain the immutable inputs to the recorded canonical run. The driver copies the full source closure into the new directory, starts with zero project objects, and compiles each module using `--trust=0 -j1 -DElab.async=false`. It verifies the configured source/import pins and fingerprints the executable, shared library, Std root, and all 1,471 installed runtime objects before and after the run. The pinned runtime is more specific than a matching version string.

Each output retains `verification.json`, exact commands, separate complete stdout/stderr, source copies, object hashes, the import graph, and declaration/axiom reports. The checker also confirms that the original sources, copies, runtime, and configuration stayed unchanged. BUILD.json remains configuration; actual run status is recorded separately.

## Verification and genuine independent review

| Gate | Actual result and coverage |
| --- | --- |
| Author canonical checker | **PASS**: 10 Lean commands, eight fresh module builds, and 37 declaration/axiom print audits: 22 named source declarations plus 15 critical prerequisites. |
| Independent semantic review (`support_semantics`) | **PASS** on the exact frozen commit, original source claim, all six contract obligations, canonical semantics, indices, parity, and overflow. The sole preliminary docstring finding was resolved before the freeze. |
| Independent execution (`support_runtime`) | **PASS**: a separate fresh eight-module build and actual signature/axiom coverage for all 2,410 module-origin constants. This includes 1,525 safe mathematical declarations, 93 of them private, and 885 implementation artifacts reported separately. |
| Independent complete public printing | **PASS**: 36 safe public constants attributed to the new module, including generated safe helpers, plus 12 critical prerequisites received 48 `pp.all` declaration/axiom prints. The retained supplement reports **zero ellipses** and reuses only the successful independent fresh-build objects. |

The 36 origin-selected safe public constants are distinct from the 22 explicitly named source declarations. The safe mathematical axiom union is exactly `propext`, `Classical.choice`, and `Quot.sound`. Author execution, nonauthor semantic review, nonauthor mechanical verification, and integration are separate states; the independent reviewers did not author the target source. The printing supplement is not represented as a second complete project rebuild.

## Evidence publication layout

The following package-relative paths provide the publication layout for completed reports and their full evidence archives:

| Evidence | Publication paths |
| --- | --- |
| Author and canonical checker | [author-evidence.tar.gz](evidence/author/author-evidence.tar.gz), [AUTHOR_REPORT.md](evidence/author/AUTHOR_REPORT.md), [CHECKER_REPORT.md](evidence/author/CHECKER_REPORT.md), [verification.json](evidence/author/verification.json) |
| Independent semantic review | [semantic-review-5d02e88f.tar.gz](evidence/semantic/semantic-review-5d02e88f.tar.gz), [FINAL_SEMANTIC_REVIEW.md](evidence/semantic/FINAL_SEMANTIC_REVIEW.md) |
| Independent execution and complete printing | [support-runtime-review-5d02e88f.tar.gz](evidence/runtime/support-runtime-review-5d02e88f.tar.gz), [FROZEN_EXECUTION_REVIEW.md](evidence/runtime/FROZEN_EXECUTION_REVIEW.md) |


The reports are preserved verbatim. Historical relative paths and absolute execution paths inside them describe the original workspaces; most detailed sources and logs are retained inside the corresponding archives, and are not all exposed separately in the visible evidence tree. Use the supplied member manifests and archive contents when following those historical paths. Failed attempts and original checker provenance remain preserved; regenerable object omissions are enumerated with hashes.

[BUILD_REGISTRY.json](BUILD_REGISTRY.json) is scoped schema-1 metadata with `catalogue_complete: false`. The shared `verify_project` runner was **not executed** for this contribution, and no shared registry was modified. Strict verification rests on the actual canonical checker and the separately attributed independent gates. Main integration remains pending.

This contribution covers the selected actual-carry support claim. It makes no assertion that J=0 iff nine is absent, nor any claim of charge persistence, a new palindrome criterion, T/R injection, H, the four evolution laws, residue saturation, quotient classification, or an all-time conclusion about 196.
