import P196.CommonOverflowRigidity.Model

/-!
Arithmetic closure of the folded carry invariant. A diagonal layer has
only four possible unequal-coefficient transitions, in addition to the
equal-coefficient case. Applying this classification to both layers
leaves twelve exceptional states. The exceptional states cannot return
to the diagonal and cannot have their first-layer carries meet.

All classifications below are proved with bounded integer arithmetic;
no external state enumeration is used as a proof certificate.
-/

set_option autoImplicit false
set_option maxHeartbeats 2000000

namespace P196.CommonOverflowRigidity

/-- Advancing any bounded local data preserves all carry and digit bounds. -/
theorem advance_bounded (t : State) (a b rq rs tq ts : Nat)
    (ht : Bounded t) (ha : a ≤ 18) (hb : b ≤ 18)
    (hrq : rq ≤ 1) (hrs : rs ≤ 1) (htq : tq ≤ 1) (hts : ts ≤ 1) :
    Bounded (advance t a b rq rs tq ts) := by
  simp only [Bounded, LayerBounded, advance, advanceLayer] at ht ⊢
  refine ⟨⟨?_, hrq, ?_, hrs⟩, ⟨?_, htq, ?_, hts⟩, ?_, ?_⟩ <;> omega

private theorem diagonal_local_cases (l h a b rq rs : Nat)
    (hl : l ≤ 1) (hh : h ≤ 1) (ha : a ≤ 18) (hb : b ≤ 18)
    (hrq : rq ≤ 1) (hrs : rs ≤ 1)
    (ht : Local ⟨l, h, l, h⟩ a b rq rs) :
    (a = b ∧ rq = rs) ∨
    (l = 1 ∧ h = 0 ∧ a = 4 ∧ b = 9 ∧ rq = 0 ∧ rs = 0) ∨
    (l = 1 ∧ h = 0 ∧ a = 9 ∧ b = 4 ∧ rq = 0 ∧ rs = 0) ∨
    (l = 0 ∧ h = 1 ∧ a = 9 ∧ b = 14 ∧ rq = 1 ∧ rs = 1) ∨
    (l = 0 ∧ h = 1 ∧ a = 14 ∧ b = 9 ∧ rq = 1 ∧ rs = 1) := by
  simp only [Local] at ht
  have hr : rq = rs := by omega
  by_cases hab : a = b
  · exact Or.inl ⟨hab, hr⟩
  · have horder : a < b ∨ b < a := by omega
    have hlow : l = 0 ∨ l = 1 := by omega
    rcases horder with hab | hba
    · rcases hlow with hlzero | hlone
      · right; right; right; left
        omega
      · right; left
        omega
    · rcases hlow with hlzero | hlone
      · right; right; right; right
        omega
      · right; right; left
        omega

/-- A diagonal transition either keeps equal low digits or enters the exceptional set. -/
theorem diagonal_step (t : State) (a b rq rs tq ts : Nat)
    (ht : Bounded t) (hd : Diagonal t) (ha : a ≤ 18) (hb : b ≤ 18)
    (hrq : rq ≤ 1) (hrs : rs ≤ 1) (htq : tq ≤ 1) (hts : ts ≤ 1)
    (htrans : Transition t a b rq rs tq ts) :
    (Diagonal (advance t a b rq rs tq ts) ∧
      (a + t.first.qLow) % 10 = (b + t.first.sLow) % 10) ∨
      Bad (advance t a b rq rs tq ts) := by
  rcases t with ⟨⟨l, h, ls, hs⟩, ⟨k, j, ks, js⟩, p, ps⟩
  simp only [Diagonal] at hd
  obtain ⟨hls, hhs, hks, hjs, hps⟩ := hd
  subst ls
  subst hs
  subst ks
  subst js
  subst ps
  simp only [Bounded, LayerBounded] at ht
  change Local ⟨l, h, l, h⟩ a b rq rs ∧
    Local ⟨k, j, k, j⟩ ((a + l) % 10 + p) ((b + l) % 10 + p) tq ts at htrans
  have hA : (a + l) % 10 + p ≤ 18 := by omega
  have hB : (b + l) % 10 + p ≤ 18 := by omega
  have hfirst := diagonal_local_cases l h a b rq rs
    ht.1.1 ht.1.2.1 ha hb hrq hrs htrans.1
  have hsecond := diagonal_local_cases k j
    ((a + l) % 10 + p) ((b + l) % 10 + p) tq ts
    ht.2.1.1 ht.2.1.2.1 hA hB htq hts htrans.2
  rcases hfirst with hfirst | hfirst | hfirst | hfirst | hfirst <;>
    rcases hsecond with hsecond | hsecond | hsecond | hsecond | hsecond <;>
    simp_all [advance, advanceLayer, Diagonal, Bad, badStates,
      List.mem_cons, List.mem_singleton, State.mk.injEq, Layer.mk.injEq] <;>
    omega

