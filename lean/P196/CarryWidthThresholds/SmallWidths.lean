import P196.Agent10EightCarry.DifferenceObservability

/-!
Complete carry histories at the two smallest admissible initial widths.
At width one, the nine positive even pair sums have distinct four-word
histories. At width two, five words force the sole independent pair
difference to vanish by the existing smoothing formula.
-/

set_option maxRecDepth 100000
set_option maxHeartbeats 10000000

namespace CarryWidthThresholds

open DecimalDigits FoldedDecimal OverflowCarryNormalization CarryHistory
open CarryObservabilityActual DifferenceObservability

/-- This finite check uses the original pair dynamics and includes every
terminal carry in each of the four observed words. -/
private theorem singleton_four_injective :
    ∀ a b : Fin 9,
      (∀ t : Fin 4, ∀ i : Fin 4,
        i.val ≤ (iterPairs (fun _ => 2 * (a.val + 1)) 1 t.val).1 →
        carry (iterPairs (fun _ => 2 * (a.val + 1)) 1 t.val).2 i.val =
          carry (iterPairs (fun _ => 2 * (b.val + 1)) 1 t.val).2 i.val) →
      a = b := by
  decide +kernel

/-- Four complete carry words determine the active pair sum at initial
width one. Values outside the active width are unrestricted. -/
theorem four_carry_words_determine_pair_sums_of_width_one
    (q r : Nat → Nat)
    (hq : Admissible 1 q) (hr : Admissible 1 r)
    (hc : ∀ t, t < 4 → ∀ i, i ≤ (iterPairs q 1 t).1 →
      carry (iterPairs q 1 t).2 i = carry (iterPairs r 1 t).2 i) :
    ∀ i, i < 1 → q i = r i := by
  have hqp := hq.2.1
  have hrp := hr.2.1
  have hqb := hq.2.2.1 0 (by decide)
  have hrb := hr.2.2.1 0 (by decide)
  have hqe := hq.2.2.2.2 0 (by decide) (by decide)
  have hre := hr.2.2.2.2 0 (by decide) (by decide)
  let a : Fin 9 := ⟨q 0 / 2 - 1, by omega⟩
  let b : Fin 9 := ⟨r 0 / 2 - 1, by omega⟩
  have hqa : q 0 = 2 * (a.val + 1) := by dsimp [a]; omega
  have hrb' : r 0 = 2 * (b.val + 1) := by dsimp [b]; omega
  have hqa' : ∀ i, i < 1 → q i = 2 * (a.val + 1) := by
    intro i hi
    have : i = 0 := by omega
    simpa [this] using hqa
  have hrb'' : ∀ i, i < 1 → r i = 2 * (b.val + 1) := by
    intro i hi
    have : i = 0 := by omega
    simpa [this] using hrb'
  have hab : a = b := by
    apply singleton_four_injective a b
    intro t i hi
    rcases iterPairs_congr_upto q (fun _ => 2 * (a.val + 1)) 1 t.val hqa'
      with ⟨hqw, hqs⟩
    rcases iterPairs_congr_upto r (fun _ => 2 * (b.val + 1)) 1 t.val hrb''
      with ⟨hrw, hrs⟩
    have hqrw := matched_widths q r 1 t.val
      (fun s hs => hc s (by have := t.isLt; omega))
    have hiq : i.val ≤ (iterPairs q 1 t.val).1 := by omega
    have hir : i.val ≤ (iterPairs r 1 t.val).1 := by omega
    calc
      carry (iterPairs (fun _ => 2 * (a.val + 1)) 1 t.val).2 i.val =
          carry (iterPairs q 1 t.val).2 i.val :=
        (carry_congr_upto _ _ _ hqs i.val hiq).symm
      _ = carry (iterPairs r 1 t.val).2 i.val := hc t.val t.isLt i.val hiq
      _ = carry (iterPairs (fun _ => 2 * (b.val + 1)) 1 t.val).2 i.val :=
        carry_congr_upto _ _ _ hrs i.val hir
  intro i hi
  rw [hqa' i hi, hrb'' i hi, hab]

/-- Five complete carry words determine both active pair sums at initial
width two. The five possible no-overflow counts give a coefficient
multiplier of 10, 12, 12, 16, or 16 in the endpoint difference. -/
theorem five_carry_words_determine_pair_sums_of_width_two
    (q r : Nat → Nat)
    (hq : Admissible 2 q) (hr : Admissible 2 r)
    (hc : ∀ t, t < 5 → ∀ i, i ≤ (iterPairs q 2 t).1 →
      carry (iterPairs q 2 t).2 i = carry (iterPairs r 2 t).2 i) :
    ∀ i, i < 2 → q i = r i := by
  have hq1 : q 1 = q 0 := by simpa using hq.2.2.2.1 1 (by decide)
  have hr1 : r 1 = r 0 := by simpa using hr.2.2.2.1 1 (by decide)
  have hf := matched_difference_formula q r 2 4 hq hr
    (fun t ht => hc t (by omega))
  have hb := cappedDiff_bounds (iterPairs q 2 4).2 (iterPairs r 2 4).2
    (iterPairs q 2 4).1 (hc 4 (by decide))
  have hn := orbitCount_le q 2 4
  have hcases : orbitCount q 2 4 = 0 ∨ orbitCount q 2 4 = 1 ∨
      orbitCount q 2 4 = 2 ∨ orbitCount q 2 4 = 3 ∨ orbitCount q 2 4 = 4 := by
    omega
  have hzero : q 0 = r 0 := by
    rcases hcases with hN | hN | hN | hN | hN
    · have h := hb 2
      rw [hf 2, hN] at h
      simp [smoothPow, smooth, cappedDiff, hq1, hr1] at h
      omega
    · have h := hb 2
      rw [hf 2, hN] at h
      simp [smoothPow, smooth, cappedDiff, hq1, hr1] at h
      omega
    · have h := hb 1
      rw [hf 1, hN] at h
      simp [smoothPow, smooth, cappedDiff, hq1, hr1] at h
      omega
    · have h := hb 1
      rw [hf 1, hN] at h
      simp [smoothPow, smooth, cappedDiff, hq1, hr1] at h
      omega
    · have h := hb 0
      rw [hf 0, hN] at h
      simp [smoothPow, smooth, cappedDiff, hq1, hr1] at h
      omega
  intro i hi
  have hi' : i = 0 ∨ i = 1 := by omega
  rcases hi' with rfl | rfl
  · exact hzero
  · simpa [hq1, hr1] using hzero

#print axioms four_carry_words_determine_pair_sums_of_width_one
#print axioms five_carry_words_determine_pair_sums_of_width_two

end CarryWidthThresholds
