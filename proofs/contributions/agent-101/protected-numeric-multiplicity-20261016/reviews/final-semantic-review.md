# Final independent review of the protected ordinary-integer family

## Result and scope

**PASS.** The exact published 26-module closure builds successfully from a new directory with the prescribed, unchanged verifier. The generated `ProjectAudit.lean`, rerun with explicit `--trust=0`, audits all **1,783 module-origin theorems** with axiom union `{propext, Classical.choice, Quot.sound}`. A separate explicit-trust-zero audit covers all **94 new public declarations: 85 theorems and 9 definitions**. Every one of these public declarations is safe and has only the permitted axiom dependencies. No mathematical source or Git state was changed by this review.

The independent semantic review below covers `Agent101NormalizationValue.lean`, `Agent101ProtectedSafety.lean`, and `Agent101ProtectedFamily.lean`. This reviewer did not author those three modules. Earlier reviews by the same reviewer cover `Agent101ProtectedMultiplicity.lean`, `Agent101ProtectedPalindrome.lean`, and `Agent101ProtectedNonpalindromic.lean`; their reports are linked below. The reviewer authored the older `Agent101SplitEnumeration.lean` and `Agent101PalindromeFibers.lean` dependencies and does **not** present this report as an independent semantic review of those two dependencies. Other workers supplied their independent reviews. Fresh compilation and theorem-origin auditing here cover the complete selected closure, including those dependencies.

This is a selected-project result. It does not certify the repository-wide catalogue.

## Exact source identity

Published source commit: `71691d50497edc83247b3571af276bb0ee438491`.

| Item | SHA256 |
| --- | --- |
| `proofs/Agent101ProtectedFamily.registry.json` | `04aba56fc69ef566d32b0c1064a4db2298f095d88e98fcd9fefe7f5c70614307` |
| `proofs/verify_project__214bf7673efe116b.py` | `c047ff1ff1fe12b2c2094ca5f36af871b1c6faf89db593a102f9c2f7d48cc98a` |
| `proofs/Agent101NormalizationValue.lean` | `50d2d40d5d8db605b8b6d363bf1d0ec762d8c06983c4bb3384f3e1f3094adac9` |
| `proofs/Agent101ProtectedSafety.lean` | `7b3f060d84e7b955f47425dc69277ea8d8f2fa94a62db173a47f3a614d2a2eb2` |
| `proofs/Agent101ProtectedFamily.lean` | `25b6d7e60929a9b98e182cd247c4693bc551b699f26f46e32743a9044c877127` |

Before building, this reviewer independently ran `git show <commit>:<path>` for every one of the 26 registered source files, the registry, and the verifier. All commands returned zero. Each published source matched the working file, the registry SHA256, and the recorded Git blob. The observed HEAD was the source commit above. `GIT_NO_LAZY_FETCH=1` prevented implicit object fetches; the operations were read-only. The individual results and exact commands are in [final-source-readback.json](final-source-readback.json), produced by [final-source-readback.py](final-source-readback.py).

### Embedded foundation adapter

The registry includes an explicit foundation adapter. The original `Lychrel196Research` source has 4,445 lines. After excluding its first `import Std` line, the remaining 4,444 lines are byte-identical to the block beginning at line 11 of `LychrelDigitSums`. This reviewer independently checked the whole block, not a selection of declarations.

The canonical verifier compiles `LychrelDigitSums` and generates a documented `Lychrel196Research` facade importing it. The generated facade is retained as [final-Lychrel196Research-adapter.lean](final-Lychrel196Research-adapter.lean), SHA256 `5c8859684f186a7121d0d3cbf82f2ad5ac9398ccb73c4dd6a9d2256be128a11b`. Thus the two imports use a single shared foundation. None of the older review directories' separately compiled foundation oleans was used in this final run. The registry and canonical report retain both original-source and actual-build hashes.

## Rebuild and audit method

The exact canonical command was:

```text
python3 proofs/verify_project__214bf7673efe116b.py \
  --registry proofs/Agent101ProtectedFamily.registry.json \
  --project agent101-protected-family \
  --lean /workspace/scratch/2a8a87fd78df/agent101-runtime/toolchain/lean-4.19.0-linux/bin/lean \
  --output /workspace/scratch/2a8a87fd78df/agent101-final-family-independent-71691d5
```

The output directory was new. The verifier constructed its source directory and used that directory as `LEAN_PATH`; all 26 selected modules were compiled afresh. The fixed executable reports Lean 4.19.0, commit `6caaee842e94`. The executable and its recorded shared libraries were hashed. The source, registry, verifier, build snapshots, and compiler files were checked again after the audits and remained unchanged.

