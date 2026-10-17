# Agent #61 — independent statement audit

## Scope and verification boundary

Read-only audit of `proofs/README.md` and `proofs/FINDINGS.md` at main commit `10a173cb635fa8d03e357f454232816fc3e77609`. The role prompt, repository `AGENTS.md`, and `proofs/PUBLICATION_POLICY.md` were read before substantive review. This audit compared selected current Lean declarations with the accepted registry and retained source/build/review records. No Lean compiler, discovery search, certificate replay, Git mutation, or external publication was performed. Findings are attributed to the independent statement-audit specialist for Agent #61; parent owns implementation and coordination.

The selected declarations support the existing statement that neither all-time palindrome avoidance for 196 nor general decimal Lychrel existence is established. The defects found are missing current index coverage and insufficient historical/current separation, not evidence of a newly proved central theorem.

## Prioritized corrections

### 1. Index the accepted nine-carry improvement without rewriting the eleven-carry history

`FINDINGS.md` currently indexes eleven complete carry words in the original carry-history row (line 20). That remains a valid historical result, but it omits the stronger, accepted nine-word result now present in the scoped core.

Exact current source: [`DifferenceObservability__dc8ff21a6bd34973.lean`](https://github.com/taco-jpg/p196-algorithm/blob/10a173cb635fa8d03e357f454232816fc3e77609/proofs/DifferenceObservability__dc8ff21a6bd34973.lean#L248-L290).

- `DifferenceObservability.nine_carry_words_determine_pair_sums`: two admissible decimal pair words at the same initial width; equality of every carry at times 0 through 8, including the terminal carry at each current width; conclusion: equality of every initial pair sum inside the width.
- `DifferenceObservability.nine_carry_words_determine_next_integer`: two canonical ordinary integers at the same initial width, with the same complete nine-word carry history; conclusion: `Lychrel196.step n = Lychrel196.step m`.
- Neither theorem says the starting integers are equal, that nine observations are optimal, or that an orbit stays nonpalindromic.

The current source Git blob `d0727d391ee901ddaa782c218f493a23b8aadff3` exactly matches the module entry in [`ACCEPTED_BUILD.json`](https://github.com/taco-jpg/p196-algorithm/blob/10a173cb635fa8d03e357f454232816fc3e77609/proofs/ACCEPTED_BUILD.json). The registry gives historical source commit `0b14bd101430e16ab06a5a9c706f0eda0a83767e` and SHA-256 `60e724414ebd2bcbe590b0d61976147ef280eedfab6ff057d7cbdb7aeb0505d7`.

Small correction: add one current row, then label the existing eleven-word row historical or append a short cross-reference to that row. Do not silently change eleven to nine while leaving the old source links.

### 2. Index the accepted thirteen-prefix theorem for 196 as a restricted all-time result

`FINDINGS.md` includes the 739-prefix result but does not directly index the thirteen two-digit-prefix family in the current accepted core. The general warning that 196 is unproved is correct; readers should nevertheless be able to find this genuine all-time restricted-family exclusion.

Exact current source: [`TwoDigitMain__ebb172c52d262b85.lean`](https://github.com/taco-jpg/p196-algorithm/blob/10a173cb635fa8d03e357f454232816fc3e77609/proofs/TwoDigitMain__ebb172c52d262b85.lean#L116-L158).

`Agent113.TwoDigit.no_196_thirteen_arith (t k : Nat) (hpal : Palindrome (orbit 196 t))` concludes that `orbit 196 t / 10 ^ k` is not in `[10,20,32,40,41,60,64,65,76,80,81,82,83]`. This is equivalent to excluding palindromes with those thirteen leading pairs at every time. It does not exclude every palindrome prefix and does not prove that 196 is Lychrel.

The current source Git blob `460096733d4ac9145371d63421b400f56e7090d5` exactly matches the accepted module registry. The registry gives historical source commit `10eea4e977f864d605c97880f2347ba5f49d14bb` and SHA-256 `c2adf3a8a1d46b4b1ab3b792da77a820576abf762852a178011fda4bf0b45847`.

Small correction: one row alongside the nine-carry row, with the exact prefix set and explicit restricted-family limit. Avoid adding a numerical count of covered palindrome families by combining unrelated historical catalogues.

### 3. Make the evidence level of the added rows explicit

The retained [`batch2.md` independent AI-agent review](https://github.com/taco-jpg/p196-algorithm/blob/2eb05ef47671d6b1883e54fec9f6a4f8de9ed8f5/proofs/contributions/agent-1/consolidation-20261015/reviews/batch2.md) checks the carry statement and records its distinction between pair sums, next integers, and initial integers. It also describes the previously accepted thirteen-prefix closure included in the combined build.

The retained [`core-entrypoint/build/verification.json`](https://github.com/taco-jpg/p196-algorithm/blob/2eb05ef47671d6b1883e54fec9f6a4f8de9ed8f5/proofs/contributions/agent-1/consolidation-20261015/verification/core-entrypoint/build/verification.json) records:

- `status: PASS`, `mathematical_proof_check: true`;
- verified source commit `2e30535d65cb55b998e9b53332277135c293db38`;
- Lean 4.19.0, commit `6caaee842e94`;
- 38 module sources, 25 named endpoints, 3,491 audited theorem constants;
- allowed mathematical axiom union `[Classical.choice, Quot.sound, propext]`;
- `repository_wide_pass: false`, `catalogue_complete: false`;
- zero exit codes for the inspected `DifferenceObservability`, `TwoDigitMain`, and combined `ProjectAudit` commands.

The source hashes recorded for these modules agree with the registry. The current selected sources match their registered Git blobs. This establishes retained historical build/review evidence for these exact sources; it does not establish a fresh build of the reorganized tree. The registry's catalogue blocker remains open, and prior accepted scopes outside it are not withdrawn.

Small correction: a short shared evidence note under the proposed rows, rather than a new global claim that all current research is kernel checked.

### 4. Optional: add the other accepted supporting families by linking the existing precise checkpoint

`STATUS.md` already distinguishes the five core families accurately. Repeating its complete table in `FINDINGS.md` is unnecessary. A single link to its scoped evidence checkpoint would also expose the outer-map residue theorem, abstract boundary obstruction, and high-base first-hit classification while preserving their hypotheses.

One exact independent check for the high-base family was made: [`HighBaseFirstHit__077e109b12c152db.lean`](https://github.com/taco-jpg/p196-algorithm/blob/10a173cb635fa8d03e357f454232816fc3e77609/proofs/HighBaseFirstHit__077e109b12c152db.lean#L136-L149), Git blob `f76d32419588a695247d1fa835a44b31a787802e`, matches its registry entry. `Agent11HighBase.numeric_interval_first_hit` requires integer base at least three, `DigitBounds`, `PositiveLast`, every pair sum in `[b-1,b+(b-1)/2-1]`, and an outside pair sum at least `b`. It gives first positive palindrome time one precisely when every pair sum is `b+1`, otherwise two. Time zero may already be palindromic, and iteration continues after hits. This is not an unrestricted base-ten termination theorem, nor a formalization of every historical general-base normalization claim.

### 5. README status gap, deferred to its current owner

The current `proofs/README.md` is only a migration/replay entry point. It does not itself state the unresolved status of the two central questions or expose the principal scoped current results. A short status paragraph linking `STATUS.md` and the improved findings index would resolve this. Parent reported an active Agent #441 ownership claim for the README, so this is a handoff recommendation only; no README edit is requested outside that ownership resolution.

## Suggested small English addition to FINDINGS.md

> ### Scoped accepted-core update
>
> The source-pinned `consolidation-core` registry contains five distinct claim families; its complete accepted-scope census remains open. The following two current endpoints supplement the historical rows below.
>
> | Result | Exact scope and limit | Evidence |
> |---|---|---|
> | Nine complete carry words | For two admissible decimal pair words at the same initial width, equal complete carries at times 0 through 8 determine the initial pair sums. For canonical ordinary integers, they determine the next integer, not the original digit splitting. No optimality or palindrome-avoidance conclusion. | `DifferenceObservability.nine_carry_words_determine_pair_sums`; `nine_carry_words_determine_next_integer`; pinned source and accepted registry. |
> | Thirteen two-digit palindrome prefixes excluded for 196 | At every time, the orbit of 196 avoids palindromes beginning with `10,20,32,40,41,60,64,65,76,80,81,82,83`. Other palindrome prefixes are not excluded by this theorem. | `Agent113.TwoDigit.no_196_thirteen_arith`; pinned source and accepted registry. |
>
> The exact source blobs retain the recorded scoped Lean 4.19.0 build and independent AI-agent review. This documentation check did not run Lean and does not certify all source selected by the reorganization. See `STATUS.md` for the other three core families and their model or arithmetic hypotheses. Neither the specific 196 claim nor general decimal Lychrel existence follows from these results.

Use the pinned source/report links above in the implemented row; keep ordinary current navigation relative. Add a short note to the historical eleven-carry row that the current core improves the observation window to nine. Preserve the historical row's original references and statement.

## Additional exact source checks that did not identify a scope error

- `DecimalDelayBridge__83037365a26a750b.lean`: `candidate_safe_prefix` requires `k <= D`; `candidate_lychrel_of_finiteDelayBound` explicitly requires `FiniteDelayBound D`; the latter quantifies over every positive seed and finite first positive hit. `existence_or_unbounded_finite_delays` is a disjunction and supplies neither disjunct separately. The existing findings row retains these distinctions correctly.
- `Conclusion739__b4ff1ef7ce07de01.lean`: `SevenColumnKernel.Finite739.ancestry_bound39` and `no_196_739_palindrome` have the advertised all-width/all-time restricted-family types and no finite-check premise left in the final endpoint. The retained 739 acceptance record explicitly excludes main P196 and optimality claims. The existing 739 scope is correct. This audit did not recheck its 383-module build.
- `WholeWordBridge__77dd94b84e64292d.lean`: `actual_saturated_prefix_return` requires admissibility, width at least three, an actual prefix return, and `2*finalWidth = 2*initialWidth + time`; the divisibility conclusion is `time % 8 = 0`. The corresponding findings row correctly retains saturated width growth.
- The historical scalar finite-certificate README at baseline `2eb05ef...` still explicitly records an interrupted production build and unaccepted final numerical Lean endpoints. This audit found no basis to upgrade that historical row solely because draft Lean declarations exist.

## Limits

This was a focused endpoint and retained-evidence audit, not a complete catalogue census or full proof dependency review. Several old relative `contributions/...` links return 404 after migration; correcting their destinations belongs to the separate navigation audit. No unrelated accepted family has been downgraded because it is absent from the incomplete core registry. No external acknowledgment, independent current build, or main-branch action is claimed.

