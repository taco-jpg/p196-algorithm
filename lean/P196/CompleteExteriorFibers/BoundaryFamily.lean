import P196.CompleteExteriorFibers.Definitions

/-!
# Complete stream collisions at both boundary phases

At phase zero or eighteen, every width at least three admits two distinct
valid words with the same two complete original streams. Their calculated
high carries are zero and one. The high numerator and its actual denominator
both scale by ten, so equality holds at every cutoff.

The words share a symbolic block of zeros. The proof uses the existing
positional value, phase-padding, normalization, and fractional scaling
identities; no bounded enumeration or new scan induction is needed.
-/

namespace Agent5.CompleteExteriorFibers

open P196.Agent7.Finite Agent115.ExteriorFactorization
open Agent5.ExactDigitStreams

/-- The boundary witness with first coefficient one. -/
def boundaryWordA (c m : Nat) : List Nat :=
  ([1, 1] ++ List.replicate m 0) ++ [11 - c / 9]

/-- The boundary witness with first coefficient eleven. -/
def boundaryWordB (c m : Nat) : List Nat :=
  (([11] ++ List.replicate m 0) ++ [10]) ++ [(11 - c / 9) - 1]

private theorem boundary_lengths (c m : Nat) :
    (boundaryWordA c m).length = m + 3 ∧
      (boundaryWordB c m).length = m + 3 := by
  simp only [boundaryWordA, boundaryWordB, List.length_append,
    List.length_cons, List.length_nil, List.length_replicate]
  omega

private theorem lowValue_append_zeros (B : List Nat) (m : Nat) :
    lowValue (B ++ List.replicate m 0) = lowValue B := by
  have h := zValue_append_replicate 0 B m
  simp [zValue] at h
  omega

private theorem highValue_append_zeros (B : List Nat) (m : Nat) :
    highValue (B ++ List.replicate m 0) = 10 ^ m * highValue B := by
  have h := rhoNum_append_replicate 0 B m
  simp only [rhoNum, Nat.add_zero] at h
  have hm : 10 ^ m * (9 * highValue B) = 9 * (10 ^ m * highValue B) := by
    ac_rfl
  rw [hm] at h
  omega

/-- The two words have the same low value. Their high values differ by the
exact scaling that compensates for opposite actual high carries. -/
theorem boundary_values (c m : Nat) (hc : c = 0 ∨ c = 18) :
    lowValue (boundaryWordA c m) = 11 + (11 - c / 9) * 10 ^ (m + 2) ∧
      lowValue (boundaryWordB c m) = lowValue (boundaryWordA c m) ∧
      highValue (boundaryWordA c m) = 11 * 10 ^ (m + 1) + (11 - c / 9) ∧
      highValue (boundaryWordB c m) = 10 * highValue (boundaryWordA c m) + c := by
  have hlowA : lowValue (boundaryWordA c m) =
      11 + (11 - c / 9) * 10 ^ (m + 2) := by
    have hlen : (([1, 1] : List Nat) ++ List.replicate m 0).length = m + 2 := by
      simp
    unfold boundaryWordA
    rw [lowValue_append, lowValue_append_zeros, hlen]
    simp [lowValue, Nat.add_assoc, Nat.add_comm, Nat.mul_comm]
  have hlowB : lowValue (boundaryWordB c m) =
      11 + (11 - c / 9) * 10 ^ (m + 2) := by
    unfold boundaryWordB
    rw [lowValue_append, lowValue_append, lowValue_append_zeros]
    rcases hc with rfl | rfl <;>
      simp [lowValue, Nat.pow_add, Nat.mul_add, Nat.add_mul, Nat.mul_assoc] <;>
      omega
  have hhighA : highValue (boundaryWordA c m) =
      11 * 10 ^ (m + 1) + (11 - c / 9) := by
    unfold boundaryWordA
    rw [highValue_append_single, highValue_append_zeros]
    simp [highValue, Nat.pow_succ, Nat.mul_assoc, Nat.mul_comm, Nat.mul_left_comm]
  have hhighB : highValue (boundaryWordB c m) =
      10 * highValue (boundaryWordA c m) + c := by
    rw [hhighA]
    unfold boundaryWordB
    rw [highValue_append_single, highValue_append_single, highValue_append_zeros]
    rcases hc with rfl | rfl <;>
      simp [highValue, Nat.pow_succ, Nat.mul_add, Nat.add_mul, Nat.mul_assoc] <;>
      omega
  exact ⟨hlowA, hlowB.trans hlowA.symm, hhighA, hhighB⟩

private theorem boundary_valid (c m : Nat) (hc : c = 0 ∨ c = 18) :
    validOuter { c := c, B := boundaryWordA c m } = true ∧
      validOuter { c := c, B := boundaryWordB c m } = true := by
  rcases hc with rfl | rfl <;>
    simp [boundaryWordA, boundaryWordB, validOuter, List.getLast?_append,
      List.getLast?_cons]

private theorem boundary_ne (c m : Nat) : boundaryWordA c m ≠ boundaryWordB c m := by
  simp [boundaryWordA, boundaryWordB]

