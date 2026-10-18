import P196.Agent5OrdinaryStreamPrefix.ExteriorArithmetic
import P196.Drafts.Agent110ReviewRadix.ExteriorCoverage

namespace P196.Agent6

/-- Alternating coefficient moment used by the concurrent mod-22 invariant. -/
def alternatingSum : Word → Int
  | [] => 0
  | x :: xs => (x : Int) - alternatingSum xs

def alternatingMoment (s : Exterior) : Int :=
  2 * alternatingSum s.word + (-1 : Int) ^ s.word.length * (s.phase : Int)

def overflow (s : Exterior) : Nat :=
  (norm s.word.reverse (carryPhase s.phase)).2

/-- A state reached by at least one step following an actual computed overflow.
This is a property of the exact exterior dynamics, not arbitrary control bits. -/
def AfterOverflow (s : Exterior) : Prop :=
  ∃ p t, Canonical p ∧ overflow p = 1 ∧ s = iterate t (advance p)

/-- Even- and odd-position subsequences, retaining their internal order. -/
def paritySplit : Word → Word × Word
  | [] => ([],[])
  | x :: xs =>
      let tail := paritySplit xs
      (x :: tail.2, tail.1)

/-- Observables that ignore permutations within each positional parity class. -/
def ParityInvariant {α : Type} (P : Exterior → α) : Prop :=
  ∀ c B C, (paritySplit B).1.Perm (paritySplit C).1 →
    (paritySplit B).2.Perm (paritySplit C).2 → P ⟨c,B⟩ = P ⟨c,C⟩

def potentialSourceA : Exterior := ⟨12,[3,9,13,5,15]⟩
def potentialTargetA : Exterior := ⟨6,[7,9,6,12,11]⟩
def potentialSourceB : Exterior := ⟨6,[6,9,11,12,7]⟩
def potentialTargetB : Exterior := ⟨12,[13,9,3,5,15]⟩
def potentialAncestorA : Exterior := ⟨12,[10,8,8,4]⟩
def potentialAncestorB : Exterior := ⟨12,[15,3,8,4]⟩

/-- Two exact edges whose endpoints coincide only after parity permutations. -/
theorem absorbed_transition_witness :
    advance potentialSourceA = potentialTargetA ∧
    advance potentialSourceB = potentialTargetB := by decide +kernel

/-- Explicit actual-overflow ancestries, including the extra step on side A. -/
theorem absorbed_ancestry_witness :
    overflow potentialAncestorA = 1 ∧
    overflow potentialAncestorB = 1 ∧
    iterate 1 (advance potentialAncestorA) = potentialSourceA ∧
    iterate 0 (advance potentialAncestorB) = potentialSourceB := by decide +kernel

theorem absorbed_canonical_witness :
    Canonical potentialAncestorA ∧ Canonical potentialAncestorB ∧
    Canonical potentialSourceA ∧ Canonical potentialTargetA ∧
    Canonical potentialSourceB ∧ Canonical potentialTargetB := by
  simp [Canonical,trim,potentialAncestorA,potentialAncestorB,
    potentialSourceA,potentialTargetA,potentialSourceB,potentialTargetB]

/-- Both tested source states really lie after a computed overflow. -/
theorem absorbed_sources_after_overflow :
    AfterOverflow potentialSourceA ∧ AfterOverflow potentialSourceB := by
  constructor
  · exact ⟨potentialAncestorA,1,absorbed_canonical_witness.1,
      absorbed_ancestry_witness.1,absorbed_ancestry_witness.2.2.1.symm⟩
  · exact ⟨potentialAncestorB,0,absorbed_canonical_witness.2.1,
      absorbed_ancestry_witness.2.1,absorbed_ancestry_witness.2.2.2.symm⟩

/-- The counterexample remains inside the absorbing alternating-moment class. -/
theorem absorbed_zero_moment_witness :
    alternatingMoment potentialSourceA % 22 = 0 ∧
    alternatingMoment potentialTargetA % 22 = 0 ∧
    alternatingMoment potentialSourceB % 22 = 0 ∧
    alternatingMoment potentialTargetB % 22 = 0 := by decide +kernel

