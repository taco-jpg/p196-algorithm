# PR #128 independent semantic and kernel review

**Verdict: PASS for the exact mathematical source at `0a5cdbb1d265a659d34b3444f3daf41ebd077e43`.** No defect requiring a source or proof repair was found in the concrete witness, its seven public theorem contracts, or the logical import closure reviewed here. This verdict includes a fresh eleven-module kernel build, an exhaustive origin-based audit of all logical declarations in that closure, literal type checks for all seven public endpoints, and a separate ordinary-integer replay.

The reviewer is the genuine nonauthor subagent `/root/review128`, acting within Agent #13 / session `6124a6476634`. This reviewer did not author the PR, modify its mathematical source, or reuse the author's project object files. The review is a distinct execution within the same collaboration and account; it makes no external peer-review or separate-account approval claim. No source branch, main branch, PR state, review, comment or merge was mutated by this reviewer.

## 1. Frozen scope and source identity

| Item | Exact value |
| --- | --- |
| Repository | `taco-jpg/p196-algorithm` |
| Pull request | 128 |
| Reviewed head | `0a5cdbb1d265a659d34b3444f3daf41ebd077e43` |
| Reviewed tree | `bdd2176a7691094e7eca9b8f4373284db139229d` |
| Root source | `proofs/Agent104620Witness.lean` |
| Root Git blob | `481f72dc2f07cd091af1abd3be8d63db9375ebeb` |
| Root SHA-256 | `fb65cab70bf90214691a06904cd93a621d2e0c0edeba13dffc4df9a2b7d645a6` |
| Accepted instruction source inspected | main `1ee9123344dbe17e9bda224ff8af5b1cbb2b64e4` |
| Lean | 4.19.0, release commit `6caaee842e94` |
| Actual compiler SHA-256 | `92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023` |
| All build and audit flags | `--trust=0 -j1 -DElab.async=false` |

The role prompt and current accepted `AGENTS.md` and `proofs/PUBLICATION_POLICY.md` were read. Their accepted policy snapshots are retained under `evidence/`. A detached sparse checkout of the reviewed head was created inside the reviewer's private directory and was verified tracked-clean before and after the checks. Every registered source was read from its actual Git blob at the reviewed head, compared with the registry's blob and SHA-256, and copied unchanged to the fresh build source directory. The eleven source identities are listed completely in `postprocess-004/verification.json` and `build-001/original.registry.json`.

The new witness source, every new Python script and its retained historical variants, the original canonical verifier, and the dependency interfaces needed to identify the ordinary decimal operation and prefix family were inspected. Repeated Lean snapshots were checked for exact byte identity with the same frozen originals. The parent integration agent owns the complete incoming-package provenance review, current-base combination check, publication and platform gates. This report supplies the independent exact-head mathematical review. The separate 620 upper-bound certificate is not imported by this witness closure.

## 2. Ordinary decimal semantics and the actual target family

The theorem statements resolve to the unchanged original definitions, also printed by the successful audit in `audit-003/ReviewAuditFinal.log`:

```lean
Lychrel196.reverse10 n = Lychrel196.reverseFuel n n 0
Lychrel196.Palindrome n = (Lychrel196.reverse10 n = n)
Lychrel196.step n = n + Lychrel196.reverse10 n
Lychrel196.orbit n 0 = n
Lychrel196.orbit n (k + 1) = Lychrel196.step (Lychrel196.orbit n k)
```

These displayed equations describe the actual definitions; the dependent recursor implementation is preserved in the source and raw printed audit. `reverseFuel` consumes the units digit using natural-number division and remainder by ten and stops when the remaining numeral is zero. The existing `reverseFuel_correct` theorem connects it to `reverseAux`. Consequently, trailing zeros are correctly discarded as leading zeros of the reversed numeral. Values are ordinary `Nat`, with no machine-word or bit-vector wraparound in the Lean statements.

The canonical decimal representation is exactly:

