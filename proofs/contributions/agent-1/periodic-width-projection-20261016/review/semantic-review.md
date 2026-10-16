# Independent review of the width projection and finite-path accounting

Frozen mathematical source: `8f9249c855418eaadf9bb68bd645948d15777b5b`. Source inspection found no unresolved semantic flaw in the contracts below. The independent fresh 30-module build and complete audit passed. All 31 Lean commands exited zero; the Python wrapper subsequently failed on a documentation word, and its corrected postcheck passed against the unchanged compiled sources and logs. That wrapper failure and both driver versions are preserved, as detailed below.

Reviewer: Agent #1 specialist `/root/research_status`, a separate specialist in the same session and GitHub account as the authors. I authored none of these four mathematical modules. My execution is independent of the authors' incremental runs and the parent's canonical run. The specialist who authored Width and WidthNumeric is a separate child agent, `/root/research_status/numeric_bridge_review`; that work and its checks are not my authorship or execution.

## Source and dependency identity

The exact closure contains the previously reviewed 25-module outer product, the prior unchanged `Agent1PeriodicNumeric`, and four new sources. Actual-import reconstruction from all three registry roots—WidthLift, WidthPath and WidthNumeric—gives exactly 30 modules. Auditing only WidthLift would omit the path and ordinary-numeric roots; the independent driver imports all three explicitly. All registered source hashes and Git blobs match the published commit and working files.

| New source | SHA256 |
| --- | --- |
| `Agent1PeriodicWidth.lean` | `0ae4dbb296dd596f305c115b7626afc44f69d7fdc0de7d56140205e4bbff8be3` |
| `Agent1PeriodicWidthLift.lean` | `a3897a4d7dc58b2f33efb519be75ea5f7ef61b8e6c4602749c0249de52b49978` |
| `Agent1PeriodicWidthPath.lean` | `e97afd670460a3df90e836360fed59797cb60b339ee63e42d51de826c46a2241` |
| `Agent1PeriodicWidthNumeric.lean` | `31a0d8c78e64e8b1a0929fb808c5dbc40adfdf39db7248c58d0870d1eeee1706` |

Registry SHA256: `e6530e34648d564be293d737a0ff666f67f7054dd122ca9b9f9e77cdde4a1980`. Original executed full-build driver SHA256: `7c149b487737e775b9402244e115af62fdf751f476e3740e16e84ddab5a6cb33`; its exact bytes remain in `clean-001/replay.py`. The corrected portable driver is separately pinned below. The prior Numeric source remains `d3142b2a44bbe471df559e74bba993a9a663592b3bf04ce973e1ef94251873f7`; its original canonical and column-sum premises are reused without editing that dependency.

## Exact mathematical interpretation

1. **Width residue with minimal premises.** `widthResidue B H` is `(2*B.length+H.length)%8`, always below eight. `periodicWord_length_mod_eight` requires only period length four and permits exponent zero, empty interfaces, and arbitrary coefficients. Each pair of period bands contributes `8*k` to the list length. The quotient residue lemmas require precisely the existing coefficient bounds and length-four premise and reuse the signed `quotient_width_balance`. They impose no safety, full validity, ordinary realization or exponent guard because they are interface-width accounting.

2. **The finite lift is compositional.** `widthCatalog` pairs every original outer/phase catalog node with each residue in `List.range 8`. Its 7,024-node length follows from the checked base count, and `widthCatalog_nodup` proves distinctness using the base node distinctness and distinct residues. `widthEdges` similarly lifts each base edge across all eight residues, retaining its source, clock and optional carry labels while advancing the residue by `(r+clock)%8`. The proved number 11,664 is an edge-list length; this package has no edge-Nodup theorem. These counts do not verify archived traversal order, reachability, SCC decomposition or the realizability of every abstract edge.

