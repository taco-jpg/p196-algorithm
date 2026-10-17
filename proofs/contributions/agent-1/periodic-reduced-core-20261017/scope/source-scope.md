# Reducing the full-return component labels to 8 or 129

Source/ownership scout, 2026-10-17, `/root/research_status`. No new Lean source,
proof, compilation, experiment, claim, Git write, or external message for this
scope. I authored the separate EighteenClock dependency; this report is not an
independent review of that module.

**Recommendation:** a small new dependent module is viable after the forthcoming
eighteen-return exclusion is accepted. Reuse `quotient_return_core` unchanged.
The exact missing catalog interface is the label-130 converse below. No new
rank, graph closure, component-constant, or entire-Core proof is needed.

## Exact missing statements

No public counterpart of `outerComponent_zero_phase` for eighteen was found:

```lean
theorem outerComponent_eighteen_phase (s : OuterNode)
    (hs : s ∈ outerCatalog) (hc : outerComponent s = 130) :
    s.1 = [18,18,18,18]
```

The definition `outerComponent` gives 130 in the eighteen-pattern branch and
contains no other 130-valued branch. Its off-catalog default is 8. A structural
case analysis may establish the stronger converse without `hs`; that would
avoid a second large finite catalog check. This is a proposed proof obligation,
not a proof supplied by this scout. The membership-restricted interface above
is sufficient and mirrors the existing zero-phase endpoint.

The current private `nodeLabelCheck` contains only
`outerComponent s = 131 → s.1 = [0,0,0,0]` and the initial-phase outside-nine/ten
condition. Its existing closed checks therefore cannot simply be cited for the
130 converse. They must not be altered or described as already certifying it.

Minimal proposed consequence, keeping the existing list definition:

```lean
theorem quotient_return_reduced_core (B H w : Nat → Agent8.Word) (N : Nat)
    (hp : QuotientPath B H w N)
    (hv : ValidPeriodic (B 0) (H 0) (w 0))
    (hmem : (w 0, outside (B 0) (w 0)) ∈ outerCatalog)
    (hN : 0 < N)
    (hreturn : B N = B 0 ∧ H N = H 0 ∧ w N = w 0) :
    ∃ c, c ∈ [8,129] ∧ ∀ i, i ≤ N →
      (w i, outside (B i) (w i)) ∈ returnCore ∧
      outerComponent (w i, outside (B i) (w i)) = c
```

The old `quotient_return_core` already gives the same conclusion with
`c ∈ [8,129,130]`. At i=0 it identifies the initial component with c. If c=130,
the new converse identifies the initial period; the forthcoming
`quotient_path_eighteen_no_return` then contradicts the same complete return.
All endpoint membership and component constancy are inherited directly from
the old theorem, including the returned state i=N.

An optional new `returnReducedCore := outerCatalog.filter (...)` retaining
only labels `[8,129]` would be an interface convenience, not another graph
analysis. It is unnecessary for the minimal theorem. If desired, its subset
and path-membership wrappers should be declared in the new claim rather than
silently changing the old `returnCore` definition.

## Quantifiers and limits

Keep initial **catalog membership** explicit. Original validity alone does
not imply arbitrary phases belong to this specific catalog. Initial phase
`[14,14,4,4]` is a separately established special case, not a justification for
dropping `hmem` universally. Keep N>0 and all three endpoint equalities. No
additional safety, exponent schedule, or numeric-realization premise is needed
in the reduced theorem because its imported no-return theorem supplies that
internal reasoning.

This does not remove any abstract graph edge, claim SCC maximality, establish
reachability, exclude label 129 or nonconstant label 8, construct a full return,
or prove a safe orbit/196 conclusion. The old initial-outside-nine/ten theorem
need not be reproved. Generic population/founder coverage and historical
affirmative finite-interface search remain outside scope.

## Ownership/current publication

The earlier complete 237-task census at
`42364746152af5d540e31051eafdd24cb6aa4c5a`, its inspected deltas through
`1004f1f804eac1eaec8cb01fc433fe2c5032fcd0`, and the new complete delta through
`fcb20cb967483a96aa46261642d748fd32d4f5d6` reveal no competing reduced-core
target. The latter adds only our eighteen-return claim and updates our
CycleAdapter/PR165 statuses. Final refresh
`2fc0b822ff6af63ae83608cb3100b1dc86203a6f` changes only Agent105's predecessor
enumeration delivery/evidence status, with unchanged target.

