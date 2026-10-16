import Agent9NumericMarkerCount
import FiniteHorizonBlocks

/-! The direct finite positive-hit count consequence of equation (3).
The original `mirroredNines_safe_prefix` supplies all orbit dynamics. -/

namespace P196.Agent9.Ensemble

open Agent101 DecimalDigits Lychrel196 FiniteHorizonBlocks

theorem numericMarker_iff_mirroredNines (n : Nat) (d : Nat → Nat) (L a r : Nat)
    (hc : Canonical n d L) (har : a + r ≤ L) :
    NumericMarker n L a r ↔ MirroredNines d L a r := by
  constructor
  · intro hm
    refine ⟨har, ?_⟩
    intro i hia hir
    have hi : i < L := by omega
    have h := hm (i - a) (by omega)
    rw [show a + (i - a) = i by omega,
      canonical_numericDigit n d L i hc hi,
      canonical_numericDigit n d L (L - 1 - i) hc (by omega)] at h
    exact h
  · intro hm i hi
    have hl : a + i < L := by omega
    rw [canonical_numericDigit n d L (a + i) hc hl,
      canonical_numericDigit n d L (L - 1 - (a + i)) hc (by omega)]
    exact hm.2 (a + i) (by omega) (by omega)

/-- Exactly the half-open canonical decimal interval. -/
def widthSeeds (L : Nat) : List Nat := List.range' (10 ^ (L - 1)) (9 * 10 ^ (L - 1))

theorem mem_widthSeeds (L n : Nat) (hL : 0 < L) :
    n ∈ widthSeeds L ↔ decimalWidth n L := by
  have hp : 10 ^ L = 10 ^ (L - 1) * 10 := by
    calc
      10 ^ L = 10 ^ ((L - 1) + 1) := congrArg (fun k : Nat => 10 ^ k) (by omega)
      _ = 10 ^ (L - 1) * 10 := by rw [Nat.pow_succ]
  simp only [widthSeeds, List.mem_range'_1, decimalWidth]
  omega

theorem widthSeeds_nodup (L : Nat) : (widthSeeds L).Nodup := List.nodup_range'

theorem length_widthSeeds (L : Nat) : (widthSeeds L).length = 9 * 10 ^ (L - 1) :=
  List.length_range'

/-- Computable finite check at precisely the positive times `1,...,R+1`. -/
def positiveHitB (n R : Nat) : Bool :=
  (List.range (R + 1)).any fun k => decide (Palindrome (orbit n (k + 1)))

theorem positiveHitB_iff (n R : Nat) :
    positiveHitB n R = true ↔ ∃ k, k ≤ R ∧ Palindrome (orbit n (k + 1)) := by
  simp [positiveHitB, List.any_eq_true, Nat.lt_succ_iff]

def positiveHits (L R : Nat) : List Nat := (widthSeeds L).filter (positiveHitB · R)

theorem mem_positiveHits (L R n : Nat) (hL : 0 < L) :
    n ∈ positiveHits L R ↔ decimalWidth n L ∧
      ∃ t, 1 ≤ t ∧ t ≤ R + 1 ∧ Palindrome (orbit n t) := by
  rw [positiveHits, List.mem_filter, mem_widthSeeds L n hL, positiveHitB_iff]
  constructor
  · rintro ⟨hw, k, hk, hp⟩
    exact ⟨hw, k + 1, by omega, by omega, hp⟩
  · rintro ⟨hw, t, ht, hR, hp⟩
    exact ⟨hw, t - 1, by omega, by simpa only [Nat.sub_add_cancel ht] using hp⟩

theorem positiveHits_nodup (L R : Nat) : (positiveHits L R).Nodup := by
  apply List.Pairwise.filter
  exact widthSeeds_nodup L

theorem nodup_length_le_of_subset (xs ys : List Nat)
    (hx : xs.Nodup) (hsub : xs ⊆ ys) : xs.length ≤ ys.length := by
  induction xs generalizing ys with
  | nil => simp
  | cons x xs ih =>
    have hd := List.pairwise_cons.mp hx
    have hxy : x ∈ ys := hsub (by simp)
    have htail : xs ⊆ ys.erase x := by
      intro z hz
      apply (List.mem_erase_of_ne (show z ≠ x by
        intro he; exact hd.1 z hz he.symm)).mpr
      exact hsub (by simp [hz])
    have h := ih (ys.erase x) hd.2 htail
    have he := List.length_erase_of_mem hxy
    have hp := List.length_pos_of_mem hxy
    simp only [List.length_cons]
    omega

theorem positiveHits_subset_unmarkedSeeds (L R : Nat) (hL : 0 < L) :
    positiveHits L R ⊆ unmarkedSeeds L (blockLength R) := by
  intro n hn
  obtain ⟨hw, t, ht, hR, hp⟩ := (mem_positiveHits L R n hL).mp hn
  obtain ⟨d, hc⟩ := (decimalWidth_iff_canonical n L).mp hw
  apply (mem_unmarkedSeeds L (blockLength R) n hL (blockLength_positive R)).mpr
  refine ⟨hw, ?_⟩
  intro j hj hm
  have hb := selected_block_bound L (blockLength R) j hL (blockLength_positive R) hj
  have hnine := (numericMarker_iff_mirroredNines n d L (1 + j * blockLength R)
    (blockLength R) hc hb).mp hm
  have hsafe := mirroredNines_safe_prefix n d L (1 + j * blockLength R) R (t - 1)
    hc (by omega) hnine
  apply hsafe
  simpa only [Nat.sub_add_cancel ht] using hp

/-- Direct natural-number upper count for all positive hits through `R+1`.
The seed at time zero may itself be a palindrome. -/
theorem positiveHits_count_le (L R : Nat) (hL : 0 < L) :
    (positiveHits L R).length ≤
      9 * 10 ^ (L - 1 - 2 * blockLength R * markerCount L (blockLength R)) *
        (10 ^ (2 * blockLength R) - 1) ^ markerCount L (blockLength R) := by
  rw [← length_unmarkedSeeds L (blockLength R) hL]
  exact nodup_length_le_of_subset _ _ (positiveHits_nodup L R)
    (positiveHits_subset_unmarkedSeeds L R hL)

end P196.Agent9.Ensemble
