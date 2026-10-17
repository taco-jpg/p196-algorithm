import P196.Agent102AffineRuns.Agent102AffineRuns

/-!
Agent #102: a finite endpoint decision procedure for affine run words.
The executable Boolean never constructs a `wordAt` list or evaluates a large
cutoff parameter. Its soundness and completeness concern the original words.
-/

namespace Agent102

/-- Lexicographic coefficient order is the eventual strict affine order. -/
def Affine.ltOnTail (f g : Affine) : Prop :=
  f.slope < g.slope ∨ (f.slope = g.slope ∧ f.intercept < g.intercept)

instance (f g : Affine) : Decidable (f.ltOnTail g) := by
  unfold Affine.ltOnTail
  infer_instance

/-- Both self comparisons are necessary when a span has zero eventual length. -/
def AffineSpan.overlapsOnTail (s t : AffineSpan) : Prop :=
  s.lo.ltOnTail s.hi ∧ s.lo.ltOnTail t.hi ∧
    t.lo.ltOnTail s.hi ∧ t.lo.ltOnTail t.hi

instance (s t : AffineSpan) : Decidable (s.overlapsOnTail t) := by
  unfold AffineSpan.overlapsOnTail
  infer_instance

theorem endpoint_ltOnTail_iff (A B : List RunSpec) (f g : Affine)
    (hf : f ∈ endpoints A ++ endpoints B) (hg : g ∈ endpoints A ++ endpoints B)
    (k : Nat) (hk : equalityCutoff A B ≤ k) :
    f.ltOnTail g ↔ (f.eval k).toNat < (g.eval k).toNat := by
  have hcut := Nat.le_trans (compareCutoff_le_pairCutoff hf hg)
    (Nat.le_trans (pairCutoff_le_equalityCutoff A B) hk)
  have h := Affine.eval_lt_iff f g k hcut
  have hf0 := combined_endpoints_nonneg A B k hk f hf
  have hg0 := combined_endpoints_nonneg A B k hk g hg
  unfold Affine.ltOnTail
  omega

theorem width_eq_iff_coefficients (A B : List RunSpec) (k : Nat)
    (hk : equalityCutoff A B ≤ k) :
    (wordAt A k).length = (wordAt B k).length ↔
      (widthAffine A).slope = (widthAffine B).slope ∧
      (widthAffine A).intercept = (widthAffine B).intercept := by
  have ha : widthAffine A ∈ endpoints A ++ endpoints B :=
    List.mem_append_left _ (widthAffine_mem_endpoints A)
  have hb : widthAffine B ∈ endpoints A ++ endpoints B :=
    List.mem_append_right _ (widthAffine_mem_endpoints B)
  have hcut := Nat.le_trans (compareCutoff_le_pairCutoff ha hb)
    (Nat.le_trans (pairCutoff_le_equalityCutoff A B) hk)
  have h := Affine.eval_eq_iff (widthAffine A) (widthAffine B) k hcut
  rw [widthAffine_eval A k (Nat.le_trans (left_lengthCutoff_le A B) hk),
    widthAffine_eval B k (Nat.le_trans (right_lengthCutoff_le A B) hk)] at h
  omega

theorem span_overlapsOnTail_iff (A B : List RunSpec) (s t : AffineSpan)
    (hs : s ∈ spanSpecs A) (ht : t ∈ spanSpecs B)
    (k : Nat) (hk : equalityCutoff A B ≤ k) :
    s.overlapsOnTail t ↔ (s.at k).overlaps (t.at k) := by
  have hslo : s.lo ∈ endpoints A ++ endpoints B :=
    List.mem_append_left _ (lo_mem_endpoints hs)
  have hshi : s.hi ∈ endpoints A ++ endpoints B :=
    List.mem_append_left _ (hi_mem_endpoints hs)
  have htlo : t.lo ∈ endpoints A ++ endpoints B :=
    List.mem_append_right _ (lo_mem_endpoints ht)
  have hthi : t.hi ∈ endpoints A ++ endpoints B :=
    List.mem_append_right _ (hi_mem_endpoints ht)
  have h₁ := endpoint_ltOnTail_iff A B s.lo s.hi hslo hshi k hk
  have h₂ := endpoint_ltOnTail_iff A B s.lo t.hi hslo hthi k hk
  have h₃ := endpoint_ltOnTail_iff A B t.lo s.hi htlo hshi k hk
  have h₄ := endpoint_ltOnTail_iff A B t.lo t.hi htlo hthi k hk
  simp only [AffineSpan.overlapsOnTail, Span.overlaps_iff_four, AffineSpan.at]
  exact and_congr h₁ (and_congr h₂ (and_congr h₃ h₄))