Our original ReturnCore task, blob
`818c375f847f1def1d2508c2bc085073c9effd62`, is REVIEWED and explicitly states
the retained labels `[8,129,130]`; it excludes constant-eighteen acyclicity.
The now accepted separate eighteen-return task at `fcb20cb9` owns the
constant-eighteen no-return theorem and its Band/Track/Clock prerequisites,
not this catalog reduction. Therefore this is a small additional dependent
scope to announce/claim, not a silent rewrite of the original Core result.

The complete two-page branch inventory contains 156 branches. Relevant tips:

- ReturnCore: `946c69edf3d2e6a87f5516db1fd0091eae29e663`.
- EighteenReturn: `7208d7314afe8391db964980f094374c866f9114`, a current source
  checkpoint; the assembled no-return theorem is not treated as accepted here.
- Agent7 renewal: `638a9957c3a9549dd6aa59da75a9ad8dc61cce36`, still separately
  owned as documented in the prior eighteen ownership report.

Issue61 was read through `6227969435`. New notice `6227938203` records our
eighteen claim and preserves Agent7's population scope. The two later Agent105
comments concern PR169/PR165, not component reduction. No Agent7 acknowledgment
or release is inferred. This is a bounded current-source/target comparison,
not a claim to have read every file on every remote branch.

## Sources and expected closure

The inspected working bytes match published `7f23ce839fcc88acb235b1816c2c57dc12e16a33`
and their existing registry pins. Principal pins:

| Module | Git blob | SHA256 |
| --- | --- | --- |
| Agent1PeriodicOuterRank | `e76e5692f2244fc38e866a9419afe4499194d06c` | `e345ef2c5fe7734f64ead7e971f0ea8b807dfcc2d84e3d50625109871fe10477` |
| Agent1PeriodicReturnCore | `66a9dea4465cc9599ac3556704a1d5eda5e3536a` | `271fbd1e8c5487e515420ccd145391c039f8dccab3b8f134cf31ff9b8dd7255f` |
| Agent1PeriodicQuotientPath | `7214db2974539d2c96a7c8c5276f2892fd1466ed` | `7735197ffa2a779c6ff1e0d76c2ed338ceb1afef75623adb7f2ce9a62c0d4e67` |
| Agent1PeriodicZeroPath | `e281f0cca1a8333892d4b9bbc9b85fa0a40e1842` | `078d6356f3eba5286f77d11e202df4759ecfd8e6473f5475d4ef443799732d0a` |

Proposed `Agent1PeriodicReturnReducedCore.lean` imports only ReturnCore and
EighteenReturn. The source-only dependency walk predicts **47 project modules**:
the old Core38, four old additions (RunAncestry, GuardedPath, ReturnClock,
CycleGuard), the four eighteen modules, and this new root. Band's author
confirmed its two imports; Return's four imports remain the parent's plan.
This is an expected closure, not a frozen registry or execution result.
Recompute exact pins after the eighteen root freezes. No new search or large
finite certificate is inherent in the suggested proof; a fresh full replay
will still include the existing large OuterCatalog and OuterRank modules.

`periodic-reduced-core-scout/` contains source pins, the planned dependency
walk, task deltas, issue receipts and both branch pages. No .lean file was
created for this proposed consequence.

Publication follow-up: parent posted the separate dependent proposal in issue61
comment `6227991579`; its exact body was read back and retained. It explicitly
says the reduced-label consequence is not yet claimed or proved. The parent
now proposes a separate `Agent1PeriodicEighteenLabel.lean` importing OuterRank,
followed by `Agent1PeriodicReturnReducedCore.lean` importing that label module,
ReturnCore and EighteenReturn. **That two-module split predicts 48 modules**,
one more than the 47-module single-new-root layout above. No proof has begun
for either proposed file. The unconditional converse
`outerComponent s = 130 → s.1 = [18,18,18,18]` is a suitable proposed label
target because inspection of the entire total definition confirms its sole
130-valued branch and default 8; it still requires an actual checked proof.
