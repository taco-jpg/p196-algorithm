# Z53 independent census prefilter audit

**Status: PARTIAL (8/8 committed short-seam cell reports inspected; 0/8 uses a known-unsound prefilter; active and uncommitted long-seam MDD shards still have unresolved completeness hazards).**  
**Label: COMPUTED** repository/issue-history audit only. This is not a decimal Lychrel theorem.

## Scope and method

The audit targeted reported-complete T* cells and the filters that could falsely turn a finite search into an EXHAUSTED-NONE claim. It cross-checked the latest #475 DONE/ALERT and FEED/COMBINE history, #474 comments pages 18-25, the binding scope in docs/FOCUS_SWARM.md, and each committed short-seam cell report listed below.

| Committed report | Cell scope | Filter audit |
|---|---|---|
| W10/CELL_REPORT.md | Phase 0, U=(4,9,14), |J|=3–4, even C=2–12 | Direct 137,180-J enumeration; explicitly no mod-11 pruning. |
| W17/CELL_REPORT.md | Phase 0, U=(8,9,10), |J|=3–4, even C=2–12 | Exact centre-independent endpoint cone; no MDD or mod-11 pruning. |
| W26/CELL_REPORT.md | Phase 0, U=(9,4,14), |J|=3–4, odd C=3–13 | Direct full-J enumeration; explicitly no MDD or mod-11 pruning. |
| W38/CELL_REPORT.md | Phase 0, U=(9,16,2), |J|=3–4, odd C=3–13 | Q39 gates are applied only to odd C; complete post-gate J enumeration; no MDD. |
| W42/CELL_REPORT.md | Phase 0, U=(10,8,9), |J|=3–4, odd C=3–13 | Q39 gates are applied only to odd C; complete post-gate J enumeration; no MDD. |
| X05/CELL_REPORT.md | Phase 0, U=(9,6,12), |J|=3–4, odd C=15–23 | Direct enumeration of all 137,180 J words; no mod-11 or MDD pruning. |
| V16/CELL_REPORT.md | Phase 3, all 30 U3 rotations, |J|=3–4, every finite C | Direct 4,115,400 (U,J) search plus reset-cone proof; no MDD or mod-11 pruning. |
| agent-X11 report (commit 22edb0b) | Phase 0, U=(9,10,8), |J|=3–4, even C=14–24 | Direct enumeration of all 137,180 J words with an independent digit-array engine; no mod-11 or MDD pruning. |

These are scoped endpoint obstructions, not global statements about the decimal Lychrel problem.

## Findings that affect search soundness

### 1. Q39's mod-11 gates are odd-centre-only

For even-length palindromic C, alternating-sum cancellation gives A(H C reverse(H))=0 identically. Therefore the odd-centre conditions A(U)=A(C) and 2A(J)+(-1)^|J|A(C)=0 cannot prune even-C candidates.

The canonical counterexample recorded by R07 is J=[5], C=[1,1], U=(9,2,16): it violates the odd-only congruences but the folded pairword has A(P)=0 and the required 120-edge overflow clock. This proves the unconditional prefilter unsound; it does **not** prove a full return. docs/FOCUS_SWARM.md explicitly flags R01/R02/R22 search pruning as needing the even-C branches retained. No completed short-seam report audited here uses the bad even-C filter.

### 2. Strict-W9 MDD is not endpoint-only completeness

S44's #475 summary (comment 6490088940) states that R02's recurrent J[0:2] pairs require strict W9 preservation at every phase and must not prune trajectories that temporarily damage and later restore W9. Thus the R02/V48 MDD is a filter for the strict-per-phase sublanguage, not a complete prefilter for the general endpoint-only condition W9(t=120)=W9(target). A census that discards all transiently broken W9 paths cannot claim completeness for the target epoch seam map.

V48's FEED (comment 6491005618) reports phase 9 counts of 12 recurrent pairs, 20 triples, and 31 quadruples, while phase-0 controls are 16/36/43. The exact R02/V48 transition artifact is reported absent from main (comment 6491116882), so an MDD-based census must reconstruct and publish the phase-tagged transition relation and source hash before claiming coverage.

### 3. Live phase-0 shard contract defect

AA10's phase-0 |J|=7–9 claim (comment 6492321857) assigns first-pair ranks s=0..11. That cardinality matches V48's phase-9 count, not the 16-state phase-0 control, so the stated shard omits four phase-0 pair states and is not completeness-certified until rebuilt from an exact phase-0 list/hash. AA02's later claim (comment 6492611613) ranks all 361 possible J[0:2] pairs and explicitly retains transient W9 defects; it is not part of this phase-count finding. Separately, COMBINE agent-602 (comment 6492465556) flags incompatible shard ownership predicates across AA01/AA08/AA10/AA12 versus AA03 and a state-index convention issue for AA05; overlaps/holes remain uncomputed, so those partitions are still provisional. This is an active claim-contract defect, not a completed false result.

### 4. Other scope hazards

Q43's 257,093,987-state SCC symmetry exclusion is a p16 result, not a p12/m9 exclusion. FOCUS_SWARM.md also marks the R05 mod-101 cocycle and R09 emitter gate as not yet audited for use as hard global SAT filters. No committed short-seam report in the audited set uses those conditions as a pruning source.

## Conclusion

No unsound prefilter was found in the eight committed short-seam cell reports inspected. The overall status is **PARTIAL**, not EXHAUSTED-NONE: the active long-seam census is not complete, strict-W9 pruning cannot stand in for endpoint-only completeness, and the phase-0 MDD shard contract needs correction before any exhaustive claim. No all-time candidate or global no-go has been established.