# Independent review of exact quotient return restrictions

Source commit: `a0ae20330cbc1da2a98dc5721228d6590f8ba6da`. Source inspection found no unresolved semantic flaw in the contracts described below. The independent fresh 38-module build and full audit passed on the first run: all 39 strict Lean commands and the Python postchecks exited successfully, with no source drift or reused project object.

Reviewer: Agent #1 specialist `/root/research_status`, a separate specialist in the same session and GitHub account. I authored none of the four new mathematical sources. OuterRank was authored by the separate specialist `/root/research_status/numeric_bridge_review`; its execution and authorship are not mine. The stored-partition diagnostic was performed by `/root/research_status/cap4_existing_theorems`, again separately attributed.

## Exact source identity

The registry SHA256 is `59f1a4693cb3adb500f731af76175ba49bf7336a6aff265bd3905713c4f52a22`. Independent DFS of actual imports reconstructs precisely the registered 38-module closure of `Agent1PeriodicReturnCore`. All source hashes, Git blobs and import lists match the published commit and working files. The existing `CondensationBound` logical import resolves to the preserved flattened source `proofs/CondensationBound__7ecf1469405ab8d0.lean`, SHA256 `04bb2ec87115a532ca91d5d0d453c0062f6c46f030c1fe072ee649db000a0ef8`. No adapter or rewritten dependency is used.

| New module | SHA256 | Public theorem count |
| --- | --- | ---: |
| OuterRank | `e345ef2c5fe7734f64ead7e971f0ea8b807dfcc2d84e3d50625109871fe10477` | 6 |
| QuotientPath | `7735197ffa2a779c6ff1e0d76c2ed338ceb1afef75623adb7f2ce9a62c0d4e67` | 2 |
| ZeroPath | `078d6356f3eba5286f77d11e202df4759ecfd8e6473f5475d4ef443799732d0a` | 3 |
| ReturnCore | `271fbd1e8c5487e515420ccd145391c039f8dccab3b8f134cf31ff9b8dd7255f` | 3 |

The 163 named Agent1 public theorems in this closure comprise fourteen new and 149 prior theorems. Original module-origin declarations, including those in CondensationBound, are also included in the complete logical dependency audit. The closure imports the existing WidthPath definition and original ZeroCycle chain. It does not need the separate WidthLift or WidthNumeric modules.

## Contract and edge-condition review

1. **The path uses exact source states.** The unchanged `QuotientPath B H w N` supplies all coefficient bounds, period length four, and the literal successor equalities for B, H and w at each `i<N`. It is a finite relation on the interfaces, not an arbitrary graph walk. The new propagation theorem starts from all seven original `ValidPeriodic` fields and original outer-catalog membership, then propagates both through every `i≤N`. Endpoint N requires no separately supplied validity premise. For N=0 the statement returns precisely the initial premises.

2. **Projected edges retain their provenance.** `quotient_path_outer_edge` uses the original actual quotient projection at each visited source and rewrites its target by the path's successor equations. The clock is the same actual `rawGamma`, and the exceptional all-nine labels are exactly `leftEntry` and `rightEntry` of that state. The physical outside remains `(B++w).headD 0`; empty stored exteriors are permitted. No label is selected from an existential abstract graph path to stand in for an actual computation.

3. **The rank facts are local certificates.** `outerComponent` is a total lookup function, with original stored labels on catalog nodes and default label eight off the listed cases. `componentRank c = 132 - min c 131` is positive for every natural c, including values outside the stored partition. This prevents accidental use of rank zero at label 131. The finite checks prove weak rank decrease on each listed edge, a decrease of at least one whenever labels change, and the implication that an internal edge has label in `[8,129,130,131]`. The two node implications identify zero-phase label 131 and the allowed initial-phase outsides. These facts do not require rank injectivity or a proof that the labels are maximal SCCs.

4. **Every certificate row is tied to the existing graph.** OuterRank uses 59 node blocks and 59 edge blocks. Each finite `List.all` check is proved by kernel `decide`; the private `RankBlocksAll.flatten` induction combines them. The exact flattened blocks equal the original `outerCatalog` and `outerEdges` by `rfl`. Thus the local theorems apply to the unchanged actual lists and their full edge records. No compiler-trusted decision tactic, deleted graph edge, replacement ordering or SCC algorithm supplies this soundness. The separately published Python stored-partition counts are diagnostic evidence, not additional Lean hypotheses.

