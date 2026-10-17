import P196.Agent101DigitSplit.Agent101NumericFibers
import P196.Agent101ProtectedFamily.FamilyCardinality

/-!
Agent #101. Complete ordinary-integer digit splitting of Agent #3's protected
coefficient-word family. The counted union includes every digit split of
each specified profile, with no duplicates. It is not asserted to contain
every possible two-step predecessor of the family's common image.

Agent #3's definitions and cardinality module are imported unchanged from
PR #81, commit 5084eadce9a7e95e518332c29e8404b00214bd0f (mathematical source
bytes identical to commit 6576cee93d18145c638f298b0abcb1cd0a0f451e).
The counting statements hold for k = 0 as well as positive k; later
finite-horizon statements retain their separate positive-k hypothesis.
-/

namespace Agent101.Protected

open P196.Agent3.OverflowHorizon

/-- All ordinary integers whose pair-sum profile is one of the protected
family's complete mirrored words, with every decimal digit split included. -/
def protectedSeeds (m k : Nat) : List Nat :=
  (allBits m).flatMap fun xs => numericFiber (inputHalf xs k) none

theorem coefficientWord_inputHalf (xs : List Bool) (k : Nat) :
    coefficientWord (inputHalf xs k) none = inputWord xs k := by
  simp [coefficientWord, inputWord]

theorem coefficientWord_inputHalf_bounded (xs : List Bool) (k : Nat) :
    ∀ s ∈ coefficientWord (inputHalf xs k) none, s ≤ 18 := by
  rw [coefficientWord_inputHalf]
  exact inputWord_bounded xs k

/-- Complete numerical membership in one fixed profile, at its ordinary
decimal width; no chosen digit realization is assumed. -/
theorem mem_inputFiber (xs : List Bool) (k n : Nat) :
    n ∈ numericFiber (inputHalf xs k) none ↔
      decimalWidth n (2 * (xs.length + k + 1)) ∧
      Lychrel196.step n = natValue (inputWord xs k) := by
  rw [mem_numericFiber _ _ _ (coefficientWord_inputHalf_bounded xs k),
    coefficientWord_inputHalf, inputWord_length]

theorem mem_protectedSeeds (m k n : Nat) :
    n ∈ protectedSeeds m k ↔ ∃ xs : List Bool, xs.length = m ∧
      n ∈ numericFiber (inputHalf xs k) none := by
  simp only [protectedSeeds, List.mem_flatMap, mem_allBits_iff]

/-- A complete specification by ordinary numerical step equations, with
the family-index witness ranging over all binary words of length m. -/
theorem mem_protectedSeeds_numeric (m k n : Nat) :
    n ∈ protectedSeeds m k ↔
      decimalWidth n (2 * (m + k + 1)) ∧
      ∃ xs : List Bool, xs.length = m ∧
        Lychrel196.step n = natValue (inputWord xs k) := by
  rw [mem_protectedSeeds]
  constructor
  · rintro ⟨xs, hlen, hn⟩
    obtain ⟨hw, hs⟩ := (mem_inputFiber xs k n).mp hn
    exact ⟨by simpa [hlen] using hw, xs, hlen, hs⟩
  · rintro ⟨hw, xs, hlen, hs⟩
    refine ⟨xs, hlen, (mem_inputFiber xs k n).mpr ?_⟩
    exact ⟨by simpa [hlen] using hw, hs⟩

theorem mem_protectedSeeds_width (m k n : Nat)
    (hn : n ∈ protectedSeeds m k) :
    decimalWidth n (2 * (m + k + 1)) :=
  ((mem_protectedSeeds_numeric m k n).mp hn).1

theorem mem_protectedSeeds_positive (m k n : Nat)
    (hn : n ∈ protectedSeeds m k) : 0 < n := by
  obtain ⟨xs, _, hx⟩ := (mem_protectedSeeds m k n).mp hn
  obtain ⟨ds, hd, _, hv⟩ := (mem_numericFiber_digits _ _ _).mp hx
  rw [← hv]
  exact natValue_positive ds hd

/-- A numerical seed cannot belong to two different protected profiles.
The argument uses finite canonical digit-list injectivity, not infinite
digit-function equality and not injectivity of the two-step map. -/
theorem inputFiber_index_unique (xs ys : List Bool) (k n : Nat)
    (hx : n ∈ numericFiber (inputHalf xs k) none)
    (hy : n ∈ numericFiber (inputHalf ys k) none) : xs = ys := by
  obtain ⟨a, ha, hpa, hva⟩ := (mem_numericFiber_digits _ _ _).mp hx
  obtain ⟨b, hb, hpb, hvb⟩ := (mem_numericFiber_digits _ _ _).mp hy
  have hab := natValue_injective_canonical a b ha hb (hva.trans hvb.symm)
  rw [coefficientWord_inputHalf] at hpa hpb
  exact inputWord_injective k xs ys
    (hpa.symm.trans ((congrArg digitPairSums hab).trans hpb))

theorem inputFibers_disjoint (xs ys : List Bool) (k : Nat) (hxy : xs ≠ ys) :
    ∀ n, n ∈ numericFiber (inputHalf xs k) none →
      n ∈ numericFiber (inputHalf ys k) none → False := by
  intro n hx hy
  exact hxy (inputFiber_index_unique xs ys k n hx hy)