3. **Membership and actual projection.** `mem_widthCatalog_iff` states exactly base membership and `r<8`. `widthProjection` uses the indexed period, the physical outside `(B++w).headD 0`, and the interface residue. The actual quotient edge theorem reuses the checked outer-product edge and matches its actual clock with `rawGamma`, then applies the exact residue-update identity. The optional all-nine pair remains the two actual phase entry carries. Empty stored exteriors are still handled by the inherited physical-head definition. `quotient_valid_in_widthCatalog` preserves all seven original validity fields and membership together; it does not replace unbounded exterior/center lists by a finite full state.

4. **The path relation is literal.** `QuotientPath B H w N` requires bounded coefficients, period length four, and all three exact successor equations at every used source index `i<N`. The next period equation is retained even though the width calculation itself only rewrites the outer and center successors. There is no extra boundedness/validity requirement at endpoint `N`, and no arbitrary abstract clock list is substituted for the actual source-state raw gammas.

5. **Signed telescope and zero transitions.** Writing `I i=2*(B i).length+(H i).length`, `C N=quotientClockSum B H w N` and `D N=quotientDeltaSum B H w N`, the proved identity is `(I N : Int)+8*D N=(I 0 : Int)+(C N : Int)`. `D` remains signed; it is the sum of literal `exponentDelta` values. The proof uses the prior local balance at exactly the used transitions. Both results include `N=0`, where the sums vanish.

6. **What equal endpoint widths imply.** The additional premise is only `I N=I 0`, weaker than equality of the full endpoint tuple. The conclusion is `8*D N=(C N : Int)`, `8 ∣ C N`, and `D N=((C N/8 : Nat) : Int)`. Divisibility concerns the actual raw terminal-carry sum, not `N`. No positive overflow sum is asserted. Without guarded natural exponents, this is formal signed interface accounting rather than a constructed ordinary or natural-exponent trajectory.

7. **Canonical input width.** `periodic_decimalLength_mod_eight` requires period length four and the original `DecimalDigits.Canonical n d` at the displayed word length. The original predicate states positive length, every in-range digit at most nine, nonzero leading digit, and equality of digit value to `n`. `decimalLength_of_canonical` therefore identifies actual ordinary decimal length without leading-zero padding ambiguity. This wrapper only identifies the input width: it needs neither coefficient bounds nor a column-sum realization, and allows `k=0` whenever the canonical premise holds. It supplies no chosen integer realization of the coefficient word.

8. **Ordinary successor width.** `periodic_actual_step_decimalLength_mod_eight` retains positive copy count `0<k`, bounds on all three coefficient blocks, the original canonical predicate, complete in-range column-sum equality for every input column, and length four. It composes the existing ordinary successor-width theorem with the interface residue identity using the same actual exponent-three terminal carry. For small positive copy counts this remains a width-residue identity. It does not assert that the whole successor equals the quotient word, nor provide that quotient's canonical digit representation. The prior whole-word quotient step still requires its original `k≥3` guard.

No theorem here establishes safety closure, positive-clock return, temporal-period divisibility, all-vertex reachability, arbitrary abstract-path realization, finite-interface return existence, an infinite ordinary orbit, palindrome avoidance or a result about 196. The finite catalog remains a necessary projection. The prior guarded/numeric representation bridges are needed for any stronger ordinary-orbit interpretation.

## Preserved author evidence

The four author directories preserve their actual incremental checks and source/object pins. They do not substitute for this review's fresh full closure. Width and WidthPath initially encountered an unsupported Lean memory flag, then address-space failures in audit processes; their successful audits used separately recorded RSS controls. WidthPath's early audit classifiers rejected generated compiler helpers before the final inventory policy accepted only separately classified implementations while retaining proof dependency checks. WidthLift preserves an earlier seven-export source, the runtime-inventory harness failure, and the final eight-export source adding node distinctness. WidthNumeric preserves a preflight failure due to missing older object hashes before Lean execution and its successful later increment. No failed author source or audit is silently converted into a pass by this report.

One historical WidthNumeric author note says the provisional registry had fifteen endpoints; that checkpoint predates the added WidthLift distinctness theorem. The final published registry has sixteen new endpoints, and the exact final source inventory contains 139 public theorem exports across the 30-module closure. The final package scope and this review use those final counts.

## Independent execution evidence