5. **The existing interval theorem is used with the correct length.** `quotient_return_component_constant` constructs `CondensationBound.RankCertificate` with weight one and `N+1` vertices. Its used transition condition `i+1<N+1` is exactly `i<N`, so it includes every edge and both endpoint states. A complete tuple return implies equal endpoint components, and the existing `component_interval` yields equality of every intervening component with the initial one. This theorem needs no `IntervalBound` and does not claim an interval residence-time bound. N=0 is allowed for this component-constancy result. The proof only uses the B and w parts of the return at this stage; the H return becomes essential when excluding the zero interface cycle.

6. **The zero path bridge reaches the original deterministic iterate.** `quotient_path_zeroStateOrbit` requires only the literal finite path and initial w equal to four zeros. The path's B/H bounds establish `rawPeriod_zero` at each used source, and the B/H successor equations identify the next pair with `zeroNext`. Induction proves the equality with `zeroStateOrbit (B 0,H 0) i` through endpoint N. No new full-validity, safety or exponent premise is introduced in that identification. Under original initial validity and N>0, the existing unconditional `zeroStateOrbit_no_cycle` then proves that even the B/H pair cannot return.

7. **Zero exclusion concerns full interfaces, not graph cycles.** The inherited ZeroCycle proof chooses one positive canonical seed, maintains its guarded literal lift under a hypothetical bounded cycle, and uses original digit-sum unboundedness. That unchanged source and all of its original dependencies are included in this fresh closure. ZeroPath transports its result to the exact finite path. The 27 abstract internal zero-phase edges remain in the catalog; no claim removes them or establishes termination or a palindrome hit.

8. **The positive return conclusion includes every state.** With N>0, component constancy makes the first actual edge internal. The finite rank certificate restricts its label to four possibilities; the original-valid zero no-return theorem excludes 131. The result gives one label c in `[8,129,130]` for the entire path, including i=N, and membership of every projected node in the literal filtered `returnCore` list. This is a necessary condition for return of all three interfaces B,H,w. Equality merely of their lengths, residues, outside values or projected nodes is insufficient. The exponent is not part of this tuple, and the theorem asserts no return existence or exponent behavior.

9. **The initial-phase corollary needs no separate catalog premise.** For `w 0 = [14,14,4,4]`, original validity supplies the physical outside bounds 1..18. The previously checked eighteen initial catalog rows give initial membership, so `quotient_return_initial_outside` concludes outside nine or ten using only the stated path, validity, phase, positive length and full tuple return. If B is empty, the physical outside is the first period coefficient 14; the theorem consequently excludes such a positive full return. It does not assert that outside nine or ten realizes a return.

No result proves SCC maximality, all-vertex reachability, arbitrary graph-path realization, a return in a surviving label, acyclicity of the constant-eighteen label, safety closure, a natural-exponent trajectory, an all-time ordinary orbit, palindrome avoidance, or a claim about 196. The numeric machinery appears only in the reused zero-branch exclusion, with its original positivity and canonical-realization obligations already present in the checked dependency chain.

## Preserved author runs

Author checks are incremental and separately attributed. OuterRank's probe, full module and origin audit passed; it reused pinned prior dependency objects. QuotientPath's first source compilation and audit passed. ZeroPath's first source compilation passed; its first audit failed under a small address-space cap, its second rejected an incorrect expected inventory count after checking the actual five theorem constants, and its third accepted the corrected complete inventory. ReturnCore attempts 001 and 002 failed on proof elaboration; the error-recovery placeholders in those failed sources are excluded from the accepted chain. Attempt 003 is the frozen successful source. The contribution retains all those source snapshots, logs, identities and receipts. None of these author executions substitutes for my fresh combined check.

## Independent execution

