import P196.ManagerTwoRunObstruction.NumericPrefixReturn

/-!
Period obstruction for literal decimal families with two equal run lengths.
Words and digit positions are least significant first. Fixed words U, M, V
and fixed run digits x, y describe U ++ x^r ++ M ++ y^r ++ V. Canonicality
is explicit at both endpoints, so leading zero padding is not counted as
width; trailing zeros remain allowed. Only one actual return at r >= 3 is
needed. No search completeness or all-period impossibility is asserted.
-/

namespace P196.ManagerTwoRun

open DecimalDigits FoldedDecimal
open P196.Agent4.WholeWord

def twoRunWidth (U M V : List Nat) (r : Nat) : Nat :=
  U.length + M.length + V.length + 2 * r

def twoRunDigit (U : List Nat) (x : Nat) (M : List Nat) (y : Nat)
    (V : List Nat) (r i : Nat) : Nat :=
  if i < U.length then U[i]!
  else if i < U.length + r then x
  else if i < U.length + r + M.length then M[i - (U.length + r)]!
  else if i < U.length + 2 * r + M.length then y
  else V[i - (U.length + 2 * r + M.length)]!

/-- Once the first run has three digits, its first three low digits stabilize. -/
theorem twoRun_low_digit (U M V : List Nat) (x y r i : Nat)
    (hr : 3 ≤ r) (hi : i < 3) :
    twoRunDigit U x M y V r i = if i < U.length then U[i]! else x := by
  unfold twoRunDigit
  split
  · rfl
  · rw [if_pos (by omega)]

/-- Once the last run has three digits, its first three high digits stabilize. -/
theorem twoRun_high_digit (U M V : List Nat) (x y r i : Nat)
    (hr : 3 ≤ r) (hi : i < 3) :
    twoRunDigit U x M y V r (twoRunWidth U M V r - 1 - i) =
      if i < V.length then V[V.length - 1 - i]! else y := by
  unfold twoRunDigit twoRunWidth
  rw [if_neg (by omega), if_neg (by omega), if_neg (by omega)]
  by_cases hV : i < V.length
  · rw [if_neg (by omega), if_pos hV]
    congr 1
    omega
  · rw [if_pos (by omega), if_neg hV]

/-- Literal two-run families return all three outside pair columns. -/
theorem twoRun_prefix_stable (U M V : List Nat) (x y r s : Nat)
    (hr : 3 ≤ r) (hs : 3 ≤ s) :
    prefix3 (columnSum (twoRunDigit U x M y V r) (twoRunWidth U M V r)) =
      prefix3 (columnSum (twoRunDigit U x M y V s) (twoRunWidth U M V s)) := by
  have hp (i : Nat) (hi : i < 3) :
      columnSum (twoRunDigit U x M y V r) (twoRunWidth U M V r) i =
        columnSum (twoRunDigit U x M y V s) (twoRunWidth U M V s) i := by
    unfold columnSum reflected
    rw [twoRun_low_digit U M V x y r i hr hi,
      twoRun_low_digit U M V x y s i hs hi,
      twoRun_high_digit U M V x y r i hr hi,
      twoRun_high_digit U M V x y s i hs hi]
  unfold prefix3
  rw [hp 0 (by decide), hp 1 (by decide), hp 2 (by decide)]

/-- A literal two-run return after P actual additions and common run increase S
has 4*S <= P. Equality forces a period divisible by eight. -/
theorem twoRun_return_constraints (U M V : List Nat) (x y r S P n m : Nat)
    (hr : 3 ≤ r)
    (hsource : Canonical n (twoRunDigit U x M y V r) (twoRunWidth U M V r))
    (htarget : Canonical m (twoRunDigit U x M y V (r + S))
      (twoRunWidth U M V (r + S)))
    (hreturn : Lychrel196.orbit n P = m) :
    4 * S ≤ P ∧ (P = 4 * S → P % 8 = 0) := by
  have htarget' : Canonical (Lychrel196.orbit n P)
      (twoRunDigit U x M y V (r + S)) (twoRunWidth U M V (r + S)) := by
    rw [hreturn]
    exact htarget
  have hp := twoRun_prefix_stable U M V x y (r + S) r (by omega) hr
  have hb := numeric_prefix_return_constraints n
    (twoRunDigit U x M y V r) (twoRunDigit U x M y V (r + S))
    (twoRunWidth U M V r) (twoRunWidth U M V (r + S)) P
    hsource htarget' (by unfold twoRunWidth; omega) hp
  unfold twoRunWidth at hb
  constructor
  · omega
  · intro heq
    apply hb.2
    omega

/-- No positive common-increment two-run family can return in at most four
actual reverse-and-add steps, for any fixed block widths or digit split. -/
theorem twoRun_positive_return_period_ge_five
    (U M V : List Nat) (x y r S P n m : Nat)
    (hr : 3 ≤ r) (hS : 0 < S)
    (hsource : Canonical n (twoRunDigit U x M y V r) (twoRunWidth U M V r))
    (htarget : Canonical m (twoRunDigit U x M y V (r + S))
      (twoRunWidth U M V (r + S)))
    (hreturn : Lychrel196.orbit n P = m) : 5 ≤ P := by
  have hb := twoRun_return_constraints U M V x y r S P n m hr hsource htarget hreturn
  have hs := hb.2
  omega

#print axioms twoRun_low_digit
#print axioms twoRun_high_digit
#print axioms twoRun_prefix_stable
#print axioms twoRun_return_constraints
#print axioms twoRun_positive_return_period_ge_five

end P196.ManagerTwoRun
