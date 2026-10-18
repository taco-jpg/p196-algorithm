import P196.Drafts.Agent103ResidualFiveFibers.ResidualFiveFibers

/-!
# Residue transport through the original finite digit enumeration

The decimal value and all digit lists below are Agent #101's original objects.
The finite pair census is checked by the Lean kernel. The parameter `r` is
arbitrary; no bounded search over `r` is used in the distribution theorem.
-/

namespace Agent103.ResidualFiveResidues

open Agent101 DecimalDigits

theorem natValue_nil : natValue [] = 0 := rfl

theorem natValue_cons (a : Nat) (ds : List Nat) :
    natValue (a :: ds) = a + 10 * natValue ds := by
  simp [natValue, value_shift, digitFn]
  rfl

theorem natValue_append (xs ys : List Nat) :
    natValue (xs ++ ys) = natValue xs + 10 ^ xs.length * natValue ys := by
  induction xs with
  | nil => simp [natValue_nil]
  | cons a xs ih =>
    simp only [List.cons_append, natValue_cons, List.length_cons, ih, Nat.pow_succ]
    simp [Nat.mul_add, Nat.add_assoc, Nat.mul_assoc, Nat.mul_comm, Nat.mul_left_comm]

theorem natValue_wrap (a b : Nat) (ds : List Nat) :
    natValue (wrapDigits a b ds) =
      a + 10 * natValue ds + b * 10 ^ (ds.length + 1) := by
  simp [wrapDigits, natValue_cons, natValue_append, natValue_nil,
    Nat.pow_succ, Nat.mul_add, Nat.add_assoc, Nat.mul_assoc,
    Nat.mul_comm, Nat.mul_left_comm]

theorem pow_ten_even_mod11 (r : Nat) : 10 ^ (2 * r) % 11 = 1 := by
  induction r with
  | zero => decide
  | succ r ih =>
    rw [show 2 * (r + 1) = 2 * r + 2 by omega, Nat.pow_add, Nat.mul_mod, ih]

theorem natValue_wrap_mod11 (a b r : Nat) (ds : List Nat)
    (hlen : ds.length = 2 * r) :
    natValue (wrapDigits a b ds) % 11 =
      (a + 10 * (natValue ds % 11) + b * 10) % 11 := by
  rw [natValue_wrap, hlen, Nat.pow_succ]
  simp only [Nat.add_mod, Nat.mul_mod, pow_ten_even_mod11, Nat.mod_mod,
    Nat.reduceMod, Nat.one_mul]

/-- Complete original raw digit lists for `r` complementary pairs of sum nine. -/
def rawNine (r : Nat) : List (List Nat) := rawWords (List.replicate r 9) none

/-- A residue count in that complete list, retaining all original multiplicities. -/
def rawCount (r t : Nat) : Nat :=
  (rawNine r).countP (fun ds => decide (natValue ds % 11 = t))

theorem rawNine_zero : rawNine 0 = [[]] := rfl

theorem rawNine_succ (r : Nat) :
    rawNine (r + 1) = (pairChoices false 9).flatMap
      (fun p => (rawNine r).map (wrapDigits p.1 p.2)) := rfl

theorem rawNine_length (r : Nat) : (rawNine r).length = 10 ^ r := by
  unfold rawNine
  rw [length_rawWords]
  simp [centerCount, List.map_replicate, natProduct_replicate, pairCount]

theorem rawNine_word_length (r : Nat) (ds : List Nat) (h : ds ∈ rawNine r) :
    ds.length = 2 * r := by
  have hh := (mem_rawWords (List.replicate r 9) none ds).mp h
  simpa [length_coefficientWord] using hh.1

/-- Splitting a rectangular enumeration at one word preserves its exact count. -/
theorem count_grid_cons {α β γ : Type} (ps : List α) (ws : List β)
    (w : β) (f : α → β → γ) (P : γ → Bool) :
    ((ps.flatMap fun p => (w :: ws).map (f p)).countP P) =
      ((ps.map fun p => f p w).countP P) +
        ((ps.flatMap fun p => ws.map (f p)).countP P) := by
  induction ps with
  | nil => simp
  | cons p ps ih =>
    simp only [List.flatMap_cons, List.countP_append]
    rw [ih]
    simp only [List.map_cons, List.countP_cons]
    omega

theorem pairChoices_nine :
    pairChoices false 9 =
      [(0, 9), (1, 8), (2, 7), (3, 6), (4, 5),
       (5, 4), (6, 3), (7, 2), (8, 1), (9, 0)] := by decide

/-- For each fixed old residue, the ten ordered pairs reach each new residue
except the negative of that old residue, exactly once. -/
theorem pair_nine_residue_census : ∀ k t : Fin 11,
    (pairChoices false 9).countP
      (fun p => decide ((p.1 + 10 * k.val + p.2 * 10) % 11 = t.val)) =
        if k.val = (10 * t.val) % 11 then 0 else 1 := by
  rw [pairChoices_nine]
  decide