theorem absorbed_parity_permutations :
    (paritySplit potentialTargetA.word).1.Perm (paritySplit potentialSourceB.word).1 ∧
    (paritySplit potentialTargetA.word).2.Perm (paritySplit potentialSourceB.word).2 ∧
    (paritySplit potentialTargetB.word).1.Perm (paritySplit potentialSourceA.word).1 ∧
    (paritySplit potentialTargetB.word).2.Perm (paritySplit potentialSourceA.word).2 := by
  decide +kernel

/-- This is NOT an actual returned exterior cycle. -/
theorem absorbed_witness_not_an_actual_cycle :
    potentialTargetA ≠ potentialSourceB ∧ potentialTargetB ≠ potentialSourceA := by
  decide +kernel

/-- No parity-permutation-invariant observable strictly progresses on every
canonical post-overflow transition, for any transitive irreflexive relation. -/
theorem no_strict_parity_invariant_after_overflow {α : Type}
    (P : Exterior → α) (r : α → α → Prop)
    (hirr : ∀ a, ¬ r a a)
    (htrans : ∀ a b c, r a b → r b c → r a c)
    (hinv : ParityInvariant P)
    (hprogress : ∀ s, Canonical s → AfterOverflow s → r (P s) (P (advance s))) :
    False := by
  have hA := hprogress potentialSourceA absorbed_canonical_witness.2.2.1
    absorbed_sources_after_overflow.1
  have hB := hprogress potentialSourceB absorbed_canonical_witness.2.2.2.2.1
    absorbed_sources_after_overflow.2
  rw [absorbed_transition_witness.1] at hA
  rw [absorbed_transition_witness.2] at hB
  have heA : P potentialTargetA = P potentialSourceB :=
    hinv 6 _ _ absorbed_parity_permutations.1 absorbed_parity_permutations.2.1
  have heB : P potentialTargetB = P potentialSourceA :=
    hinv 12 _ _ absorbed_parity_permutations.2.2.1 absorbed_parity_permutations.2.2.2
  rw [heA] at hA
  rw [heB] at hB
  exact hirr (P potentialSourceA)
    (htrans _ _ _ hA hB)

/-- Allowing plateaus avoids the contradiction but forces these two plateaus. -/
theorem parity_invariant_after_overflow_stagnates (P : Exterior → Int)
    (hinv : ParityInvariant P)
    (hprogress : ∀ s, Canonical s → AfterOverflow s → P s ≤ P (advance s)) :
    P potentialSourceA = P potentialTargetA ∧
    P potentialSourceB = P potentialTargetB := by
  have hA := hprogress potentialSourceA absorbed_canonical_witness.2.2.1
    absorbed_sources_after_overflow.1
  have hB := hprogress potentialSourceB absorbed_canonical_witness.2.2.2.2.1
    absorbed_sources_after_overflow.2
  rw [absorbed_transition_witness.1] at hA
  rw [absorbed_transition_witness.2] at hB
  have heA : P potentialTargetA = P potentialSourceB :=
    hinv 6 _ _ absorbed_parity_permutations.1 absorbed_parity_permutations.2.1
  have heB : P potentialTargetB = P potentialSourceA :=
    hinv 12 _ _ absorbed_parity_permutations.2.2.1 absorbed_parity_permutations.2.2.2
  omega

#print axioms absorbed_transition_witness
#print axioms absorbed_ancestry_witness
#print axioms absorbed_canonical_witness
#print axioms absorbed_sources_after_overflow
#print axioms absorbed_zero_moment_witness
#print axioms absorbed_parity_permutations
#print axioms absorbed_witness_not_an_actual_cycle
#print axioms no_strict_parity_invariant_after_overflow
#print axioms parity_invariant_after_overflow_stagnates
end P196.Agent6
