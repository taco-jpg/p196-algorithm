import P196.TrimmedStreamObservation.LowPrefix
import P196.Agent5ExactDigitStreams.FractionDigits

/-!
# Appending a coefficient without changing the observed prefixes

The low stream through the old word width is unaffected by an appended
coefficient, for arbitrary natural coefficients and phases. The high
stream has the same property when that coefficient preserves the phase's
incoming carry. Each high observation retains its own actual width and
outgoing normalization carry in its denominator.
-/

namespace Agent5.StreamNonisolation

open P196.Agent7.Finite Agent115.ExteriorFactorization
open Agent5.ExactDigitStreams

private theorem low_prefix_take (c cut : Nat) (B : List Nat)
    (hcut : cut ≤ B.length) :
    adicNumeratorDigits cut (zValue c B - (c : Int)) =
      ((normalize B 0).1).take cut := by
  have hsum : cut + (B.length - cut) = B.length := Nat.add_sub_of_le hcut
  have h := adicNumeratorDigits_prefix cut (B.length - cut)
    (zValue c B - (c : Int))
  rw [hsum, Agent5.TrimmedStreamObservation.low_prefix_normalized] at h
  exact h.symm

/-- Any appended coefficient preserves the original low observations
through the old word width. No phase or coefficient bound is needed. -/
theorem append_low_prefix (c cut : Nat) (B : List Nat) (d : Nat)
    (hcut : cut ≤ B.length) :
    adicNumeratorDigits cut (zValue c (B ++ [d]) - (c : Int)) =
      adicNumeratorDigits cut (zValue c B - (c : Int)) := by
  have hcut' : cut ≤ (B ++ [d]).length := by
    simp only [List.length_append, List.length_singleton]
    omega
  rw [low_prefix_take c cut (B ++ [d]) hcut', low_prefix_take c cut B hcut]
  simp only [normalize_append_single]
  exact List.take_append_of_le_length (by simpa only [normalize_length] using hcut)

/-- An appended coefficient that returns the incoming phase carry leaves
the actual outgoing high carry unchanged, without coefficient bounds. -/
theorem append_high_carry (c : Nat) (B : List Nat) (d : Nat)
    (hcarry : (d + (if 10 ≤ c then 1 else 0)) / 10 =
      (if 10 ≤ c then 1 else 0)) :
    (normalize (B ++ [d]).reverse (if 10 ≤ c then 1 else 0)).2 =
      (normalize B.reverse (if 10 ≤ c then 1 else 0)).2 := by
  simp only [List.reverse_append, List.reverse_cons, List.reverse_nil,
    List.nil_append, List.singleton_append, normalize, hcarry]

private theorem fraction_take (cut n r D : Nat) (hcut : cut ≤ n) :
    (fractionDigits n r D).take cut = fractionDigits cut r D := by
  have hsum : cut + (n - cut) = n := Nat.add_sub_of_le hcut
  simpa only [hsum] using fractionDigits_prefix cut (n - cut) r D

/-- A carry-preserving appended coefficient preserves the original high
observations through the old width. Both denominators use their original
word widths and their own calculated outgoing carries. -/
theorem append_high_prefix (c cut : Nat) (B : List Nat) (d : Nat)
    (hc : nonneutralPhase c) (hB : ∀ x ∈ B, x ≤ 18) (hd : d ≤ 18)
    (hcarry : (d + (if 10 ≤ c then 1 else 0)) / 10 =
      (if 10 ≤ c then 1 else 0))
    (hcut : cut ≤ B.length) :
    fractionDigits cut (rhoNum c (B ++ [d]))
        (9 * 10 ^ (B ++ [d]).length *
          10 ^ (normalize (B ++ [d]).reverse (if 10 ≤ c then 1 else 0)).2) =
      fractionDigits cut (rhoNum c B)
        (9 * 10 ^ B.length *
          10 ^ (normalize B.reverse (if 10 ≤ c then 1 else 0)).2) := by
  let k : Nat := if 10 ≤ c then 1 else 0
  let g : Nat := (normalize B.reverse k).2
  let X : List Nat := (normalize B.reverse k).1.reverse
  let t : Nat := c - 9 * k
  let e : Nat := (d + k) % 10
  change (d + k) / 10 = k at hcarry
  have hBD : ∀ x ∈ B ++ [d], x ≤ 18 := by
    intro x hx
    rcases List.mem_append.mp hx with hx | hx
    · exact hB x hx
    · have hxd : x = d := List.mem_singleton.mp hx
      simpa only [hxd] using hd
  have hnorm :
      (normalize (B ++ [d]).reverse k).1.reverse = X ++ [e] := by
    dsimp only [X, e]
    simp only [List.reverse_append, List.reverse_cons, List.reverse_nil,
      List.nil_append, List.singleton_append, normalize, hcarry]
  change (normalize (B ++ [d]).reverse (if 10 ≤ c then 1 else 0)).1.reverse =
    X ++ [e] at hnorm
  have hsB := fractionDigits_exterior c B 0 hc hB
  have hsD := fractionDigits_exterior c (B ++ [d]) 0 hc hBD
  simp only [Nat.add_zero, List.replicate_zero, List.append_nil] at hsB hsD
  simp only [append_high_carry c B d hcarry, hnorm] at hsD
  change fractionDigits (B.length + 1) (rhoNum c B)
      (9 * 10 ^ B.length * 10 ^ g) =
    (if g == 0 then X ++ [t] else [1] ++ X) at hsB
  change fractionDigits ((B ++ [d]).length + 1) (rhoNum c (B ++ [d]))
      (9 * 10 ^ (B ++ [d]).length * 10 ^ g) =
    (if g == 0 then (X ++ [e]) ++ [t] else [1] ++ (X ++ [e])) at hsD
  have hlenX : X.length = B.length := by
    dsimp only [X]
    rw [List.length_reverse, normalize_length, List.length_reverse]
  have hcutX : cut ≤ X.length := by simpa only [hlenX] using hcut
  have hcut1X : cut ≤ ([1] ++ X).length := by
    simp only [List.length_append, List.length_singleton, hlenX]
    omega
  have hlists :
      (if g == 0 then (X ++ [e]) ++ [t] else [1] ++ (X ++ [e])).take cut =
        (if g == 0 then X ++ [t] else [1] ++ X).take cut := by
    by_cases hg : g = 0
    · simp only [hg, beq_self_eq_true, if_true]
      rw [List.append_assoc, List.take_append_of_le_length hcutX,
        List.take_append_of_le_length hcutX]
    · have hfalse : (g == 0) = false := by simp [hg]
      simp only [hfalse, Bool.false_eq_true, if_false]
      rw [← List.append_assoc, List.take_append_of_le_length hcut1X]
  have hcutB : cut ≤ B.length + 1 := by omega
  have hcutD : cut ≤ (B ++ [d]).length + 1 := by
    simp only [List.length_append, List.length_singleton]
    omega
  have hpB := congrArg (List.take cut) hsB
  have hpD := congrArg (List.take cut) hsD
  rw [fraction_take cut (B.length + 1) _ _ hcutB] at hpB
  rw [fraction_take cut ((B ++ [d]).length + 1) _ _ hcutD] at hpD
  rw [append_high_carry c B d hcarry]
  exact hpD.trans (hlists.trans hpB.symm)

#print axioms append_low_prefix
#print axioms append_high_carry
#print axioms append_high_prefix

end Agent5.StreamNonisolation
