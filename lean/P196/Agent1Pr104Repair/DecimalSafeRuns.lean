import P196.Foundations.LychrelDigitSums

/-!
Unconditional, finite decimal safe prefixes of arbitrary length.
The explicit initial number consists entirely of nines. Its initial value
is permitted to be a palindrome; all claimed safe indices are positive.
A later module shifts once when extracting an all-index Lychrel witness.
-/

namespace DecimalSafeRuns

open Lychrel196 DecimalDigits FoldedDecimal OverflowCarryNormalization CarryHistory

def Run18 (q : Nat → Nat) (L a m : Nat) : Prop :=
  a + m ≤ L ∧ ∀ i, a ≤ i → i < a + m → q i = 18

def HasRun18 (q : Nat → Nat) (L m : Nat) : Prop :=
  ∃ a, Run18 q L a m

theorem output_eighteen_after_eighteen (q : Nat → Nat) (L i : Nat)
    (ha : Admissible L q) (hi0 : 0 < i) (hi : i < L)
    (hp : q (i - 1) = 18) (hq : q i = 18) : output q i = 9 := by
  have hb := carry_bounded q L ha.2.2.1 (i - 1) (by omega)
  have he : i - 1 + 1 = i := by omega
  have hc : carry q i = 1 := by
    have hc' : carry q (i - 1 + 1) = (q (i - 1) + carry q (i - 1)) / 10 := rfl
    rw [he, hp] at hc'
    omega
  simp only [output, hq, hc]

/-- Three consecutive 18 columns preserve their middle column in both
overflow branches. Only actual finite-word admissibility is assumed. -/
theorem next_eighteen (q : Nat → Nat) (L i : Nat)
    (ha : Admissible L q) (hi0 : 0 < i) (hi : i + 1 < L)
    (hleft : q (i - 1) = 18) (hmid : q i = 18) (hright : q (i + 1) = 18) :
    nextColumns q L i = 18 := by
  have hlo := output_eighteen_after_eighteen q L i ha hi0 (by omega) hleft hmid
  by_cases hc : carry q L = 0
  · have hm : q (L - 1 - i) = 18 :=
      (ha.2.2.2.1 i (by omega)).symm.trans hmid
    have hp : q (L - 1 - i - 1) = 18 := by
      have hs := (ha.2.2.2.1 (i + 1) hi).symm.trans hright
      have he : L - 1 - (i + 1) = L - 1 - i - 1 := by omega
      simpa only [he] using hs
    have hhi := output_eighteen_after_eighteen q L (L - 1 - i) ha
      (by omega) (by omega) hp hm
    simp only [nextColumns, hc, if_true, columnSum, reflected, hlo, hhi]
  · have hm : q (L - i) = 18 := by
      have hs := (ha.2.2.2.1 (i - 1) (by omega)).symm.trans hleft
      have he : L - 1 - (i - 1) = L - i := by omega
      simpa only [he] using hs
    have hp : q (L - i - 1) = 18 := by
      have hs := (ha.2.2.2.1 i (by omega)).symm.trans hmid
      have he : L - 1 - i = L - i - 1 := by omega
      simpa only [he] using hs
    have hhi := output_eighteen_after_eighteen q L (L - i) ha
      (by omega) (by omega) hp hm
    simp only [nextColumns, hc, if_false, columnSum, reflected,
      Nat.add_sub_cancel, extended, show i < L by omega,
      show L - i < L by omega, if_true, hlo, hhi]

theorem run18_next (q : Nat → Nat) (L a m : Nat)
    (ha : Admissible L q) (hr : Run18 q L a (m + 2)) :
    Run18 (nextColumns q L) (nextWidth q L) (a + 1) m := by
  constructor
  · unfold nextWidth
    split <;> have := hr.1 <;> omega
  · intro i hia him
    apply next_eighteen q L i ha (by omega) (by have := hr.1; omega)
    · exact hr.2 (i - 1) (by omega) (by omega)
    · exact hr.2 i (by omega) (by omega)
    · exact hr.2 (i + 1) (by omega) (by omega)

theorem hasRun18_next (q : Nat → Nat) (L m : Nat)
    (ha : Admissible L q) (hr : HasRun18 q L (m + 2)) :
    HasRun18 (nextColumns q L) (nextWidth q L) m := by
  obtain ⟨a, hr⟩ := hr
  exact ⟨a + 1, run18_next q L a m ha hr⟩

