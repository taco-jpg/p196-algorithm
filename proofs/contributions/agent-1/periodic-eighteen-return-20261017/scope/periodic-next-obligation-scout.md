# Next substantive periodic obligation: the constant-eighteen return class

Source-only scout, 2026-10-17. Inspected worktree:
`/workspace/p196-agent1-cycle-adapter-20261017`, foundation
`3b018f7032b537cd7f6218fb9ad979842bb286d0`.
Coordination snapshot read:
`d0d45ac5ad277b914edce6d7173e45b7a93ac804`. Relevant Agent7, Agent418 and
Agent8 task records were unchanged at the later observed
`e3627129da61950b28aa51279d1b5770aaa5ca8e`.

No proof, Lean execution, graph search, new mathematical experiment, claim,
Git mutation or external message was performed. The proposed endpoint and
geometric bridge below remain obligations, not accepted results.

## Recommendation

Prioritize a **single-run obstruction to positive full-tuple returns whose
initial period is `[18,18,18,18]`**. This would remove the actual surviving
component label 130 from ReturnCore, leaving only labels 8 and 129 after
the already-proved zero exclusion. It is more substantive than another
checker wrapper and does not search for a positive certificate.

Proposed endpoint, in existing notation:

```lean
theorem quotient_path_eighteen_no_return
    (B H w : Nat → Agent8.Word) (N : Nat)
    (hp : QuotientPath B H w N)
    (hv : ValidPeriodic (B 0) (H 0) (w 0))
    (hw : w 0 = [18,18,18,18]) (hN : 0 < N) :
    ¬ (B N = B 0 ∧ H N = H 0 ∧ w N = w 0)
```

No safety premise should be needed. No condition should exclude empty B,
an exterior ending in eighteens, empty H, or H consisting entirely of
eighteens. The proof must establish the relevant maximal-run geometry;
those boundary cases cannot be assumed away.

The source supplies a plausible finite proof route below. Its missing work
is a specific static list/index bridge plus tracking one selected ancestry.
It does **not** require a theorem classifying every new run, unique founders,
global population coverage, absence of births, or eventual disappearance of
all eighteens. Those stronger premises are neither available nor needed.

## Why this is an existing unresolved return class

`Agent1PeriodicOuterRank.outerComponent` literally assigns constant zero to
131, constant nine to 129, and constant eighteen to 130. The checked
`quotient_return_core` in `Agent1PeriodicReturnCore.lean` retains `[8,129,130]`.
Only class 131 is currently eliminated by
`quotient_path_zero_no_return` in `Agent1PeriodicZeroPath.lean`.

The existing phase catalog has both labelled eighteen self-edges:

```text
([18,18,18,18], clock0, none) → [18,18,18,18]
([18,18,18,18], clock1, none) → [18,18,18,18].
```

These are necessary model edges, not a returned finite exterior and center.
No currently supplied full tuple cycle was found in the bounded inspected
sources. The new `quotient_cycle_actual_orbit` makes one supplied cycle a
single ordinary trajectory. `quotient_cycle_safe_positive_seed` still assumes
the complete cycle and every finite safety flag; it does not instantiate
them. Current inspected CycleNumeric SHA:
`4cbf4ee50c819e71ee09d108ab62fd703af1287507b969988a09e61b3fe2c527`
(blob `920e7a58f61eba4a913e12ac4d3dd92d0883ce41`). Its combined build/review
status remains root's responsibility; this scout does not assert acceptance.

The historical nonconstant candidate is a different class: the eight-step
phase/outside walk beginning `([0,9,18,9],17)` with clock `10101010`, traversed
twice to obtain length16 and clock8. It already satisfies the known eight-state
prefix condition. No finite B/H return is supplied. The eleven saved B=[17]
probes all become zero-phase by time26 and stop UNKNOWN at128; they are not
candidate cycles. This recommended eighteen obstruction does not pretend to
reject that saved nonconstant walk or resolve those capped probes.

## The precise missing single-run bridge

Write `E=[18,18,18,18]`, `W_k=periodicWord B H E k`, and
`q_k(i)=((W_k[i]?).getD 0)`. The left periodic band is exactly
`[B.length, B.length+4*k)`.

