import P196.TerminalCarryCensus.Complement

/-!
The terminal carry census on the existing half-word product.
Complementation pairs the zero and one carries except for the unique
all-nine half word at even width. The empty half word is included, so
the balance identity and both closed forms also cover width zero.
-/

set_option autoImplicit false

namespace TerminalCarryCensus

open DecimalDigits Agent124.PrefixK SevenColumn.ShortBoundary

/-- Number of half words whose mirrored full word has terminal carry one. -/
def halfOnes (L : Nat) : Nat :=
  (halves L).countP (fun h => carry (wordFun (mirror L h)) L == 1)

private theorem all_nines_iff_replicate (L : Nat) (h : List Nat)
    (hh : h ∈ halves L) :
    h.all (fun a => a == 9) ↔ h = List.replicate ((L + 1) / 2) 9 := by
  have hlen := ((mem_halves_iff L h).mp hh).1
  simp only [List.all_eq_true, beq_iff_eq, List.eq_replicate_iff, hlen, true_and]

private theorem all_nines_count (L : Nat) :
    (halves L).countP (fun h => h.all (fun a => a == 9)) =
      if L % 2 = 0 then 1 else 0 := by
  by_cases he : L % 2 = 0
  · let w := List.replicate ((L + 1) / 2) 9
    have hw : w ∈ halves L := by
      apply (mem_halves_iff L w).mpr
      refine ⟨by simp [w], ?_, Or.inl he⟩
      intro a ha
      have ha9 : a = 9 := (List.mem_replicate.mp ha).2
      omega
    have hcount :
        (halves L).countP (fun h => h.all (fun a => a == 9)) =
          (halves L).count w := by
      rw [List.count_eq_countP]
      apply List.countP_congr
      intro h hh
      simpa only [beq_iff_eq] using all_nines_iff_replicate L h hh
    have hnd := List.Pairwise.filter (fun h : List Nat => h == w) (halves_nodup L)
    rw [List.filter_beq] at hnd
    have hle := List.nodup_replicate.mp hnd
    have hpos : 1 ≤ (halves L).count w := List.one_le_count_iff.mpr hw
    rw [hcount, if_pos he]
    omega
  · rw [if_neg he]
    apply List.countP_eq_zero.mpr
    intro h hh hnine
    have hrep := (all_nines_iff_replicate L h hh).mp hnine
    have hindex : L / 2 < (L + 1) / 2 := by omega
    have hcenter := ((mem_halves_iff L h).mp hh).2.2.resolve_left he
    have hget : h.getD (L / 2) 0 = 9 := by
      rw [hrep, List.getD_eq_getElem?_getD,
        List.getElem?_replicate_of_lt hindex]
      rfl
    rw [hget] at hcenter
    omega

/-- The all-nine even half is the only unpaired zero terminal carry. -/
theorem half_balance (L : Nat) :
    (halves L).length = 2 * halfOnes L + (if L % 2 = 0 then 1 else 0) := by
  let p : List Nat → Bool := fun h => carry (wordFun (mirror L h)) L == 1
  let a : List Nat → Bool := fun h => h.all (fun x => x == 9)
  have hswap := (halfComplement_perm L).countP_eq p
  rw [List.countP_map] at hswap
  have hpart := List.length_eq_countP_add_countP p (l := halves L)
  have hsplit := List.countP_eq_countP_filter_add (halves L) (fun h => ¬p h) a
  rw [List.countP_filter, List.countP_filter] at hsplit
  have hfirst :
      (halves L).countP (fun h => decide (¬p h) && a h) =
        (halves L).countP a := by
    apply List.countP_congr
    intro h hh
    have hsum := terminal_complement_sum L h hh
    dsimp [p, a]
    cases ha : h.all (fun x => x == 9) <;>
      simp [ha] at hsum ⊢ <;> omega
  have hsecond :
      (halves L).countP (fun h => decide (¬p h) && !a h) =
        (halves L).countP (p ∘ halfComplement) := by
    apply List.countP_congr
    intro h hh
    have hsum := terminal_complement_sum L h hh
    dsimp [p, a, Function.comp_def]
    cases ha : h.all (fun x => x == 9) <;>
      simp [ha] at hsum ⊢ <;> omega
  rw [hfirst, hsecond, hswap] at hsplit
  have hex : (halves L).countP a = if L % 2 = 0 then 1 else 0 := all_nines_count L
  change (halves L).length = 2 * (halves L).countP p + _
  omega

/-- Closed terminal-one count for even half-word products, including width zero. -/
theorem half_ones_even (m : Nat) : halfOnes (2 * m) = (19 ^ m - 1) / 2 := by
  have hmod : (2 * m) % 2 = 0 := by omega
  have hdiv : (2 * m) / 2 = m := by omega
  have hbalance : 19 ^ m = 2 * halfOnes (2 * m) + 1 := by
    simpa [halves_length, hmod, hdiv] using half_balance (2 * m)
  omega

/-- Closed terminal-one count for odd half-word products, including width one. -/
theorem half_ones_odd (m : Nat) : halfOnes (2 * m + 1) = 5 * 19 ^ m := by
  have hmod : (2 * m + 1) % 2 = 1 := by omega
  have hdiv : (2 * m + 1) / 2 = m := by omega
  have hbalance : 10 * 19 ^ m = 2 * halfOnes (2 * m + 1) := by
    simpa [halves_length, hmod, hdiv] using half_balance (2 * m + 1)
  omega

end TerminalCarryCensus

#print axioms TerminalCarryCensus.half_balance
#print axioms TerminalCarryCensus.half_ones_even
#print axioms TerminalCarryCensus.half_ones_odd
