import Agent102RunEndpoints
import Agent102RunWord

/-!
Agent #102: exact, computable tail equality and palindrome decisions for
arbitrary finite affine run words, including clipped negative lengths.
-/

namespace Agent102

def pairCutoff (es : List Affine) : Nat :=
  maxList (es.flatMap (fun f => es.map (Affine.compareCutoff f)))

theorem compareCutoff_le_pairCutoff {es : List Affine} {f g : Affine}
    (hf : f ∈ es) (hg : g ∈ es) : Affine.compareCutoff f g ≤ pairCutoff es := by
  apply le_maxList_of_mem
  apply List.mem_flatMap.mpr
  refine ⟨f, hf, ?_⟩
  exact List.mem_map.mpr ⟨g, hg, rfl⟩

/-- Every clipped length and every endpoint comparison is stable at this bound. -/
def equalityCutoff (A B : List RunSpec) : Nat :=
  max (lengthCutoff A) (max (lengthCutoff B) (pairCutoff (endpoints A ++ endpoints B)))

theorem left_lengthCutoff_le (A B : List RunSpec) : lengthCutoff A ≤ equalityCutoff A B :=
  Nat.le_max_left _ _

theorem right_lengthCutoff_le (A B : List RunSpec) : lengthCutoff B ≤ equalityCutoff A B :=
  Nat.le_trans (Nat.le_max_left _ _) (Nat.le_max_right _ _)

theorem pairCutoff_le_equalityCutoff (A B : List RunSpec) :
    pairCutoff (endpoints A ++ endpoints B) ≤ equalityCutoff A B :=
  Nat.le_trans (Nat.le_max_right _ _) (Nat.le_max_right _ _)

theorem combined_endpoints_nonneg (A B : List RunSpec) (k : Nat)
    (hk : equalityCutoff A B ≤ k) (f : Affine) (hf : f ∈ endpoints A ++ endpoints B) :
    0 ≤ f.eval k := by
  rcases List.mem_append.mp hf with hf | hf
  · exact endpoints_nonneg A k (Nat.le_trans (left_lengthCutoff_le A B) hk) f hf
  · exact endpoints_nonneg B k (Nat.le_trans (right_lengthCutoff_le A B) hk) f hf

theorem endpoint_nat_lt_stable (A B : List RunSpec) (f g : Affine)
    (hf : f ∈ endpoints A ++ endpoints B) (hg : g ∈ endpoints A ++ endpoints B)
    (k : Nat) (hk : equalityCutoff A B ≤ k) :
    ((f.eval k).toNat < (g.eval k).toNat ↔
      (f.eval (equalityCutoff A B)).toNat < (g.eval (equalityCutoff A B)).toNat) := by
  have hcut := Nat.le_trans (compareCutoff_le_pairCutoff hf hg)
    (pairCutoff_le_equalityCutoff A B)
  have h := Affine.eval_lt_stable f g (equalityCutoff A B) k hcut hk
  have hfk := combined_endpoints_nonneg A B k hk f hf
  have hgk := combined_endpoints_nonneg A B k hk g hg
  have hfK := combined_endpoints_nonneg A B (equalityCutoff A B) (Nat.le_refl _) f hf
  have hgK := combined_endpoints_nonneg A B (equalityCutoff A B) (Nat.le_refl _) g hg
  omega

theorem width_eq_stable (A B : List RunSpec) (k : Nat) (hk : equalityCutoff A B ≤ k) :
    ((wordAt A k).length = (wordAt B k).length ↔
      (wordAt A (equalityCutoff A B)).length = (wordAt B (equalityCutoff A B)).length) := by
  have ha : widthAffine A ∈ endpoints A ++ endpoints B :=
    List.mem_append_left _ (widthAffine_mem_endpoints A)
  have hb : widthAffine B ∈ endpoints A ++ endpoints B :=
    List.mem_append_right _ (widthAffine_mem_endpoints B)
  have hcut := Nat.le_trans (compareCutoff_le_pairCutoff ha hb)
    (pairCutoff_le_equalityCutoff A B)
  have h := Affine.eval_eq_stable (widthAffine A) (widthAffine B) (equalityCutoff A B) k hcut hk
  rw [widthAffine_eval A k (Nat.le_trans (left_lengthCutoff_le A B) hk),
    widthAffine_eval B k (Nat.le_trans (right_lengthCutoff_le A B) hk),
    widthAffine_eval A _ (left_lengthCutoff_le A B),
    widthAffine_eval B _ (right_lengthCutoff_le A B)] at h
  omega

/-- Four strict inequalities retain the positive length of both spans. -/
theorem Span.overlaps_iff_four (s t : Span) :
    s.overlaps t ↔ s.lo < s.hi ∧ s.lo < t.hi ∧ t.lo < s.hi ∧ t.lo < t.hi := by
  unfold Span.overlaps
  omega

theorem span_overlap_stable (A B : List RunSpec) (s t : AffineSpan)
    (hs : s ∈ spanSpecs A) (ht : t ∈ spanSpecs B)
    (k : Nat) (hk : equalityCutoff A B ≤ k) :
    ((s.at k).overlaps (t.at k) ↔
      (s.at (equalityCutoff A B)).overlaps (t.at (equalityCutoff A B))) := by
  have hslo : s.lo ∈ endpoints A ++ endpoints B :=
    List.mem_append_left _ (lo_mem_endpoints hs)
  have hshi : s.hi ∈ endpoints A ++ endpoints B :=
    List.mem_append_left _ (hi_mem_endpoints hs)
  have htlo : t.lo ∈ endpoints A ++ endpoints B :=
    List.mem_append_right _ (lo_mem_endpoints ht)
  have hthi : t.hi ∈ endpoints A ++ endpoints B :=
    List.mem_append_right _ (hi_mem_endpoints ht)
  have h₁ := endpoint_nat_lt_stable A B s.lo s.hi hslo hshi k hk
  have h₂ := endpoint_nat_lt_stable A B s.lo t.hi hslo hthi k hk
  have h₃ := endpoint_nat_lt_stable A B t.lo s.hi htlo hshi k hk
  have h₄ := endpoint_nat_lt_stable A B t.lo t.hi htlo hthi k hk
  simp only [Span.overlaps_iff_four, AffineSpan.at]
  exact and_congr h₁ (and_congr h₂ (and_congr h₃ h₄))

