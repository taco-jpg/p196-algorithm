# Nine-phase persistence: independent adversarial source review

Reviewer: Agent #1 specialist `symbolic_scope`, 2026-10-17. Source pin: `5e67f08231c1973cb4908c167dbd8e08b3ee50fa` in `/workspace/p196-agent1-eighteen-return-20261017`. All cited current source bytes were checked against that commit. Coordinated directly with `numeric_bridge_review` and read its sealed `periodic-nines-return-scope.md` (SHA256 `5fe1d321688192d172c1732c732fd9400fa92dc05daeb41b6b82c2bf816ad002`). No Lean execution, source proof development, mathematical experiment, math/Git edit, or external message occurred. This is statement analysis, not a newly checked theorem or a broad ownership claim.

**Finding:** a literal finite quotient path that starts and ends with four nines cannot leave that phase in between. A phase exit can only be to four zeros or four eighteens, and each is absorbing under the bounds already present at every used source. No counterexample to the proposed finite persistence statement was found. Unconditional nine persistence, even from valid input, is false.

## Minimal proposed interface

```text
(B H w : Nat → Word) (N : Nat)
(hp : QuotientPath B H w N)
(hw0 : w 0 = [9,9,9,9]) (hwN : w N = [9,9,9,9])
⊢ ∀ i, i ≤ N → w i = [9,9,9,9]
```

This phase-only implication needs neither `0<N` nor initial `ValidPeriodic`, exterior/center return, safety, catalog membership, an exponent schedule, or ordinary-number realization. N=0 is the trivial one-state case. In the parent's intended full-return application, `hwN` follows from the period component of the full endpoint equality. Initial validity and positive N remain needed by the separate existing cycle-realization theorem, not by this preliminary phase reduction. Input values beyond N are unconstrained and must remain irrelevant.

## Exact source interfaces and absorption boundary

- `proofs/Agent1PeriodicWidthPath.lean:17` defines the literal `QuotientPath`: bounds on B,H,w and length four at every i<N, plus all three successor equations. The phase successor is exactly `w(i+1)=rawPeriod (B i) (H i) (w i)` at line23. There is no `hp N` premise; induction must use source i<N and may conclude about endpoint i+1=N.
- `proofs/Agent1PeriodicNines.lean:34`, `nines_entry_bits`, bounds both **actual** entries by one from bounds18 on B,H. `rawPeriod_nines` at44 gives the constant block `replicate 4 (18-9*(leftEntry B+rightEntry B H [9,9,9,9]))`. The sum is0,1,or2, hence the output can only be eighteen,nine,orzero. `rightEntry_nines` at26 identifies the center scan as `terminalCarry H (leftEntry B)`; no freely chosen bit is being substituted.
- `proofs/Agent1PeriodicZeroPeriod.lean:50`, `rawPeriod_zero`, already states exact zero absorption for **every bounded B,H**, with no symmetry, parity, positivity, or nonempty-interface premise. Thus it covers every valid B,H and more. Its proof explicitly retains both actual clock cases. `zero_quotient_valid` at62 additionally preserves original validity, but that stronger wrapper is unnecessary for phase persistence.
- No standalone exported `rawPeriod_eighteen` was found in the inspected top-level periodic declarations. The narrow missing local specialization is `rawPeriod B H [18,18,18,18]=[18,18,18,18]` under `Bounded B 18` and `Bounded H 18`. Existing `rawPeriod_eq_phaseImage` in `proofs/Agent1PeriodicPhase.lean:63` applies because E has length4, is bounded18, and is not four nines. Its result uses the actual `rawGamma`, not an assumed external clock.
- `phaseImage` at `Agent1PeriodicPhase.lean:15` is the zipper of each period normalized with its stabilized carry. On E, the original stable digit bands are both four nines, so either actual clock displacement gives E again. `scan_carry_le_one` in `proofs/Agent1PeriodicDigits.lean:68` supplies the actual bit bound from B,H,E bounds. `rawGamma` is literally the exponent-three terminal carry at `proofs/Agent1PeriodicGuard.lean:164`; `zipperPeriod` at85 retains its displacement. This establishes the proposed eighteen absorption route for every bounded B,H, including empty and nonsymmetric centers; it does not require a previously valid ordinary realization. The specialization itself still needs formalization after the claim.

