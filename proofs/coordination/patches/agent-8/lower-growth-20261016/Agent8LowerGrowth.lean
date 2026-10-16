import PrefixModel

/-!
Agent #8: an exact obstruction to stronger lower-width potentials on the
existing three-column necessary relation. This is not an integer-orbit witness.
Dependency: original PrefixModel.lean from source tree
2eb05ef47671d6b1883e54fec9f6a4f8de9ed8f5, unchanged.
-/
namespace P196.Agent8.LowerGrowth
open P196.Agent4.Saturation

/-- Four legal prefixes with one overflow per closed four-edge walk. -/
def slowState (i : Nat) : Prefix :=
  match i % 4 with
  | 0 => ⟨1, 5, 10⟩
  | 1 => ⟨2, 11, 1⟩
  | 2 => ⟨5, 2, 3⟩
  | _ => ⟨10, 4, 6⟩

def slowControl (i : Nat) : Nat := if i % 4 = 0 then 1 else 0

def slowOverflow (i : Nat) : Nat := if i % 4 = 3 then 1 else 0

/-- Every displayed edge is checked by the Lean kernel, not a native oracle. -/
theorem slow_edges : ∀ i : Fin 4,
    advance (slowState i.val) (slowControl i.val) =
      (slowState (i.val + 1), slowOverflow i.val) := by decide +kernel

/-- The periodic abstract walk satisfies the original transition for all time. -/
theorem slow_evolution (t : Nat) :
    advance (slowState t) (slowControl t) =
      (slowState (t + 1), slowOverflow t) := by
  have h := slow_edges ⟨t % 4, Nat.mod_lt _ (by decide)⟩
  have hn : (t % 4 + 1) % 4 = (t + 1) % 4 := by omega
  simpa only [slowState, slowControl, slowOverflow, Nat.mod_mod, hn] using h

/-- Actual validity of every prefix, independently of transition hypotheses. -/
theorem slow_valid (t : Nat) :
    0 < (slowState t).a ∧ (slowState t).a ≤ 18 ∧
    (slowState t).b ≤ 18 ∧ (slowState t).c ≤ 18 ∧ slowControl t ≤ 1 := by
  have h : ∀ i : Fin 4,
      0 < (slowState i.val).a ∧ (slowState i.val).a ≤ 18 ∧
      (slowState i.val).b ≤ 18 ∧ (slowState i.val).c ≤ 18 ∧
      slowControl i.val ≤ 1 := by decide +kernel
  simpa only [slowState, slowControl, Nat.mod_mod] using
    h ⟨t % 4, Nat.mod_lt _ (by decide)⟩

/-- Any integer-valued universal potential with slope p/q must have 4*p <= q.
Only the four concrete transitions are needed, so no finiteness or boundedness
assumption on V is concealed in this obstruction. -/
theorem universal_potential_slope_le (V : Prefix → Int) (p q : Int)
    (h : ∀ s : Prefix, ∀ e : Nat,
      0 < s.a → s.a ≤ 18 → s.b ≤ 18 → s.c ≤ 18 → e ≤ 1 →
      V (advance s e).1 + p ≤ V s + q * (advance s e).2) :
    4 * p ≤ q := by
  have h0 := h ⟨1, 5, 10⟩ 1 (by decide) (by decide) (by decide) (by decide) (by decide)
  have h1 := h ⟨2, 11, 1⟩ 0 (by decide) (by decide) (by decide) (by decide) (by decide)
  have h2 := h ⟨5, 2, 3⟩ 0 (by decide) (by decide) (by decide) (by decide) (by decide)
  have h3 := h ⟨10, 4, 6⟩ 0 (by decide) (by decide) (by decide) (by decide) (by decide)
  change V ⟨2, 11, 1⟩ + p ≤ V ⟨1, 5, 10⟩ + q * 0 at h0
  change V ⟨5, 2, 3⟩ + p ≤ V ⟨2, 11, 1⟩ + q * 0 at h1
  change V ⟨10, 4, 6⟩ + p ≤ V ⟨5, 2, 3⟩ + q * 0 at h2
  change V ⟨1, 5, 10⟩ + p ≤ V ⟨10, 4, 6⟩ + q * 1 at h3
  simp only [Int.mul_zero, Int.mul_one, Int.add_zero] at h0 h1 h2 h3
  omega

/-- In particular, the proposed three-tenths inequality is impossible here. -/
theorem no_three_tenths_potential :
    ¬ ∃ V : Prefix → Int, ∀ s : Prefix, ∀ e : Nat,
      0 < s.a → s.a ≤ 18 → s.b ≤ 18 → s.c ≤ 18 → e ≤ 1 →
      V (advance s e).1 + 3 ≤ V s + 10 * (advance s e).2 := by
  rintro ⟨V, h⟩
  have bad := universal_potential_slope_le V 3 10 h
  omega

#print axioms slow_edges
#print axioms slow_evolution
#print axioms slow_valid
#print axioms universal_potential_slope_le
#print axioms no_three_tenths_potential

end P196.Agent8.LowerGrowth
