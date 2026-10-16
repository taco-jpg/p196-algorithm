import Agent101DigitPairs

/-!
Agent #101. The exact digit-splitting product and its sharp uniform bound.
The empty profile is not a positive numeral; a one-digit profile has its
own positive-center condition. No claim about an infinite orbit is made.
-/

namespace Agent101

def natProduct : List Nat → Nat
  | [] => 1
  | a :: xs => a * natProduct xs

/-- Proposed enumeration cardinality, including every leading/center case. -/
def profileCount : List Nat → Option Nat → Nat
  | [], none => 0
  | [], some s => if 0 < s then centerCount (some s) else 0
  | s :: h, c => pairCount true s * centerCount c * natProduct (h.map (pairCount false))

theorem pairCount_inner_le (s : Nat) : pairCount false s ≤ 10 := by
  unfold pairCount
  split <;> split <;> omega

theorem pairCount_outer_le (s : Nat) : pairCount true s ≤ 9 := by
  unfold pairCount
  split <;> split <;> omega

theorem centerCount_le (c : Option Nat) : centerCount c ≤ 1 := by
  cases c with
  | none => decide
  | some s => simp only [centerCount]; split <;> omega

theorem pairProduct_le (h : List Nat) :
    natProduct (h.map (pairCount false)) ≤ 10 ^ h.length := by
  induction h with
  | nil => simp [natProduct]
  | cons s h ih =>
    simp only [List.map_cons, natProduct, List.length_cons, Nat.pow_succ]
    have hb := Nat.mul_le_mul (pairCount_inner_le s) ih
    simpa [Nat.mul_comm] using hb

/-- At each fixed positive half-width this is a uniform bound for all profiles. -/
theorem profileCount_cons_le (s : Nat) (h : List Nat) (c : Option Nat) :
    profileCount (s :: h) c ≤ 9 * 10 ^ h.length := by
  have hc : pairCount true s * centerCount c ≤ 9 := by
    have hb := Nat.mul_le_mul (pairCount_outer_le s) (centerCount_le c)
    simpa using hb
  exact Nat.mul_le_mul hc (pairProduct_le h)

theorem profileCount_single_le (c : Option Nat) : profileCount [] c ≤ 1 := by
  cases c with
  | none => decide
  | some s =>
    simp only [profileCount]
    split
    · exact centerCount_le (some s)
    · omega

theorem natProduct_replicate (n a : Nat) :
    natProduct (List.replicate n a) = a ^ n := by
  induction n with
  | zero => rfl
  | succ n ih => simp [List.replicate_succ, natProduct, ih, Nat.pow_succ, Nat.mul_comm]

/-- The full upper bound is attained with either no center or any valid center. -/
theorem profileCount_nines (k : Nat) (c : Option Nat) (hc : centerCount c = 1) :
    profileCount (9 :: List.replicate k 9) c = 9 * 10 ^ k := by
  simp [profileCount, hc, pairCount, List.map_replicate, natProduct_replicate]

/-- A second maximizer has outer sum ten, so its next integer need not be a palindrome. -/
theorem profileCount_ten_nines (k : Nat) (c : Option Nat) (hc : centerCount c = 1) :
    profileCount (10 :: List.replicate k 9) c = 9 * 10 ^ k := by
  simp [profileCount, hc, pairCount, List.map_replicate, natProduct_replicate]

theorem sharp_profile_bound (k : Nat) :
    (∀ s h c, h.length = k → profileCount (s :: h) c ≤ 9 * 10 ^ k) ∧
    profileCount (9 :: List.replicate k 9) none = 9 * 10 ^ k ∧
    profileCount (9 :: List.replicate k 9) (some 0) = 9 * 10 ^ k := by
  refine ⟨?_, profileCount_nines k none rfl, profileCount_nines k (some 0) (by decide)⟩
  intro s h c hh
  simpa [hh] using profileCount_cons_le s h c

#print axioms pairCount_inner_le
#print axioms pairCount_outer_le
#print axioms centerCount_le
#print axioms pairProduct_le
#print axioms profileCount_cons_le
#print axioms profileCount_single_le
#print axioms natProduct_replicate
#print axioms profileCount_nines
#print axioms profileCount_ten_nines
#print axioms sharp_profile_bound

end Agent101
