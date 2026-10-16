import Agent102RunEndpoints
import Agent102RunWord

/-!
Agent #102 的真实词区间子代理对母代理端点模块的独立复核。
本文件不修改端点实现；在冻结模块之上重新导出具体覆盖与逐位取值，
并以内核判定检查空输入、负斜率、负常数和零长度段的组合边界。
-/

namespace Agent102.EndpointReview

/-- 仿射区间表覆盖的自然数位置精确等于实际词的全部合法下标。 -/
theorem exact_coverage (rs : List RunSpec) (k i : Nat)
    (hk : lengthCutoff rs ≤ k) :
    (∃ s ∈ spanSpecs rs, (s.at k).covers i) ↔ i < (wordAt rs k).length := by
  constructor
  · rintro ⟨s, hs, hcov⟩
    have hm : s.at k ∈ spans (runsAt rs k) := by
      rw [← spanSpecs_at rs k hk]
      exact List.mem_map.mpr ⟨s, hs, rfl⟩
    exact (exists_mem_spans_covers_iff (runsAt rs k) i).mp ⟨s.at k, hm, hcov⟩
  · intro hi
    obtain ⟨s, hs, hcov⟩ := exists_mem_spans_covers (rs := runsAt rs k) hi
    rw [← spanSpecs_at rs k hk] at hs
    obtain ⟨t, ht, heq⟩ := List.mem_map.mp hs
    exact ⟨t, ht, by simpa only [heq] using hcov⟩

/-- 区间表保留了实际字符值，而不只是宽度和端点集合。 -/
theorem exact_digit {rs : List RunSpec} {k i : Nat} {s : AffineSpan}
    (hk : lengthCutoff rs ≤ k) (hs : s ∈ spanSpecs rs) (hi : (s.at k).covers i) :
    (wordAt rs k)[i]? = some s.digit := by
  have hm : s.at k ∈ spans (runsAt rs k) := by
    rw [← spanSpecs_at rs k hk]
    exact List.mem_map.mpr ⟨s, hs, rfl⟩
  exact getElem?_word_of_covers hm hi

/-- 每个保存端点在尾部求值后均是实际词宽以内的自然数边界。 -/
theorem endpoint_bounds {rs : List RunSpec} {k : Nat}
    (hk : lengthCutoff rs ≤ k) :
    ∀ f ∈ endpoints rs, 0 ≤ f.eval k ∧ f.eval k ≤ (wordAt rs k).length := by
  intro f hf
  refine ⟨endpoints_nonneg rs k hk f hf, ?_⟩
  rcases List.mem_cons.mp hf with he | hf
  · subst f
    simpa only [widthAffine_eval rs k hk] using Int.le_refl ((wordAt rs k).length : Int)
  · obtain ⟨s, hs, hf⟩ := List.mem_flatMap.mp hf
    have hm : s.at k ∈ spans (runsAt rs k) := by
      rw [← spanSpecs_at rs k hk]
      exact List.mem_map.mpr ⟨s, hs, rfl⟩
    have hbounds := mem_spans_bounds hm
    have hn := spanSpecs_nonneg rs k hk s hs
    simp only [AffineSpan.at] at hbounds
    simp only [List.mem_cons, List.not_mem_nil, or_false] at hf
    rcases hf with rfl | rfl
    · have hcast : ((s.lo.eval k).toNat : Int) ≤ (wordAt rs k).length := by
        exact Int.ofNat_le.mpr (Nat.le_trans hbounds.1 hbounds.2)
      simpa only [Int.toNat_of_nonneg hn.1] using hcast
    · have hcast : ((s.hi.eval k).toNat : Int) ≤ (wordAt rs k).length := by
        exact Int.ofNat_le.mpr hbounds.2
      simpa only [Int.toNat_of_nonneg hn.2] using hcast

def mixed : List RunSpec :=
  [⟨8, ⟨-1, 3⟩⟩, ⟨4, ⟨0, -2⟩⟩, ⟨5, ⟨1, -1⟩⟩,
   ⟨5, ⟨0, 0⟩⟩, ⟨5, ⟨0, 2⟩⟩]

theorem empty_cutoff : lengthCutoff [] = 0 := rfl
theorem empty_word : wordAt [] 0 = [] := rfl
theorem empty_spans : spanSpecs [] = [] := rfl
theorem empty_endpoints : endpoints [] = [Affine.zero] := rfl

theorem mixed_cutoff : lengthCutoff mixed = 4 := by decide
theorem mixed_word : wordAt mixed 4 = [5, 5, 5, 5, 5] := by decide
theorem mixed_runs : runsAt mixed 4 =
    [⟨8, 0⟩, ⟨4, 0⟩, ⟨5, 3⟩, ⟨5, 0⟩, ⟨5, 2⟩] := by decide
theorem mixed_spans : (spanSpecs mixed).map (fun s => s.at 4) =
    [⟨8, 0, 0⟩, ⟨4, 0, 0⟩, ⟨5, 0, 3⟩, ⟨5, 3, 3⟩, ⟨5, 3, 5⟩] := by decide
theorem mixed_width : (widthAffine mixed).eval 4 = 5 := by decide
theorem mixed_endpoints : (endpoints mixed).map (fun f => f.eval 4) =
    [5, 0, 0, 0, 0, 0, 3, 3, 3, 3, 5] := by decide
theorem mixed_shifted_spans :
    (spanSpecsFrom ⟨0, 7⟩ mixed).map (fun s => s.at 4) =
    [⟨8, 7, 7⟩, ⟨4, 7, 7⟩, ⟨5, 7, 10⟩, ⟨5, 10, 10⟩, ⟨5, 10, 12⟩] := by decide

end Agent102.EndpointReview

#print axioms Agent102.maxList
#print axioms Agent102.le_maxList_of_mem
#print axioms Agent102.lengthCutoff
#print axioms Agent102.cutoff_le_lengthCutoff
#print axioms Agent102.wordAt_nil
#print axioms Agent102.wordAt_cons
#print axioms Agent102.widthAffine
#print axioms Agent102.widthAffine_eval
#print axioms Agent102.widthAffine_nonneg
#print axioms Agent102.AffineSpan.at
#print axioms Agent102.spanSpecsFrom
#print axioms Agent102.spanSpecs
#print axioms Agent102.spanSpecsFrom_at
#print axioms Agent102.spanSpecs_at
#print axioms Agent102.spanSpecsFrom_nonneg
#print axioms Agent102.spanSpecs_nonneg
#print axioms Agent102.endpoints
#print axioms Agent102.widthAffine_mem_endpoints
#print axioms Agent102.lo_mem_endpoints
#print axioms Agent102.hi_mem_endpoints
#print axioms Agent102.endpoints_nonneg
#print axioms Agent102.EndpointReview.exact_coverage
#print axioms Agent102.EndpointReview.exact_digit
#print axioms Agent102.EndpointReview.endpoint_bounds
#print axioms Agent102.EndpointReview.mixed
#print axioms Agent102.EndpointReview.empty_cutoff
#print axioms Agent102.EndpointReview.empty_word
#print axioms Agent102.EndpointReview.empty_spans
#print axioms Agent102.EndpointReview.empty_endpoints
#print axioms Agent102.EndpointReview.mixed_cutoff
#print axioms Agent102.EndpointReview.mixed_word
#print axioms Agent102.EndpointReview.mixed_runs
#print axioms Agent102.EndpointReview.mixed_spans
#print axioms Agent102.EndpointReview.mixed_width
#print axioms Agent102.EndpointReview.mixed_endpoints
#print axioms Agent102.EndpointReview.mixed_shifted_spans
