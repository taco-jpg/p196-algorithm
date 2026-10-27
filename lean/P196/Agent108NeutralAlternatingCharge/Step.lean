import P196.Agent108NeutralAlternatingCharge.Base

/-!
The existing decimal alternating charge, specialized to the unchanged
Agent120 neutral exterior. This is an API bridge, not a new invariant.
-/

namespace Agent108.NeutralCharge

open Agent120.Neutral
open Agent2Exterior (paritySign alternatingSum alternatingSum_append
  alternatingSum_reverse alternatingSum_zip_add paritySign_cases)

private theorem nextB_length_zero {B C : List Nat} (hg : gam 10 B C = 0) :
    (nextB 10 B C).length = B.length := by
  simp [nextB, hg, length_DB, length_DR]

private theorem nextB_length_one {B C : List Nat} (hg : gam 10 B C = 1) :
    (nextB 10 B C).length = B.length + 1 := by
  simp [nextB, hg, length_DB, length_DR]

theorem raw_charge_nooverflow {B C : List Nat}
    (h : Hyp 10 B C) (hg : gam 10 B C = 0) :
    charge (nextB 10 B C) % 11 = (2 * charge B) % 11 := by
  have hD := norm_alternating_mod11 B 0
  have hR := norm_alternating_mod11 B.reverse (e2 10 B C)
  change (alternatingSum (DB 10 B) + paritySign B.length * (e1 10 B : Int)) % 11 =
    (alternatingSum B + (0 : Int)) % 11 at hD
  change (alternatingSum (DR 10 B C) + paritySign B.reverse.length *
    (gam 10 B C : Int)) % 11 =
    (alternatingSum B.reverse + (e2 10 B C : Int)) % 11 at hR
  simp only [List.length_reverse, alternatingSum_reverse, hg,
    Int.ofNat_zero, Int.mul_zero, Int.add_zero] at hD hR
  have h1 := h.e1_le
  have h2 := h.e2_le
  have hf := h.flip
  have hc : e1 10 B + e2 10 B C = 1 := by omega
  unfold charge Agent2Exterior.alternatingCharge
  rw [nextB_length_zero hg]
  simp only [nextB, hg, if_true]
  rw [alternatingSum_zip_add _ _ (by simp [length_DB, length_DR])]
  simp only [alternatingSum_reverse, length_DR]
  rcases paritySign_cases B.length with hs | hs <;>
    simp only [hs, Int.one_mul, Int.neg_mul, Int.neg_neg] at * <;> omega

theorem raw_charge_overflow {B C : List Nat}
    (h : Hyp 10 B C) (hg : gam 10 B C = 1) :
    charge (nextB 10 B C) % 11 = 0 := by
  have hD := norm_alternating_mod11 B 0
  have hR := norm_alternating_mod11 B.reverse (e2 10 B C)
  change (alternatingSum (DB 10 B) + paritySign B.length * (e1 10 B : Int)) % 11 =
    (alternatingSum B + (0 : Int)) % 11 at hD
  change (alternatingSum (DR 10 B C) + paritySign B.reverse.length *
    (gam 10 B C : Int)) % 11 =
    (alternatingSum B.reverse + (e2 10 B C : Int)) % 11 at hR
  simp only [List.length_reverse, alternatingSum_reverse, hg,
    Int.ofNat_one, Int.mul_one, Int.add_zero] at hD hR
  have h1 := h.e1_le
  have h2 := h.e2_le
  have hf := h.flip
  have hother : e2 10 B C = 1 - e1 10 B := by omega
  unfold charge Agent2Exterior.alternatingCharge
  rw [nextB_length_one hg]
  simp only [nextB, hg, Nat.one_ne_zero, if_false, paritySign]
  rw [alternatingSum_zip_add _ _ (by simp [length_DB, length_DR])]
  simp only [alternatingSum_append, alternatingSum_reverse, length_DB,
    length_DR, alternatingSum, Int.sub_zero]
  rcases paritySign_cases B.length with hs | hs <;>
    rcases (by omega : e1 10 B = 0 ∨ e1 10 B = 1) with he | he <;>
    simp only [hs, he, hother, xd, he, Int.one_mul, Int.neg_mul,
      Int.neg_neg, Nat.sub_zero, Nat.sub_self, Nat.mul_zero, Nat.mul_one,
      Int.ofNat_zero, Int.mul_zero, Int.add_zero] at * <;> omega

/-- The actual Boolean edge checker gives reset/doubling after any legal trim. -/
theorem edge_charge_step {E : Edge} (h : edgeOK 10 E = true) :
    charge E.B2 % 11 =
      (if gam 10 E.B E.C = 0 then 2 * charge E.B else 0) % 11 := by
  obtain ⟨hyp, hB, _⟩ := edgeOK_sound h
  have ht : charge (nextB 10 E.B E.C) = charge E.B2 := by
    rw [hB]
    exact charge_append_neutral E.B2 E.u
  by_cases hg : gam 10 E.B E.C = 0
  · simpa only [hg, if_true, ht] using raw_charge_nooverflow hyp hg
  · have hle := hyp.gam_le
    have hpos : gam 10 E.B E.C = 1 := by omega
    simpa only [hg, if_false, Int.zero_emod, ht] using raw_charge_overflow hyp hpos

end Agent108.NeutralCharge
