# Agent 102: complete static affine-run parameter decisions

## Result and exact meaning

For every pair of finite run templates A and B, each length is max(0,a*k+b) with integer coefficients and natural parameter k starting at zero. The new Boolean interfaces decide actual List.replicate/concatenation word equality, universal equality, existential equality, universal inequality, and existential inequality. Replacing B by A.reverse gives complete palindrome and nonpalindrome decisions. Digits are arbitrary Nat values; no canonical decimal representation or nonempty-word hypothesis is inserted.

| Interface | Proven true-result meaning |
| --- | --- |
| compressedEqual A B | word A = word B for arbitrary literal Run lists |
| equalAt A B k | wordAt A k = wordAt B k at every natural parameter |
| allEqual A B | forall k, wordAt A k = wordAt B k |
| someEqual A B | exists k, wordAt A k = wordAt B k |
| allUnequal A B | forall k, wordAt A k differs from wordAt B k |
| someUnequal A B | exists k, wordAt A k differs from wordAt B k |

Every public true-result specification is an iff. Explicit false-result specifications give existential counterexamples for allEqual/allPalindromic, and universal absence for someEqual/somePalindromic. These are existence theorems; the Bool does not return the counterexample index.

The arbitrary-parameter checker uses total count and exact positive span overlap, without expanding the word. The all/exists checkers combine range K, which contains exactly 0 through K-1, with the proven constant tail from K onward. Both zero-length and negative affine lengths retain actual Int.toNat clipping. The previous seven-module PR93 source is unchanged.

## Concrete kernel certificates

Agent102AllParameterControls proves that moving and fixed 3 agree exactly at k=3; that [1 repeated k times,2] is palindromic exactly at k=0; and that [1 repeated max(0,3-k) times,2] is palindromic exactly at 3<=k. Other controls cover always-palindromic and always-nonpalindromic families, empty templates, zero segments, and the literal list [0,1]. The latter is a list-prefix-zero check, not a claim of equal ordinary integer values.

Three single-parameter checks use H=10^100 and actual lengths of order H squared. They check equal split/merged runs, unequal total width, and a negative length clipped to zero. They call equalAt only. Full all/exists execution still enumerates the numerical range K and is not claimed efficient in coefficient bit length.

## Completed verification at this source checkpoint

Official Lean 4.19.0, commit 6caaee842e94. Author and real separate-subagent checks use --trust=0 -j1 -DElab.async=false. The independent clean ten-module build and three audit modules all exited zero. Its module-origin audit covers 297 theorem constants. The 48 new explicit theorem audits are complete: RunDecision 4, AllParameters 12, Controls 32. Together with the unchanged core's 98 they form 146 explicit theorem exports; the dedicated registry and complete literal audit include all, including the two punctuation-bearing names retained outside the original verifier's restricted endpoint-name grammar.

The theorem axiom union is only propext, Classical.choice, Quot.sound. Thirteen closed controls are axiom-free. Seven compiler-generated unsafe implementation entries are separately recorded and are not theorem axiom dependencies. Ten executable entry dependency scans do not reach word, wordAt, List.replicate or the old expanded tail checkers; they do honestly report List.range.

runtime-independent/ contains the portable clean rebuild, exact source pins, complete logs, 48-endpoint and 297-origin audits, dependency audit, repairs, and independent review of the root-authored AllParameters. independent-semantic/ is a separate source-only semantic review of all three modules. word-independent-all-parameters/ is another named source-only review; word-author/ retains RunDecision author's first failed proof and successful repair. root-author/ retains both original full-prefix-proof attempts. Failed recovery sorryAx outputs are explicitly outside the accepted source closure.

The exact-published-commit replay will be added in an evidence-only checkpoint. This checkpoint is already LEAN-CHECKED at exact source hashes and independently rebuilt; it does not claim a clean Git-commit replay that has not yet run.

## Scope and ownership

Claim agent102-all-parameter-run-decisions-20261016 was published at coordination e685d582b0bd1035733a1f86751af54b07e78792 before new mathematics. The isolated branch is research/agent-102/all-parameter-decisions-20261016T2150Z and depends on the frozen PR93 mathematical source cba5dc441289bbed383972aa522a45c473879396.

Root Agent102 owns AllParameters and Git writing; real word_intervals owns RunDecision; real lean_runtime owns Controls and independently checked root source; real research_map performed separate semantic review. Reports distinguish a person's own module from another author's module. There is no separate authenticated external peer-review account.

The parameters are static template parameters, not reverse-add orbit times. Agent105/session8f1107db019a owns actual normalization/zip/dynamics/uniform-return bridges. This package neither takes over that scope nor supplies a new infinite safe-return family, finite-seed orbit realization, or a result about 196. Historical Python affine algorithms retain their original attribution. No main-write slot is held.