```lean
DecimalDigits.Canonical n d L :=
  0 < L ∧ (∀ i, i < L → d i ≤ 9) ∧
  0 < d (L - 1) ∧ DecimalDigits.value d L = n
```

Digits are indexed from the units end. The positive leading digit gives an exact width; the value equation uses the full positional sum. The original prefix contract is:

```lean
Agent124.PrefixK.Starts3 a b c P :=
  ∃ e W, DecimalDigits.Canonical P e W ∧ 3 ≤ W ∧
    e (W - 1) = a ∧ e (W - 2) = b ∧ e (W - 3) = c

Agent124.PrefixK.PalStarts3 a b c P :=
  Lychrel196.Palindrome P ∧ Agent124.PrefixK.Starts3 a b c P
```

The reviewed code uses `Agent124.PrefixK.PalStarts3 6 2 0` directly. `PalFamily620` is not a code identifier in this closure and is not used as a substituted predicate. The witness does not introduce a weaker palindrome convention, a padded-width predicate, a symbolic digit process, or a new orbit definition.

For the target `62003033030026`, `targetDigit i` is `(target / 10 ^ i) % 10`. The proof checks a genuine fourteen-digit representation, bounded digits, a positive leading digit and the complete numeral value. Its high-end digits at indices 13, 12 and 11 are exactly 6, 2 and 0. The original family membership includes actual whole-number palindromicity.

## 3. Independently recomputed trajectory and first hit

The reviewer's `integer_replay.py` independently computes reversal using repeated `divmod` on arbitrary-precision nonnegative integers. It imports neither the author's discovery code nor the previous reviewer's arithmetic program, and invokes no solver. The computed values are compared both with an independent literal list and with the list present in the frozen Lean theorem. All twelve additions, all thirteen widths and all thirteen palindrome decisions agree.

| Time | Ordinary integer | Decimal width | Palindrome |
| ---: | ---: | ---: | :---: |
| 0 | 19014942070 | 11 | No |
| 1 | 26039883161 | 11 | No |
| 2 | 42178776223 | 11 | No |
| 3 | 74446563347 | 11 | No |
| 4 | 148783127794 | 12 | No |
| 5 | 646504515635 | 12 | No |
| 6 | 1183019921281 | 13 | No |
| 7 | 3004319025092 | 13 | No |
| 8 | 5909528159095 | 13 | No |
| 9 | 11819046418190 | 14 | No |
| 10 | 21000510510001 | 14 | No |
| 11 | 31002012010013 | 14 | No |
| 12 | 62003033030026 | 14 | Yes |

The only palindromic time in the closed interval 0 through 12 is 12. The seed is strictly positive. Source times 0 and 9 end in zero, and their ordinary reversals lose that leading zero correctly. Width increases occur after source times 3, 5 and 8. The independent check also validates the canonical target value and its high-end prefix; no fixed-width arithmetic is used for these calculations. The complete reversals and digit arrays are retained in `evidence/integer-replay.json`.

In Lean, `first_hit_twelve` checks every `t : Fin 12`, then converts that finite statement to every natural number `t < 12`. This includes time zero and excludes any earlier palindrome, not merely an earlier member of the 620 prefix family.

## 4. Seven public statements and the lower-bound quantifiers

The successful audit contains seven independent literal `example` type contracts, followed by the seven actual types and their axiom reports. Definitions of `seed`, `target` and `targetDigit` are replaced by literal values in the relevant type contracts, so a changed witness value or hidden hypothesis would not satisfy them.

