import P196.Agent102AffineScalar.Agent102AffineArithmetic

/-!
Agent #102: an exact affine description of every literal run boundary on a tail.
No decimal carry operation is approximated here; these are List-level identities.
-/

namespace Agent102

def maxList : List Nat → Nat
  | [] => 0
  | n :: ns => max n (maxList ns)

theorem le_maxList_of_mem {n : Nat} {ns : List Nat} (h : n ∈ ns) : n ≤ maxList ns := by
  induction ns with
  | nil => simp at h
  | cons m ms ih =>
    rcases List.mem_cons.mp h with h | h
    · subst n
      exact Nat.le_max_left _ _
    · exact Nat.le_trans (ih h) (Nat.le_max_right _ _)

def lengthCutoff : List RunSpec → Nat
  | [] => 0
  | r :: rs => max r.length.cutoff (lengthCutoff rs)

theorem cutoff_le_lengthCutoff {r : RunSpec} {rs : List RunSpec} (h : r ∈ rs) :
    r.length.cutoff ≤ lengthCutoff rs := by
  induction rs with
  | nil => simp at h
  | cons s ss ih =>
    rcases List.mem_cons.mp h with h | h
    · subst r
      exact Nat.le_max_left _ _
    · exact Nat.le_trans (ih h) (Nat.le_max_right _ _)

@[simp] theorem wordAt_nil (k : Nat) : wordAt [] k = [] := rfl

@[simp] theorem wordAt_cons (r : RunSpec) (rs : List RunSpec) (k : Nat) :
    wordAt (r :: rs) k = List.replicate (r.length.eval k).toNat r.digit ++ wordAt rs k := rfl

def widthAffine : List RunSpec → Affine
  | [] => Affine.zero
  | r :: rs => r.length.positivePart.add (widthAffine rs)

theorem widthAffine_eval (rs : List RunSpec) (k : Nat) (hk : lengthCutoff rs ≤ k) :
    (widthAffine rs).eval k = ((wordAt rs k).length : Int) := by
  induction rs with
  | nil => simp [widthAffine]
  | cons r rs ih =>
    have hr : r.length.cutoff ≤ k := Nat.le_trans (Nat.le_max_left _ _) hk
    have ht : lengthCutoff rs ≤ k := Nat.le_trans (Nat.le_max_right _ _) hk
    simp only [widthAffine, Affine.eval_add, wordAt_cons, List.length_append,
      List.length_replicate, Int.natCast_add]
    rw [Affine.eval_positivePart r.length k hr, ih ht]

theorem widthAffine_nonneg (rs : List RunSpec) (k : Nat) (hk : lengthCutoff rs ≤ k) :
    0 ≤ (widthAffine rs).eval k := by
  rw [widthAffine_eval rs k hk]
  exact Int.ofNat_zero_le _

structure AffineSpan where
  digit : Nat
  lo : Affine
  hi : Affine
  deriving DecidableEq, Repr

def AffineSpan.at (s : AffineSpan) (k : Nat) : Span :=
  ⟨s.digit, (s.lo.eval k).toNat, (s.hi.eval k).toNat⟩

def spanSpecsFrom (start : Affine) : List RunSpec → List AffineSpan
  | [] => []
  | r :: rs =>
      ⟨r.digit, start, start.add r.length.positivePart⟩ ::
        spanSpecsFrom (start.add r.length.positivePart) rs

def spanSpecs (rs : List RunSpec) : List AffineSpan := spanSpecsFrom Affine.zero rs

