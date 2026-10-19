import P196.BidirectionalWordDecoder.Numeric

/-!
# Exact coefficient thresholds for paired positional values

At a supplied width, the original low and high positional values are
injective without a coefficient bound through width two, through bound
100 at width three, and through bound 90 at every larger width. The
uniform bound over all shared widths is therefore exactly 90.

The width-three conclusion concerns injectivity, not correctness of the
recursive decoder above its bound of 90. Explicit collisions at 101 and
91 prove necessity. The latter family has positive first coefficients
and is extended to every width at least four by a symbolic zero suffix.
No phase, normalization, or ordinary-orbit assertion is made here.
-/

namespace Agent5.BidirectionalWordDecoder

open Agent115.ExteriorFactorization

/-- Injectivity of both original positional values at one fixed width
and one inclusive coefficient bound. -/
def ValuesInjectiveAt (n M : Nat) : Prop :=
  ∀ A B : List Nat, A.length = n → B.length = n →
    (∀ x ∈ A, x ≤ M) → (∀ x ∈ B, x ≤ M) →
    lowValue A = lowValue B → highValue A = highValue B → A = B

/-- Uniform injectivity over every shared width at the given inclusive
coefficient bound. The width is still supplied for each comparison. -/
def ValuesInjectiveUpTo (M : Nat) : Prop :=
  ∀ n : Nat, ValuesInjectiveAt n M

private theorem values_injective_at_of_le_ninety (n M : Nat) (hM : M ≤ 90) :
    ValuesInjectiveAt n M := by
  intro A B hlenA hlenB hA hB hlo hhi
  have hA90 : ∀ x ∈ A, x ≤ 90 := fun x hx => Nat.le_trans (hA x hx) hM
  have hB90 : ∀ x ∈ B, x ≤ 90 := fun x hx => Nat.le_trans (hB x hx) hM
  have hlen : A.length = B.length := hlenA.trans hlenB.symm
  calc
    A = decodeValues A.length (lowValue A) (highValue A) :=
      (decodeValues_correct A hA90).symm
    _ = decodeValues B.length (lowValue B) (highValue B) := by rw [hlen, hlo, hhi]
    _ = B := decodeValues_correct B hB90

private theorem length_two_word (B : List Nat) (h : B.length = 2) :
    ∃ x y : Nat, B = [x, y] := by
  cases B with
  | nil => simp at h
  | cons x xs =>
    cases xs with
    | nil => simp at h
    | cons y ys =>
      have hys : ys = [] := List.length_eq_zero_iff.mp (by simpa using h)
      subst ys
      exact ⟨x, y, rfl⟩

private theorem length_three_word (B : List Nat) (h : B.length = 3) :
    ∃ x y z : Nat, B = [x, y, z] := by
  cases B with
  | nil => simp at h
  | cons x xs =>
    have hxs : xs.length = 2 := by simpa using h
    obtain ⟨y, z, rfl⟩ := length_two_word xs hxs
    exact ⟨x, y, z, rfl⟩

private theorem values_injective_zero (M : Nat) : ValuesInjectiveAt 0 M := by
  intro A B hlenA hlenB _ _ _ _
  have hA : A = [] := List.length_eq_zero_iff.mp hlenA
  have hB : B = [] := List.length_eq_zero_iff.mp hlenB
  rw [hA, hB]

private theorem values_injective_one (M : Nat) : ValuesInjectiveAt 1 M := by
  intro A B hlenA hlenB _ _ hlo _
  obtain ⟨x, rfl⟩ := List.length_eq_one_iff.mp hlenA
  obtain ⟨y, rfl⟩ := List.length_eq_one_iff.mp hlenB
  have hxy : x = y := by simpa [lowValue] using hlo
  rw [hxy]

private theorem values_injective_two (M : Nat) : ValuesInjectiveAt 2 M := by
  intro A B hlenA hlenB _ _ hlo hhi
  obtain ⟨a₀, a₁, rfl⟩ := length_two_word A hlenA
  obtain ⟨b₀, b₁, rfl⟩ := length_two_word B hlenB
  simp only [lowValue, highValue, List.foldl_cons, List.foldl_nil,
    Nat.mul_zero, Nat.zero_add, Nat.add_zero] at hlo hhi
  have h₀ : a₀ = b₀ := by omega
  have h₁ : a₁ = b₁ := by omega
  rw [h₀, h₁]