For `k>0`, a maximal eighteen run containing any position in that band has
a left endpoint determined only by the terminal eighteen suffix of B:

```text
a(B) = B.length - (B.reverse.takeWhile (fun x => x == 18)).length.
```

This is the proposed **static boundary lemma**, not an existing checked API:
if `RunAncestry.MaximalRun q_k W_k.length 18 a b`, and
`B.length ≤ i < B.length+4*k` and `a ≤ i < b`, then `a=a(B)`.
It also needs existence of one maximal run containing the initial band.
Only one finite run must be selected; no list of all maximal runs is required.

Why the statement covers the delicate cases:

- B empty, or B entirely eighteen: `a(B)=0`; no predecessor coefficient is
  demanded at a negative index.
- B has an eighteen suffix: the selected run starts inside B, rather than
  automatically at `B.length`. The last non-eighteen coefficient before that
  suffix supplies maximality on the left.
- H arbitrary, empty, or all eighteen: it can change the right endpoint and
  can join the two periodic bands into one central run. It cannot change the
  left endpoint of a run containing the left band. The proposed proof avoids
  an assumed right-endpoint formula and does not distinguish central and
  separated cases unnecessarily.

For a putative full return, use the finite guarded schedule beginning at
`k0=2*N+3`. Existing finite accounting and ReturnClock give
`kN=k0+G` with `G>0` and actual clock total `C=8*G>0`.

Starting from the selected maximal run `[a0,b0)`, track **its original
descendant** through the N actual steps. The displayed existing descendant
formula permits the following scoped endpoint estimates to be proved:

```text
a_t ≤ a0+t,          b0 ≤ b_t+t,
a0 + (actual overflow sum through t) ≤ a_t.
```

The first two follow because a single step advances the left endpoint by at
most one and retreats the right endpoint by at most one. The third uses that
every actual overflow advances the left endpoint by exactly one, while a
nonoverflow never moves it left. These estimates have not been formalized
in this scout and should be included explicitly in the new claim; do not
mistake them for an already exported theorem.

The fixed index `i=B0.length+N` is the useful anchor. Initially
`a0≤B0.length` and `B0.length+4*k0≤b0`. Since `4*k0>2*N`, the first two
estimates place i inside the nonempty tracked descendant at every step up
to N. Thus the existing maximality conclusion applies; no population or
birth-classification theorem is involved.

At time N the complete word is `W_(k0+G)` with exactly the original B,H,E.
The same i lies in its left periodic band. The static boundary lemma therefore
identifies its maximal descendant's left endpoint with the original `a(B0)`.
The third endpoint estimate instead makes it at least `a(B0)+C`, with C>0.
This is the proposed contradiction.

This argument uses the actual overflow from the full word. A phase label or
chosen abstract bit cannot replace it. It also does not infer persistence
merely from a long band appearing at both endpoints: tracking, nonemptiness,
and successor maximality must all be proved before the boundary comparison.

## Existing exact APIs to reuse

`RunAncestry__5f2702512ad8719e.lean` is the key dependency:

- `RunAncestry.MaximalRun` at line31 means `[a,b)` is nonempty, in range,
  constant c, and bordered by unequal coefficients unless at a word end.
- `RunAncestry.descendant` at line39 is exactly `(a or a+1,b or b-1)` without
  overflow and `(a+1,b)` with overflow, using the actual indexed carries.
- `RunAncestry.descendant_step` at line178 assumes full
  `FoldedDecimal.Admissible L q`, c=0 or18, and a maximal run. It gives exact
  survival on the old interval, maximality of every nonempty descendant,
  and no expansion/merging. Reuse this theorem unchanged.

Minimal periodic dependencies already available:

- `periodicWord_admissible` in `Agent1PeriodicRealizability.lean` gives the
  exact original Admissible predicate for every valid positive-exponent word.
- `quotientPathExponent_lower_bound` and `quotient_path_guarded_step` in
  `Agent1PeriodicGuardedPath.lean` supply all finite guards and literal list
  transitions; `quotient_path_valid` in ReturnClock supplies state validity.
- `quotientPathExponent_accounting` in the new CycleGuard identifies the
  guarded finite natural exponent with its signed delta. Combine with
  existing `quotient_return_clock_gain` to get the endpoint gain, or use the
  explicit CycleGuard schedule. A new all-time numeric proof is unnecessary.
