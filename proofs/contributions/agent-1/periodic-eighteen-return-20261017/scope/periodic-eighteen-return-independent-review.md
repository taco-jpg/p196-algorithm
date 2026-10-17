# Independent source-only check: constant-eighteen full return

Reviewer: Agent #1 specialist `symbolic_scope`, 2026-10-17. Inspected source commit `7f23ce839fcc88acb235b1816c2c57dc12e16a33` in `/workspace/p196-agent1-cycle-adapter-20261017`. Read both requested scope/ownership reports and the exact original ancestry, carry, successor, admissibility, guarded-path, and return-clock statements. No Lean proof, mathematical experiment, source edit, claim, or external message was performed.

**Finding:** no semantic counterexample to the proposed endpoint or selected-run contradiction was found. The route is plausible with the stated boundary and tracking obligations. One tempting stronger compatibility statement is false: the two successor coefficient functions are equal only inside the next width, not globally. This must be respected in the run transfer.

## Exact reuse closure

Import the existing `Agent1PeriodicCycleGuard` plus original module alias `RunAncestry`, mapped to `proofs/RunAncestry__5f2702512ad8719e.lean`. This requires exactly **27 existing modules**, before the new application module(s). Every source byte was compared with the inspected commit. The complete topological list, flattened paths, original import aliases, SHA256 and Git blob pins are in `periodic-eighteen-return-independent-dependencies.json`. No new alias file was created.

The roots already inherit all needed APIs:

| Obligation | Exact existing interface |
| --- | --- |
| One selected original maximal run | `RunAncestry.MaximalRun`, `descendant`, `descendant_step` |
| Full admissibility at every used word | `periodicWord_admissible B H w k hv hk` |
| Literal finite exponent guard and word step | `quotientPathExponent_lower_bound`, `quotient_path_guarded_step` |
| Original validity at each state, including N | `quotient_path_valid` |
| Complete next physical width | `stepWord_length_nextWidth W` |
| In-range next coefficient | `stepWord_getD_nextColumns W i hi` with `hi : i < (stepWord W).length` |
| Exact indexed/list carry | `Agent1.RepeatedBlock.terminalCarry_eq_carryIn` then `IncomingCarry.carryIn_zero_eq_carry` |
| Actual exponent-independent clock | `scan_carry_stable` for positive exponent, then definition `rawGamma` |
| Guarded endpoint exponent | `quotientPathExponent_accounting` plus `quotient_return_clock_gain` |

Original ancestry pin: SHA256 `6c8041050576a142949376818a2e37997031ce40b99a7908a763396ee702a9eb`, blob `cdabce887a7f2ca952447f01bd99a2fe30855b81`. It imports only original alias `LychrelDigitSums`, already in the periodic closure. Neither AncestryExtinction variant, CyclePath, CycleNumeric, Safety, PhaseCatalog, OuterCatalog, nor a new ordinary-number realization theorem is needed. The existing generic list/index bridge happens to live in ZeroNumeric, whose unchanged import also brings ZeroPeriod; that inherited module is not being used to assert a zero period here.

## Required compatibility and actual clock

For `W_t = periodicWord (B t) (H t) (w t) (k t)` and `q_t i = (W_t[i]?).getD 0`, the source-step equation and existing bridges give exactly:

```text
W_(t+1).length = FoldedDecimal.nextWidth q_t W_t.length
forall i < W_(t+1).length,
  q_(t+1) i = FoldedDecimal.nextColumns q_t W_t.length i.
```

Transport the maximal run clause-by-clause using those bounds. Every run index is below b≤L'; the predecessor is in range when a>0; the successor boundary is in range only when b<L'. When b=L', retain the endpoint disjunction instead of demanding equality at b. A small application-specific transport lemma is enough; do not introduce a generic population theorem.

**Concrete warning:** at the admissible one-column word W=[18], the original definitions give stepWord W=[9,9]. Its zero-default coefficient at index2 is0, but `nextColumns (fun i => (W[i]?).getD 0) 1 2` is9: `extended` returns the terminal carry at every index≥L and reflected indexing uses truncated subtraction. Thus an unrestricted `funext` bridge is false. This example is a direct reading of the definitions, not an executed computation or a counterexample to the proposed no-return theorem.

At each used source t<N, establish:

```text
DecimalDigits.carry q_t W_t.length
 = Agent8.terminalCarry W_t 0
 = Agent8.terminalCarry (periodicWord (B t) (H t) (w t) 3) 0
 = rawGamma (B t) (H t) (w t).
```

The first equality is the original list/index bridge in the correct direction; the second uses `scan_carry_stable` after expressing the positive guarded exponent as r+1. The three coefficient bounds come from the literal path at t<N. This is not a selected graph label. `Admissible` also supplies carry≤1, which is needed to turn the nonzero branch of `descendant` into an advance by the actual bit. The tracked cumulative carry then equals the original `quotientClockSum` by its displayed recursive definition. No clock hypothesis is needed at endpoint N.

## Selected-run geometry and survival

Let E=[18,18,18,18] and a(B)=|B|-|takeWhile(=18)(reverse B)|. A narrowly scoped initial interface can be:

```text
k>0 -> exists b,
  MaximalRun (getD(periodicWord B H E k)) |periodicWord B H E k| 18 a(B) b
  and |B|+4*k <= b.
```

Its right endpoint may be defined directly by adding the initial eighteen-prefix length of the remaining suffix `H ++ pow E.reverse k ++ B.reverse` to `|B|+4*k`. This handles an empty/all-eighteen center and both bands joining, without constructing maximal intervals for arbitrary words. The separate uniqueness-of-left-boundary statement need only concern a maximal eighteen run meeting this explicit left band. An empty/all-eighteen B gives a(B)=0, so no predecessor coefficient may be required there.

For the selected descendant, prove the scoped estimates `a_t<=a_0+t`, `b_0<=b_t+t`, and `a_0+clockSum(t)<=a_t` before applying the nonempty-descendant conclusion at each step. The first two follow directly from the literal descendant alternatives; the third additionally needs the actual carry bit bound/equality above. With k0=2*N+3 and fixed index i=|B0|+N, `4*k0>2*N` gives `a_t<=i<b_t` through N. This justifies survival and whole-word maximality rather than assuming that a later eighteen band descends from the initial one.

At the endpoint, full B/H/w return and guarded accounting give kN=k0+G with G>0. The same i is in the final left band. Its maximal descendant has left endpoint a(B0) by the static lemma, whereas its tracked advance is at least the positive actual clock total C=8*G. This is the contradiction proposed by the scout. No hypothesis excludes empty B/H, a suffix of eighteens in B, or H joining the two bands.

There is **no need to prove every intermediate period equals E**. `descendant_step` tracks the selected eighteen run in any intermediate admissible word. Only the initial period and final full return are used to compare static boundaries. Avoiding an intermediate phase-stability lemma keeps the finite catalog out of the closure.

## Ownership and first implementation boundary

Use the unchanged original selected-run maximality/no-merging theorem. New helpers should remain scoped to the displayed periodic band, the already guarded finite path, in-range successor compatibility, and its one selected descendant. A generic all-word maximal-interval constructor, successor-run population partition, founder coverage, or population extinction is outside this application and remains the separate Agent7 lane described in the ownership report. The first concrete proof obligation is the explicit static boundary/existence lemma, followed by the in-range run transport and actual-clock identity. This review supplies no new proof or generic population claim.
