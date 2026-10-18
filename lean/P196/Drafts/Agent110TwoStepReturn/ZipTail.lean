import P196.Agent5OrdinaryStreamPrefix.ExteriorCore

/-! Generic last-column preservation for original exterior raw zipWith Nat.add.
This is a bridge lemma, not an all-length cycle theorem. -/
namespace Agent110.TwoStepZip
open P196.Agent6

theorem zipWith_add_snoc (xs ys : Word) (x y : Nat)
    (hlen : xs.length = ys.length) :
    List.zipWith Nat.add (xs ++ [x]) (ys ++ [y]) =
      List.zipWith Nat.add xs ys ++ [x + y] := by
  induction xs generalizing ys with
  | nil =>
      cases ys with
      | nil => simp
      | cons y ys => simp at hlen
  | cons a as ih =>
      cases ys with
      | nil => simp at hlen
      | cons b bs =>
          have htail : as.length = bs.length := by simpa using hlen
          simp [List.zipWith, ih bs htail]

theorem zipWith_add_terminal (xs ys : Word) (x y : Nat)
    (hlen : xs.length = ys.length) :
    (List.zipWith Nat.add (xs ++ [x]) (ys ++ [y])).getLast? =
      some (x + y) := by
  rw [zipWith_add_snoc xs ys x y hlen]
  simp

#print axioms zipWith_add_snoc
#print axioms zipWith_add_terminal
end Agent110.TwoStepZip
