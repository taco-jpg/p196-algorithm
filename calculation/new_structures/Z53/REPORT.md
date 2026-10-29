# Z53 independent census prefilter audit

**Status: PARTIAL (10/10 committed cell reports inspected; 0/10 uses a known-unsound prefilter; active and uncommitted long-seam MDD shards still have unresolved completeness hazards).**  
**Label: COMPUTED** repository/issue-history audit only. This is not a decimal Lychrel theorem.

## Scope and method

The audit targeted reported-complete T* cells and the filters that could falsely turn a finite search into an EXHAUSTED-NONE claim. It cross-checked the latest #475 DONE/ALERT and FEED/COMBINE history, #474 comments pages 18-25, the binding scope in docs/FOCUS_SWARM.md, and each committed cell report listed below.

| Committed report | Cell scope | Filter audit |
|---|---|---|
| W10/CELL_REPORT.md | Phase 0, U=(4,9,14), |J|=3–4, even C=2–12 | Direct 137,180-J enumeration; explicitly no mod-11 pruning. |
| W17/CELL_REPORT.md | Phase 0, U=(8,9,10), |J|=3–4, even C=2–12 | Exact centre-independent endpoint cone; no MDD or mod-11 pruning. |
| W26/CELL_REPORT.md | Phase 0, U=(9,4,14), |J|=3–4, odd C=3–13 | Direct full-J enumeration; explicitly no MDD or mod-11 pruning. |
| W38/CELL_REPORT.md | Phase 0, U=(9,16,2), |J|=3–4, odd C=3–13 | Q39 gates are applied only to odd C; complete post-gate J enumeration; no MDD. |
| W42/CELL_REPORT.md | Phase 0, U=(10,8,9), |J|=3–4, odd C=3–13 | Q39 gates are applied only to odd C; complete post-gate J enumeration; no MDD. |
| X05/CELL_REPORT.md | Phase 0, U=(9,6,12), |J|=3–4, odd C=15–23 | Direct enumeration of all 137,180 J words; no mod-11 or MDD pruning. |
| V16/CELL_REPORT.md | Phase 3, all 30 U3 rotations, |J|=3–4, every finite C | Direct 4,115,400 (U,J) search plus reset-cone proof; no MDD or mod-11 pruning. |
| agent-X11/CELL_REPORT.md (commit 22edb0b) | Phase 0, U=(9,10,8), |J|=3–4, even C=14–24 | Direct enumeration of all 137,180 J words with an independent digit-array engine; no mod-11 or MDD pruning. |
| X24/CELL_REPORT.md | Phase 1, all 30 U3 rows, |J|=3–4, both C parities | Full unfiltered 4,115,400 (U,J) product; temporary W9 damage is allowed; R02 MDD not used. |
| X24/U6_REPORT.md | Phase 1, U6=(17,14,17,1,4,1), |J|=3–4, both C parities | Direct 137,180-J local-collar scan with a proved centre cone; no odd-only modular gate. |

These are scoped endpoint obstructions, not global statements about the decimal Lychrel problem.

## Findings that affect search soundness

### 1. Q39's mod-11 gates are odd-centre-only

For even-length palindromic C, alternating-sum cancellation gives A(H C reverse(H))=0 identically. Therefore the odd-centre conditions A(U)=A(C) and 2A(J)+(-1)^|J|A(C)=0 cannot prune even-C candidates.

The canonical counterexample recorded by R07 is J=[5], C=[1,1], U=(9,2,16): it violates the odd-only congruences but the folded pairword has A(P)=0 and the required 120-edge overflow clock. This proves the unconditional prefilter unsound; it does **not** prove a full return. docs/FOCUS_SWARM.md explicitly flags R01/R02/R22 search pruning as needing the even-C branches retained. No completed short-seam report audited here uses the bad even-C filter.

### 2. Strict-W9 MDD is not endpoint-only completeness

S44's #475 summary (comment 6490088940) states that R02's recurrent J[0:2] pairs require strict W9 preservation at every phase and must not prune trajectories that temporarily damage and later restore W9. Thus the R02/V48 MDD is a filter for the strict-per-phase sublanguage, not a complete prefilter for the general endpoint-only condition W9(t=120)=W9(target). A census that discards all transiently broken W9 paths cannot claim completeness for the target epoch seam map.

V48's FEED (comment 6491005618) reports phase 9 counts of 12 recurrent pairs, 20 triples, and 31 quadruples, while phase-0 controls are 16/36/43. The exact R02/V48 transition artifact is reported absent from main (comment 6491116882), so an MDD-based census must reconstruct and publish the phase-tagged transition relation and source hash before claiming coverage.

### 3. Live phase-0 shard contract defect

AA10's initial phase-0 |J|=7–9 claim (comment 6492321857) assigned first-pair ranks s=0..11, which omits four states from the 16-state phase-0 control. AA10 explicitly retracted that contract (BREAK 6492969761) and corrected its claim to use the 16-state phase-0 universe (6492970680) before making any completion claim. AA02's later claim (comment 6492611613) ranks all 361 possible J[0:2] pairs and explicitly retains transient W9 defects; it is not part of this phase-count finding. COMBINE agent-602 (comment 6492465556) flagged incompatible shard ownership predicates across AA01/AA08/AA10/AA12 versus AA03 and a state-index convention issue for AA05. AA13 later verified that the proposed common owner `1+((s+u) mod 12)` is disjoint and covers all 480 `(s,u)` pairs for `s=0..15,u=0..29`, but its slice sizes are uneven: `[39,40,41,42,42,42,41,40,39,38,38,38]`, not 40 each. Unequal sizes are not a soundness bug if every shard uses the same owner predicate, but any scheduler/count check assuming 40 per slice is wrong. The exact phase-0 transition artifact remains absent from main, and the actual predicates across all claimers have not yet been reconciled; this defect was caught before a completed false result.

### 4. Other scope hazards

Q43's 257,093,987-state SCC symmetry exclusion is a p16 result, not a p12/m9 exclusion. FOCUS_SWARM.md also marks the R05 mod-101 cocycle and R09 emitter gate as not yet audited for use as hard global SAT filters. Q51 independently found the general Q03 overflow row `18 -> 9` with `cL:any` is false; its physical counterexample has `(cL,cU,dU)=(1,0,0)`, so the general row must require `cL=0` (Q51 commit `bfa09b0`). The Q51 note says the instantiated T* gate remains consistent because its physical `18 -> 9` gate has `cL=0`. Repository search found no audited census report or committed census code using the broader `cL:any` row as a filter. No committed short-seam report in the audited set uses Q43, R05, or R09 as a pruning source.

## Conclusion

No unsound prefilter was found in the ten committed cell reports inspected. The overall status is **PARTIAL**, not EXHAUSTED-NONE: the active long-seam census is not complete, strict-W9 pruning cannot stand in for endpoint-only completeness, and the phase-0 MDD shard contract needs source-grounded validation before any exhaustive claim. No all-time candidate or global no-go has been established.