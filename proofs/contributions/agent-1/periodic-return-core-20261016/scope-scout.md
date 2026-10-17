# After width projection: concrete return-core restriction

Source-only scout by Agent #1 specialist `/root/verification_plan`, 2026-10-16.
No new Lean proof, graph traversal/SCC calculation, experiment replay, claim,
Git command, or external message was performed. Reads included existing JSON
partitions and literal graph rows; their recorded SCC classifications were
not independently verified here. Only this report was written.

## Recommendation

The next useful negative theorem is a **specific return-core restriction for
the original 878-node period/exterior catalog**, not a new generic SCC theorem
or a repetition of its counts. Reuse the existing condensation certificate
soundness. Certify only the local component-rank inequalities and internal
edge exclusions needed to constrain a positive exact quotient return.

The concrete payoff is sharp at the original initial phase:

> For every finite exact quotient path starting from original `ValidPeriodic`
> data with period `[14,14,4,4]`, if its complete tuple `(B,H,w)` returns after
> a positive number of steps, its initial physical outside coefficient is
> **9 or 10**. More generally every state on a positive complete tuple return
> from this catalog lies in the same retained nonzero recurrent component.

The stored partition places `([14,14,4,4],9)` and
`([14,14,4,4],10)` in its 696-node nonconstant component, index 8.
The other sixteen initial exterior values are singleton components: values
1 through 8 occur in components 128 through 121; values 11 through 18 occur
in components 7 through 0. These are exact stored memberships, not newly
computed SCCs. The proposed theorem excludes sixteen of the eighteen
original initial exterior choices from a full return, uniformly over all
finite exterior and center contents. It says nothing about existence of a
return for the two survivors.

This is a reasonable queue item only if the parent wants that concrete
uniform exclusion. Merely formalizing the 132-component count or an
eventual-SCC lemma would add little after the current projection work.

## Precise proposed contract

Use the existing `QuotientPath B H w N`, together with:

```
ValidPeriodic (B 0) (H 0) (w 0)
(w 0, outside (B 0) (w 0)) ∈ outerCatalog
0 < N
B N = B 0 ∧ H N = H 0 ∧ w N = w 0
```

Define `returnCore` by the original stored components 8, 129 and 130:
the 696-node nonconstant component, the eighteen constant-nine nodes and
the eighteen constant-eighteen nodes. The desired conclusion is

```
∀ i, i < N → (w i, outside (B i) (w i)) ∈ returnCore
```

with all those projected nodes in one component. Its initial-phase corollary
is `w 0 = [14,14,4,4] → outside (B 0) (w 0) = 9 ∨ outside (B 0) (w 0) = 10`.
The return is equality of the complete tuple, not merely equality of its
width or its finite projection. The positive-step condition is essential.
No safety or exponent guard is needed for this formal quotient-path claim.
Any additional ordinary numeric trajectory interpretation must retain every
used exponent guard; it is outside this proposed certificate task.

The constant-zero component, index 131 with eighteen nodes, must be removed
using `zeroStateOrbit_no_cycle`, not by pretending its abstract edges are
absent. Full validity propagates by the existing quotient theorem. The
literal path restricted to zero is the existing `zeroStateOrbit`; equating
these iterations supplies the required interface to that no-return theorem.

The larger obligation advanced is the necessary-condition side of a finite
interface return: it separates genuinely recurrent candidates from 128
transient projections and excludes zero-period full returns. It does not
settle the surviving nonconstant, nine, or eighteen cases, nor show any safe
cycle or safe infinite orbit. It does not terminate the eleven retained
UNKNOWN trajectories.

## Reuse, first step and expected effort

`CondensationBound__7ecf1469405ab8d0.lean` already supplies
`RankCertificate`, `rank_antitone`, `same_component_of_equal_rank` and
`component_interval`. In particular, `component_interval` needs local rank
conditions and positive component weights; it does **not** require proving
a Tarjan/SCC algorithm correct or assuming a bound on time inside a cyclic
component. Use weight one for the component-separation argument.

First concrete action after a fresh claim: pin the stored component map and
a proposed rank, then kernel-check for every literal outer edge that rank
does not increase and strictly decreases across different components.
Separately check that every internal edge of a singleton component is
absent. The stored component numbering is only data; its suitability as a
rank has not been checked in this scout. No graph discovery is needed.

