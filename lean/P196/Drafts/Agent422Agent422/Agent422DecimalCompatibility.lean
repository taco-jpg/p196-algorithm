import P196.Drafts.Agent422Agent422.Agent422NormalizationSharpness
import P196.Foundations.LychrelDigitSums

/-!
# Compatibility with the repository's original decimal definitions

Agent #422. The original dependency is the unmodified
`proofs/research/Lychrel196Research.lean` at
2eb05ef47671d6b1883e54fec9f6a4f8de9ed8f5, Git blob
c6c1f5441c54a36f2d82b3ef78dff1ccdbc5a506.
These are equalities to existing declarations, not a second interpretation
of the original conjecture. The original file must be rebuilt from its pinned
source when clean-checking this optional compatibility module.
-/

namespace Agent422DecimalCompatibility
open Agent422BaseDigits

theorem reverseAux_eq (n acc : Nat) :
    Agent422BaseDigits.reverseAux 10 (by decide) n acc =
      Lychrel196.reverseAux n acc := by
  induction n using Nat.strongRecOn generalizing acc with
  | ind n ih =>
    by_cases hn : n = 0
    · subst n
      simp [Agent422BaseDigits.reverseAux, Lychrel196.reverseAux]
    · rw [Agent422BaseDigits.reverseAux, Lychrel196.reverseAux]
      simp only [hn, ↓reduceDIte, ↓reduceIte]
      exact ih (n / 10)
        (Nat.div_lt_self (Nat.pos_of_ne_zero hn) (by decide)) (10 * acc + n % 10)

theorem reverse_eq (n : Nat) :
    Agent422BaseDigits.reverse 10 (by decide) n = Lychrel196.reverse10 n := by
  rw [Agent422BaseDigits.reverse, reverseAux_eq]
  exact (Lychrel196.reverseFuel_correct n n 0 (Nat.le_refl n)).symm

theorem step_eq (n : Nat) :
    Agent422BaseDigits.step 10 (by decide) n = Lychrel196.step n := by
  simp only [Agent422BaseDigits.step, Lychrel196.step, reverse_eq]

theorem orbit_eq (n k : Nat) :
    Agent422BaseDigits.orbit 10 (by decide) n k = Lychrel196.orbit n k := by
  induction k with
  | zero => rfl
  | succ k ih =>
    simp only [Agent422BaseDigits.orbit, Lychrel196.orbit, step_eq, ih]

theorem palindrome_iff (n : Nat) :
    Agent422BaseDigits.Palindrome 10 (by decide) n ↔ Lychrel196.Palindrome n := by
  simp only [Agent422BaseDigits.Palindrome, Lychrel196.Palindrome, reverse_eq]

theorem value_eq (d : Nat → Nat) (L : Nat) :
    Agent422BaseDigits.value 10 d L = DecimalDigits.value d L := by
  induction L with
  | zero => rfl
  | succ L ih => simp only [Agent422BaseDigits.value, DecimalDigits.value, ih]

theorem reflected_eq (d : Nat → Nat) (L i : Nat) :
    Agent422BaseDigits.reflected d L i = DecimalDigits.reflected d L i := rfl

theorem columnSum_eq (d : Nat → Nat) (L i : Nat) :
    Agent422BaseDigits.columnSum d L i = DecimalDigits.columnSum d L i := rfl

theorem carry_eq (q : Nat → Nat) (i : Nat) :
    Agent422BaseDigits.carry 10 q i = DecimalDigits.carry q i := by
  induction i with
  | zero => rfl
  | succ i ih => simp only [Agent422BaseDigits.carry, DecimalDigits.carry, ih]

theorem output_eq (q : Nat → Nat) (i : Nat) :
    Agent422BaseDigits.output 10 q i = DecimalDigits.output q i := by
  simp only [Agent422BaseDigits.output, DecimalDigits.output, carry_eq]

/-- Includes the opposite equality orientations in the two canonical records. -/
theorem canonical_iff (n : Nat) (d : Nat → Nat) (L : Nat) :
    Agent422BaseDigits.Canonical 10 n d L ↔ DecimalDigits.Canonical n d L := by
  unfold Agent422BaseDigits.Canonical DecimalDigits.Canonical
  rw [value_eq]
  constructor
  · rintro ⟨hL, hd, hp, he⟩
    exact ⟨hL, fun i hi => by have h := hd i hi; omega, hp, he.symm⟩
  · rintro ⟨hL, hd, hp, he⟩
    exact ⟨hL, fun i hi => by have h := hd i hi; omega, hp, he.symm⟩

/-- The generic source theorem specializes to the repository's EXACT original
numeric predicates and carry function, with no bridge hypothesis. -/
theorem source_sharpness_decimal :
    (∃ n d, 0 < n ∧ DecimalDigits.Canonical n d 5 ∧
      (∀ i, i ≤ 5 → DecimalDigits.carry (DecimalDigits.columnSum d 5) i =
        Agent422NormalizationSharpness.slowCarry i) ∧
      Lychrel196.Palindrome (Lychrel196.orbit n 4)) ∧
    (∀ n d, DecimalDigits.Canonical n d 5 →
      (∀ i, i ≤ 5 → DecimalDigits.carry (DecimalDigits.columnSum d 5) i =
        Agent422NormalizationSharpness.slowCarry i) →
      ∀ k, 0 < k → k ≤ 3 → ¬ Lychrel196.Palindrome (Lychrel196.orbit n k)) := by
  have h := Agent422NormalizationSharpness.source_sharpness 10 (by decide)
  simpa only [canonical_iff, columnSum_eq, carry_eq, palindrome_iff, orbit_eq] using h

end Agent422DecimalCompatibility