/-- The first coefficients force opposite actual high carries, for every
natural phase. The boundary restrictions are needed only for stream equality. -/
theorem boundary_carries (c m : Nat) :
    (normalize (boundaryWordA c m).reverse (if 10 ≤ c then 1 else 0)).2 = 0 ∧
      (normalize (boundaryWordB c m).reverse (if 10 ≤ c then 1 else 0)).2 = 1 := by
  let X : List Nat := (1 :: List.replicate m 0) ++ [11 - c / 9]
  let Y : List Nat := (List.replicate m 0 ++ [10]) ++ [(11 - c / 9) - 1]
  have hA : boundaryWordA c m = 1 :: X := rfl
  have hB : boundaryWordB c m = 11 :: Y := rfl
  have ht : 11 - c / 9 ≤ 11 := Nat.sub_le _ _
  have hX : ∀ x ∈ X, x ≤ 18 := by
    intro x hx
    simp only [X, List.mem_append, List.mem_cons, List.mem_replicate,
      List.mem_singleton, List.mem_nil_iff, or_false] at hx
    omega
  have hY : ∀ x ∈ Y, x ≤ 18 := by
    intro x hx
    simp only [Y, List.mem_append, List.mem_replicate, List.mem_singleton] at hx
    omega
  have hk : (if 10 ≤ c then 1 else 0) ≤ 1 := by
    split <;> omega
  have hgX := normalize_carry_le X.reverse (if 10 ≤ c then 1 else 0)
    (fun x hx => hX x (List.mem_reverse.mp hx)) hk
  have hgY := normalize_carry_le Y.reverse (if 10 ≤ c then 1 else 0)
    (fun x hx => hY x (List.mem_reverse.mp hx)) hk
  constructor
  · rw [hA, List.reverse_cons, normalize_append_single]
    change (1 + (normalize X.reverse (if 10 ≤ c then 1 else 0)).2) / 10 = 0
    omega
  · rw [hB, List.reverse_cons, normalize_append_single]
    change (11 + (normalize Y.reverse (if 10 ≤ c then 1 else 0)).2) / 10 = 1
    omega

/-- The literal two-stream equality uses each word's own original width
and calculated high carry, and holds at every cutoff. -/
theorem boundary_sameStreams (c m : Nat) (hc : c = 0 ∨ c = 18) :
    sameStreams { c := c, B := boundaryWordA c m }
      { c := c, B := boundaryWordB c m } := by
  obtain ⟨hlenA, hlenB⟩ := boundary_lengths c m
  obtain ⟨_, hlow, _, hhigh⟩ := boundary_values c m hc
  obtain ⟨hcarryA, hcarryB⟩ := boundary_carries c m
  have hz : zValue c (boundaryWordB c m) = zValue c (boundaryWordA c m) := by
    simp only [zValue, hlow, hlenA, hlenB]
  have hr : rhoNum c (boundaryWordB c m) = 10 * rhoNum c (boundaryWordA c m) := by
    simp only [rhoNum, hhigh, Nat.mul_add]
    omega
  intro cut
  constructor
  · change adicNumeratorDigits cut (zValue c (boundaryWordB c m) - (c : Int)) =
        adicNumeratorDigits cut (zValue c (boundaryWordA c m) - (c : Int))
    rw [hz]
  · change fractionDigits cut (rhoNum c (boundaryWordB c m))
        (9 * 10 ^ (boundaryWordB c m).length *
          10 ^ (normalize (boundaryWordB c m).reverse (if 10 ≤ c then 1 else 0)).2) =
      fractionDigits cut (rhoNum c (boundaryWordA c m))
        (9 * 10 ^ (boundaryWordA c m).length *
          10 ^ (normalize (boundaryWordA c m).reverse (if 10 ≤ c then 1 else 0)).2)
    rw [hr, hlenA, hlenB, hcarryA, hcarryB]
    simpa only [Nat.pow_zero, Nat.pow_one, Nat.mul_one, Nat.one_mul,
      Nat.mul_comm, Nat.mul_left_comm, Nat.mul_assoc] using
      fractionDigits_scale cut (rhoNum c (boundaryWordA c m))
        (9 * 10 ^ (m + 3)) 10 (by decide)

/-- At both boundary phases, every width at least three contains two
distinct valid states with identical complete streams and opposite carries. -/
theorem boundary_double_fiber (c m : Nat) (hc : c = 0 ∨ c = 18) :
    ∃ A B : List Nat,
      A.length = m + 3 ∧ B.length = m + 3 ∧
      validOuter { c := c, B := A } = true ∧
      validOuter { c := c, B := B } = true ∧ A ≠ B ∧
      (normalize A.reverse (if 10 ≤ c then 1 else 0)).2 = 0 ∧
      (normalize B.reverse (if 10 ≤ c then 1 else 0)).2 = 1 ∧
      sameStreams { c := c, B := A } { c := c, B := B } := by
  obtain ⟨hlenA, hlenB⟩ := boundary_lengths c m
  obtain ⟨hvalidA, hvalidB⟩ := boundary_valid c m hc
  obtain ⟨hcarryA, hcarryB⟩ := boundary_carries c m
  exact ⟨boundaryWordA c m, boundaryWordB c m, hlenA, hlenB,
    hvalidA, hvalidB, boundary_ne c m, hcarryA, hcarryB, boundary_sameStreams c m hc⟩

#print axioms boundary_values
#print axioms boundary_carries
#print axioms boundary_sameStreams
#print axioms boundary_double_fiber

end Agent5.CompleteExteriorFibers