**Trust-setting distinction:** the prescribed original verifier invokes compilation and its initial audit with `-j1 -DElab.async=false`; these commands do **not** explicitly include `--trust=0`. This review does not describe them as explicit-trust-zero module builds. After their successful completion, this reviewer ran the generated, unchanged `ProjectAudit.lean` with `--trust=0 -j1 -DElab.async=false`, then ran the separate complete public-declaration audit with those same flags. No second full closure was built.

| Verification stage | Actual result |
| --- | --- |
| Published-source readback, 26 modules | PASS; exact bytes and Git blob identities match |
| Canonical fresh module builds | 26/26 return code 0 |
| Canonical generated ProjectAudit | Return code 0; 1,783 theorems |
| Unchanged ProjectAudit with explicit `--trust=0` | Return code 0; 1,783 unique theorem names; 36.97 seconds |
| Separate public audit with explicit `--trust=0` | Return code 0; 94/94 public declarations safe; 5.48 seconds |
| Theorem and public axiom dependencies | Only `propext`, `Classical.choice`, `Quot.sound` |
| Post-audit source and tool identity | All recorded hashes unchanged |

The generated ProjectAudit selects declarations by their actual originating module. It rejects safe custom axioms and rejects any audited theorem with an axiom outside the allowed set. It records compiler implementation axioms marked unsafe separately. The latter do not become permitted proof dependencies. The public audit additionally rejects an unsafe public declaration or a public axiom declaration and requires an exact census of 94 public names. This review makes no claim of a separate census of every transitive safe definition.

The 94 public declarations belong to the following eight modules:

| Module | Public declarations |
| --- | ---: |
| Agent101ProtectedMultiplicity | 18 |
| Agent101NormalizationValue | 5 |
| Agent101ProtectedSafety | 10 |
| Agent101PalindromeFibers | 14 |
| Agent101NonpalindromicFibers | 18 |
| Agent101ProtectedPalindrome | 15 |
| Agent101ProtectedNonpalindromic | 10 |
| Agent101ProtectedFamily | 4 |
| **Total** | **94** |

The exact inventory, commands, output logs, and hash checks are retained in [final-public-exports.json](final-public-exports.json), [final-audit-commands.json](final-audit-commands.json), and [final-verification.json](final-verification.json). The unchanged verifier's original report retains its original `agent: Agent #1` author field; that field is not an assertion that Agent #1 performed this independent run. This review's own report identifies the actual reviewer.

## Semantic review: normalization to ordinary integers

`Agent101NormalizationValue` introduces no new arithmetic interpretation. `natValue_eq_digitValue` is definitionally reflexive: both values use the original finite decimal evaluation of the least-significant-first digit list.

`natValue_normalize w e` transports the already published theorem `P196.Agent3.TwoHistory.digitValue_normalize w e`. The pinned `IntegerInterfaces.lean` dependency, SHA256 `bc6d2926cd16c43de990ede025b9ba69e50d1e7e2a578044ad65bdf348e8b4fe`, retains that theorem's proof through `Agent109.Compat.normalize_eq` and `Agent109.evalL_norm`. Its provenance records Agent #3 commit `0be2a5aad6060d052141246d09bf05a8068f7c3e` and original path `proofs/contributions/agent-3/two-history-20261016/IntegerInterfaces.lean`. Attribution to the underlying Agent #109 result is preserved.

The value equality allows arbitrary words and arbitrary incoming carries. It does not assert that every such resulting list is a canonical digit list. This distinction is correct, including carries greater than nine.

`step_eq_normalized_pair_value` applies the existing ordinary-integer `step_natValue` theorem only under `canonicalDigits ds`. `numericFiber_first_step` obtains precisely that canonical witness from complete fiber membership, substitutes its coefficient word, and derives the normalized first value. No extra coefficient-validity assumption is silently introduced, and no nonempty-fiber claim is needed for this membership implication. All five exported statements agree with their uses in the safety bridge.

## Semantic review: the finite safety bridge

`Agent101ProtectedSafety.inputFiber_first_value` identifies the actual first ordinary step of every original digit split with the normalized Agent #3 input word. The `coefficientWord_inputHalf` substitution preserves the full mirrored profile, including its width.

For `inputFiber_second_value`, the first-value equality exposes exactly the input to the unchanged `inputWord_common_next_value`. The latter yields the fixed decimal value of `target xs.length k`; its `targetColumn` agrees definitionally with the digit function used by `natValue`. Replacing `xs.length` by `m` after family membership therefore gives the same explicit second value for every family member.

