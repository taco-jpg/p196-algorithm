# Agent #14 — P196 commit, evidence, and progress audit

The strongest verified change is a complete two-sided picture of consecutive high-region returns in ordinary decimal arithmetic. The actual orbit admits at most three consecutive two-step returns to that region, and the explicit positive family `81*10^(m+7)-1` attains three returns without a palindrome through time six. The arithmetic correspondence is proved, not assumed. Agent #14 independently rebuilt both chains, the exact local return/safety criteria, and the ordinary-integer template transports.

The main remaining gap is an all-time argument: none of the audited constructions supplies a fixed finite positive seed with a proved infinite palindrome-free orbit, and the target-family exclusions do not cover every possible palindrome reachable from 196. These are precise remaining obligations, not a percentage estimate of distance to a solution.

## 1. Snapshot, baseline, and actual coverage

This audit began at **2026-10-15 05:03:30 UTC**, equivalent to **October 14, 2026, 22:03:30 PDT**. The initial default branch was `main` at `169c4c86d1dc9086e9a3754bc1c3d63408a8736f`. The principal later source snapshot was `eb893f01c3d9f6e46007178326d7b19f92529d3e`. A subsequent status-only refresh observed `main` at `4ffba5a60b6089075f6e3e4ab5952eb6bc46a4d7`; that entire later tree was not rebuilt.

The earlier Agent #14 artifact at `2a960162394400d910163636d304b96e5f7772f7`, `proofs/coordination/audits/agent-14/2026-10-15-initial-audit.md`, explicitly described a partial, source-inspected audit. It did not provide a pinned default-branch head or a fresh Lean run. Its concrete verification queue, rather than an invented complete baseline, guided this audit.

Discovery began with approximately 50 recent commit results, initial branch/PR listings, and coordination records. The discovered recent-commit window included committer timestamps from approximately 04:42:33 to 05:10:35 UTC. Dependencies were then followed backward and into later integrated contributions. This is not a claim that every diff in that discovery window, every branch, or every subsequent commit was semantically audited. The initial branch request returned 21 entries on page 1 with `per_page=100`; oversized PR/tree responses and a 300-file compare limit restricted broad inventories.

Commit ancestry was checked separately from timestamps. The safe-family source `9096791...` is an ancestor of initial `main` `169c4c8...` (ahead 22, behind 0). Initial `main` is an ancestor of the later `eb893f0...` snapshot (ahead 62, behind 0). Agent #105's release `4c8ae8a...` and Agent #109's transport source `d5c799f...` are also ancestors of `eb893f0...` (ahead 94 and 47, respectively; behind 0; merge bases equal to the source commits). These counts describe graph inclusion, not new mathematical results.

Author, committer, and audit times are different fields. For example, `d5c799f...` records author time **05:09:52 UTC** and committer time **05:10:35 UTC**. The safe-family commit records both as **04:55:46 UTC**. Neither time field alone establishes integration.

The exact selected inventory contains **24 distinct Lean source modules and 629 distinct public theorem/lemma identifiers**. Every selected source was rebuilt; every listed identifier received transitive axiom inspection. Repeated imports, reruns, and duplicate queries were deduplicated. This does not mean 629 new mathematical discoveries or 629 separately reconstructed semantic proofs.

The selected local builds used official **Lean 4.19.0**, commit `6caaee842e94`, with the bundled `Std` dependencies. No Mathlib cache or historical project objects were used. The final combined local replay ran from **05:50:02 to 05:52:54 UTC**. A separate GitHub runner repeated the exact inventory from **05:56:06 to 05:58:51 UTC**, run **38689475631**. Its complete axiom output was byte-identical to the local output:

`bbe77ab10d1788ec598f0282c458aaaaf3ce23420ee3ce1492078be306ab260d`.

All 629 queried dependency sets use only `propext`, `Classical.choice`, and/or `Quot.sound`, or no axioms. No `sorryAx`, newly introduced mathematical axiom, `Lean.ofReduceBool`, or compiler-trusted evaluation shortcut appeared. The five finite-witness results are axiom-free; all 70 family results use `propext` or `propext` plus `Quot.sound`.

Raw CI commands, source/object fingerprints, compiler output, theorem inventory, and the complete axiom driver were committed on the isolated audit branch at **`062e75ff3f0c60770ddad1a39f1ba82d971a53b7`**, under `evidence/ci-38689475631/`. This is selected-source CI inclusion, not a whole-repository accepted-build claim. The two replay environments still constitute one Agent #14 review, not two independent human or AI reviewers.

## 2. Newly established or newly verified mathematical conclusions

### Actual high-region return bound and its sharp nonpalindromic family

For canonical decimal digits `d_i`, let `q_i = d_i + d_(L-1-i)` denote mirrored digit-pair sums. The high region requires every `q_i` to lie in 9..18 and the exterior sum to be at least ten. A two-step return means membership again after two ordinary reverse-and-add iterations.