/-- Only affine coefficients, digit equality, and a finite span-pair scan occur. -/
def fastEqualOnTail (A B : List RunSpec) : Bool :=
  decide ((widthAffine A).slope = (widthAffine B).slope ∧
    (widthAffine A).intercept = (widthAffine B).intercept) &&
  (spanSpecs A).all (fun s => (spanSpecs B).all (fun t =>
    decide (s.overlapsOnTail t → s.digit = t.digit)))

theorem fastEqualOnTail_iff_coefficients (A B : List RunSpec) :
    fastEqualOnTail A B = true ↔
      ((widthAffine A).slope = (widthAffine B).slope ∧
        (widthAffine A).intercept = (widthAffine B).intercept) ∧
      ∀ s ∈ spanSpecs A, ∀ t ∈ spanSpecs B,
        s.overlapsOnTail t → s.digit = t.digit := by
  simp only [fastEqualOnTail, Bool.and_eq_true, decide_eq_true_eq, List.all_eq_true]

/-- The finite test decides exact equality at every parameter beyond the bound. -/
theorem fastEqualOnTail_iff_wordAt (A B : List RunSpec) (k : Nat)
    (hk : equalityCutoff A B ≤ k) :
    fastEqualOnTail A B = true ↔ wordAt A k = wordAt B k := by
  rw [fastEqualOnTail_iff_coefficients,
    wordAt_eq_iff_spans A B k (Nat.le_trans (left_lengthCutoff_le A B) hk)
      (Nat.le_trans (right_lengthCutoff_le A B) hk),
    width_eq_iff_coefficients A B k hk]
  constructor
  · rintro ⟨hw, hd⟩
    refine ⟨hw, ?_⟩
    intro s hs t ht hov
    exact hd s hs t ht ((span_overlapsOnTail_iff A B s t hs ht k hk).mpr hov)
  · rintro ⟨hw, hd⟩
    refine ⟨hw, ?_⟩
    intro s hs t ht hov
    exact hd s hs t ht ((span_overlapsOnTail_iff A B s t hs ht k hk).mp hov)

theorem fastEqualOnTail_eq_equalOnTail (A B : List RunSpec) :
    fastEqualOnTail A B = equalOnTail A B := by
  have h := fastEqualOnTail_iff_wordAt A B (equalityCutoff A B) (Nat.le_refl _)
  simp only [equalOnTail]
  cases he : fastEqualOnTail A B
  · have hn : ¬ wordAt A (equalityCutoff A B) = wordAt B (equalityCutoff A B) := by
      intro hw
      have := h.mpr hw
      simp [he] at this
    simp [hn]
  · have hw := h.mp he
    simp [hw]

theorem fastEqualOnTail_spec (A B : List RunSpec) :
    fastEqualOnTail A B = true ↔
      ∀ k, equalityCutoff A B ≤ k → wordAt A k = wordAt B k := by
  rw [fastEqualOnTail_eq_equalOnTail]
  exact equalOnTail_spec A B

theorem fastUnequalOnTail_spec (A B : List RunSpec) :
    fastEqualOnTail A B = false ↔
      ∀ k, equalityCutoff A B ≤ k → wordAt A k ≠ wordAt B k := by
  rw [fastEqualOnTail_eq_equalOnTail]
  exact unequalOnTail_spec A B

def fastPalindromicOnTail (A : List RunSpec) : Bool := fastEqualOnTail A A.reverse

theorem fastPalindromicOnTail_eq (A : List RunSpec) :
    fastPalindromicOnTail A = palindromicOnTail A :=
  fastEqualOnTail_eq_equalOnTail A A.reverse

theorem fastPalindromicOnTail_spec (A : List RunSpec) :
    fastPalindromicOnTail A = true ↔
      ∀ k, palindromeCutoff A ≤ k → wordAt A k = (wordAt A k).reverse := by
  rw [fastPalindromicOnTail_eq]
  exact palindromicOnTail_spec A

theorem fastNonpalindromicOnTail_spec (A : List RunSpec) :
    fastPalindromicOnTail A = false ↔
      ∀ k, palindromeCutoff A ≤ k → wordAt A k ≠ (wordAt A k).reverse := by
  rw [fastPalindromicOnTail_eq]
  exact nonpalindromicOnTail_spec A

#print axioms endpoint_ltOnTail_iff
#print axioms width_eq_iff_coefficients
#print axioms span_overlapsOnTail_iff
#print axioms fastEqualOnTail_iff_coefficients
#print axioms fastEqualOnTail_iff_wordAt
#print axioms fastEqualOnTail_eq_equalOnTail
#print axioms fastEqualOnTail_spec
#print axioms fastUnequalOnTail_spec
#print axioms fastPalindromicOnTail_eq
#print axioms fastPalindromicOnTail_spec
#print axioms fastNonpalindromicOnTail_spec

end Agent102