private theorem values_injective_short (n M : Nat) (hn : n ≤ 2) :
    ValuesInjectiveAt n M := by
  have hc : n = 0 ∨ n = 1 ∨ n = 2 := by omega
  rcases hc with rfl | rfl | rfl
  · exact values_injective_zero M
  · exact values_injective_one M
  · exact values_injective_two M

private theorem values_injective_three (M : Nat) (hM : M ≤ 100) :
    ValuesInjectiveAt 3 M := by
  intro A B hlenA hlenB hA hB hlo hhi
  obtain ⟨a₀, a₁, a₂, rfl⟩ := length_three_word A hlenA
  obtain ⟨b₀, b₁, b₂, rfl⟩ := length_three_word B hlenB
  have ha₁ : a₁ ≤ 100 := Nat.le_trans (hA a₁ (by simp)) hM
  have hb₁ : b₁ ≤ 100 := Nat.le_trans (hB b₁ (by simp)) hM
  simp only [lowValue, highValue, List.foldl_cons, List.foldl_nil,
    Nat.mul_zero, Nat.zero_add, Nat.add_zero] at hlo hhi
  have h₀ : a₀ = b₀ := by omega
  have h₁ : a₁ = b₁ := by omega
  have h₂ : a₂ = b₂ := by omega
  rw [h₀, h₁, h₂]

/-- The first width-three obstruction uses coefficient 101. Both words
have the same original low and high value, namely 1010. -/
theorem width_three_collision :
    lowValue [10, 0, 10] = 1010 ∧ highValue [10, 0, 10] = 1010 ∧
      lowValue [0, 101, 0] = 1010 ∧ highValue [0, 101, 0] = 1010 ∧
      ([10, 0, 10] : List Nat) ≠ [0, 101, 0] := by
  decide

private theorem not_values_injective_three (M : Nat) (hM : 101 ≤ M) :
    ¬ValuesInjectiveAt 3 M := by
  intro h
  obtain ⟨hVA, hHA, hVB, hHB, hne⟩ := width_three_collision
  apply hne
  apply h [10, 0, 10] [0, 101, 0] rfl rfl
  · intro x hx
    simp only [List.mem_cons, List.not_mem_nil, or_false] at hx
    omega
  · intro x hx
    simp only [List.mem_cons, List.not_mem_nil, or_false] at hx
    omega
  · exact hVA.trans hVB.symm
  · exact hHA.trans hHB.symm

private theorem lowValue_replicate_zero (m : Nat) :
    lowValue (List.replicate m 0) = 0 := by
  induction m with
  | zero => rfl
  | succ m ih => simp [List.replicate_succ, lowValue, ih]

private theorem lowValue_zero_padding (B : List Nat) (m : Nat) :
    lowValue (B ++ List.replicate m 0) = lowValue B := by
  rw [lowValue_append, lowValue_replicate_zero, Nat.mul_zero, Nat.add_zero]

private theorem highValue_zero_padding (B : List Nat) (m : Nat) :
    highValue (B ++ List.replicate m 0) = highValue B * 10 ^ m := by
  have h := rhoNum_append_replicate 0 B m
  simp only [rhoNum, Nat.add_zero] at h
  have hmul : 10 ^ m * (9 * highValue B) = 9 * (highValue B * 10 ^ m) := by
    ac_rfl
  rw [hmul] at h
  omega