- `stepWord_length_nextWidth` and `stepWord_getD_nextColumns` in
  `Agent1PeriodicZeroNumeric.lean:76,81` already bridge list transitions to
  the original indexed successor. They avoid reproving digit normalization.
- `terminalCarry_eq_carryIn` in `Agent1RepeatedBlock.lean:24`, original
  `IncomingCarry.carryIn_zero_eq_carry`, and `scan_carry_stable` in
  `Agent1PeriodicDigits.lean:53` identify the carry of each guarded W_k with
  the raw clock read at exponent3. Do not silently substitute that clock.

One may instead reuse `RunAncestry.track_invariant` from the mapped
AncestryExtinction module after proving the finite path's indexed iterPairs
correspondence. A narrower route is a local run-position recursion on the
already guarded word path, applying `descendant_step` each time and the
existing list/index bridge. This avoids adding an unnecessary whole-orbit
representation theorem. Root should choose the smaller checked dependency
closure after the scope is claimed.

## Pins and prior verification caveat

SOURCE_MAP identifies:

```text
RunAncestry__5f2702512ad8719e.lean
  SHA 6c8041050576a142949376818a2e37997031ce40b99a7908a763396ee702a9eb
  blob cdabce887a7f2ca952447f01bd99a2fe30855b81
AncestryExtinction__567be2f804ec7f4c.lean (Agent102 final source)
  SHA 4563ec3dffa0a69d3df3b3312eb783f835f76cacdd2261f9c88ed0b9f06d3c7e
  blob aa32de68b258f36361f56c102852f39bc21b29c5
AncestryExtinction__91bf7e70e989cdfe.lean (retained earlier reviewed source)
  SHA d0099b058b94f5edc083b9f6e3f38495ee6405f9d9feadeb75d88c39bc33a768
  blob ec56db105bc7d987d518eaa1c167fef1e40f4ea0
```

The two extinction files are not interchangeable by filename: the later one
adds `central_run_step`. The proposed left-boundary proof does not require
that extension. Original Agent102 README says author Lean-checked and awaiting
review; preserved Agent109 `review-agent102-ancestry/REVIEW.md` records an
independent PASS at source commit `f5f64336b1eb276f6d66b7b95f4cdd103789e2d3`,
with the unchanged RunAncestry SHA above and the **earlier d0099b** extinction
file. It rebuilt all three modules from empty, audited 26 exports, and records
standard axioms only. That historical review does not automatically cover
the later `central_run_step` addition. The new task still needs a fresh
combined strict build and full origin audit; none was run in this scout.

## Ownership and first action

Agent7's current `agent7-run-population-renewal-20261016` is CLAIMED. Its
target is successor-run partition into wholly born versus unique descendant,
temporal founder coverage, and eventual absence/birth equivalences. Its
exclusions explicitly say **“No reproof or new ownership of existing
no-merging, one-run lifetime, numerical representation or restart facts.”**
The recommended task must reuse those existing facts and own only the
period-four eighteen-band geometry and its one-selected-run return
contradiction. It must not prove a new generic population/coverage theorem
or assert births stop. Root should explicitly mention this distinction in
the fresh overlap notice/claim; no ownership clearance is inferred here.

Agent418 retains actual saturated-prefix multiblock compatibility and
balanced continuation. The saved 17/8 loop remains in that adjacent lane;
the proposed eighteen obstruction uses neither its controls nor a false
odd-input balance law. Agent8 lower3 remains untouched. The historical
`periodic_interface_followup` affirmative finite exterior/center search
reservation is preserved; no release was recovered. Current Agent102 affine
run decision/interval work is also distinct and is not needed here.

First action after an accepted narrow claim: implement and check the static
`a(B)` boundary lemma and single selected maximal-run existence against the
literal `periodicWord` indexing, including empty B and all-eighteen H. Then
transport `descendant_step` along the finite guarded path, retaining actual
clock equality and the scoped endpoint bounds before attempting the
contradiction. If that boundary bridge fails, preserve its exact failing
case and reassess; do not replace it with an assumed endpoint geometry.

No claim should be made to a no-return theorem for constant nine, all
nonconstant phases, arbitrary recurrence, or ordinary global extinction.
