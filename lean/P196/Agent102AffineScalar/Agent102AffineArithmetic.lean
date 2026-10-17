import P196.Agent102AffineScalar.Agent102RunDefs

/-!
Agent #102: exact scalar arithmetic for eventual affine run lengths.
All bounds are explicit and retain negative slopes and zero-length cases.
-/

namespace Agent102.Affine

@[simp] theorem eval_zero (k : Nat) : zero.eval k = 0 := by
  simp [eval, zero]

@[simp] theorem eval_add (f g : Agent102.Affine) (k : Nat) :
    (f.add g).eval k = f.eval k + g.eval k := by
  dsimp [eval, add]
  rw [Int.add_mul]
  omega

theorem intercept_bounds_of_cutoff (f : Agent102.Affine) (k : Nat)
    (hk : f.cutoff ≤ k) : -(k : Int) < f.intercept ∧ f.intercept < (k : Int) := by
  have hu : f.intercept ≤ (f.intercept.natAbs : Int) := Int.le_natAbs
  have hl : -f.intercept ≤ (f.intercept.natAbs : Int) := by
    simpa only [Int.natAbs_neg] using (Int.le_natAbs (a := -f.intercept))
  unfold cutoff at hk
  omega

theorem eval_pos_of_slope_pos (f : Agent102.Affine) (k : Nat)
    (hk : f.cutoff ≤ k) (hs : 0 < f.slope) : 0 < f.eval k := by
  have hb := (intercept_bounds_of_cutoff f k hk).1
  have hs' : (1 : Int) ≤ f.slope := by omega
  have hm := Int.mul_le_mul_of_nonneg_right hs' (Int.ofNat_zero_le k)
  simp only [Int.one_mul] at hm
  unfold eval
  omega

theorem eval_neg_of_slope_neg (f : Agent102.Affine) (k : Nat)
    (hk : f.cutoff ≤ k) (hs : f.slope < 0) : f.eval k < 0 := by
  have hb := (intercept_bounds_of_cutoff f k hk).2
  have hs' : f.slope ≤ (-1 : Int) := by omega
  have hm := Int.mul_le_mul_of_nonneg_right hs' (Int.ofNat_zero_le k)
  have hm' : f.slope * (k : Int) ≤ -(k : Int) := by simpa using hm
  unfold eval
  omega

theorem eval_nonneg_iff (f : Agent102.Affine) (k : Nat) (hk : f.cutoff ≤ k) :
    0 ≤ f.eval k ↔ 0 < f.slope ∨ (f.slope = 0 ∧ 0 ≤ f.intercept) := by
  constructor
  · intro h
    by_cases hs : f.slope < 0
    · have hn := eval_neg_of_slope_neg f k hk hs
      omega
    · by_cases hz : f.slope = 0
      · right
        refine ⟨hz, ?_⟩
        simpa only [eval, hz, Int.zero_mul, Int.zero_add] using h
      · left
        omega
  · rintro (hs | ⟨hs, hb⟩)
    · exact Int.le_of_lt (eval_pos_of_slope_pos f k hk hs)
    · simpa only [eval, hs, Int.zero_mul, Int.zero_add] using hb

theorem eval_neg_iff (f : Agent102.Affine) (k : Nat) (hk : f.cutoff ≤ k) :
    f.eval k < 0 ↔ f.slope < 0 ∨ (f.slope = 0 ∧ f.intercept < 0) := by
  have h := eval_nonneg_iff f k hk
  omega

theorem eval_positivePart (f : Agent102.Affine) (k : Nat) (hk : f.cutoff ≤ k) :
    f.positivePart.eval k = ((f.eval k).toNat : Int) := by
  unfold positivePart
  split
  · rename_i h
    have hn := (eval_neg_iff f k hk).2 h
    simp [Int.toNat_of_nonpos (Int.le_of_lt hn)]
  · rename_i h
    have hn : 0 ≤ f.eval k := by
      have hneg := eval_neg_iff f k hk
      omega
    exact (Int.toNat_of_nonneg hn).symm

theorem eval_positivePart_nonneg (f : Agent102.Affine) (k : Nat)
    (hk : f.cutoff ≤ k) : 0 ≤ f.positivePart.eval k := by
  rw [eval_positivePart f k hk]
  exact Int.ofNat_zero_le _

