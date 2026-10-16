import LeadingWitness
import Family

/-!
Agent #122. Exact ordinary-decimal labels for the finite-seed countermodel.
The node formula is the original report's c(a,j), with a >= 3.
The imported decimal bounds and singleton-value lemma are reused, not new results.
-/
namespace Agent122.Countermodel

open Lychrel196 DecimalDigits DecimalQuantitativeMass ModularAutonomy

/-- The actual one-step palindrome predecessor predicate, including zero. -/
def B (n : Nat) : Prop := Palindrome (step n)

instance (n : Nat) : Decidable (B n) := inferInstanceAs (Decidable (Palindrome (step n)))

/-- The original sparse chain label. Only a >= 3 is used in the countermap. -/
def node (a j : Nat) : Nat := 10^(a+j) + 10*a + 9

/-- The report's nonpalindromic exit, whose genuine next step is palindromic. -/
def terminal (a k : Nat) : Nat := 10^(a+k+1) + 2

private theorem marker_lt_shift (k : Nat) : 10*(k+3)+9 < 10^(k+3) := by
  induction k with
  | zero => decide
  | succ k ih =>
    rw [show k+1+3 = (k+3)+1 by omega, Nat.pow_succ]
    omega

theorem marker_lt (a : Nat) (ha : 3 ≤ a) : 10*a+9 < 10^a := by
  obtain ⟨k, rfl⟩ := Nat.exists_eq_add_of_le ha
  simpa only [Nat.add_comm 3 k] using marker_lt_shift k

theorem node_bounds (a j : Nat) (ha : 3 ≤ a) :
    10^(a+j) ≤ node a j ∧ node a j < 2*10^(a+j) := by
  have hb := marker_lt a ha
  have hm := Nat.pow_le_pow_right (by decide : 0 < 10) (show a ≤ a+j by omega)
  unfold node
  omega

theorem node_positive (a j : Nat) : 0 < node a j := by
  have hp : 0 < 10^(a+j) := Nat.pow_pos (by decide)
  unfold node
  omega

theorem node_canonical (a j : Nat) (ha : 3 ≤ a) :
    ∃ d, Canonical (node a j) d (a+j+1) := by
  have hb := node_bounds a j ha
  apply canonical_of_pow_bounds (node a j) (a+j+1) (by omega)
  · simpa only [Nat.add_sub_cancel] using hb.1
  · rw [Nat.pow_succ]
    omega

theorem node_width (a j : Nat) (ha : 3 ≤ a) :
    decimalLength (node a j) = a+j+1 := by
  obtain ⟨d, hc⟩ := node_canonical a j ha
  exact decimalLength_of_canonical _ _ _ hc

theorem node_units (a j : Nat) (ha : 3 ≤ a) : node a j % 10 = 9 := by
  have hp : 10^(a+j) % 10 = 0 := by
    rw [show a+j = (a+j-1)+1 by omega, Nat.pow_succ]
    simp
  simp [node, Nat.add_mod, hp]

/-- A canonical number beginning in 1 and ending in 9 is neither palindromic
nor an actual one-step palindrome predecessor. -/
theorem leading_one_units_nine_safe (n k : Nat)
    (hlo : 10^k ≤ n) (hhi : n < 2*10^k) (hu : n % 10 = 9) :
    ¬ Palindrome n ∧ ¬ B n := by
  obtain ⟨d, hc⟩ := canonical_of_pow_bounds n (k+1) (by omega)
    (by simpa only [Nat.add_sub_cancel] using hlo)
    (by rw [Nat.pow_succ]; omega)
  have htop : d k = 1 := canonical_lead_of_interval n k 1 d hc (by simpa using hlo) hhi
  have hd0 := hc.2.1 0 (by omega)
  have hv := hc.2.2.2
  rw [value_shift] at hv
  have hbottom : d 0 = 9 := by omega
  constructor
  · intro hp
    rw [← hc.2.2.2] at hp
    have hs := (palindrome_value_iff d (k+1) hc.2.1 (Or.inr hc.2.2.1)).mp hp
    have hz := hs 0 (by omega)
    simp only [Nat.add_sub_cancel, Nat.sub_zero, hbottom, htop] at hz
    omega
  · intro hp
    unfold B at hp
    rw [← hc.2.2.2] at hp
    have hs := (step_palindrome_iff d (k+1) hc.1 hc.2.1 hc.2.2.1).mp hp
    have ho : columnSum d (k+1) 0 = 10 := by
      simp [columnSum, reflected, hbottom, htop]
    rcases hs with hs | hs
    · have hz := hs 0 (by omega)
      omega
    · omega

