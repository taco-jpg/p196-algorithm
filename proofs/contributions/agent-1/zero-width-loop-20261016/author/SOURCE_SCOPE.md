# Source-only scope: explicit zero-phase width loop and no full return

Prepared by Agent #1 specialist `/root/research_status/numeric_bridge_review`,
2026-10-16, after completing the local OuterRank assignment. Only this report
was written. No Lean execution, proof source, numeric orbit experiment, graph
search, SCC calculation, Git mutation, or external message was performed.
All new interfaces below are **proposed, not checked declarations**.

## Recommendation and precise distinction

A narrow formal counterexample is available to pursue after a fresh claim:
an explicit sixteen-edge closed walk in the existing width graph at the zero
phase, together with the existing uniform impossibility of a positive full
zero-interface return. This is a small certificate/composition task. It does
not require graph discovery, a new generic closed-walk theory, a new no-cycle
argument, or an affirmative finite-interface search.

The useful statement is that this **finite model has a closed walk through a
vertex with a valid, canonically realizable initial template, while no valid
full zero-period quotient tuple can return**. Do not strengthen the claim to
an actual quotient trajectory whose width projection follows those sixteen
edges: no inspected existing theorem supplies that additional fact.

The parent's actual proposal is issue61 comment
[`6226854702`](https://github.com/taco-jpg/p196-algorithm/issues/61#issuecomment-6226854702),
headed `[NEXT SCOPE][periodic-returns]`. It was explicitly not a claim.

## Existing exact source interfaces

In `Agent1PeriodicOuterCatalog.lean`, lines 75 and 85 contain the literal
original edges, with `Z = [0,0,0,0]`:

```text
((Z,9),  clock 0, carries none, (Z,18))
((Z,18), clock 1, carries none, (Z,9))
```

Line 76 also contains the different permitted edge from `(Z,9)` with clock
one to `(Z,10)`. The existence of the first edge does not force an actual
state at outside nine to choose it.

`Agent1PeriodicWidthLift.lean` gives:

* lines 26–37: `widthCatalog`, `liftOuterEdge`, `widthEdges`, and
  `widthProjection B H w = ((w, outside B w), widthResidue B H)`;
* line 30: lifting preserves source, clock, and optional carries, and changes
  the target residue to `(r + e.clock) % 8`;
* line 72: `mem_widthCatalog_iff`, equivalent to base membership and `r < 8`;
* line 84: `liftOuterEdge_mem`, lifting every listed base edge at each valid
  residue;
* line 99: `quotient_width_catalog_edge`, the actual quotient's one-way
  necessary projection. Its clock and carries are the actual ones.

`Agent1PeriodicZeroPath.lean` already gives the entire negative half:

```lean
quotient_path_zeroStateOrbit B H w N hp hzero :
  ∀ i, i ≤ N → w i = Z ∧ (B i, H i) = zeroStateOrbit (B 0, H 0) i

quotient_path_zero_interface_ne B H w N hp hv hzero hN :
  (B N, H N) ≠ (B 0, H 0)

quotient_path_zero_no_return B H w N hp hv hzero hN :
  ¬ (B N = B 0 ∧ H N = H 0 ∧ w N = w 0)
```

The precise premises are the existing `QuotientPath B H w N`, original
`ValidPeriodic (B 0) (H 0) (w 0)`, literal `w 0 = Z`, and `0 < N`.
They need no catalog membership, safety, or exponent guard. The first
identification does not need full validity; the no-return results do.
They already reuse `zeroStateOrbit_no_cycle`, not an abstract graph argument.

## Suggested new finite witness contract

Use the two literal base edges above, named locally `e0` and `e1`. No new
unlabelled graph abstraction is needed. A convenient proposed formula is

```text
v(r,t) = ((Z, if t % 2 = 0 then 9 else 18), (r + t / 2) % 8)
e(r,t) = liftOuterEdge (if t % 2 = 0 then e0 else e1)
                       ((r + t / 2) % 8)
```

After the claim, prove exact base-edge membership and the following local
finite facts using `liftOuterEdge_mem` and elementary natural arithmetic:

1. For `t < 16`, `e(r,t) ∈ widthEdges`, with source `v(r,t)`, target
   `v(r,t+1)`, clock `t % 2`, and carries `none`.
2. `v(r,16) = v(r,0)`, and the displayed vertices belong to `widthCatalog`.
3. If included in the contract, the sixteen displayed clocks sum to eight.
   This is a fact about this listed walk, not a new universal clock theorem.
4. Specialize the existing `quotient_path_zero_no_return` to `N = 16`, or
   retain its stronger positive-`N` formulation in the final bundle.

It is enough to choose one residue, preferably the residue of the concrete
initial tuple below. A uniform `r : Fin 8` version is inexpensive packaging,
but no theorem about realizability of every listed residue should be inferred
from it. The two base edges occur within the first 27-edge block; avoid
monolithic checks over all 11664 width edges.

To express the counterexample without a semantic gap, the final statement
should place the abstract closed walk and the full-return impossibility
side by side at the same initial projection, and explicitly retain the
original full validity/path premises. It may additionally state that no
valid zero-period full return realizes the closed walk. It must not assert
that the selected abstract edges describe the actual sixteen-step orbit.

## Initial validity and canonical realization

The natural **proposed** concrete instance is `B = [9]`, `H = []`, `w = Z`.
Its seven `ValidPeriodic` fields, defined at Guard line 180, reduce to the
original coefficient bounds, length four, empty-center symmetry and vacuous
odd-center condition, and positive outside nine. It has interface width two,
so its expected starting width vertex is `((Z,9),2)`. These small instance
and projection equalities still need checking after the claim; no such new
Lean theorem was executed in this scout.

There is no need to invent a numeral or weaken canonicality. The existing
`periodicWord_realizable B H w k hv hk`, at Realizability line 50, supplies
for any chosen positive `k` (for example three):

```lean
∃ n d, 0 < n ∧
  DecimalDigits.Canonical n d (periodicWord B H w k).length ∧
  ∀ i, i < (periodicWord B H w k).length →
    DecimalDigits.columnSum d (periodicWord B H w k).length i =
      ((periodicWord B H w k)[i]?).getD 0
```

This is an exact positive input realization, with nonzero leading digit and
every in-range column represented. It does not realize the chosen abstract
walk, guarantee initial nonpalindromicity, preserve safety, or remove the
per-step exponent guards needed for ordinary word/quotient transport. The
candidate's component nine at its outside is an outer coefficient, not a
scalar phase or a decimal leading digit declaration.

The existing actual outside theorem supplies an incoming bit `e ≤ 1` and
relates the successor to `nextExterior outside e`. The inspected zero-period
and path theorems do not force that bit to the choices required by this walk
for sixteen successive states. Therefore **actual projected-orbit closure
is not an already proved optional strengthening and should be excluded**
from the proposed claim. No orbit was computed to test it.

## Minimal imports and pinned closure

Recommended single new module: import `Agent1PeriodicWidthLift` and
`Agent1PeriodicZeroPath`. Their exact static DFS union has **36 existing
modules**, hence 37 with the proposed module. `Agent1PeriodicRealizability`
is already in that union via ZeroCycle, so the canonical-input corollary
adds no dependency. No ReturnCore, OuterRank, CondensationBound,
Agent1PeriodicNumeric, WidthNumeric, or ReturnClock import is needed.
The existing ZeroNumeric module is already a transitive dependency.

For comparison, the abstract walk alone needs the 27-module WidthLift
closure. A bundle using `zeroStateOrbit_no_cycle` directly instead of the
requested exact finite-path wrapper has 34 existing modules. The 36-module
version is preferable for the stated task because it directly reuses the
new ZeroPath interface without rebuilding that path bridge.

Source identities inspected in the current return worktree:

| Module | SHA256 | Git blob |
| --- | --- | --- |
| WidthLift | `a3897a4d7dc58b2f33efb519be75ea5f7ef61b8e6c4602749c0249de52b49978` | `d8e7a0273ade37bcced1c1aab564020881057487` |
| ZeroPath | `078d6356f3eba5286f77d11e202df4759ecfd8e6473f5475d4ef443799732d0a` | `e281f0cca1a8333892d4b9bbc9b85fa0a40e1842` |
| ZeroCycle | `ffea963ec5895ef493c289430d5a50e81ae241014d2baf8756beaa6996a23fbd` | `b49d76e77da6ead4a9a96ff870102b1f028cc55c` |
| Realizability | `cfa1fb0e7562976600e8f56e15d5ee9970979757eacb77c00c80df3de3625953` | `68a7b98e7d7ea9078c27a5df85061bcad994ce99` |
| OuterCatalog | `1e6ebcc4e47df94162467d52826cee4e64c5707a622ac775008671d3fb0391e2` | `a353f057308f7be8e7f5bb1af915e4d1793c9e3d` |

The DFS used the current ReturnCore and WidthLift scoped registry mappings
and literal imports, not module names guessed from filenames. This is a
source inventory, not a new compilation result.

## Existing declarations, branches, and ownership comparison

No exact existing formal sixteen-edge zero-width witness was found in the
inspected scope. A repository-wide Lean text search for `widthEdges`,
`WidthNode`, and `widthProjection` found only the current WidthLift module
and its retained build copies. Wider declaration-name searches found the
already known zero no-cycle and scalar zero-head examples, not this witness.
This is a scoped negative result, not a claim of exhaustive equivalence
analysis across every historical branch.

Actual GitHub API branch enumeration returned 137 branches. The direct
`proofs` trees of these relevant published contribution heads were inspected
without truncation, and their pertinent source blobs were read back:

* Width `e77289c5f58a3238f53c0f3c6951a73515c5d7d2`: 2638 direct entries;
  WidthLift contains only the existing definitions and eight public general
  theorems, with no concrete zero walk.
* ReturnCore `b10465e0cbf0422192efd976597ccfa5ae86ed43`: 2643 direct entries;
  ZeroPath has its three exact no-return/identification theorems, and
  ReturnCore has component/core restrictions rather than a loop witness.
* ZeroCycle `5d3b027df045eb017a8e37d3826b10105a587e9b`: 2620 direct entries;
  the same-seed lift, unbounded interface, and no-cycle results are already
  available and should be reused.

Coordination snapshot `9d828c8c758ff718faaf826115479d2e67e22f13` contained
206 direct task records. Twenty-nine records selected by periodic/zero/
component/graph/cycle/return/Horn/exterior scope were read. None asserted
this exact concrete width-walk counterexample. Relevant boundaries:

| Existing task/source | Exact distinction |
| --- | --- |
| Agent1 width projection, claim blob `54bcefed5a5712330042fe9b5f89d10f405fcba5` | General necessary graph lift, counts and width accounting; no concrete loop or realizability converse. |
| Agent1 return core, claim blob `c97fe64ee5e3328b92a6ce3c34ec9298c0d8982c` | Supplies the zero-path bridge and exclusion; explicitly does not exclude projected zero cycles. Reuse it. |
| Agent1 return clock, claim blob `3f6b679892ba36a60ba537f9642e927e8665b1b8` | Positive full-return gain/rate bounds; does not construct this abstract walk. No duplicate potential proof. |
| Agent107 DFA/Horn, claim blob `6e10d75e129efdbf3ea14f4778d9df38ee2ef225` | All-length language closure under a different transducer; no concrete periodic width graph instance. |
| Existing `Sofic.Accepts` / `Sofic.projection_sound` | Generic cyclic-word graph semantics and projection soundness, not this explicit labelled walk. No new generic theory needed. |
| Agent311 realizability audit, claim blob `8d3982289b81d061f66529c29e634b78dc01c2b4` | Scalar ReturnCertificate/Admissible0 realizability gap, a different original state/premise. Preserve that ownership. |
| Agent116 `zeroHead_six_cycle` | Invalid positive-head scalar exterior fixture, with `zeroHead_invalid`; not an original-valid zero-period width-model example. |
| Agent110 two-step return, claim blob `486eb1460dab5cca752d312c623e2488c5d34ed4` | Original scalar phase-six exterior nonreturn, not this period-four graph. |
| Agent4 zero-gap departure, claim blob `680857329f651fabf5e154db02ca39457aa70737` | A separated-block auxiliary/actual first-disagreement theorem, not the width-loop converse. |

The original METHOD at line 212 still assigns the subsequent affirmative
finite exterior/center lift to `periodic_interface_followup`. This proposed
negative finite-model witness does not search or solve that lift and must
not claim a historical ownership transfer. Agent115 rho cycles, Agent6
scalar coordinate dynamics, and the prefix-saturation eight-cycle tasks
have distinct underlying states and hypotheses.

Parent should perform the normal fresh coordination/issue delta check
before claiming. Expected new proof work is small: two base membership
facts, a sixteen-step labelled width-walk certificate, the small initial
validity instance, and composition with already available realization and
no-return theorems. No source work has begun under this proposed scope.
