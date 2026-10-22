import P196.Agent104P620Witness.ActualPrefix

/-!
# Unguarded enrichment of the forward prefix abstraction gains nothing (sprint agent 03)

The forward prefix abstraction (`SevenColumnProjection.forwardPrefix`, used by
`Agent124.Forward`) moves a width-`k` word `w` to `forwardPrefix w e` for either
inner carry `e ≤ 1`.  A natural idea is to *enrich* the abstract state with extra
196-specific information `x : X` — the residue mod 99, the width mod `m`, the
time mod 6, the inner carry used on the previous step, … — updated along each
abstract step by a function `δ x w e`.

This file proves that such an enrichment can never exclude a word that the plain
forward closure contains, *whatever* `X` and `δ` are, as long as the update never
blocks a carry choice (no guard).  Every update used in practice for residues,
widths and clocks is of this form: it depends only on the previous value, the
word and the carry (e.g. through the overflow bit `(highDigits w e).1`), and it
does not forbid either carry.

Statements:
* `ereach_proj`, `reach_lift`, `proj_iff`: the words of the least enriched
  invariant are exactly the words of the least plain invariant `Reach`;
* `enriched_invariant_covers` / `no_new_exclusion`: any enriched forward-closed
  set containing the start pairs every `Reach`-word with some extra value, so a
  word it excludes is already outside `Reach`.

Nothing here is about 196 specifically, about palindromes, or about actual
orbits; it is a statement about the abstraction only.
-/

namespace Sprint.Agent03

open SevenColumnProjection

/-- Words reachable from `w0` under the forward prefix map with carries `0` or `1`. -/
inductive Reach (w0 : List Nat) : List Nat → Prop
  | refl : Reach w0 w0
  | step {w : List Nat} (e : Nat) : e ≤ 1 → Reach w0 w → Reach w0 (forwardPrefix w e)

/-- Enriched reachability.  The extra component is updated by an arbitrary
function `δ` of the previous extra value, the current word and the carry; no
carry choice is ever blocked. -/
inductive EReach {X : Type} (δ : X → List Nat → Nat → X) (w0 : List Nat) (x0 : X) :
    List Nat → X → Prop
  | refl : EReach δ w0 x0 w0 x0
  | step {w : List Nat} {x : X} (e : Nat) : e ≤ 1 → EReach δ w0 x0 w x →
      EReach δ w0 x0 (forwardPrefix w e) (δ x w e)

variable {X : Type} {δ : X → List Nat → Nat → X} {w0 : List Nat} {x0 : X}

/-- Projection: an enriched-reachable state has a plainly reachable word. -/
theorem ereach_proj {w : List Nat} {x : X} (h : EReach δ w0 x0 w x) : Reach w0 w := by
  induction h with
  | refl => exact Reach.refl
  | step e he _ ih => exact Reach.step e he ih

/-- Lifting: every plainly reachable word occurs in some enriched-reachable state. -/
theorem reach_lift {w : List Nat} (h : Reach w0 w) : ∃ x, EReach δ w0 x0 w x := by
  induction h with
  | refl => exact ⟨x0, EReach.refl⟩
  | step e he _ ih =>
      obtain ⟨x, hx⟩ := ih
      exact ⟨δ x _ e, EReach.step e he hx⟩

/-- The least enriched invariant projects exactly onto the least plain invariant. -/
theorem proj_iff (w : List Nat) : (∃ x, EReach δ w0 x0 w x) ↔ Reach w0 w :=
  ⟨fun ⟨_, h⟩ => ereach_proj h, reach_lift⟩

/-- `Reach` is contained in every plain forward-closed set containing the start. -/
theorem reach_sub_invariant (T : List Nat → Prop)
    (closed : ∀ w e, e ≤ 1 → T w → T (forwardPrefix w e)) (init : T w0) :
    ∀ w, Reach w0 w → T w := by
  intro w h
  induction h with
  | refl => exact init
  | step e he _ ih => exact closed _ e he ih

/-- Any enriched forward-closed set containing the start state covers every
plainly reachable word with at least one extra value. -/
theorem enriched_invariant_covers (S : List Nat → X → Prop)
    (closed : ∀ w x e, e ≤ 1 → S w x → S (forwardPrefix w e) (δ x w e))
    (init : S w0 x0) : ∀ w, Reach w0 w → ∃ x, S w x := by
  intro w h
  obtain ⟨x, hx⟩ := reach_lift (δ := δ) (x0 := x0) h
  refine ⟨x, ?_⟩
  clear h
  induction hx with
  | refl => exact init
  | step e he _ ih => exact closed _ _ e he ih

/-- No new exclusions: a word that an enriched invariant excludes for every extra
value is already outside the plain forward closure `Reach w0`. -/
theorem no_new_exclusion (S : List Nat → X → Prop)
    (closed : ∀ w x e, e ≤ 1 → S w x → S (forwardPrefix w e) (δ x w e))
    (init : S w0 x0) {w : List Nat} (hex : ∀ x, ¬ S w x) : ¬ Reach w0 w := by
  intro h
  obtain ⟨x, hx⟩ := enriched_invariant_covers S closed init w h
  exact hex x hx

/-- Special case used for residues, width parity and width mod `m`: the update
depends only on the extra value and the overflow bit of the abstract step. -/
theorem overflow_driven_no_new_exclusion (upd : X → Nat → X) (S : List Nat → X → Prop)
    (closed : ∀ w x e, e ≤ 1 → S w x → S (forwardPrefix w e) (upd x (highDigits w e).1))
    (init : S w0 x0) {w : List Nat} (hex : ∀ x, ¬ S w x) : ¬ Reach w0 w :=
  no_new_exclusion (δ := fun x w e => upd x (highDigits w e).1) S closed init hex

end Sprint.Agent03

#print axioms Sprint.Agent03.ereach_proj
#print axioms Sprint.Agent03.reach_lift
#print axioms Sprint.Agent03.proj_iff
#print axioms Sprint.Agent03.reach_sub_invariant
#print axioms Sprint.Agent03.enriched_invariant_covers
#print axioms Sprint.Agent03.no_new_exclusion
#print axioms Sprint.Agent03.overflow_driven_no_new_exclusion