theorem wordAt_eq_iff_spans (A B : List RunSpec) (k : Nat)
    (ha : lengthCutoff A ≤ k) (hb : lengthCutoff B ≤ k) :
    wordAt A k = wordAt B k ↔
      (wordAt A k).length = (wordAt B k).length ∧
      ∀ s ∈ spanSpecs A, ∀ t ∈ spanSpecs B,
        (s.at k).overlaps (t.at k) → s.digit = t.digit := by
  have h := word_eq_iff_length_and_overlap_digits (runsAt A k) (runsAt B k)
  rw [← spanSpecs_at A k ha, ← spanSpecs_at B k hb] at h
  simpa only [wordAt, List.forall_mem_map, AffineSpan.at] using h

/-- Tail equality is the exact equality at one computable parameter, not a sample heuristic. -/
theorem wordAt_eq_stable (A B : List RunSpec) (k : Nat) (hk : equalityCutoff A B ≤ k) :
    (wordAt A k = wordAt B k ↔
      wordAt A (equalityCutoff A B) = wordAt B (equalityCutoff A B)) := by
  rw [wordAt_eq_iff_spans A B k (Nat.le_trans (left_lengthCutoff_le A B) hk)
    (Nat.le_trans (right_lengthCutoff_le A B) hk),
    wordAt_eq_iff_spans A B (equalityCutoff A B)
      (left_lengthCutoff_le A B) (right_lengthCutoff_le A B)]
  constructor
  · rintro ⟨hl, hd⟩
    refine ⟨(width_eq_stable A B k hk).mp hl, ?_⟩
    intro s hs t ht hov
    exact hd s hs t ht ((span_overlap_stable A B s t hs ht k hk).mpr hov)
  · rintro ⟨hl, hd⟩
    refine ⟨(width_eq_stable A B k hk).mpr hl, ?_⟩
    intro s hs t ht hov
    exact hd s hs t ht ((span_overlap_stable A B s t hs ht k hk).mp hov)

theorem wordAt_reverse (A : List RunSpec) (k : Nat) :
    wordAt A.reverse k = (wordAt A k).reverse := by
  simp only [wordAt, runsAt, List.map_reverse, word_reverse]

def palindromeCutoff (A : List RunSpec) : Nat := equalityCutoff A A.reverse

theorem wordAt_palindrome_stable (A : List RunSpec) (k : Nat) (hk : palindromeCutoff A ≤ k) :
    (wordAt A k = (wordAt A k).reverse ↔
      wordAt A (palindromeCutoff A) = (wordAt A (palindromeCutoff A)).reverse) := by
  simpa only [palindromeCutoff, wordAt_reverse] using wordAt_eq_stable A A.reverse k hk

def equalOnTail (A B : List RunSpec) : Bool :=
  decide (wordAt A (equalityCutoff A B) = wordAt B (equalityCutoff A B))

theorem equalOnTail_spec (A B : List RunSpec) :
    equalOnTail A B = true ↔ ∀ k, equalityCutoff A B ≤ k → wordAt A k = wordAt B k := by
  simp only [equalOnTail, decide_eq_true_eq]
  constructor
  · intro h k hk
    exact (wordAt_eq_stable A B k hk).mpr h
  · intro h
    exact h _ (Nat.le_refl _)

theorem unequalOnTail_spec (A B : List RunSpec) :
    equalOnTail A B = false ↔ ∀ k, equalityCutoff A B ≤ k → wordAt A k ≠ wordAt B k := by
  simp only [equalOnTail, decide_eq_false_iff_not]
  constructor
  · intro h k hk he
    exact h ((wordAt_eq_stable A B k hk).mp he)
  · intro h
    exact h _ (Nat.le_refl _)

theorem equality_before_cutoff_of_tail_mismatch (A B : List RunSpec)
    (h : equalOnTail A B = false) (k : Nat) (he : wordAt A k = wordAt B k) :
    k < equalityCutoff A B := by
  have hn := (unequalOnTail_spec A B).mp h
  by_cases hk : equalityCutoff A B ≤ k
  · exact False.elim (hn k hk he)
  · omega

def palindromicOnTail (A : List RunSpec) : Bool := equalOnTail A A.reverse

theorem palindromicOnTail_spec (A : List RunSpec) :
    palindromicOnTail A = true ↔
      ∀ k, palindromeCutoff A ≤ k → wordAt A k = (wordAt A k).reverse := by
  simpa only [palindromicOnTail, palindromeCutoff, wordAt_reverse] using equalOnTail_spec A A.reverse

theorem nonpalindromicOnTail_spec (A : List RunSpec) :
    palindromicOnTail A = false ↔
      ∀ k, palindromeCutoff A ≤ k → wordAt A k ≠ (wordAt A k).reverse := by
  simpa only [palindromicOnTail, palindromeCutoff, wordAt_reverse] using unequalOnTail_spec A A.reverse

end Agent102