/-- A shared explicit threshold for every pairwise comparison of two affine data. -/
def compareCutoff (f g : Agent102.Affine) : Nat :=
  f.intercept.natAbs + g.intercept.natAbs + 1

theorem compareCutoff_comm (f g : Agent102.Affine) :
    compareCutoff f g = compareCutoff g f := by
  unfold compareCutoff
  omega

theorem eval_lt_of_slope_lt (f g : Agent102.Affine) (k : Nat)
    (hk : compareCutoff f g ≤ k) (hs : f.slope < g.slope) : f.eval k < g.eval k := by
  have hs' : f.slope + 1 ≤ g.slope := by omega
  have hm := Int.mul_le_mul_of_nonneg_right hs' (Int.ofNat_zero_le k)
  rw [Int.add_mul, Int.one_mul] at hm
  have hf : f.intercept ≤ (f.intercept.natAbs : Int) := Int.le_natAbs
  have hg : -g.intercept ≤ (g.intercept.natAbs : Int) := by
    simpa only [Int.natAbs_neg] using (Int.le_natAbs (a := -g.intercept))
  unfold compareCutoff at hk
  unfold eval
  omega

theorem eval_le_iff (f g : Agent102.Affine) (k : Nat)
    (hk : compareCutoff f g ≤ k) :
    f.eval k ≤ g.eval k ↔
      f.slope < g.slope ∨ (f.slope = g.slope ∧ f.intercept ≤ g.intercept) := by
  constructor
  · intro h
    by_cases hs : f.slope < g.slope
    · exact Or.inl hs
    · by_cases he : f.slope = g.slope
      · right
        refine ⟨he, ?_⟩
        unfold eval at h
        rw [he] at h
        omega
      · have hrev : g.slope < f.slope := by omega
        have hk' : compareCutoff g f ≤ k := by
          simpa only [compareCutoff_comm g f] using hk
        have hv := eval_lt_of_slope_lt g f k hk' hrev
        omega
  · rintro (hs | ⟨hs, hb⟩)
    · exact Int.le_of_lt (eval_lt_of_slope_lt f g k hk hs)
    · unfold eval
      rw [hs]
      omega

theorem eval_lt_iff (f g : Agent102.Affine) (k : Nat)
    (hk : compareCutoff f g ≤ k) :
    f.eval k < g.eval k ↔
      f.slope < g.slope ∨ (f.slope = g.slope ∧ f.intercept < g.intercept) := by
  have hk' : compareCutoff g f ≤ k := by
    simpa only [compareCutoff_comm g f] using hk
  have h := eval_le_iff g f k hk'
  omega

theorem eval_eq_iff (f g : Agent102.Affine) (k : Nat)
    (hk : compareCutoff f g ≤ k) :
    f.eval k = g.eval k ↔ f.slope = g.slope ∧ f.intercept = g.intercept := by
  have hk' : compareCutoff g f ≤ k := by
    simpa only [compareCutoff_comm g f] using hk
  have h₁ := eval_le_iff f g k hk
  have h₂ := eval_le_iff g f k hk'
  omega

theorem eval_le_stable (f g : Agent102.Affine) (K k : Nat)
    (hK : compareCutoff f g ≤ K) (hk : K ≤ k) :
    (f.eval k ≤ g.eval k ↔ f.eval K ≤ g.eval K) :=
  (eval_le_iff f g k (Nat.le_trans hK hk)).trans (eval_le_iff f g K hK).symm

theorem eval_lt_stable (f g : Agent102.Affine) (K k : Nat)
    (hK : compareCutoff f g ≤ K) (hk : K ≤ k) :
    (f.eval k < g.eval k ↔ f.eval K < g.eval K) :=
  (eval_lt_iff f g k (Nat.le_trans hK hk)).trans (eval_lt_iff f g K hK).symm

theorem eval_eq_stable (f g : Agent102.Affine) (K k : Nat)
    (hK : compareCutoff f g ≤ K) (hk : K ≤ k) :
    (f.eval k = g.eval k ↔ f.eval K = g.eval K) :=
  (eval_eq_iff f g k (Nat.le_trans hK hk)).trans (eval_eq_iff f g K hK).symm

#print axioms eval_zero
#print axioms eval_add
#print axioms eval_positivePart
#print axioms eval_le_iff
#print axioms eval_lt_iff
#print axioms eval_eq_iff
#print axioms eval_le_stable
#print axioms eval_lt_stable
#print axioms eval_eq_stable

end Agent102.Affine