Then reuse the already proved actual quotient edge projection and
`component_interval` to keep a closed projected path in one component.
Apply the internal-edge exclusion for positive paths, and the existing
zero-period no-return theorem for the remaining zero component. Finally
read the eighteen initial rows to obtain the two-value exterior conclusion.

Expected mathematical effort is small to moderate; exact finite data
certification and resource management dominate. The current outer catalog
already required bounded-memory factoring. Prefer per-phase or per-component
finite checks instead of another monolithic decision over 878 nodes or a
7024-node SCC replay. The width product adds no new exclusion needed for
this result. No new generic graph, cyclic telescope, or decimal outer rule
is needed.

## Exact obstruction to a naive graph-to-return inference

The retained graph contains these literal rows, with `Z=[0,0,0,0]`:

```
(Z,9)  --clock 0--> (Z,18)
(Z,18) --clock 1--> (Z,9)
```

Thus its already specified width lift contains, for each residue `r`,

```
((Z,9),r) --0--> ((Z,18),r) --1--> ((Z,9),(r+1)%8).
```

Eight repetitions form a 16-edge abstract closed walk with eight overflows.
It satisfies width closure and the necessary equation `8*sumDelta=8` would
permit total exponent gain one. Nevertheless **no valid complete quotient
state with period Z returns after sixteen steps**, by the existing
`zeroStateOrbit_no_cycle`. This is an exact source-supported counterexample
to sufficiency of the phase/exterior/width cycle conditions. The little
abstract-walk composition is not a newly compiled theorem in this scout.

It is equally incorrect to delete the zero component from the projection
of an arbitrary infinite actual quotient path: `zeroStateOrbit_valid` and
`zeroStateOrbit_escape` allow and describe valid zero-phase paths whose
interfaces escape every fixed cap. A finite projection may recur while the
full interface grows. Likewise `CondensationBound.graph_path_vertices_le_rank`
still requires `IntervalBound`; no-zero-cycle alone does not supply that
bound on time spent in a projected cyclic component.

The old nonzero eight-clock witness `10101010` also survives: twice around
it closes width modulo eight. Neither a condensation certificate nor the
zero obstruction excludes that 696-component witness. Its finite interface
and center remain unprovided. The old `1000111` four-overflow rejection is
prior work and is not a proposed task.

## Exact sources and status

Primary inspection checkout: `/workspace/p196-agent1-width-20261016`.
Parent reports WidthPath source published at `80345e62`; exact file identities
below avoid relying on a moving checkout. The outer whole-catalog gate was
still WIP in the latest inspected issue message, despite checked local
arithmetic. Do not build accepted new results on an unverified root snapshot.

| File | Existing interface | SHA-256 or preserved blob |
| --- | --- | --- |
| `Agent1PeriodicPhaseCatalog.lean` | `rawPeriod_catalog_edge`, `rawPeriod_mem_phaseCatalog`, `quotient_valid_in_phaseCatalog` | SHA `44445a343635503c940ea125727d0bbb75bbf7dce24be62c28a660241363f9f9`; reviewed PR143 head `d299c930273adccb1d1ef8288c23c8c9ce8aeace` |
| `Agent1PeriodicOuter.lean` | `outside_bounds`, `quotient_outside_step` with actual last incoming carry | SHA `b30b54bce57542a649208c29900d511e9cc4b64429fb4a48f8da2a387d040678` |
| `Agent1PeriodicOuterChoices.lean` | labelled `OuterEdge`, `outerOutputs`, `outerOutputs_mem_of_phaseEdge` | SHA `9bd84fb0c22b2252fb71f0310fe763e6a07192ef0fb80299763459ab48fb76ad` |
| `Agent1PeriodicWidthPath.lean` | exact `QuotientPath`, signed finite telescope and equal-width clock result | SHA `e97afd670460a3df90e836360fed59797cb60b339ee63e42d51de826c46a2241` |
| `Agent1PeriodicZeroCycle.lean` | `zeroStateOrbit_no_cycle`; same-seed lift | SHA `ffea963ec5895ef493c289430d5a50e81ae241014d2baf8756beaa6996a23fbd`; published math `fc17722becfd671e349aeae21501d0fd5867dfb0` |
| `Agent1PeriodicZeroEscape.lean` | explicit `zeroStateOrbit_escape` | SHA `e1c9b9f90b5b2fddf3a4642b29030b1db7ab507d155a092facc713de5aaf0969`; published math `6145e2aa53861bdf6c7a820dd8ee78da9abc014f` |
| `CondensationBound__7ecf1469405ab8d0.lean` | generic rank and component interval soundness, already present | blob `6130c4c54acb9bf9f6f00932084eed66e3b45980`; SHA `04bb2ec87115a532ca91d5d0d453c0062f6c46f030c1fe072ee649db000a0ef8` |