theorem wrapped_nine_single_count (r t : Nat) (ht : t < 11)
    (ds : List Nat) (hlen : ds.length = 2 * r) :
    ((pairChoices false 9).map (fun p => wrapDigits p.1 p.2 ds)).countP
      (fun xs => decide (natValue xs % 11 = t)) =
        if natValue ds % 11 = (10 * t) % 11 then 0 else 1 := by
  rw [List.countP_map]
  have heq :
      (pairChoices false 9).countP
          ((fun xs => decide (natValue xs % 11 = t)) ∘
            (fun p => wrapDigits p.1 p.2 ds)) =
        (pairChoices false 9).countP
          (fun p => decide ((p.1 + 10 * (natValue ds % 11) + p.2 * 10) % 11 = t)) := by
    apply List.countP_congr
    intro p hp
    simp only [Function.comp_apply, natValue_wrap_mod11 p.1 p.2 r ds hlen]
  rw [heq]
  exact pair_nine_residue_census ⟨natValue ds % 11, Nat.mod_lt _ (by decide)⟩ ⟨t, ht⟩

/-- The missing class is counted in the same original input list. -/
theorem wrapped_nine_count_complement (r t : Nat) (ht : t < 11)
    (ws : List (List Nat)) (hlen : ∀ ds ∈ ws, ds.length = 2 * r) :
    ((pairChoices false 9).flatMap
      (fun p => ws.map (wrapDigits p.1 p.2))).countP
        (fun ds => decide (natValue ds % 11 = t)) +
      ws.countP (fun ds => decide (natValue ds % 11 = (10 * t) % 11)) = ws.length := by
  induction ws with
  | nil => simp
  | cons ds ws ih =>
    rw [count_grid_cons]
    rw [wrapped_nine_single_count r t ht ds (hlen ds (by simp))]
    rw [List.countP_cons, List.length_cons]
    have hh := ih (fun x hx => hlen x (by simp [hx]))
    by_cases h : natValue ds % 11 = (10 * t) % 11 <;> simp [h] <;> omega

/-- An all-parameter recurrence for the actual original raw enumeration. -/
theorem rawCount_succ_complement (r t : Nat) (ht : t < 11) :
    rawCount (r + 1) t + rawCount r ((10 * t) % 11) = 10 ^ r := by
  unfold rawCount
  rw [rawNine_succ, ← rawNine_length r]
  exact wrapped_nine_count_complement r t ht (rawNine r) (rawNine_word_length r)

theorem negative_residue_nonzero : ∀ t : Fin 11,
    t.val ≠ 0 → (10 * t.val) % 11 ≠ 0 := by decide

/-- Every one of the ten nonzero residue classes has the same exact count. -/
theorem rawCount_nonzero (r t : Nat) (ht : t < 11) (hz : t ≠ 0) :
    rawCount r t = rawCount r 1 := by
  induction r generalizing t with
  | zero => simp [rawCount, rawNine_zero, natValue_nil, Ne.symm hz]
  | succ r ih =>
    have h1 := rawCount_succ_complement r 1 (by decide)
    have ht' := rawCount_succ_complement r t ht
    have hn := negative_residue_nonzero ⟨t, ht⟩ hz
    have heq := ih ((10 * t) % 11) (Nat.mod_lt _ (by decide)) hn
    have heq1 := ih 10 (by decide) (by decide)
    simp only [Nat.reduceMul, Nat.reduceMod] at h1
    omega

theorem rawCount_zero_recurrence (r : Nat) :
    rawCount (r + 1) 0 + rawCount r 0 = 10 ^ r := by
  simpa using rawCount_succ_complement r 0 (by decide)

theorem rawCount_nonzero_recurrence (r : Nat) :
    rawCount (r + 1) 1 + rawCount r 1 = 10 ^ r := by
  have h := rawCount_succ_complement r 1 (by decide)
  simpa [rawCount_nonzero r 10 (by decide) (by decide)] using h

#print axioms natValue_nil
#print axioms natValue_cons
#print axioms natValue_append
#print axioms natValue_wrap
#print axioms pow_ten_even_mod11
#print axioms natValue_wrap_mod11
#print axioms rawNine
#print axioms rawCount
#print axioms rawNine_zero
#print axioms rawNine_succ
#print axioms rawNine_length
#print axioms rawNine_word_length
#print axioms count_grid_cons
#print axioms pairChoices_nine
#print axioms pair_nine_residue_census
#print axioms wrapped_nine_single_count
#print axioms wrapped_nine_count_complement
#print axioms rawCount_succ_complement
#print axioms negative_residue_nonzero
#print axioms rawCount_nonzero
#print axioms rawCount_zero_recurrence
#print axioms rawCount_nonzero_recurrence

end Agent103.ResidualFiveResidues
