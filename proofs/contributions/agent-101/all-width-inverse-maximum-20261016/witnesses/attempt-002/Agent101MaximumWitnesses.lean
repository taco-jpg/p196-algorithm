import Agent105CrossWidth9df76b

/-!
Agent 101: explicit attainment of the all-width numerical inverse maximum.
For output width D >= 2 the half-profile consists of nines; an odd-width
profile has center zero. Different-width predecessors are excluded by the
published Agent 105 target-digit theorem. The original fixed-width fiber
enumeration supplies all multiplicities. No global upper bound is reproved.
-/

namespace Agent101.MaximumWitnesses

open Lychrel196 DecimalDigits

def maximumHalf (D : Nat) : List Nat := List.replicate (D / 2) 9

def maximumCenter (D : Nat) : Option Nat := if D % 2 = 0 then none else some 0

def maximumWord (D : Nat) : List Nat :=
  coefficientWord (maximumHalf D) (maximumCenter D)

def maximumTarget (D : Nat) : Nat := natValue (maximumWord D)

def maximumPreimages (D : Nat) : List Nat :=
  numericFiber (maximumHalf D) (maximumCenter D)

theorem maximumHalf_cons (D : Nat) (hD : 2 ≤ D) :
    maximumHalf D = 9 :: List.replicate (D / 2 - 1) 9 := by
  have hhalf : D / 2 = (D / 2 - 1) + 1 := by omega
  simpa only [maximumHalf, List.replicate_succ] using
    congrArg (fun r => List.replicate r 9) hhalf

theorem length_maximumWord (D : Nat) : (maximumWord D).length = D := by
  by_cases heven : D % 2 = 0 <;>
    simp [maximumWord, maximumHalf, maximumCenter, heven, length_coefficientWord] <;>
    omega

theorem maximumWord_bounded (D : Nat) : digitsBounded (maximumWord D) := by
  intro a ha
  simp only [maximumWord, coefficientWord, List.mem_append, List.mem_reverse,
    maximumHalf, List.mem_replicate] at ha
  rcases ha with (ha | ha) | ha
  · omega
  · unfold maximumCenter at ha
    split at ha
    · simp at ha
    · simp at ha
      omega
  · omega

theorem maximumWord_canonical (D : Nat) (hD : 2 ≤ D) :
    canonicalDigits (maximumWord D) := by
  refine ⟨maximumWord_bounded D, ?_⟩
  have hword : maximumWord D =
      wrapDigits 9 9 (coefficientWord (List.replicate (D / 2 - 1) 9)
        (maximumCenter D)) := by
    simp only [maximumWord, maximumHalf_cons D hD, coefficientWord_cons]
  rw [hword, getLastD_wrapDigits]
  decide

theorem maximumWord_units (D : Nat) (hD : 2 ≤ D) :
    digitFn (maximumWord D) 0 = 9 := by
  simp only [maximumWord, maximumHalf_cons D hD, coefficientWord_cons]
  rfl

theorem maximumTarget_width (D : Nat) (hD : 2 ≤ D) :
    decimalWidth (maximumTarget D) D := by
  have hw := canonical_decimalWidth _ _ _
    ((canonicalDigits_iff (maximumWord D)).mp (maximumWord_canonical D hD))
  simpa only [maximumTarget, length_maximumWord] using hw

theorem maximumCenter_count (D : Nat) : centerCount (maximumCenter D) = 1 := by
  unfold maximumCenter
  split <;> rfl

theorem maximumPreimages_nodup (D : Nat) : (maximumPreimages D).Nodup :=
  numericFiber_nodup (maximumHalf D) (maximumCenter D)

theorem length_maximumPreimages (D : Nat) (hD : 2 ≤ D) :
    (maximumPreimages D).length = 9 * 10 ^ (D / 2 - 1) := by
  unfold maximumPreimages
  rw [length_numericFiber, maximumHalf_cons D hD]
  exact profileCount_nines (D / 2 - 1) (maximumCenter D) (maximumCenter_count D)

theorem mem_maximumPreimages_fixed (D n : Nat) :
    n ∈ maximumPreimages D ↔ decimalWidth n D ∧ step n = maximumTarget D := by
  have hb : ∀ a ∈ coefficientWord (maximumHalf D) (maximumCenter D), a ≤ 18 := by
    intro a ha
    have h9 := maximumWord_bounded D a ha
    omega
  have hf := mem_numericFiber (maximumHalf D) (maximumCenter D) n hb
  change n ∈ maximumPreimages D ↔
    decimalWidth n (maximumWord D).length ∧ step n = maximumTarget D at hf
  simpa only [length_maximumWord] using hf

