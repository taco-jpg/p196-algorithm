import Agent102PiecewiseCounts
import Agent102AffineRuns

/-!
Agent #102: exact finite unions of natural parameter intervals for actual
clipped-affine run words. The executable construction depends on the finite
run tables and integer coefficient arithmetic, never on a scan of parameters
or expansion of the represented words. Zero-length runs and literal zero
digits retain the original RunDefs semantics.
-/

namespace Agent102.ParameterSets

def widthExpr : List RunSpec → CountExpr
  | [] => .zero
  | r :: A => .add (.atom r.length) (widthExpr A)

theorem widthExpr_value (A : List RunSpec) (k : Nat) :
    (widthExpr A).value k = (wordAt A k).length := by
  induction A with
  | nil => simp [widthExpr, CountExpr.value, wordAt, runsAt, word]
  | cons r A ih =>
      simp_all [widthExpr, CountExpr.value, wordAt, runsAt, word]

structure CountSpan where
  digit : Nat
  lo : CountExpr
  hi : CountExpr
  deriving Repr

def CountSpan.at (s : CountSpan) (k : Nat) : Span :=
  ⟨s.digit, s.lo.value k, s.hi.value k⟩

def spanExprsFrom (start : CountExpr) : List RunSpec → List CountSpan
  | [] => []
  | r :: A =>
      let next := start.add (.atom r.length)
      ⟨r.digit, start, next⟩ :: spanExprsFrom next A

def spanExprs (A : List RunSpec) : List CountSpan := spanExprsFrom .zero A

theorem spanExprsFrom_at (start : CountExpr) (A : List RunSpec) (k : Nat) :
    (spanExprsFrom start A).map (fun s => s.at k) =
      spansFrom (start.value k) (runsAt A k) := by
  induction A generalizing start with
  | nil => rfl
  | cons r A ih =>
      simp [spanExprsFrom, runsAt, spansFrom, CountSpan.at, CountExpr.value, ih]

theorem spanExprs_at (A : List RunSpec) (k : Nat) :
    (spanExprs A).map (fun s => s.at k) = spans (runsAt A k) := by
  simpa only [spanExprs, spans, CountExpr.value] using spanExprsFrom_at .zero A k

theorem wordAt_eq_iff_countSpans (A B : List RunSpec) (k : Nat) :
    wordAt A k = wordAt B k ↔
      (widthExpr A).value k = (widthExpr B).value k ∧
      ∀ s ∈ spanExprs A, ∀ t ∈ spanExprs B,
        (s.at k).overlaps (t.at k) → s.digit = t.digit := by
  rw [widthExpr_value, widthExpr_value]
  have h := word_eq_iff_length_and_overlap_digits (runsAt A k) (runsAt B k)
  rw [← spanExprs_at A k, ← spanExprs_at B k] at h
  simpa only [wordAt, List.forall_mem_map, CountSpan.at] using h

/-- Positive overlap requires the two self-length inequalities as well as
the cross inequalities. In particular an empty run never conflicts. -/
def overlapRegion (s t : CountSpan) : Region :=
  fastInterAll [ltRegion s.lo s.hi, ltRegion s.lo t.hi,
    ltRegion t.lo s.hi, ltRegion t.lo t.hi]

theorem holds_overlapRegion (s t : CountSpan) (k : Nat) :
    holds (overlapRegion s t) k ↔ (s.at k).overlaps (t.at k) := by
  rw [Span.overlaps_iff_four]
  simp [overlapRegion, holds_fastInterAll, holds_ltRegion, CountSpan.at]

def agreementRegion (s t : CountSpan) : Region :=
  if s.digit = t.digit then univ else fastComplement (overlapRegion s t)

theorem holds_agreementRegion (s t : CountSpan) (k : Nat) :
    holds (agreementRegion s t) k ↔
      ((s.at k).overlaps (t.at k) → s.digit = t.digit) := by
  by_cases h : s.digit = t.digit <;>
    simp [agreementRegion, h, holds_fastComplement, holds_overlapRegion]

/-- All natural parameters at which the actual represented words are equal.
The answer is a finite, possibly overlapping list of half-open intervals. -/
def equalityRegions (A B : List RunSpec) : Region :=
  fastInter (eqRegion (widthExpr A) (widthExpr B))
    (fastInterAll ((spanExprs A).flatMap (fun s =>
      (spanExprs B).map (fun t => agreementRegion s t))))

theorem holds_equalityRegions (A B : List RunSpec) (k : Nat) :
    holds (equalityRegions A B) k ↔ wordAt A k = wordAt B k := by
  rw [wordAt_eq_iff_countSpans]
  simp only [equalityRegions, holds_fastInter, holds_eqRegion,
    holds_fastInterAll, List.forall_mem_flatMap, List.forall_mem_map,
    holds_agreementRegion]

def palindromeRegions (A : List RunSpec) : Region := equalityRegions A A.reverse

theorem holds_palindromeRegions (A : List RunSpec) (k : Nat) :
    holds (palindromeRegions A) k ↔ wordAt A k = (wordAt A k).reverse := by
  simp only [palindromeRegions, holds_equalityRegions, wordAt_reverse]

#print axioms widthExpr_value
#print axioms spanExprsFrom_at
#print axioms spanExprs_at
#print axioms wordAt_eq_iff_countSpans
#print axioms holds_overlapRegion
#print axioms holds_agreementRegion
#print axioms holds_equalityRegions
#print axioms holds_palindromeRegions

end Agent102.ParameterSets