Build directory: `/workspace/p196-agent1-session-20261016/periodic-return-review-clean-001`. Exact executed driver SHA256: `ea8aa0cd57af0253df4cfb9b62fe8222cc80a37bad9098a0cd5beb33f29ff754`. The driver snapshots itself and all 38 source inputs before execution, uses only its fresh build directory for `LEAN_PATH`, and compiles with official Lean 4.19.0 commit `6caaee842e94`, executable SHA256 `92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023`. Every source and audit command uses `--trust=0 -j1 -DElab.async=false`, default stack, an 8-GiB address-space cap, and a 600-second timeout. No prior project objects are reused.

This execution uses the corrected comment-aware source scanner from the earlier Width wrapper recovery from the outset. The preflight scanner already passed on all 38 source files. The complete audit checks actual-origin theorem dependencies and safe-definition dependencies, rejects custom safe axioms, and inventories generated nonsafe compiler declarations separately. All 38 module compilations and `ReviewAudit` passed on their first attempt, in 278.938 seconds total. The complete audit checked 1,942 theorem constants and 566 safe definitions/opaques by actual module origin. The theorem axiom union is exactly `Classical.choice`, `Quot.sound`, and `propext`; the safe-definition union is `Quot.sound` and `propext`. All 163 named Agent1 public theorem types and axiom prints were checked, comprising fourteen new and 149 prior theorems. The original CondensationBound source contributes 55 theorem constants and seven safe definitions to the origin audit.

The four new modules contribute the following actual-origin inventory (including generated proof auxiliaries): OuterRank 133 theorem constants and 136 safe definitions; QuotientPath five theorems and no safe definitions; ZeroPath five and zero; ReturnCore nine and one. No theorem or checked safe definition depends on a forbidden axiom.

The separate compiler implementation inventory contains 12,146 nonsafe definitions: 12,111 cstage helpers and 35 unsafe recursion helpers with audited safe bases. It also contains 32 unsafe implementation axioms (13 original Lychrel, seven PhaseCatalog, seven OuterChoices, one CatalogOrder, two OuterCatalog, one ZeroState and one ReturnCore). There are no unsafe opaques or unclassified nonsafe definitions. These implementation declarations are explicitly inventoried and do not enlarge the logical dependency sets just reported.

There were no failed Lean commands, timeouts or wrapper failures in this fresh ReturnCore run. The earlier Width comment-scanner failure is not part of this run; its corrected scanner was used and snapshotted before this execution began. All 38 source identities were rechecked after completion against the published mathematical commit, working files, actual build inputs and archived compiled-source snapshots. The generated audit source and exact executed driver match their archived bytes.

| Evidence | SHA256 |
| --- | --- |
| Executed `replay.py` | `ea8aa0cd57af0253df4cfb9b62fe8222cc80a37bad9098a0cd5beb33f29ff754` |
| `clean-001/verification.json` | `afd2d832607ff5ed219ffc67274be20d18aa78f4959bcb8ba10080a5426ae971` |
| `clean-001/implementation-inventory.json` | `5c90e5aee2ebae47af6a250e3a7932ef9960700a39c7d1b49b4049d91ca228c2` |
| `clean-001/publication-source-receipt.json` | `d0d8be222e029591db7eb8ef19ae2340fd0f76ae58d061be00fe8f2b9d5851b3` |

## Separate parent execution

At the parent's request, I copied its separately completed canonical fresh 38-module/ProjectAudit evidence into `../verification/parent-clean-001/`. This is the parent's execution, not mine. Its original report records PASS, 1,942 theorem constants, source commit `a0ae2033`, and `source_tree_clean: true`. The original report, all 79 original manifest entries and original `FILES.json` are copied byte-for-byte; all 38 source inputs match publication and the current registry. The exact published canonical checker and a source-identity receipt are additional files, covered by a separate 82-entry `PACKAGE-FILES.json`. No compiled objects are packaged.

The canonical recorded commands do not explicitly specify `--trust=0`; that difference from my own 39 explicit strict commands is preserved. Its registry's historical pre-verification pending text also remains unchanged. The package identity receipt is `472553159cfe7cb14643d9196a2cd00d28dbce0a75db1d74e6868023181ca449`; its separate package manifest is `e41d7b693a1a25454e6763ea29adc61c89db1967663e8f38e396256e059083fe`.

Source inspection and both separately attributed execution reports support the precise necessary-condition statements above. No unresolved defect was found; the excluded claims remain excluded.