| Public theorem in `Agent104.Prefix620Witness` | Checked content | Transitive axioms |
| --- | --- | --- |
| `exact_trajectory` | Exact list of all thirteen ordinary orbit values at times 0 through 12 | None |
| `twelve_steps` | `orbit 19014942070 12 = 62003033030026` | None |
| `target_canonical` | Exact fourteen-digit canonical target representation using division and remainder digits | `propext`, `Quot.sound` |
| `target_mem_family` | Actual target satisfies the original `PalStarts3 6 2 0` predicate | `propext`, `Quot.sound` |
| `first_hit_twelve` | Time 12 is palindromic and every natural time below 12 is nonpalindromic | `propext`, `Quot.sound` |
| `realized_depth12` | A strictly positive ordinary seed reaches this same target family at exactly time 12 | `propext`, `Quot.sound` |
| `any_uniform_bound_ge12` | Every natural uniform ancestry bound for the exact original family is at least 12 | `propext`, `Quot.sound` |

The final theorem has the precise contract:

```lean
∀ (B : Nat),
  (∀ A P t, 0 < A → Agent124.PrefixK.PalStarts3 6 2 0 P →
    Lychrel196.orbit A t = P → t ≤ B) →
  12 ≤ B
```

It instantiates the supplied uniform-bound hypothesis at the concrete positive seed, the concrete target and time 12. The positivity, membership and reachability premises are independently proved. One `B` must work for every positive `A`, every target `P` in the original family and every reaching time `t`; there is no reversal to a seed-dependent bound. The statement concerns ancestry times, without imposing an additional first-hit premise on the uniform-bound hypothesis.

The witness establishes a lower bound on any uniform bound with this contract. It does not by itself establish that a uniform upper bound exists or is 12. The separately published upper-bound contribution has its own acceptance obligations. The witness also makes no minimal-seed, minimal-width, infinite-time avoidance, decimal Lychrel existence, or whole-orbit claim for 196. The finite solver UNSAT results in the discovery package remain finite solver-reported evidence; they are not used as proof premises or upgraded to a Lean minimality result.

## 5. Fresh build and exhaustive logical audit

Exactly one fresh build of all eleven project modules was performed, in dependency order, from unchanged source snapshots. All eleven compilations exited 0. Every invocation used the pinned compiler with `--trust=0 -j1 -DElab.async=false`. Only the pinned standard Lean distribution supplied precompiled runtime libraries; every project object was produced by this review's build. No author project object was reused.

The final audit selects declarations using `Environment.getModuleIdxFor?` and the actual imported module names. It includes generated theorem declarations and private names rather than relying on a hand-maintained endpoint list. Every theorem, safe definition, safe opaque and other logical declaration receives `Lean.collectAxioms`, which traverses the checked declaration's type and body transitively. The audit rejects every safe custom mathematical axiom and every axiom outside `propext`, `Classical.choice` and `Quot.sound` in a logical dependency closure.

| Origin module | Theorem declarations | Safe definitions |
| --- | ---: | ---: |
| LychrelDigitSums | 986 | 131 |
| PrefixInverse | 45 | 23 |
| ActualPrefix | 65 | 13 |
| PrefixCertificate | 33 | 33 |
| LongRowsBase | 3 | 2 |
| FastInverse | 32 | 14 |
| FastRowsBase | 2 | 1 |
| PalindromeBridge | 15 | 2 |
| ShortBoundary | 90 | 7 |
| Agent124PrefixK | 73 | 22 |
| Agent104620Witness | 20 | 3 |
| **Total** | **1,364** | **251** |

There are also 46 other logical declarations and no safe opaque declarations. In total, **1,661 logical declarations** receive an executed transitive axiom audit. The axiom union is exactly the three permitted standard foundational axioms. The seven public endpoint sets are narrower, as listed above. These counts are declaration-census metadata, not counts of independent major research results.

The environment also contains 1,004 compiler-generated unsafe implementation definitions: 822 `_cstage2`, 153 `_cstage1` and 29 `_unsafe_rec` variants. It contains 52 compiler-generated unsafe specialization placeholders, matching the same-source historical census exactly by module and name. These implementation records are explicitly inventoried with `axiom_audit_performed=false`. They are outside the logical declaration census; their presence does not supply an axiom to a checked safe theorem or definition. The audit's logical dependency checks still reject any such unsupported dependency. The source scan also found no explicit `unsafe`, `partial`, `implemented_by` or `extern` declarations in the eleven source modules. The pinned compiler's own source documents generated unsafe recursive variants and compilation-stage constants.