`Agent105.ActualHighReturn.numeric_high_returns_after_le_three` states: for every positive integer `n`, starting time `s`, and natural `R`, membership at every time `s+2j`, `j≤R`, implies `R≤3`. Thus the bound allows four high-region states at times `s,s+2,s+4,s+6`, but not a fourth consecutive return at `s+8`. It includes changing widths and widths one and two. The actual-control, second-overflow, canonical-representation, small-width, and checked 900-state rank obligations are discharged in the rebuilt chain.

The bound does not prohibit a later reentry following departure, and it does not prove that an arbitrary orbit reaches a palindrome. A proposed Lychrel construction cannot be dismissed merely because it fails to remain in this one region.

The matching family is already present at source `9096791b36bd8b18985328a6970a4abfc9eb4272`:

- `SafeHighFamily.seed_closed_form`: `seed m = 81*10^(m+7)-1` for every natural `m`.
- `SafeHighFamily.safe_three_returns_family`: positivity, high membership at times 0,2,4,6, and nonpalindromicity at times 0 through 6.

This is uniform in decimal width, but bounded in time. For `m=0`, the seed is **809999999**. The separate finite witness also proves nonpalindromicity through time seven and a palindrome at time eight, **3964546454693**. That observation concerns this member, not an unproved claim about every member's subsequent behavior.

The new audit contribution is fresh exact-source verification and interpretation of the family, not rediscovery of its already published theorem. The numeric upper-bound bridge is a genuinely newer completed obligation relative to the earlier partial audit.

Source locations: `proofs/contributions/2026-10-15-safe-high-return/{SafeHighWitness,SafeHighFamily}.lean`; `proofs/contributions/agent-105/actual-high-return/ActualHighReturn.lean`; `proofs/contributions/2026-10-15-high-return-rank-formal/HighReturnRank.lean`. Agent #105's source endpoint is pinned at `167eed51bc2ae014450626b9e5c0d3302a5ae5c4`; its reviewed release `4c8ae8a...` was merged through PR #15 at `250a555e228a0ffb0ceb1daa16b8bcfe85db5a8f`.

### Exact local return and two-output safety criteria

`Agent105.ReturnCriterion.numeric_high_return_iff` gives necessary and sufficient conditions for an actual two-step high return. The relevant second-stage carries are the carries determined by arithmetic, not unconstrained symbolic choices. The coefficient conditions, exterior threshold, and overflow condition are all explicit.

More directly, `Agent105.ReturnSafety.numeric_two_outputs_safe_iff_large_adjacent` says that, from a represented high-region integer, the first and second positive outputs are both nonpalindromes exactly when some adjacent source pair sums satisfy `q_(i-1)+q_i ≥ 28`, with `0<i<L`. There is no additional return premise. The theorem says nothing about whether the starting integer itself is a palindrome or about outputs after time two.

Agent #14 read the three source modules and independently rebuilt their entire dependency chain. This supplies the separate review/rebuild that the package's earlier publication record left open. Review evidence was posted to PR #15, comment **6185381242**. Owner acknowledgment and shared acceptance are not inferred from posting a comment.

Source: `proofs/contributions/agent-105/high-return-criterion/{LocalHigh,ReturnCriterion,ReturnSafety}.lean` at `eb893f0...`, matching the inspected criterion source checkpoint `8f846def03ec368d1de0fe20965f5e47f6172bc5`. These are local tools that may support a larger construction; they are not such a construction themselves.

### Ordinary-integer transport of the template obstructions

Agent #8's proofs exclude particular returns of canonical coefficient-word templates. Agent #109 now proves compatibility with the accepted ordinary decimal orbit, rather than leaving these as abstract word statements.

`Agent109.Compat.pairWord_orbit` identifies the actual integer pair-word sequence with the Agent #8 iteration. `Agent109.Endpoints.no_two_step_actual_template_return` then excludes the specified two-step return for a positive integer with positive initial and final outer gaps. `no_repeatable_six_step_actual_template_return` excludes the specified six-step return when both gaps do not decrease, in the six phases named by `Agent8.SixPhase`.

A specific remaining coverage improvement is visible: Agent #8's rebuilt word theorem covers all eight periodic even phases, while the current ordinary-integer six-step endpoint uses only the six-phase predicate. Transport of phases 6 and 12 is a concrete next target. It should not be described as already exported by the existing endpoint.

`Agent109.Compat.isLychrel_iff` is a correct equivalence with an all-time word-safety condition. No seed is shown to satisfy that condition. The distinction between an arithmetic bridge and an infinite construction remains essential.

Source: `proofs/contributions/agent-109/template-step-bridge/{TemplateStep,Compat,IntegerEndpoints}.lean` at `d5c799f1e55de0ed89f1b20d0e36cfe954aa6e31`, together with the three Agent #8 modules in `proofs/contributions/2026-10-15-agent8-complementary-bulk/`.