The time-index transport in `inputFiber_safe_positive_times` is exact. A time satisfying `1 <= t <= k+1` is written as `t=j+1`. The original `Lychrel196.orbit_from_step` changes the state to `orbit (step n) j`. The first-value equality then permits `inputWord_normalized_safe xs k hk`, whose time premise is `j <= k`. These are the same bounds, so the proof has no endpoint shift gap. In particular, it includes the last required original time `k+1`.

All second-value and future-safety statements retain the hypothesis `0 < k`. First-value membership remains valid for `k=0`, as do the independently proved counting statements. The module does not extend its future-time conclusion to `k=0`.

The unfiltered family may contain an initial palindrome. Accordingly, its unfiltered safety theorem begins at time one. `protectedSeeds_safe_all_times_of_nonpalindrome` separately takes `not Palindrome n`: time zero reduces to that premise, and positive times use the preceding bridge. This supplies exactly the additional condition consumed by the filtered family.

## Semantic review: the final family endpoint

`Agent101ProtectedFamily` only combines established membership, counting, nonemptiness, ordinary-value, and safety results. `mem_protectedNonpalSeeds` supplies both membership in the complete specified profile family and initial nonpalindromicity. The first component permits the second-value result; both components permit the all-times finite safety result.

The main statement `Agent101.Protected.protectedNonpalFamily_exact m k hk` asserts, for every natural `m` and every positive `k`, a list with:

- exactly `5 * 11^m - 1` distinct members;
- an explicit nonemptiness conclusion;
- positive integers of decimal width `2 * (m + k + 1)`;
- the common second ordinary iterate `natValue (target m k)`;
- nonpalindromicity of the same chosen member at every time `0 <= t <= k+1`.

The decimal-width predicate is the existing numerical interval condition `0 < L` and `10^(L-1) <= n < 10^L`. Thus the endpoint is stated about original natural numbers and their actual decimal width, rather than just coefficient words.

The count subtraction is justified in the previously independently reviewed `Agent101ProtectedNonpalindromic`: the removed palindrome filter is exactly the singleton containing the explicit `palindromeSeed`; partitioning the full list gives `1 + remaining.length = 5 * 11^m`. Nonemptiness is proved separately and is used by the endpoint. Consequently, natural-number subtraction cannot hide an empty-family safety claim. The `m=0` boundary leaves four members. Counts and palindrome removal also apply when `k=0`, while this final safety endpoint deliberately requires positive `k`.

The completeness scope is the union of all original digit realizations of the specified Agent #3 profiles, after initial-palindrome removal. It is not an enumeration of every second preimage of the common target. The horizon parameter and seed family may vary together; there is no exchange of quantifiers asserting a fixed seed avoiding palindromes for all time. Both limits are consistent with the source statements and module documentation.

## Retained evidence and preceding reviews

All 27 canonical logs (26 builds plus its initial audit) are copied, without changes, to [final-build-logs](final-build-logs/). Their identities and the generated foundation adapter are recorded in [final-retained-evidence.json](final-retained-evidence.json). The original canonical output remains at `/workspace/scratch/2a8a87fd78df/agent101-final-family-independent-71691d5`.

Primary retained records:

- [final-source-readback.json](final-source-readback.json) and [final-registry.json](final-registry.json): published-byte and registry checks.
- [final-canonical-verification.json](final-canonical-verification.json) and [final-canonical-FILES.json](final-canonical-FILES.json): the unchanged verifier's original reports, copied verbatim.
- [final-ProjectAudit.lean](final-ProjectAudit.lean) and [final-ProjectAudit-trust0.log](final-ProjectAudit-trust0.log): the unchanged generated module-origin audit and its explicit-trust-zero run.
- [final-PublicAudit.lean](final-PublicAudit.lean) and [final-PublicAudit-trust0.log](final-PublicAudit-trust0.log): the complete 94-public-declaration audit.
- [final-audits.py](final-audits.py) and [final-verification.json](final-verification.json): explicit audit runner and final machine-readable result.
- [counts-semantic-review.md](counts-semantic-review.md), [counts-palindrome-semantic-review.md](counts-palindrome-semantic-review.md), and [counts-nonpalindromic-semantic-review.md](counts-nonpalindromic-semantic-review.md): earlier independent semantic reviews of the three family-counting modules, with their separate exact-source build evidence.

The prescribed final run and both additional audits succeeded on their first execution. No failed mathematical source was created or discarded in this final review. No new theorem, claim, or repository mutation was undertaken for the paused Agent #9 follow-up investigation.
