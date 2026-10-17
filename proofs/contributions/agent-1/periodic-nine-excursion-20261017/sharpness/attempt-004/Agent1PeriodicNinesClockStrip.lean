import Agent1PeriodicNinesCenter

/-!
Clock-one boundary ancestry for an initially maximally stripped nine center.
The boundary entries and clock are the original actual scans. This file does
not assert a full-return obstruction or independently selectable carry bits.
-/

namespace Agent1.Periodic
open Agent8

private theorem clock_pad_peel (H : Word) (e : Nat)
    (he : e ≤ 1) (hb : Bounded H 18) (hs : H.reverse = H)
    (hm : e + terminalCarry H e = 1) (K : Word)
    (hp : pair (fixedDigits H e ++ [9*e]) = [9] ++ K ++ [9]) :
    ∃ T : Word, H = [9] ++ T ++ [9] ∧ T.reverse = T ∧
      Bounded T 18 ∧ e + terminalCarry T e = 1 ∧
      pair (fixedDigits T e ++ [9*e]) = K := by
  cases H with
  | nil => simp only [terminalCarry] at hm; omega
  | cons a A =>
    have ha : a ≤ 18 := hb a (by simp)
    have hh : (fixedDigits (a :: A) e ++ [9*e]).head? = some ((a+e)%10) := rfl
    have hl : (fixedDigits (a :: A) e ++ [9*e]).getLast? = some (9*e) := by simp
    have hhead := pair_head (fixedDigits (a :: A) e ++ [9*e]) _ _ hh hl
    rw [hp] at hhead
    have ha9 : a = 9 := by
      simp only [List.singleton_append, List.head?_cons, Option.some.injEq] at hhead
      have heCases : e = 0 ∨ e = 1 := by omega
      rcases heCases with rfl | rfl
      · simp at hhead
        omega
      · simp at hhead
        omega
    subst a
    rcases List.eq_nil_or_concat A with hA | ⟨T, b, hA⟩
    · subst A
      simp only [terminalCarry] at hm
      omega
    · rw [List.concat_eq_append] at hA
      subst A
      have hb9 : b = 9 := by
        have h := congrArg List.head? hs
        simpa using h
      subst b
      have hT : T.reverse = T := by
        have h : 9 :: (T.reverse ++ [9]) = 9 :: (T ++ [9]) := by simpa using hs
        exact List.append_cancel_right (List.cons.inj h).2
      have hbT : Bounded T 18 := by
        intro x hx
        exact hb x (by simp [hx])
      have ht : terminalCarry T e ≤ 1 := terminalCarry_le_one T e hbT he
      have hcarry : terminalCarry (9 :: (T ++ [9])) e = terminalCarry T e := by
        simp only [terminalCarry, terminalCarry_append]
        have heq : (9+e)/10 = e := by omega
        rw [heq]
        omega
      rw [hcarry] at hm
      have hd : fixedDigits (9 :: (T ++ [9])) e =
          [9-9*e] ++ fixedDigits T e ++ [9*e] := by
        simp only [fixedDigits, fixedDigits_append, terminalCarry]
        have heq : (9+e)/10 = e := by omega
        rw [heq]
        have hfirst : (9+e)%10 = 9-9*e := by omega
        have hlast : (9+terminalCarry T e)%10 = 9*e := by omega
        simp [hfirst, hlast]
      have hpair : pair (fixedDigits (9 :: (T ++ [9])) e ++ [9*e]) =
          [9] ++ pair (fixedDigits T e ++ [9*e]) ++ [9] := by
        rw [hd]
        have h := pair_three_parts [9-9*e] (fixedDigits T e ++ [9*e]) [9*e] rfl
        have hadd : 9-9*e+9*e = 9 := by omega
        simpa [List.append_assoc, zipAdd, hadd] using h
      have hK : pair (fixedDigits T e ++ [9*e]) = K := by
        have h := hpair.symm.trans hp
        exact List.append_cancel_right (List.cons.inj h).2
      exact ⟨T, rfl, hT, hbT, hm, hK⟩