### Exterior obstructions: useful, but scoped

The rebuilt `P196.Agent6.capTwo_uniform_escape` proves that every canonical periodic exterior initially of length at most two exceeds that length at some time at most seven. `capTwo_coverage` supplies the finite decoder representation, removing a formerly separate coverage premise. This excludes the specified bounded exterior behavior; it does not establish escape for arbitrary exterior lengths or classify all ordinary integer orbits.

A newer one-step digit/value bridge, `ordinary_reverse_add_exterior`, is already present in `proofs/contributions/agent6-complementary-bulk/ExteriorArithmetic.lean`, source `3d5e304012c0136c87522146525d2a4c02b2a1fe`. Its source was inspected, but this later module was not included in the 24-module fresh-build inventory. Recommendations should target continued applicability or a full iterated correspondence, not pretend that no one-step arithmetic bridge exists.

Agent #2's `ExteriorCharge.lean` and Agent #5's `ExteriorClock.lean` both rebuilt successfully. Their modulo-nine closed-exterior constraints substantially overlap and should not be counted as separate discoveries of the same conservation mechanism. The stronger lower bounds of 18 overflows and period 36 require the stated parity, progress, or full-interface hypotheses. They are not unconditional lower bounds on arbitrary ordinary-integer cycles.

## 3. Progress specifically relevant to 196

The unchanged seven-column verifier was run against all five published certificates at source `f49d2fa2319d34e3f97fc94e49523c3ed3e056f4`. It exited zero after 11.277 seconds. Complete inverse-edge/rank checks, the finite short-source boundary checks, and its additional controls passed.

| Palindrome prefix | Certified ancestry-depth upper bound |
|---|---:|
| 217 | 23 |
| 218 | 34 |
| 620 | 12 |
| 739 | 39 |
| 777 | 25 |

The 739 certificate contains 58,501 nodes and 68,152 edges. Its written all-length correspondence, finite rank certificate, and exact check of the 196 orbit through time 39 yield the target-specific conclusion that the orbit never reaches a palindrome beginning with 739. This is not merely extrapolation from 40 observed orbit values: the ancestry bound is the separate all-time argument for that target family. The four other rows improve existing exclusions rather than discovering four additional prefix classes. State counts from separate certificates are not disjoint counts.

Verification level here is **executed Python certificate replay plus source review of the written mathematical bridge**, not a newly completed concrete Lean certificate. Agent #104's `ActualAncestry.lean` supplies the generic ordinary-integer composition, but `no_196_739_palindrome_of_finite_checks` still takes three explicit premises: complete checked rank rows, short-source exclusion, and checked initial targets. The inspected current certificate README still marks their complete assemblies as WIP. PR #18 was merged at `d807d4746bc87c32a98bb02c91e8ec6134655e65`; merging the package does not discharge those premises.

The named completion targets are `AllRows739`, `Initial739`, the complete generated short-source checks, and the final instantiation of `ancestry_bound39_of_finite_checks` / `no_196_739_palindrome_of_finite_checks`. The terminal pair-column prefix `(1,9,6)` in this argument is not the decimal digits of the starting number 196; its own pair word is `(7,18,7)`.

Source: `proofs/contributions/2026-10-15-seven-column-prefix/{verify_certificates.py,P196_739_Proof.md,certificate_739.json}` and `proofs/contributions/agent-104/seven-column-kernel/{ActualAncestry,TerminalObstruction}.lean`. The last two endpoint sources and the certificate README were inspected at `4ffba5a...`.

## 4. Important gaps, corrections, and non-results

**Stale summary, confirmed.** At both `eb893f0...` and the later inspected `4ffba5a...`, `proofs/README.md:26–35` still says three nonpalindromic high returns remain UNKNOWN. `proofs/FINDINGS.md:238–244` at `eb893f0...` repeats the obsolete status. The integrated, independently rebuilt family disproves that status label. This understates progress; it is not evidence of a false central theorem.

Discrepancy **A14-D01**, severity `REPORTING_OR_METADATA_ERROR`, is recorded in `DISCREPANCY-01.md`, source audit commit `319326564b367de55748c57de78cc9e35db3e52c`. The owner was notified through issue #1, comment **6185177497**; Agent #15 was notified through the actual coordination task. No acknowledgment or corrected overview was observed in the subsequent checks. Preserve the original unsafe witness as historical evidence; add a supersession link to the later nonpalindromic witness and family. The old rank-only package's lack of an arithmetic bridge remains literally true for that old package; cross-link the new Agent #105 package instead of silently rewriting its history.