theorem spanSpecsFrom_at (rs : List RunSpec) (start : Affine) (k : Nat)
    (hk : lengthCutoff rs ≤ k) (hs : 0 ≤ start.eval k) :
    (spanSpecsFrom start rs).map (fun s => s.at k) =
      spansFrom (start.eval k).toNat (runsAt rs k) := by
  induction rs generalizing start with
  | nil => rfl
  | cons r rs ih =>
    have hr : r.length.cutoff ≤ k := Nat.le_trans (Nat.le_max_left _ _) hk
    have ht : lengthCutoff rs ≤ k := Nat.le_trans (Nat.le_max_right _ _) hk
    have hp := Affine.eval_positivePart r.length k hr
    have hp0 := Affine.eval_positivePart_nonneg r.length k hr
    have ha : 0 ≤ (start.add r.length.positivePart).eval k := by
      rw [Affine.eval_add]
      omega
    have he : ((start.add r.length.positivePart).eval k).toNat =
        (start.eval k).toNat + (r.length.eval k).toNat := by
      rw [Affine.eval_add, Int.toNat_add hs hp0, hp]
      omega
    simp only [spanSpecsFrom, List.map_cons, runsAt, List.map_cons, spansFrom]
    rw [ih _ ht ha]
    simp only [AffineSpan.at, he, runsAt]

theorem spanSpecs_at (rs : List RunSpec) (k : Nat) (hk : lengthCutoff rs ≤ k) :
    (spanSpecs rs).map (fun s => s.at k) = spans (runsAt rs k) := by
  simpa only [spanSpecs, spans, Affine.eval_zero, Int.toNat_zero] using
    spanSpecsFrom_at rs Affine.zero k hk (by simp)

theorem spanSpecsFrom_nonneg (rs : List RunSpec) (start : Affine) (k : Nat)
    (hk : lengthCutoff rs ≤ k) (hs : 0 ≤ start.eval k) :
    ∀ s ∈ spanSpecsFrom start rs, 0 ≤ s.lo.eval k ∧ 0 ≤ s.hi.eval k := by
  induction rs generalizing start with
  | nil => simp [spanSpecsFrom]
  | cons r rs ih =>
    have hr : r.length.cutoff ≤ k := Nat.le_trans (Nat.le_max_left _ _) hk
    have ht : lengthCutoff rs ≤ k := Nat.le_trans (Nat.le_max_right _ _) hk
    have hp := Affine.eval_positivePart_nonneg r.length k hr
    have ha : 0 ≤ (start.add r.length.positivePart).eval k := by
      rw [Affine.eval_add]
      omega
    intro s hm
    rcases List.mem_cons.mp hm with he | hm
    · subst s
      exact ⟨hs, ha⟩
    · exact ih _ ht ha s hm

theorem spanSpecs_nonneg (rs : List RunSpec) (k : Nat) (hk : lengthCutoff rs ≤ k) :
    ∀ s ∈ spanSpecs rs, 0 ≤ s.lo.eval k ∧ 0 ≤ s.hi.eval k :=
  spanSpecsFrom_nonneg rs Affine.zero k hk (by simp)

def endpoints (rs : List RunSpec) : List Affine :=
  widthAffine rs :: (spanSpecs rs).flatMap (fun s => [s.lo, s.hi])

theorem widthAffine_mem_endpoints (rs : List RunSpec) : widthAffine rs ∈ endpoints rs := by
  simp [endpoints]

theorem lo_mem_endpoints {rs : List RunSpec} {s : AffineSpan} (hs : s ∈ spanSpecs rs) :
    s.lo ∈ endpoints rs := by
  simp only [endpoints, List.mem_cons, List.mem_flatMap]
  exact Or.inr ⟨s, hs, by simp⟩

theorem hi_mem_endpoints {rs : List RunSpec} {s : AffineSpan} (hs : s ∈ spanSpecs rs) :
    s.hi ∈ endpoints rs := by
  simp only [endpoints, List.mem_cons, List.mem_flatMap]
  exact Or.inr ⟨s, hs, by simp⟩

theorem endpoints_nonneg (rs : List RunSpec) (k : Nat) (hk : lengthCutoff rs ≤ k) :
    ∀ f ∈ endpoints rs, 0 ≤ f.eval k := by
  intro f hf
  rcases List.mem_cons.mp hf with he | hf
  · subst f
    exact widthAffine_nonneg rs k hk
  · rcases List.mem_flatMap.mp hf with ⟨s, hs, hf⟩
    have h := spanSpecs_nonneg rs k hk s hs
    simp only [List.mem_cons, List.not_mem_nil, or_false] at hf
    rcases hf with he | he
    · subst f
      exact h.1
    · subst f
      exact h.2

end Agent102