/-- A run of m+2t consecutive 18s leaves a run of at least m after t
actual column transitions, irrespective of the overflow schedule. -/
theorem hasRun18_iter (q : Nat → Nat) (L m t : Nat)
    (ha : Admissible L q) (hr : HasRun18 q L (m + 2 * t)) :
    HasRun18 (iterPairs q L t).2 (iterPairs q L t).1 m := by
  induction t generalizing m with
  | zero => simpa only [Nat.mul_zero, Nat.add_zero, iterPairs] using hr
  | succ t ih =>
    have he : m + 2 + 2 * t = m + 2 * (t + 1) := by omega
    have hp := ih (m + 2) (by simpa only [he] using hr)
    exact hasRun18_next _ _ m (iterPairs_admissible q L t ha) hp

theorem hasRun18_not_bad (q : Nat → Nat) (L : Nat)
    (hr : HasRun18 q L 1) : ¬ BadWord L q := by
  obtain ⟨a, ha, hq⟩ := hr
  have haL : a < L := by omega
  have hqa : q a = 18 := hq a (by omega) (by omega)
  rintro (hsmall | ⟨_, he⟩)
  · have := hsmall a haL
    omega
  · rcases he a haL with hz | he
    · omega
    · omega

/-- A finite-word avoidance fact transfers to the actual next integer. -/
theorem next_not_palindrome_of_not_bad (n : Nat) (d q : Nat → Nat) (L : Nat)
    (hc : Canonical n d L) (hr : ∀ i, i < L → columnSum d L i = q i)
    (hb : ¬ BadWord L q) : ¬ Palindrome (step n) := by
  intro hp
  apply hb
  have hp' : Palindrome (step (value d L)) := by simpa only [hc.2.2.2] using hp
  rcases (step_palindrome_iff d L hc.1 hc.2.1 hc.2.2.1).mp hp' with hlo | hhi
  · left
    intro i hi
    rw [← hr i hi]
    exact hlo i hi
  · right
    constructor
    · rw [← hr 0 hc.1]
      exact hhi.1
    · intro i hi
      rw [← hr i hi]
      exact hhi.2 i hi

theorem iter_not_palindrome_of_run (n : Nat) (d q : Nat → Nat) (L t : Nat)
    (hc : Canonical n d L) (hr : ∀ i, i < L → columnSum d L i = q i)
    (ha : Admissible L q) (h18 : HasRun18 q L (1 + 2 * t)) :
    ¬ Palindrome (orbit n (t + 1)) := by
  obtain ⟨e, he, hrep⟩ := iterPairs_representation n d q L t hc hr
  exact next_not_palindrome_of_not_bad _ e _ _ he hrep
    (hasRun18_not_bad _ _ (hasRun18_iter q L 1 t ha h18))

/-- The ordinary decimal integer with exactly L copies of digit nine. -/
def nines (L : Nat) : Nat := value (fun _ => 9) L

theorem nines_canonical (L : Nat) (hL : 0 < L) :
    Canonical (nines L) (fun _ => 9) L :=
  ⟨hL, by intro i hi; exact Nat.le_refl 9, by exact Nat.zero_lt_succ 8, rfl⟩

theorem nines_positive (L : Nat) (hL : 0 < L) : 0 < nines L :=
  value_positive (fun _ => 9) L hL (by exact Nat.zero_lt_succ 8)

/-- Unconditional explicit safe finite segments: a string of 2R+1 nines
avoids palindromes at each positive time 1,...,R+1. -/
theorem nines_safe_prefix (R k : Nat) (hk : k ≤ R) :
    ¬ Palindrome (orbit (nines (2 * R + 1)) (k + 1)) := by
  let d : Nat → Nat := fun _ => 9
  let q : Nat → Nat := fun _ => 18
  have hc : Canonical (nines (2 * R + 1)) d (2 * R + 1) :=
    nines_canonical _ (by omega)
  have hrep : ∀ i, i < 2 * R + 1 → columnSum d (2 * R + 1) i = q i := by
    intro i hi
    rfl
  have ha : Admissible (2 * R + 1) q :=
    NormalizationBridge.admissible_congr _ _ _
      (NormalizationBridge.canonical_admissible _ _ _ hc) hrep
  apply iter_not_palindrome_of_run _ d q _ k hc hrep ha
  exact ⟨0, by omega, by intro i hi hlt; rfl⟩

#print axioms next_eighteen
#print axioms run18_next
#print axioms hasRun18_iter
#print axioms next_not_palindrome_of_not_bad
#print axioms nines_safe_prefix

end DecimalSafeRuns