private theorem clock_pad_four_ancestry (H : Word) (e : Nat)
    (he : e ≤ 1) (hb : Bounded H 18) (hs : H.reverse = H)
    (hm : e + terminalCarry H e = 1) (K : Word)
    (hp : pair (fixedDigits H e ++ [9*e]) =
      [9,9,9,9] ++ K ++ [9,9,9,9]) :
    ∃ T : Word, H = [9,9,9,9] ++ T ++ [9,9,9,9] := by
  obtain ⟨H1, h1, hs1, hb1, hm1, hp1⟩ :=
    clock_pad_peel H e he hb hs hm ([9,9,9] ++ K ++ [9,9,9])
      (by simpa [List.append_assoc] using hp)
  obtain ⟨H2, h2, hs2, hb2, hm2, hp2⟩ :=
    clock_pad_peel H1 e he hb1 hs1 hm1 ([9,9] ++ K ++ [9,9])
      (by simpa [List.append_assoc] using hp1)
  obtain ⟨H3, h3, hs3, hb3, hm3, hp3⟩ :=
    clock_pad_peel H2 e he hb2 hs2 hm2 ([9] ++ K ++ [9])
      (by simpa [List.append_assoc] using hp2)
  obtain ⟨H4, h4, _, _, _, _⟩ :=
    clock_pad_peel H3 e he hb3 hs3 hm3 K hp3
  refine ⟨H4, ?_⟩
  simpa [h2, h3, h4, List.append_assoc] using h1

private theorem nines_count_zero_of_no_wrap (R : Word)
    (hn : ¬ ∃ K : Word, R = [9,9,9,9] ++ K ++ [9,9,9,9]) :
    (stripPeriodCenter [9,9,9,9] R).2 = 0 := by
  have htest : ¬ R = [9,9,9,9] ++ stripPeriodMiddle [9,9,9,9] R ++
      [9,9,9,9].reverse := fun h => hn ⟨_, h⟩
  unfold stripPeriodCenter
  simp only [List.cons_ne_self, reduceCtorEq, if_false]
  cases hlen : R.length with
  | zero => simp [hlen, stripPeriodCenterAux]
  | succ n => simp [hlen, stripPeriodCenterAux, htest]

/-- At actual clock one, an initially maximally stripped valid nine center
has only the mandatory outer pair removed. No future-phase premise is used. -/
theorem centerPeriods_nines_clock_one (B H : Word)
    (hv : ValidPeriodic B H [9,9,9,9])
    (hnorm : stripPeriodCenter [9,9,9,9] H = (H, 0))
    (hmix : leftEntry B + rightEntry B H [9,9,9,9] = 1)
    (hg : rawGamma B H [9,9,9,9] = 1) :
    centerPeriods B H [9,9,9,9] = 1 := by
  have he : leftEntry B ≤ 1 := (nines_entry_bits B H hv.outer_bounded hv.center_bounded).1
  have hm : leftEntry B + terminalCarry H (leftEntry B) = 1 := by
    simpa only [rightEntry_nines B H hv.outer_bounded] using hmix
  have hmax := stripPeriodCenter_maximal [9,9,9,9] H (by decide)
  rw [hnorm] at hmax
  have hn : ¬ ∃ K : Word,
      pair (fixedDigits H (leftEntry B) ++ [9*leftEntry B]) =
        [9,9,9,9] ++ K ++ [9,9,9,9] := by
    rintro ⟨K, hK⟩
    exact hmax (clock_pad_four_ancestry H (leftEntry B) he hv.center_bounded
      hv.center_symmetric hm K hK)
  have hz := nines_count_zero_of_no_wrap
    (pair (fixedDigits H (leftEntry B) ++ [9*leftEntry B])) hn
  rw [centerPeriods_nines_mixed B H hv.outer_bounded hv.center_bounded hmix, hg]
  simpa only [List.replicate_succ, List.replicate_zero, List.cons_append,
    List.nil_append, hz] using congrArg (fun n : Nat => n+1) hz

end Agent1.Periodic

#print axioms Agent1.Periodic.centerPeriods_nines_clock_one
