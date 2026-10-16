# Independent review of the three-layer prefix obstruction

**PASS. One fresh 27-module Lean 4.19.0 build completed with `--trust=0`; the complete compiled-ownership audit covered all 231 explicit declarations and all 373 safe logical constants in the 17 contribution modules. No semantic or integration blocker was found in the four new proof modules.**

Reviewer: Agent #3 runtime/review specialist (`/root/lean_runtime`), who authored none of the four assigned proof modules. The parent handles source publication and all issue/PR relay. This is a nonauthor review within the same collaborating Agent #3 session; it does not assert a separate GitHub identity.

## Reviewed source and inherited semantics

The completed semantic review covers all four modules, `DeadPrefix.lean`, `ActualDepth.lean`, `SharpHistoryFamily.lean`, and `SharpHistoryTheorem.lean`, together with the unchanged original `Local`, `Path`, `Realizes`, `ActualFiber`, and complete arithmetic converse. All 23 inherited source modules match baseline `89287c9d3eb7dd801c2b1a59eff03140d47d24ec` by SHA-256 and Git blob identity.

All four new sources match the parent's explicit freeze:

| Module | SHA-256 | Explicit declarations | Safe logical constants audited |
| --- | --- | ---: | ---: |
| `DeadPrefix` | `09c01111e2eb2f57637fe7d3a04e45aca4ca3d20c0248dc349e956c6ffc1fc64` | 15 | 15 |
| `ActualDepth` | `dcc9655c0fe9f60419fc60b821e225f705f3ce713792419586d623125ca9d0e2` | 14 | 19 |
| `SharpHistoryFamily` | `6e3b02999b118ed00133d7bebdbf553a6f19d6bfaec4f6abbf982ab7ee2fb002` | 16 | 25 |
| `SharpHistoryTheorem` | `d6afdf3e252b1b223ad30548ba6f72a3ba17604dfba43563ea28a5a9435a2f29` | 7 | 10 |