theorem protectedSeeds_nodup (m k : Nat) : (protectedSeeds m k).Nodup := by
  apply List.pairwise_flatMap.mpr
  constructor
  · intro xs _
    exact numericFiber_nodup (inputHalf xs k) none
  · apply List.Pairwise.imp (R := fun xs ys : List Bool => xs ≠ ys) ?_
      (allBits_nodup m)
    intro xs ys hxy n hn p hp heq
    subst p
    exact hxy (inputFiber_index_unique xs ys k n hn hp)

theorem natProduct_append (xs ys : List Nat) :
    natProduct (xs ++ ys) = natProduct xs * natProduct ys := by
  induction xs with
  | nil => simp [natProduct]
  | cons a xs ih => simp [natProduct, ih, Nat.mul_assoc]

/-- Each inner false choice contributes six splits, each true choice five;
every protective 18 contributes one. The outer 14 contributes five. -/
theorem length_inputFiber (xs : List Bool) (k : Nat) :
    (numericFiber (inputHalf xs k) none).length =
      5 * natProduct (xs.map fun b => pairCount false (choice b)) := by
  rw [length_numericFiber]
  simp only [inputHalf, List.singleton_append, profileCount,
    List.map_append, List.map_map, List.map_replicate, natProduct_append,
    natProduct_replicate]
  simp [pairCount, centerCount, natProduct_append, natProduct_replicate, Function.comp_def]

theorem length_inputFiber_cons (b : Bool) (xs : List Bool) (k : Nat) :
    (numericFiber (inputHalf (b :: xs) k) none).length =
      pairCount false (choice b) * (numericFiber (inputHalf xs k) none).length := by
  rw [length_inputFiber, length_inputFiber]
  simp only [List.map_cons, natProduct, Nat.mul_left_comm]

theorem length_flatMap_scale {α β γ : Type} (xs : List α)
    (f : α → List β) (g : α → List γ) (a : Nat)
    (h : ∀ x ∈ xs, (f x).length = a * (g x).length) :
    (xs.flatMap f).length = a * (xs.flatMap g).length := by
  induction xs with
  | nil => simp
  | cons x xs ih =>
    have hx := h x (by simp)
    have ht : ∀ y ∈ xs, (f y).length = a * (g y).length := by
      intro y hy
      exact h y (by simp [hy])
    simp only [List.flatMap_cons, List.length_append, hx, ih ht, Nat.mul_add]

theorem length_protectedSeeds_cons_choice (b : Bool) (m k : Nat) :
    ((allBits m).flatMap fun xs =>
      numericFiber (inputHalf (b :: xs) k) none).length =
      pairCount false (choice b) * (protectedSeeds m k).length := by
  exact length_flatMap_scale (allBits m) _ _ _
    (fun xs _ => length_inputFiber_cons b xs k)

/-- Exact cardinality of the whole disjoint union of complete integer
digit-split fibers: five outer choices times eleven choices per bit. -/
theorem length_protectedSeeds (m k : Nat) :
    (protectedSeeds m k).length = 5 * 11 ^ m := by
  induction m with
  | zero =>
    simp only [protectedSeeds, allBits, List.flatMap_cons, List.flatMap_nil,
      List.append_nil, length_inputFiber, List.map_nil, natProduct, Nat.pow_zero]
  | succ m ih =>
    change ((allBits (m + 1)).flatMap fun xs =>
      numericFiber (inputHalf xs k) none).length = _
    simp only [allBits, List.flatMap_append, List.flatMap_map, List.length_append]
    rw [length_protectedSeeds_cons_choice false m k,
      length_protectedSeeds_cons_choice true m k, ih]
    simp only [choice, Bool.false_eq_true, ↓reduceIte, pairCount,
      Nat.reduceLeDiff, Nat.reduceAdd, Nat.reduceSub, Nat.pow_succ]
    omega

/-- Exact counted ordinary-integer family, including complete numerical
membership, positivity, common input width, and no repeated seed. -/
theorem protectedSeeds_exact (m k : Nat) :
    (protectedSeeds m k).length = 5 * 11 ^ m ∧
    (protectedSeeds m k).Nodup ∧
    ∀ n ∈ protectedSeeds m k,
      0 < n ∧ decimalWidth n (2 * (m + k + 1)) := by
  exact ⟨length_protectedSeeds m k, protectedSeeds_nodup m k,
    fun n hn => ⟨mem_protectedSeeds_positive m k n hn,
      mem_protectedSeeds_width m k n hn⟩⟩

#print axioms protectedSeeds
#print axioms coefficientWord_inputHalf
#print axioms coefficientWord_inputHalf_bounded
#print axioms mem_inputFiber
#print axioms mem_protectedSeeds
#print axioms mem_protectedSeeds_numeric
#print axioms mem_protectedSeeds_width
#print axioms mem_protectedSeeds_positive
#print axioms inputFiber_index_unique
#print axioms inputFibers_disjoint
#print axioms protectedSeeds_nodup
#print axioms natProduct_append
#print axioms length_inputFiber
#print axioms length_inputFiber_cons
#print axioms length_flatMap_scale
#print axioms length_protectedSeeds_cons_choice
#print axioms length_protectedSeeds
#print axioms protectedSeeds_exact

end Agent101.Protected