The stored partition and rows come from `outer_filtered_graph.json.gz` under
`proofs/archive/source-trees/2eb05ef47671d6b1883e54fec9f6a4f8de9ed8f5/proofs/research/main_existence_attempt/continuation_pass/periodic_bulk_followup/`:
blob `c7bcc931f3cb36bd6845abeade0f7fd7b9723e08`, compressed SHA
`c3eb0a4bd4bc8e390d7681746e66300851035dff1b102412e2d14977ed1088e5`,
decoded SHA `cbd5c62ac2af58d0d0ce1cbb6f0cf9199ac49c75291d062179caf15f96e1ad50`.
Original METHOD blob `5c5f94c66d6c3adb0288b610f748fcbed32b115c` explicitly
states these are necessary graphs and the finite interface lift is absent.

## Prior results and ownership boundaries

Read-only GitHub API access succeeded. The complete coordination tree at
`b89dc1f20f61b54f09b197ddc242eaa901d34305` contained 174 direct task records,
without truncation. Relevant current records were read, including Agent1,
2, 6, 7, 107, 110 and 414. Issue61 was read through comment `6226428852`;
the latest Agent1 checkpoint was `6226425521`. No acknowledgment or posting
is claimed. A fresh claim check remains necessary before any proof.

- Agent2's `ExteriorCharge__52cbb237030a07b3.lean` (blob
  `3020c27a4f65aa5c59a76d2facecc6739fc25d00`) proves scalar exterior charge
  modulo nine and `full_return_arithmetic` under its explicit separate
  charge/width/rate premises. It is not the concrete four-site return-core
  theorem. Current Agent2 first-hit-eleven and overflow-fiber tasks are distinct.
- Agent110's `CertificatePhases` and `CertificateSaturation` (blobs
  `6921374766aadbc38bca86fc79d3a47b7d737400` and
  `e90960e42b165e7c328935406968ceaff0e409be`) prove restrictions for the
  original scalar six-phase certificate, including period at least 42 and
  saturated period divisible by 72. Their `SixPhase`, valid certificate,
  positive exterior and saturation hypotheses do not follow from membership
  in this nonconstant period-four graph. The current phase-six two-step
  exterior-return task remains claimed; preserve it.
- Agent107's active DFA/Horn closure task at `fe9e073a757267aa2f95c9fd4e3b10f6ab377353`
  is the finite-Horn-to-all-length language bridge. Existing
  `Sofic.projection_sound` (blob `7ba0129c374957c684324d8166fcef8488701605`)
  also already supplies a generic cyclic rank/projection argument. Neither
  should be reproved or presented as new. No concrete 878-node return-core
  instance was found in the inspected declarations.
- Agent414's active bulk-period premise discharge at
  `2a3ce996cc7e100f13c90e41cb8b4599360b7adc` concerns exact original scalar
  `bulkWord` period-six divisibility and its K exclusion. Its separate graph0
  certificate bridge and Agent415 review are also owned. They do not certify
  this period-four component partition.
- Agent7 owns zero/eighteen run-population renewal. The proposed result does
  not claim constant-eighteen acyclicity or any new run-lifetime theorem.
- Historical `periodic_interface_followup` remains expressly reserved by the
  original METHOD; no release or transfer was recovered. Its affirmative
  finite exterior/center lift/search remains excluded. The referenced sibling
  directory was absent at the inspected archived path, so no contents or
  release were inferred from that missing path.

No exact overlapping active target was found in these inspected records.
This is a scoped negative finding, not an exhaustive theorem-equivalence
claim. Required prerequisites remain: complete frozen outer certificate,
fresh narrow claim, local finite rank/internal-edge checks, exact path-to-zero
iteration bridge, and normal strict fresh build/axiom review. There is no
new accepted theorem or reserved scope from this scout.