**Scalar 659/94/98 remains unaccepted.** `ScalarHierarchy.finite_root_bound` and the wrappers in `ScalarBound.lean` require all production finite row checks. The latest inspected issue #13 checkpoint reports `JobData0–7` passed and original `JobData8` active, but no accepted production `JobChecks` or numeric endpoint. Agent #9's faster table-refactoring experiment is still experimental. This audit did not execute that large build or independently verify the performance comparison.

The actual chain to finish is the production `JobChecks` set → `ScalarHierarchy.finite_root_bound` → `RootBridge.certificate_of_finite_root_bound` → `ScalarBound.wide_periods_le_94` / `periods_le_98` / `canonical_periods_le_98`, followed by the final transitive axiom audit. Agent #103 retains primary completion; Agent #9 explicitly accepted independent replay. These are existing roles, not assignments made by this audit.

**Historical acceptance levels remain separate.** Old compiler-trusted certificates retain their historical evidence labels. This audit's selected new proofs meet the stricter ordinary-kernel standard; it does not retroactively pretend that every older package met it. Source inclusion on `main`, a successful selected rebuild, current CI membership, shared acceptance, semantic review, and external peer review remain different facts.

**Self-correction retained.** An early audit checkpoint loosely suggested that some family theorems were axiom-free. The complete output shows all 70 use standard axioms; it is the five witness theorems that are axiom-free. `EXPANDED_REBUILD.md` explicitly records this correction. The accepted standard-axiom conclusion is unchanged.

## 5. Dependency bottleneck and priorities

For the specific orbit of **196**, a useful route is: canonical arithmetic → sound finite abstraction → concrete rank/initial/boundary instances → target-family exclusion → coverage of every remaining possible palindrome family. The current 739 result advances one target-family exclusion, not the final coverage step. The most immediate formalization target is its three concrete kernel instances, while preserving the already proved generic bridge.

For **existence of some finite positive decimal Lychrel seed**, the route is: a realizable finite seed → a family or invariant preserved under every ordinary reverse-and-add step → incompatibility with every palindrome → an all-time theorem. Canonical realizability and exact local transitions are now much better supported. A closed all-time invariant, or an equivalent induction/return construction with every premise discharged, remains absent from the audited chains. The high-region upper bound removes the simplest perpetual-high-return approach; a broader construction must explain behavior outside that region.

The most useful immediate actions are therefore concrete:

1. Finish Agent #104's complete rank-row, initial-target, and short-source assemblies, then instantiate the ordinary 739 endpoint without finite-check premises.
2. Complete the existing Agent #103/Agent #9 scalar row-check chain; validate any source refactoring against exact tables and unchanged production proofs before adoption.
3. Extend `Agent109.Endpoints.no_repeatable_six_step_actual_template_return` to the existing all-eight-phase word theorem, particularly phases 6 and 12; separately audit applicability of the newer Agent #6 arithmetic factor across iterations.
4. Correct the two stale overview statements and explicitly record the accepted-build target for each completed package. Acknowledgment of the new Agent #105 independent review should be recorded rather than assumed.

These recommendations do not reassign research ownership. A rolling queue also retains unreviewed Agent #101/#106/#107/#108 contributions, later Agent #102/Agent #109 changes, and newer branch commits outside the pinned selected-source inventory. Their commit messages, declaration counts, or PR descriptions were not promoted to verified conclusions.

## 6. Deliverables and limits

Owned branch: `audit/agent-14/20261015T050330-rebuild`.

Owned report path: `proofs/coordination/audits/agent-14/20261015T050330-rebuild/`.

The report directory contains the snapshot, independent rebuild checkpoints, discrepancy note, evidence ledger, reproducible source specification, audit scripts, and committed CI raw evidence. `reproduce/source_spec.json` records every selected source path/hash and the hash of the exact 629-identifier inventory. The replay requires a fresh output directory and the pinned Linux Lean compiler; it fails on a changed source, missing result, duplicate identifier, or forbidden axiom. The declaration scanner is explicitly reused from the reviewed Agent #105 checker; the separate execution orchestration and final output parser are retained, not advertised as an independent theorem prover.

The delivered archive additionally retains original local-session commands, logs, failed/interrupted-attempt records, audit drivers, complete local execution metadata, selected source copies, and checksum inventories. Runtime installations, compiled objects, caches, and redundant dependency trees are omitted as reproducible infrastructure.

There was no subagent launcher, direct control over other sessions, or external peer review. Local Git cloning initially failed because DNS was unavailable; exact source and runtime artifacts supplied by the connected GitHub route enabled actual execution. All 2,695 manifest entries in the older proof-tree artifact and all 194 entries in the later selected-source artifact matched their recorded file hashes and Git blob identities. These integrity checks are not mathematical coverage counts.

This is a completed **selected-source audit checkpoint with an explicit remaining queue**, not an exhaustive repository audit or a claim that every active branch is integrated. Later commits remain outside the declared coverage.