/-- Every legal transition from an exceptional state remains exceptional. -/
theorem bad_step (t : State) (a b rq rs tq ts : Nat)
    (ht : Bounded t) (hbad : Bad t) (ha : a ≤ 18) (hb : b ≤ 18)
    (hrq : rq ≤ 1) (hrs : rs ≤ 1) (htq : tq ≤ 1) (hts : ts ≤ 1)
    (htrans : Transition t a b rq rs tq ts) :
    Bad (advance t a b rq rs tq ts) := by
  have hnext := advance_bounded t a b rq rs tq ts ht ha hb hrq hrs htq hts
  simp only [Bounded, LayerBounded, advance, advanceLayer] at hnext
  simp only [Bad, badStates, List.mem_cons, List.not_mem_nil, or_false] at hbad
  rcases hbad with rfl | rfl | rfl | rfl | rfl | rfl |
    rfl | rfl | rfl | rfl | rfl | rfl
  all_goals dsimp at hnext
  · have hinputs : a = 4 ∧ b = 9 ∧ rq = 1 ∧ rs = 0 ∧ tq = 1 ∧ ts = 0 := by
      simp only [Transition, Local] at htrans
      have hedge : (b + 1) % 10 + 9 + ts < 10 :=
        (Nat.div_eq_zero_iff_lt (by decide)).mp htrans.2.2.1
      have hzero : (b + 1) % 10 = 0 := by omega
      have hbvalue : b = 9 := by omega
      subst b
      simp at htrans
      omega
    rcases hinputs with ⟨rfl, rfl, rfl, rfl, rfl, rfl⟩
    unfold Bad
    decide
  · exfalso
    simp only [Transition, Local, Nat.add_zero] at htrans
    have haqSmall : a + rq < 10 :=
      (Nat.div_eq_zero_iff_lt (by decide)).mp htrans.1.1
    have hbsSmall : b + rs < 10 :=
      (Nat.div_eq_zero_iff_lt (by decide)).mp htrans.1.2.1
    have haSmall : a < 10 := by omega
    have hbSmall : b < 10 := by omega
    have haMod : a % 10 = a := Nat.mod_eq_of_lt haSmall
    simp only [haMod, Nat.mod_eq_of_lt haqSmall,
      Nat.mod_eq_of_lt hbsSmall] at htrans
    by_cases hbNine : b = 9
    · subst b
      simp at htrans
      omega
    · have hbNextSmall : b + 1 < 10 := by omega
      have hbMod : (b + 1) % 10 = b + 1 := Nat.mod_eq_of_lt hbNextSmall
      simp only [hbMod] at htrans
      have haqDiv : (a + 4 + 1) / 10 = 1 := by omega
      have hbsDiv : (b + 1 + 9) / 10 = 1 := by omega
      omega
  · exfalso
    simp [Transition, Local] at htrans <;> omega
  · exfalso
    simp [Transition, Local] at htrans <;> omega
  · exfalso
    simp only [Transition, Local, Nat.add_zero] at htrans
    have hbsDiv : (b + 1) / 10 = 1 := by omega
    have hbsSmall : (b + 1) % 10 + 5 + ts < 10 :=
      (Nat.div_eq_zero_iff_lt (by decide)).mp htrans.2.2.1
    have hbBound : b ≤ 13 := by omega
    by_cases haNine : a = 9
    · subst a
      simp at htrans
      omega
    · have haqDiv : a / 10 = 1 := by omega
      have haRem : a % 10 ≤ 8 := by omega
      have haLowDiv : (a % 10 + 1) / 10 = 0 := by omega
      have hbLowDiv : ((b + 1) % 10 + 5) / 10 = 0 := by omega
      omega
  · have hinputs : a = 9 ∧ b = 14 ∧ rq = 1 ∧ rs = 0 ∧ tq = 1 ∧ ts = 0 := by
      simp [Transition, Local] at htrans <;> omega
    rcases hinputs with ⟨rfl, rfl, rfl, rfl, rfl, rfl⟩
    unfold Bad
    decide
  · have hinputs : a = 9 ∧ b = 4 ∧ rq = 0 ∧ rs = 1 ∧ tq = 0 ∧ ts = 1 := by
      simp only [Transition, Local] at htrans
      have hedge : (a + 1) % 10 + 9 + tq < 10 :=
        (Nat.div_eq_zero_iff_lt (by decide)).mp htrans.2.1
      have hzero : (a + 1) % 10 = 0 := by omega
      have havalue : a = 9 := by omega
      subst a
      simp at htrans
      omega
    rcases hinputs with ⟨rfl, rfl, rfl, rfl, rfl, rfl⟩
    unfold Bad
    decide
  · exfalso
    simp only [Transition, Local, Nat.add_zero] at htrans
    have haqSmall : a + rq < 10 :=
      (Nat.div_eq_zero_iff_lt (by decide)).mp htrans.1.1
    have hbsSmall : b + rs < 10 :=
      (Nat.div_eq_zero_iff_lt (by decide)).mp htrans.1.2.1
    have haSmall : a < 10 := by omega
    have hbSmall : b < 10 := by omega
    have hbMod : b % 10 = b := Nat.mod_eq_of_lt hbSmall
    simp only [hbMod, Nat.mod_eq_of_lt haqSmall,
      Nat.mod_eq_of_lt hbsSmall] at htrans
    by_cases haNine : a = 9
    · subst a
      simp at htrans
      omega
    · have haNextSmall : a + 1 < 10 := by omega
      have haMod : (a + 1) % 10 = a + 1 := Nat.mod_eq_of_lt haNextSmall
      simp only [haMod] at htrans
      have haqDiv : (a + 1 + 9) / 10 = 1 := by omega
      have hbsDiv : (b + 4 + 1) / 10 = 1 := by omega
      omega
  · exfalso
    simp [Transition, Local] at htrans <;> omega
  · exfalso
    simp [Transition, Local] at htrans <;> omega
  · exfalso
    simp only [Transition, Local, Nat.add_zero] at htrans
    have haqDiv : (a + 1) / 10 = 1 := by omega
    have haqSmall : (a + 1) % 10 + 5 + tq < 10 :=
      (Nat.div_eq_zero_iff_lt (by decide)).mp htrans.2.1
    have haBound : a ≤ 13 := by omega
    by_cases hbNine : b = 9
    · subst b
      simp at htrans
      omega
    · have hbsDiv : b / 10 = 1 := by omega
      have hbRem : b % 10 ≤ 8 := by omega
      have haLowDiv : ((a + 1) % 10 + 5) / 10 = 0 := by omega
      have hbLowDiv : (b % 10 + 1) / 10 = 0 := by omega
      omega
  · have hinputs : a = 14 ∧ b = 9 ∧ rq = 0 ∧ rs = 1 ∧ tq = 0 ∧ ts = 1 := by
      simp [Transition, Local] at htrans <;> omega
    rcases hinputs with ⟨rfl, rfl, rfl, rfl, rfl, rfl⟩
    unfold Bad
    decide

/-- The first low carries of an exceptional state are distinct. -/
theorem bad_low_ne (t : State) (hbad : Bad t) :
    t.first.qLow ≠ t.first.sLow := by
  simp only [Bad, badStates, List.mem_cons, List.not_mem_nil, or_false] at hbad
  rcases hbad with rfl | rfl | rfl | rfl | rfl | rfl |
    rfl | rfl | rfl | rfl | rfl | rfl <;> decide

/-- An exceptional state cannot satisfy both first-layer carry meeting equations. -/
theorem bad_no_meeting (t : State) (hbad : Bad t) :
    ¬ (t.first.qLow = t.first.qHigh ∧ t.first.sLow = t.first.sHigh) := by
  simp only [Bad, badStates, List.mem_cons, List.not_mem_nil, or_false] at hbad
  rcases hbad with rfl | rfl | rfl | rfl | rfl | rfl |
    rfl | rfl | rfl | rfl | rfl | rfl <;> decide

end P196.CommonOverflowRigidity