The existing finite catalog agrees with these rules: zero self-edges at `Agent1PeriodicPhaseCatalog.lean:86`, nine's eight carry-labelled alternatives at144, and eighteen self-edges at208. Those list entries alone must not be cited as actual transition completeness. The local exact formulas above avoid the catalog and its large proof closure entirely.

## Adversarial cases and exclusions

A valid nine tuple can leave nine immediately. Directly reading the existing carry definitions and nines formula:

| B | H | actual (leftEntry,rightEntry) | raw period |
| --- | --- | --- | --- |
| [] | [] | (0,0) | [18,18,18,18] |
| [18] | [] | (1,1) | [0,0,0,0] |

Both satisfy the original `ValidPeriodic` fields in `Agent1PeriodicGuard.lean:180`: bounded coefficients, length-four period, empty symmetric/even center, and positive outside `(B++w).headD 0`. These are source-level formula counterexamples to unconditional persistence, not executed experiments or full-return counterexamples. The empty center is especially important: it transmits the entering carry, so its two entries agree and the nine branch cannot stay nine there.

Under a returning-nine endpoint, an exit to zero or eighteen at any index≤N would persist to N using only the bounds at subsequent used sources, contradicting `hwN`. This uses phase absorption; it does **not** require the stronger zero/eighteen no-full-tuple-return theorems. A suffix starting at an exit need not have returned its exterior or center, so those no-return APIs would have mismatched hypotheses if used as a shortcut.

The resulting nine-at-every-state condition also forces `leftEntry(B i)+rightEntry(B i)(H i)[9,9,9,9]=1` at each i<N. That is a consequence of the literal phase equality and actual bit bounds, not a new independent carry choice. It does not identify the whole-word raw clock, which still depends on the original exterior scan. No temporal center decrease or obstruction follows merely from this mixed-entry condition.

Finally, nine presence concerns an odd pair coefficient of the represented input. It does not alone imply `safePeriodic=true`, because that Boolean classifies the **next output**. The first table row has alphabet only9 and `safePeriodic=false` by `Agent1PeriodicSafety.lean:16`. The proposed cycle-safety adapter must use successor-nine persistence and the exact ordinary representation/safety bridge, as the companion scout explains. Do not turn this phase-only result into unconditional safety preservation or a constructed safe cycle.

## Smallest useful scope and dependency boundary

The local work should consist of the missing bounded-eighteen absorption specialization, the three-successor nine classification if a named helper is useful, and finite returned-nine persistence. Existing ZeroPeriod/Nines/Phase/WidthPath supply the source interfaces; no OuterCatalog, OuterRank, ReturnCore, ReducedCore, RunAncestry, or new population theorem is needed. The companion source DFS identifies21 inherited modules for this phase-only union and32 for the intended complete cycle-safety adapter with CycleNumeric. These are source-derived counts, not new compiler results from this review. The precise final graph should be re-derived from actual authored imports.

## Exact relevant pins

All paths below are under `proofs/` at commit `5e67f08231c1973cb4908c167dbd8e08b3ee50fa`.

| Source | SHA256 | Git blob |
| --- | --- | --- |
| Agent1PeriodicNines.lean | b8aae1033e8e90c78f48888ea698e5d345c21e6b99970842dc5a9f3341cd193c | fc4b17311a291870b122ff97e3618fb7452e978e |
| Agent1PeriodicPhase.lean | 705c139614ffd4f9f20a305f7c4bff20059da0c7fa127ca180ff8a88397a51ce | ecb0816aa6411068956b9c746c61d267dcd11feb |
| Agent1PeriodicZeroPeriod.lean | 3761744f62cabdf25cf69f8e2990ce81eec9ac75cfb2273a5e80974304795a8a | abcff9926278c746d311ad24fc0c0d0a22c24a3a |
| Agent1PeriodicWidthPath.lean | e97afd670460a3df90e836360fed59797cb60b339ee63e42d51de826c46a2241 | ad3cee7e70fddbf0220c66313d8421e99f90678b |
| Agent1PeriodicDigits.lean | dc6cc1dadb74c4927f0635107fdc1eb62cebac3038dea4e97ad4229fc8703eab | 6a6f02ae17d7aaa8e728a6588edf080c9ffd7ad5 |
| Agent1PeriodicGuard.lean | 4ba3877f27250e066bbe19dd066b55fa667576281e8dc984334b9a9b82fcee91 | 7c62748625cecbc277ddd5e01ffb17671e4db7a8 |

No new theorem has been proved or compiled by this review, and no generic or historical search lane is claimed.
