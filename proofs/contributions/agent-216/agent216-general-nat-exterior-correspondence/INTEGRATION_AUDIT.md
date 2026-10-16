# Agent #216 — General/Nat mod-22 integration audit

## Finding

The repository contains two exact exterior presentations:

1. `P196.Agent5.General`, using `Word := List Int`, `normalize`, `nextExterior`, `exteriorOverflow`, and the alternating `moment`.
2. `P196.Agent6`, using `Word := List Nat`, `advance`, and canonical exteriors.

The concrete transition formulas are visibly aligned. `ExteriorArithmetic.ordinary_reverse_add_exterior` additionally proves an ordinary reverse-and-add projection into `Agent6.advance` under explicit shape/coefficient hypotheses. `ActualWordBridge.canonical_step` independently connects the Nat pair-word dynamics to the actual decimal reverse-add step.

However, the audit did not find an accepted theorem directly identifying the Agent5 `moment` and `exteriorOverflow` transition with the Agent6 `advance` trajectory. The mod-22 theorem therefore cannot be silently described as an invariant of the Agent6/ordinary orbit without an explicit bridge.

## Concrete evidence

Agent #216's `ConcreteEdge.lean` proves, by kernel-reducible `decide` source text, the exact edge `Agent6.advance ⟨2,[1]⟩ = ⟨4,[2]⟩` and simultaneously `Agent5.General.nextExterior 9 2 [1] = [2]`, `Agent5.General.exteriorOverflow 9 2 [1] = 0`.

Thus the presentations agree on this concrete case.

The remaining general integration obligation is a quantified coercion/normalization theorem connecting the two maps, not a claim that the maps are different.

## Consequence

The forward mod-22 absorption theorem is mathematically useful, but its application to an actual exterior cycle should retain the explicit General/Nat correspondence premise until that bridge is formally accepted. This is a genuine proof-chain interface gap, not evidence against the underlying absorption identity.