theorem node_safe (a j : Nat) (ha : 3 ≤ a) :
    ¬ Palindrome (node a j) ∧ ¬ B (node a j) := by
  exact leading_one_units_nine_safe _ _ (node_bounds a j ha).1
    (node_bounds a j ha).2 (node_units a j ha)

/-- Numeric labels are unambiguous even before the finite chain cutoff is fixed. -/
theorem node_injective (a j b k : Nat) (ha : 3 ≤ a) (hb : 3 ≤ b)
    (h : node a j = node b k) : a = b ∧ j = k := by
  have hw := congrArg decimalLength h
  rw [node_width a j ha, node_width b k hb] at hw
  have he : a+j = b+k := by omega
  unfold node at h
  rw [he] at h
  constructor <;> omega

/-- A numeral with prescribed lower and upper endpoint digits. -/
def endsDigit (k a b i : Nat) : Nat :=
  (if i = k then a else 0) + (if i = 0 then b else 0)

theorem endsDigit_value (k a b : Nat) :
    value (endsDigit k a b) (k+1) = a*10^k+b := by
  unfold endsDigit
  rw [value_add, Agent13SafeFamily.value_single, Agent13SafeFamily.value_single]
  simp

theorem endsDigit_bounded (k a b : Nat) (hk : 0 < k) (ha : a ≤ 9) (hb : b ≤ 9) :
    ∀ i, i < k+1 → endsDigit k a b i ≤ 9 := by
  intro i hi
  unfold endsDigit
  split <;> split <;> omega

theorem endsDigit_reflected (k a b i : Nat) (hk : 0 < k) (hi : i < k+1) :
    reflected (endsDigit k a b) (k+1) i = endsDigit k b a i := by
  simp only [reflected, Nat.add_sub_cancel, endsDigit]
  by_cases hz : i = 0
  · subst i
    simp [Nat.ne_of_gt hk, Nat.ne_of_gt hk |>.symm]
  by_cases ht : i = k
  · subst i
    simp [Nat.ne_of_gt hk, (Nat.ne_of_gt hk).symm]
  · have h1 : k-i ≠ 0 := by omega
    have h2 : k-i ≠ k := by omega
    simp [hz, ht, h1, h2]

/-- Closed-form reversal of these sparse canonical decimal numerals. -/
theorem reverse_endpoints (k a b : Nat) (hk : 0 < k) (ha : a ≤ 9)
    (hb : b ≤ 9) (hapos : 0 < a) :
    reverse10 (a*10^k+b) = b*10^k+a := by
  rw [← endsDigit_value, reverse10_value]
  · rw [← endsDigit_value k b a]
    apply value_congr
    intro i hi
    exact endsDigit_reflected k a b i hk hi
  · exact endsDigit_bounded k a b hk ha hb
  · right
    simp [endsDigit, Nat.ne_of_gt hk]
    exact hapos

theorem terminal_properties (a k : Nat) (ha : 3 ≤ a) :
    0 < terminal a k ∧ ¬ Palindrome (terminal a k) ∧ B (terminal a k) := by
  have hp : 0 < 10^(a+k+1) := Nat.pow_pos (by decide)
  have hr : reverse10 (terminal a k) = 2*10^(a+k+1)+1 := by
    simpa [terminal] using reverse_endpoints (a+k+1) 1 2 (by omega) (by decide) (by decide) (by decide)
  have hs : step (terminal a k) = 3*10^(a+k+1)+3 := by
    unfold step
    rw [hr]
    unfold terminal
    omega
  refine ⟨by unfold terminal; omega, ?_, ?_⟩
  · intro h
    unfold Palindrome at h
    rw [hr] at h
    unfold terminal at h
    have hten : 10 ≤ 10^(a+k+1) := by
      exact Nat.pow_le_pow_right (by decide : 0 < 10) (show 1 ≤ a+k+1 by omega)
    omega
  · unfold B Palindrome
    rw [hs]
    exact reverse_endpoints (a+k+1) 3 3 (by omega) (by decide) (by decide) (by decide)

end Agent122.Countermodel