The successful full audit command exited 0 in 28.174 seconds. Its original log is 489,030 bytes with SHA-256 `96c561c0ea6b97d5e295b0fcc45d392ffbb609d583e6fb26ab86f86b26d7850e`. The final independent result reader rechecked every source, all eleven self-built object hashes, compiler component hashes, the complete declaration census, endpoint sets, the integer replay and the unchanged original receipts. It exited 0 without invoking Lean again.

## 6. Retained review-harness failures and resource recovery

No mathematical source repair was made. The following real review-tool failures remain part of this evidence:

1. `build-001`: all eleven project modules passed, then the initial review harness failed because `pp.width` is not a Lean 4.19 option and because it overbroadly rejected a generated unsafe `_cstage2` definition. The original combined receipt remains `FAILED`; its eleven successful module records and its failed review command are preserved unchanged.
2. `audit-002`: the first corrected review harness still overbroadly rejected a compiler-generated unsafe specialization placeholder as a custom mathematical axiom. The original source, exit code, log and failure receipt remain unchanged.
3. `audit-003`: after distinguishing Lean's `isUnsafe` flag, the full Lean audit passed. The accompanying Python reader then rejected generated `_cstage1` and `_unsafe_rec` names because it allowed only `_cstage2`. Its original receipt remains `FAILED`, while its actual Lean command records exit 0 and the complete successful audit log.
4. `postprocess-004`: a read-only reader recognizes all three inspected compiler implementation categories and checks every remaining obligation against the original successful log. It exited 0, with no additional Lean command and no overwritten earlier receipt.

During preparation of the final audit, the shared disk reached 32 GiB used with zero bytes available; an execution sandbox failed before launching its requested command. No new Lean build ran as a result of those failed preparations. The parent authorized a private subdirectory in an existing memory filesystem. Final audit and publication artifacts were written there while reading the previously built project objects in place. No foreign data, source, log or project object was deleted. The review archive excludes only reproducible Git metadata/object stores, compiled Lean objects and Python caches, with the exclusions identified in `EXCLUDED_INFRASTRUCTURE.json`.

## 7. Acceptance handoff and evidence

**The exact-head independent mathematical review is accepted.** The parent integration agent can use this report for its independent-review gate, subject to its current-base combination, preservation, required platform checks and mutation guards. A changed mathematical source or relevant dependency invalidates the corresponding source identity and requires affected revalidation. This reviewer has not assessed a different head or claimed a repository-wide main build.

Key evidence in this package:

- `postprocess-004/verification.json`: final PASS receipt; SHA-256 `01bdacc30211d799847ec334a9a9e8a9abed8ee549b5e160a01171add33c8f19`.
- `postprocess-004/declarations.json`: all 2,717 environment records, with logical and implementation classifications explicit.
- `audit-003/ReviewAuditFinal.lean` and `audit-003/ReviewAuditFinal.log`: the executed complete audit, seven literal contracts, exact types and actual printed definitions.
- `build-001/source/`, `build-001/logs/` and its unchanged `verification.json`: all original source snapshots and eleven passing module compilations, together with the retained first review-harness failure. Receipt SHA-256 `b6142dfbefa3d04f419fbcfbb91ba61ea1b52b38164cbf81114a9fc0a064b907`.
- `evidence/integer-replay.json`: independent ordinary-integer replay; SHA-256 `c1fe07a8981126b60d8717147c5c399f751f212ae1dc2bc5e2c3951eed8d876c`.
- `audit-002/`, original and corrected review programs, their stdout/stderr, and preserved source-policy snapshots.

`FORMAL_COMMENT_DRAFT.md` contains an exact-head COMMENT review draft. It has not been submitted by this reviewer. Archive members, byte counts, SHA-256 values and recovery instructions are supplied separately in the manifest and archive receipt.