The build directory is `/workspace/p196-agent1-session-20261016/periodic-width-review-clean-001`. The driver snapshots all 30 source files and itself before executing, uses only the fresh project directory for `LEAN_PATH`, and compiles with official Lean 4.19.0 commit `6caaee842e94`, SHA256 `92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023`. Every command uses `--trust=0 -j1 -DElab.async=false`, default stack, an 8 GiB address-space cap, and a 600-second timeout. No prior project objects are reused.

All 30 source compilations and the generated `ReviewAudit` completed with exit zero, in 252.242 seconds total. The module-origin audit checked 1,695 theorem constants and 430 safe definitions/opaques. All 139 named public theorem types and axiom prints were checked: sixteen new exports and 123 prior exports. The theorem dependency union is exactly `Classical.choice`, `Quot.sound`, and `propext`; the safe-definition union is `propext`. No forbidden proof dependency, timeout, Lean command failure, source drift, or reused project object was found.

The environment inventory separately records 6,895 nonsafe compiler definitions: 6,864 generated cstage helpers and 31 unsafe recursion helpers whose safe bases were audited. It also records 35 unsafe compiler implementation axioms (13 original Lychrel, seven PhaseCatalog, seven OuterChoices, one CatalogOrder, two OuterCatalog, five WidthLift). No unsafe opaque or unclassified nonsafe definition remains. Those entries are not dependencies of the checked theorem or safe-definition constants; their existence is explicitly retained rather than misreported as absent.

After Lean completed, the original Python wrapper rejected the word `admit` in the WidthLift documentation sentence “No abstract edge is asserted to admit a finite-word realization.” This was a source-scanner false positive, not an accepted Lean error. `clean-001/postcheck-recovery-001/original-wrapper-failure.json` retains the actual exception and exact failed driver identity. The original build driver and all Lean logs remain unchanged.

The corrected scanner masks nested block comments, line comments, and string contents, while still rejecting forbidden tokens in code and unterminated comments/strings. Eight diagnostic controls passed. The separately executed `recover-postcheck.py` verified all 31 recorded exit codes and log hashes, all 30 publication/working/build/archive source identities, the compiler and generated audit source, and then executed only the complete corrected postcheck tail. No Lean process was rerun in that recovery. The successful postcheck produced `verification.json` and the complete implementation inventory. The corrected portable driver has not been presented as a second full build; its postcheck tail was actually executed in the preserved recovery.

| Evidence | SHA256 |
| --- | --- |
| Corrected portable `replay.py` | `bd888efc4d239a7cf41ae0fada2c3762c802f28896a8b5b8c37a27bc62fe52e3` |
| Executed `recover-postcheck.py` | `5771c4353706dcdd7753ca9419ca76c54b8f6804b4979efb44ebbf94543acf3d` |
| `clean-001/verification.json` | `ff8809cabb67eee4d0973fbfc9ccb825c0606a877b5fd688d61ed89617089d98` |
| `clean-001/implementation-inventory.json` | `13fce6586de4b477fd9325e463c51f8e77811963360c8b16578adf79d2d6146a` |

## Separate parent execution

At the parent's request I copied its already completed canonical fresh 30-module/ProjectAudit run into `../verification/parent-clean-001/`. This is the parent's execution, not mine. Its report records PASS, 1,695 theorem constants, and `source_tree_clean: true`; these original bytes and all 63 original manifest entries are preserved. The copied source inputs match all 30 published source hashes at `8f9249c8`. The original checker is archived with its published identity, and a separate 66-entry `PACKAGE-FILES.json` covers the original evidence plus packaging receipts. No compiled objects were copied.

The parent's recorded commands do not explicitly specify `--trust=0`; this distinction is preserved. My separate fresh run specifies that flag on every source and audit command. The parent's original registry metadata also retains the pre-verification “pending” catalogue-blocker text; it has not been rewritten to pretend that it was generated later.

Source inspection and execution found no unresolved defect in the stated contracts. The limitations above remain part of the result; neither build establishes the excluded ordinary-orbit or finite-return claims.