The full published source checkpoint reported by the parent is [6ce47fddb10f15b4af1025954f1694825093673d](https://github.com/taco-jpg/p196-algorithm/commit/6ce47fddb10f15b4af1025954f1694825093673d), with tree `a3448c1d0da258403a3e3f44cd2ca3eeec052da2`. I directly observed local commit `34481a73247e04345a0c67d8717df7e7cbf23136` with exactly that tree and verified all four local committed Git blobs against the reviewed files. The published commit object itself was not available locally: its remote identity is parent-reported, while the matching local tree and source blobs were independently observed. [publication.json](publication.json) records this distinction.

[freeze.json](freeze.json) preserves the timestamp and authority of the source freeze. Every source remained unchanged after the build. The original Agent #9 dependency hashes and Git blob pins also match `dependencies/agent9/SOURCE_PINS.json`.

## Local obstruction and arbitrary suffix

An original Agent #9 state in `Fin 4` records two carries: `low p = p.val / 2` and `high p = p.val % 2`. `Local s p q x` states a coefficient bound, both decimal carry equations, and the mirrored digit-sum equation. The new `Forced` predicate is an implication identifying the next state and emitted coefficient whenever a transition exists. It does not itself assert transition existence, which is unnecessary for the exclusion proof.

The nine forced-row assertions, proved by ordinary kernel-checked `decide`, produce the following prefix composition:

| Layer | Target prefix | Forced predecessor prefix | Carry states after the columns |
| --- | --- | --- | --- |
| First inverse layer | `[14,14,14,5]` | `[7,7,7,2]` | `0,0,0,1` |
| Second inverse layer | `[7,7,7,2]` | `[3,13,13,0]` | `1,3,2,1` |
| Third inverse layer | `[3,13,13,0]` | `[1,16,16]`, then failure | `1,3,2`, then no transition |

The last step would require an original `Local 0 2 q x`, which the finite arithmetic theorem excludes for every next state and every bounded coefficient. The original `Path` predicate is peeled one column at a time. Its own coefficient bound permits the final ancestor to remain a `List Nat`; there is no extra assumption that its values were already packaged as `Fin 19`.

The contradiction occurs at the fourth column, before inspecting the tail or the even-center acceptance condition. Thus every `List Symbol` tail is covered, including tails containing zero or eighteen. No complete 65-state automaton, asymptotic language result, or general contraction claim is used.

## Full-word arithmetic transport

The original `ActualFiber ss xs` requires equal half-lengths, all source coefficients below 19, zero final scan carry, and the exact original `Agent8.stepWord` equality between the mirrored words. `ActualDepth` applies `actual_realizes` followed by `realizes_path` separately to all three fibers. These are the original complete converses, not new arithmetic assumptions.

The two existing history halves are repackaged as `List Symbol` by preserving their emitted symbols and the eighteen suffix. Their value identities use the literal equality `(18 : Symbol).val = 18`. Their accepting paths and actual fibers follow from the previously proved two-history construction.

`historyWord0_no_zero_predecessor` retains the precise conditions on a proposed earlier half `ys`: equal half-length to the constructed initial word, every coefficient below 19, and `terminalCarry (mirror ys) 0 = 0`. A hypothetical full-word step to the constructed initial word would form a third `ActualFiber`, contradicting the arbitrary-history exclusion. This is sharpness within the stated equal-width, bounded, all-zero-carry domain; mixed-overflow or unrestricted numerical ancestry is outside its conclusion.

## Restricted family and numerical interpretation

`depthBits free` fixes exactly three free choices, `[true,true,false]`, before the remaining free bits. The inherited protected half therefore begins `[14,14,14,5]`; the six correction bits and eighteen reservoir remain in the arbitrary tail.

For `free.length = m`, both restricted coefficient-word families have exactly `2^m` distinct members. Injectivity is obtained from the existing history-word injectivity followed by cancellation of the fixed Boolean prefix. The actual two-step map sends the complete initial enumeration to the protected enumeration in the same order.

The width shift is exactly `2 * (m + k + 10)`: the three fixed bits add three positions to each half of the previous construction. The common fourth ordinary value correspondingly becomes `digitValue (target (m + 9) k)`. Positive realizability and nonpalindromicity through every time `0 <= t <= k + 3` are inherited for `k > 0`, universally over every ordinary canonical realization of an initial word. Both time endpoints are included. Cardinalities count coefficient words, not all ordinary integer realizations.

## Final aggregate and exact depth

`ExactlyTwoZeroCarryLayers` explicitly means that two original `ActualFiber` layers exist and that no triple of such layers exists. The witnesses and the exclusion use the same unchanged relation. The positive part comes from the existing two-history paths, so the result is not a vacuous exclusion.

`sharp_protected_exact_depth` supplies the corresponding symbol half for every member of the protected enumeration. `sharp_initial_no_zero_predecessor` states equal width in full-word form as `2 * ys.length = w.length`; its proof correctly derives equality with the original half-length before applying the exclusion.

The separately exported `sharp_initial_canonical_chain` exposes canonical intermediate and protected words with the same even width. The first two word transitions have final carry zero; the protected word has final carry one and its next word is `target (m + 9) k` when `k > 0`.

The final `finite_horizon_exact_two_history_family` joins exact lengths and `Nodup` for both enumerations, their exact two-step map, canonical even-width properties, protected exact depth, initial positive integer realizability, universal ordinary safety through `k + 3`, common ordinary time-four value, and the precise predecessor exclusion for every initial word.

The ordinary integer equality is `orbit n 4 = digitValue (target (m + 9) k)`. It applies to every `IntegerRealizes n w`, rather than only to an existentially selected witness. The finite time shift agrees with the two incoming history steps and the inherited overflow/realization bridge. No all-time result or claim about seed 196 is present.

## Clean rebuild and complete declaration audit

The one independent run began at `2026-10-16T22:15:55.699147+00:00` and finished at `2026-10-16T22:17:21.932536+00:00`. Recorded command time totals 85.880 seconds. All 29 commands exited zero: a runtime version check, 27 module builds, and the ownership audit. All builds and the audit used `--trust=0`. No compiler warning or error was reported. The four new module compilation logs are empty.

The verified executable is:

```text
/workspace/scratch/4ce7c54d31f6/lean-runtime/lean-4.19.0-linux/bin/lean
Lean (version 4.19.0, x86_64-unknown-linux-gnu, commit 6caaee842e94, Release)
SHA-256 92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023
```

Only exact `.lean` sources were staged into the new build directory. No preexisting project `.olean` was copied or referenced. `LEAN_PATH` contained only that new module directory, and inherited Lean path/option overrides were removed before invocation. The standard library came from the pinned installed runtime. Source hashes, import order, inherited Git blob identities, and final object hash stability were checked.

The audit enumerated constants by their owning module across all 17 contribution modules. It inventoried **620 compiled constants** and issued `#print axioms` for **all 373 safe, nonpartial logical constants**, including generated equations and helpers. It required exact equality between the safe inventory and the returned axiom records. It matched **all 231 explicit source declarations**, including all 52 new declarations, to safe compiled constants with accepted axiom audits.

All three inherited explicit private declarations were included: `nodup_map_of_injective`, `replicate_join`, and `jointData`. The diagnostic used `mkIdent` on exact compiled Lean `Name` values, preserving numeric components of private names. Private generated safe helpers were included by the same ownership rule.

The other **247 generated unsafe or partial implementation constants** were separately retained in the inventory and machine report. None is an explicit source declaration. These are compiler implementation stages; the corresponding logical constants and all their transitive axiom dependencies were checked. The axiom union is exactly `Classical.choice`, `Quot.sound`, and `propext`.

The contribution source scan found no `sorry`, custom axiom, `native_decide`, native-cast shortcut, explicit unsafe/partial declaration, or source metaprogramming bypass. The logical audit rejected any axiom outside the stated set and found none. The diagnostic audit's own `run_cmd` only inventories the environment and issues `#print axioms`; it contributes no proof module.

## Reproduction and retained evidence

The exact invocation was:

```bash
python3 proofs/contributions/agent-3/three-layer-prefix-20261016/review/verify_independent.py \
  --repo /workspace/scratch/4ce7c54d31f6/p196-depth \
  --lean /workspace/scratch/4ce7c54d31f6/lean-runtime/lean-4.19.0-linux/bin/lean \
  --build /workspace/scratch/4ce7c54d31f6/agent3-three-layer-independent-build \
  --freeze /workspace/scratch/4ce7c54d31f6/p196-depth/proofs/contributions/agent-3/three-layer-prefix-20261016/review/freeze.json
```

The environment required the already authorized compiler escalation because the default sandbox could not locate the runtime application. A later reproduction must choose a fresh empty build directory. This completed build was not rerun.

The evidence files are:

- [verification.json](verification.json): 27-source mapping, SHA-256/Git identities, imports, exact commands, runtime pin, timings, explicit declaration matches, and final acceptance results.
- [compiled-declarations.json](compiled-declarations.json): all 620 module-owned compiled constants, including private and implementation names.
- [axiom-dependencies.json](axiom-dependencies.json): the complete 373-entry logical axiom audit.
- [IndependentOwnershipAudit.lean](IndependentOwnershipAudit.lean): the generated ownership and axiom diagnostic.
- [logs/28-compiled-ownership-axioms.log](logs/28-compiled-ownership-axioms.log) and the other `logs/` files: unedited runtime, compilation, and audit output.
- [verify_independent.py](verify_independent.py), [freeze.json](freeze.json), and [publication.json](publication.json): reproducible checker and exact provenance.
- [evidence-manifest.json](evidence-manifest.json): sizes and SHA-256 values for the completed evidence files, excluding the manifest itself.

No proof source was changed, and this review performed no Git or issue/PR mutation. The required compilation, audit, and semantic review are complete. No further testing is needed for the assigned scope.
