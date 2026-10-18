import P196.Drafts.Agent110ReviewRadix.ExteriorCoverage

namespace P196.Agent6

/-- This is a two-step word reversal, not a returned exterior cycle. -/
theorem reversal_transition_witness :
    advance ⟨6,[1,5]⟩ = ⟨12,[2,10]⟩ ∧
    advance ⟨12,[2,10]⟩ = ⟨6,[5,1]⟩ := by
  decide

theorem reversal_witness_canonical :
    Canonical ⟨6,[1,5]⟩ ∧ Canonical ⟨12,[2,10]⟩ ∧
    Canonical ⟨6,[5,1]⟩ := by
  simp [Canonical,trim]

def ReversalInvariant (P : Exterior → Int) : Prop :=
  ∀ c B, P ⟨c,B.reverse⟩ = P ⟨c,B⟩

/-- Even unrestricted reversal-invariant potentials cannot strictly increase
on every canonical exterior transition. No additive-form assumption is needed. -/
theorem no_reversal_invariant_strict_potential (P : Exterior → Int)
    (hr : ReversalInvariant P)
    (hs : ∀ s, Canonical s → P s < P (advance s)) : False := by
  have h0 := hs ⟨6,[1,5]⟩ reversal_witness_canonical.1
  have h1 := hs ⟨12,[2,10]⟩ reversal_witness_canonical.2.1
  rw [reversal_transition_witness.1] at h0
  rw [reversal_transition_witness.2] at h1
  have he : P ⟨6,[5,1]⟩ = P ⟨6,[1,5]⟩ := hr 6 [1,5]
  omega

/-- Any nondecreasing reversal-invariant potential stagnates on both
explicit transitions in the witness. -/
theorem reversal_invariant_stagnates (P : Exterior → Int)
    (hr : ReversalInvariant P)
    (hs : ∀ s, Canonical s → P s ≤ P (advance s)) :
    P ⟨6,[1,5]⟩ = P ⟨12,[2,10]⟩ ∧
    P ⟨12,[2,10]⟩ = P ⟨6,[5,1]⟩ := by
  have h0 := hs ⟨6,[1,5]⟩ reversal_witness_canonical.1
  have h1 := hs ⟨12,[2,10]⟩ reversal_witness_canonical.2.1
  rw [reversal_transition_witness.1] at h0
  rw [reversal_transition_witness.2] at h1
  have he : P ⟨6,[5,1]⟩ = P ⟨6,[1,5]⟩ := hr 6 [1,5]
  omega

def symbolSum (f : Nat → Int) : Word → Int
  | [] => 0
  | x :: xs => f x + symbolSum f xs

theorem symbolSum_append (f : Nat → Int) (a b : Word) :
    symbolSum f (a ++ b) = symbolSum f a + symbolSum f b := by
  induction a with
  | nil => simp [symbolSum]
  | cons x xs ih => simp only [List.cons_append,symbolSum,ih]; omega

theorem symbolSum_reverse (f : Nat → Int) (w : Word) :
    symbolSum f w.reverse = symbolSum f w := by
  induction w with
  | nil => rfl
  | cons x xs ih =>
      simp only [List.reverse_cons,symbolSum_append,symbolSum,ih]
      omega

def additivePotential (phaseWeight : Nat → Int) (symbolWeight : Nat → Nat → Int)
    (s : Exterior) : Int :=
  phaseWeight s.phase + symbolSum (symbolWeight s.phase) s.word

theorem additivePotential_reversal (p : Nat → Int) (w : Nat → Nat → Int) :
    ReversalInvariant (additivePotential p w) := by
  intro c B
  simp [additivePotential,symbolSum_reverse]

/-- No choice of phase-dependent symbol weights supplies a strict additive
Lyapunov function for all canonical exterior steps. -/
theorem no_strict_additive_potential (p : Nat → Int) (w : Nat → Nat → Int)
    (hs : ∀ s, Canonical s → additivePotential p w s <
      additivePotential p w (advance s)) : False :=
  no_reversal_invariant_strict_potential (additivePotential p w)
    (additivePotential_reversal p w) hs

#print axioms reversal_transition_witness
#print axioms reversal_witness_canonical
#print axioms no_reversal_invariant_strict_potential
#print axioms reversal_invariant_stagnates
#print axioms symbolSum_append
#print axioms symbolSum_reverse
#print axioms additivePotential_reversal
#print axioms no_strict_additive_potential
end P196.Agent6
