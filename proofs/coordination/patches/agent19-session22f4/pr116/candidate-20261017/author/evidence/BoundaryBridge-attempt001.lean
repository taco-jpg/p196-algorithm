import RawBridge
import ShortWidths
import ExteriorCoverage

namespace Agent19.TwoStep
open P196.Agent6
open Agent110.TwoStepBoundary Agent110.TwoStepShort

theorem terminal_eq (p q : Word) (x y : Nat)
    (h : p ++ [x] = q ++ [y]) : x = y := by
  have hh := congrArg List.getLast? h
  simpa using hh

theorem terminal_pair_eq (p q : Word) (x y u v : Nat)
    (h : p ++ [x,y] = q ++ [u,v]) : x = u ∧ y = v := by
  have hh := congrArg (fun w : Word => w.reverse.take 2) h
  simpa [List.reverse_append, and_comm] using hh

/-- The three possible trim allocations force exactly the existing finite
boundary predicate. All inputs here are equalities of original raw words. -/
theorem boundary_from_suffixes (xs ys : Word) (x w q r : Nat)
    (hx : x ≠ 6) (hw : w ≠ 12) (hqr : q+r=2)
    (hB : Bounded (xs ++ [x])) (hW : Bounded (ys ++ [w]))
    (hfirst : rawWord 6 (xs ++ [x]) = (ys ++ [w]) ++ List.replicate q 12)
    (hsecond : rawWord 12 (ys ++ [w]) = (xs ++ [x]) ++ List.replicate r 6) :
    False := by
  obtain ⟨a,mu,p,P,ha,hmu,hraw1,hP⟩ := raw_six_tail xs x hB
  obtain ⟨b,nu,z,Q,hb,hnu,hraw2,hQ⟩ := raw_twelve_tail ys w hW
  have hxbound : x ≤ 18 := hB x (by simp)
  have hwbound : w ≤ 18 := hW w (by simp)
  have hq : q=0 ∨ q=1 ∨ q=2 := by omega
  rcases hq with rfl | rfl | rfl
  · have hr : r=2 := by omega
    subst r
    have hl1 : firstLast mu x a = w := terminal_eq (p++[P]) ys _ _ (by
      simpa [List.append_assoc] using hraw1.symm.trans hfirst)
    have hl2 : Q=6 ∧ secondLast nu w b=6 := terminal_pair_eq z (xs++[x]) _ _ _ _ (by
      simpa using hraw2.symm.trans hsecond)
    apply boundary_impossible 0 mu nu x a b w (by omega) hmu hnu hxbound ha hb hwbound
    simp [boundaryCandidate, hx, hl1, hw, hl2.2, ← hl2.1, hQ]
  · have hr : r=1 := by omega
    subst r
    have hl1 : P=w ∧ firstLast mu x a=12 := terminal_pair_eq p ys _ _ _ _ (by
      simpa [List.append_assoc] using hraw1.symm.trans hfirst)
    have hl2 : Q=x ∧ secondLast nu w b=6 := terminal_pair_eq z xs _ _ _ _ (by
      simpa [List.append_assoc] using hraw2.symm.trans hsecond)
    apply boundary_impossible 1 mu nu x a b w (by omega) hmu hnu hxbound ha hb hwbound
    simp [boundaryCandidate, hx, hl1.2, hw, ← hl1.1, hP, hl2.2, ← hl2.1, hQ]
  · have hr : r=0 := by omega
    subst r
    have hl1 : P=12 ∧ firstLast mu x a=12 := terminal_pair_eq p (ys++[w]) _ _ _ _ (by
      simpa using hraw1.symm.trans hfirst)
    have hl2 : secondLast nu w b=x := terminal_eq (z++[Q]) xs _ _ (by
      simpa [List.append_assoc] using hraw2.symm.trans hsecond)
    apply boundary_impossible 2 mu nu x a b w (by omega) hmu hnu hxbound ha hb hwbound
    simp [boundaryCandidate, hx, hl1.2, hw, ← hl1.1, hP, hl2]

#print axioms boundary_from_suffixes
end Agent19.TwoStep