theorem maximumPreimages_nonempty (D : Nat) (hD : 2 ≤ D) :
    ∃ n, n ∈ maximumPreimages D := by
  have hpos : 0 < (maximumPreimages D).length := by
    rw [length_maximumPreimages D hD]
    exact Nat.mul_pos (by decide) (Nat.pow_pos (by decide))
  cases he : maximumPreimages D with
  | nil => simp only [he, List.length_nil, Nat.lt_irrefl] at hpos
  | cons n ns => exact ⟨n, by simp [he]⟩

/-- The displayed finite list is the complete inverse fiber across every
positive input width, with no width condition left on the right side. -/
theorem mem_maximumPreimages (D : Nat) (hD : 2 ≤ D) (n : Nat) :
    n ∈ maximumPreimages D ↔ 0 < n ∧ step n = maximumTarget D := by
  constructor
  · intro hn
    obtain ⟨hw, hs⟩ := (mem_maximumPreimages_fixed D n).mp hn
    exact ⟨Nat.lt_of_lt_of_le (Nat.pow_pos (by decide)) hw.2.1, hs⟩
  · rintro ⟨hn, hs⟩
    obtain ⟨a, ha⟩ := maximumPreimages_nonempty D hD
    obtain ⟨hwa, hsa⟩ := (mem_maximumPreimages_fixed D a).mp ha
    obtain ⟨da, hca⟩ := (decimalWidth_iff_canonical a D).mp hwa
    obtain ⟨dn, L, hcn⟩ := canonical_exists n hn
    have htarget : Canonical (maximumTarget D) (digitFn (maximumWord D)) D := by
      simpa only [maximumTarget, length_maximumWord] using
        (canonicalDigits_iff (maximumWord D)).mp (maximumWord_canonical D hD)
    have houtn : Canonical (step n) (digitFn (maximumWord D)) D := by
      rw [hs]
      exact htarget
    have houta : Canonical (step a) (digitFn (maximumWord D)) D := by
      rw [hsa]
      exact htarget
    have hLD : L = D := by
      by_cases heq : L = D
      · exact heq
      · have hunit : digitFn (maximumWord D) 0 = 1 := by
          rcases Nat.lt_or_gt_of_ne heq with hlt | hgt
          · exact (Agent105CrossWidth9df76b.cross_width_target_digits
              hcn hca hlt (hs.trans hsa.symm) houtn).2.1
          · exact (Agent105CrossWidth9df76b.cross_width_target_digits
              hca hcn hgt (hsa.trans hs.symm) houta).2.1
        have hnine := maximumWord_units D hD
        omega
    apply (mem_maximumPreimages_fixed D n).mpr
    refine ⟨?_, hs⟩
    simpa only [hLD] using canonical_decimalWidth n dn L hcn

/-- The all-width maximum is attained for every output width at least two. -/
theorem all_width_maximum_witness (D : Nat) (hD : 2 ≤ D) :
    ∃ Y : Nat, ∃ ns : List Nat,
      decimalWidth Y D ∧ ns.Nodup ∧
      (∀ n, n ∈ ns ↔ 0 < n ∧ step n = Y) ∧
      ns.length = 9 * 10 ^ (D / 2 - 1) := by
  exact ⟨maximumTarget D, maximumPreimages D, maximumTarget_width D hD,
    maximumPreimages_nodup D, mem_maximumPreimages D hD,
    length_maximumPreimages D hD⟩

theorem one_digit_preimages (n : Nat) :
    n ∈ ([1] : List Nat) ↔ 0 < n ∧ step n = 2 := by
  constructor
  · intro hn
    have he : n = 1 := by simpa only [List.mem_singleton] using hn
    subst n
    decide
  · rintro ⟨hn, hs⟩
    have hle : n ≤ 2 := by
      have h : n ≤ step n := by unfold step; omega
      omega
    by_cases he : n = 1
    · simp [he]
    · have he2 : n = 2 := by omega
      subst n
      have htwo : step 2 = 4 := by decide
      omega

theorem one_digit_maximum_witness :
    ∃ Y : Nat, ∃ ns : List Nat,
      decimalWidth Y 1 ∧ ns.Nodup ∧
      (∀ n, n ∈ ns ↔ 0 < n ∧ step n = Y) ∧ ns.length = 1 := by
  exact ⟨2, [1], by simp [decimalWidth], by decide, one_digit_preimages, by decide⟩

#print axioms maximumHalf
#print axioms maximumCenter
#print axioms maximumWord
#print axioms maximumTarget
#print axioms maximumPreimages
#print axioms maximumHalf_cons
#print axioms length_maximumWord
#print axioms maximumWord_bounded
#print axioms maximumWord_canonical
#print axioms maximumWord_units
#print axioms maximumTarget_width
#print axioms maximumCenter_count
#print axioms maximumPreimages_nodup
#print axioms length_maximumPreimages
#print axioms mem_maximumPreimages_fixed
#print axioms maximumPreimages_nonempty
#print axioms mem_maximumPreimages
#print axioms all_width_maximum_witness
#print axioms one_digit_preimages
#print axioms one_digit_maximum_witness

end Agent101.MaximumWitnesses