/-- At every width at least four, bound 91 permits a collision even when
both first coefficients are positive. The fixed four-coefficient pair is
extended by a shared zero suffix; no bounded width search is used. -/
theorem width_ge_four_collision (n : Nat) (hn : 4 ≤ n) :
    ∃ A B : List Nat,
      A.length = n ∧ B.length = n ∧
      (∀ x ∈ A, x ≤ 91) ∧ (∀ x ∈ B, x ≤ 91) ∧
      A.head? = some 11 ∧ B.head? = some 1 ∧ A ≠ B ∧
      lowValue A = lowValue B ∧ highValue A = highValue B := by
  let A := [11, 0, 0, 11] ++ List.replicate (n - 4) 0
  let B := [1, 91, 91, 1] ++ List.replicate (n - 4) 0
  refine ⟨A, B, ?_, ?_, ?_, ?_, rfl, rfl, ?_, ?_, ?_⟩
  · dsimp only [A]
    rw [List.length_append, List.length_replicate]
    change 4 + (n - 4) = n
    omega
  · dsimp only [B]
    rw [List.length_append, List.length_replicate]
    change 4 + (n - 4) = n
    omega
  · intro x hx
    rcases List.mem_append.mp hx with hx | hx
    · simp only [List.mem_cons, List.not_mem_nil, or_false] at hx
      omega
    · have hx0 := List.eq_of_mem_replicate hx
      omega
  · intro x hx
    rcases List.mem_append.mp hx with hx | hx
    · simp only [List.mem_cons, List.not_mem_nil, or_false] at hx
      omega
    · have hx0 := List.eq_of_mem_replicate hx
      omega
  · intro heq
    have hbad : (some 11 : Option Nat) = some 1 := congrArg List.head? heq
    cases hbad
  · dsimp only [A, B]
    rw [lowValue_zero_padding, lowValue_zero_padding]
    decide
  · dsimp only [A, B]
    rw [highValue_zero_padding, highValue_zero_padding]
    rfl

private theorem not_values_injective_ge_four (n M : Nat)
    (hn : 4 ≤ n) (hM : 91 ≤ M) : ¬ValuesInjectiveAt n M := by
  intro h
  obtain ⟨A, B, hlenA, hlenB, hA, hB, _, _, hne, hlo, hhi⟩ :=
    width_ge_four_collision n hn
  exact hne (h A B hlenA hlenB
    (fun x hx => Nat.le_trans (hA x hx) hM)
    (fun x hx => Nat.le_trans (hB x hx) hM) hlo hhi)

/-- The exact coefficient threshold at each supplied width. Widths zero,
one, and two need no bound; width three allows 100; larger widths allow 90. -/
theorem values_injective_at_iff (n M : Nat) :
    ValuesInjectiveAt n M ↔ n ≤ 2 ∨ (n = 3 ∧ M ≤ 100) ∨ M ≤ 90 := by
  constructor
  · intro h
    by_cases hshort : n ≤ 2
    · exact Or.inl hshort
    by_cases hthree : n = 3
    · apply Or.inr
      apply Or.inl
      refine ⟨hthree, ?_⟩
      by_cases hsmall : M ≤ 100
      · exact hsmall
      · have hm : 101 ≤ M := by omega
        exact False.elim
          (not_values_injective_three M hm (by simpa only [hthree] using h))
    · apply Or.inr
      apply Or.inr
      by_cases hsmall : M ≤ 90
      · exact hsmall
      · have hn : 4 ≤ n := by omega
        have hm : 91 ≤ M := by omega
        exact False.elim (not_values_injective_ge_four n M hn hm h)
  · intro h
    rcases h with hshort | ⟨rfl, hthree⟩ | hlarge
    · exact values_injective_short n M hshort
    · exact values_injective_three M hthree
    · exact values_injective_at_of_le_ninety n M hlarge

/-- The largest coefficient bound supporting injectivity uniformly over
every shared width is exactly 90. -/
theorem values_injective_bound_iff (M : Nat) :
    ValuesInjectiveUpTo M ↔ M ≤ 90 := by
  constructor
  · intro h
    have hfour := (values_injective_at_iff 4 M).mp (h 4)
    omega
  · intro hM n
    exact values_injective_at_of_le_ninety n M hM

#print axioms width_three_collision
#print axioms width_ge_four_collision
#print axioms values_injective_at_iff
#print axioms values_injective_bound_iff

end Agent5.BidirectionalWordDecoder
