import RawBridge
import TrimBridge
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
    rw [hl2.1] at hQ
    simp [boundaryCandidate, hx, hl1, hw, hl2.2, hQ]
  · have hr : r=1 := by omega
    subst r
    have hl1 : P=w ∧ firstLast mu x a=12 := terminal_pair_eq p ys _ _ _ _ (by
      simpa [List.append_assoc] using hraw1.symm.trans hfirst)
    have hl2 : Q=x ∧ secondLast nu w b=6 := terminal_pair_eq z xs _ _ _ _ (by
      simpa [List.append_assoc] using hraw2.symm.trans hsecond)
    apply boundary_impossible 1 mu nu x a b w (by omega) hmu hnu hxbound ha hb hwbound
    rw [hl1.1] at hP
    rw [hl2.1] at hQ
    simp [boundaryCandidate, hx, hl1.2, hw, hP, hl2.2, hQ]
  · have hr : r=0 := by omega
    subst r
    have hl1 : P=12 ∧ firstLast mu x a=12 := terminal_pair_eq p (ys++[w]) _ _ _ _ (by
      simpa using hraw1.symm.trans hfirst)
    have hl2 : secondLast nu w b=x := terminal_eq (z++[Q]) xs _ _ (by
      simpa [List.append_assoc] using hraw2.symm.trans hsecond)
    apply boundary_impossible 2 mu nu x a b w (by omega) hmu hnu hxbound ha hb hwbound
    rw [hl1.1] at hP
    simp [boundaryCandidate, hx, hl1.2, hw, hP, hl2]


/-- Every bounded word fixed by the original phase-six trim fails to return
under two applications of the original advance, at every finite width. -/
theorem bounded_trim_not_period_two (w : Word) (hB : Bounded w)
    (htrim : trim 6 w = w) :
    advance (advance (⟨6,w⟩ : Exterior)) ≠ (⟨6,w⟩ : Exterior) := by
  intro hcycle
  by_cases hlen : 2 ≤ w.length
  · let v := trim 12 (rawWord 6 w)
    have hreturn : trim 6 (rawWord 12 v) = w := by
      have hh := congrArg Exterior.word hcycle
      simpa only [advance_six, advance_twelve] using hh
    obtain ⟨q,hq⟩ := trim_spec 12 (rawWord 6 w)
    obtain ⟨r,hr⟩ := trim_spec 6 (rawWord 12 v)
    have hqr : q+r=2 := trim_two_step_count 12 6 w
      (rawWord 6 w) (rawWord 12 v) q r
      (raw_length 6 w) (raw_length 12 v) hreturn hq hr
    have hvlen : 1 ≤ v.length := by
      have hh := congrArg List.length hq
      simp only [List.length_append, List.length_replicate, raw_length] at hh
      change w.length + 1 = v.length + q at hh
      omega
    obtain ⟨xs,x,hx⟩ := exists_snoc w (by intro hz; simp [hz] at hlen)
    obtain ⟨ys,y,hy⟩ := exists_snoc v (by intro hz; simp [hz] at hvlen)
    have hxphase : x ≠ 6 := by
      have hh := trim_last 6 w
      rw [htrim, hx] at hh
      simpa using hh
    have hyphase : y ≠ 12 := by
      have hh := trim_last 12 (rawWord 6 w)
      change v.getLast? ≠ some 12 at hh
      rw [hy] at hh
      simpa using hh
    have hV : Bounded v := trim_bounded 18 12 (rawWord 6 w)
      (raw_bounded 6 w (Or.inl rfl) hB)
    apply boundary_from_suffixes xs ys x y q r hxphase hyphase hqr
    · simpa only [← hx] using hB
    · simpa only [← hy] using hV
    · simpa only [← hx, ← hy] using hq
    · simpa only [← hx, ← hy, hreturn] using hr
  · cases w with
    | nil => exact empty_not_period_two hcycle
    | cons x xs =>
        have hxs : xs = [] := List.length_eq_zero_iff.mp (by
          simp only [List.length_cons] at hlen; omega)
        subst xs
        exact singleton_not_period_two x (hB x (by simp)) hcycle

/-- The requested theorem for the unchanged original Canonical predicate and
unchanged original advance, with no restriction on the word length. -/
theorem canonical_phase_six_not_period_two (s : Exterior) (hs : Canonical s)
    (hphase : s.phase = 6) : advance (advance s) ≠ s := by
  rcases s with ⟨c,w⟩
  change c = 6 at hphase
  subst c
  rcases hs with ⟨_,_,_,hB,_,htrim⟩
  exact bounded_trim_not_period_two w hB htrim

#print axioms boundary_from_suffixes
#print axioms bounded_trim_not_period_two
#print axioms canonical_phase_six_not_period_two
end Agent19.TwoStep
