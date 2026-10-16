import Agent102AffineInequalityIntervals
import Agent102ParameterIntervalAlgebra
import Agent102AffineArithmetic

/-!
Agent #102: exact finite affine pieces for sums of clipped run lengths.
Every natural parameter is covered. Every applicable piece equals the actual
natural-valued expression. No interval's points are enumerated.
-/

namespace Agent102.ParameterSets

inductive CountExpr where
  | zero : CountExpr
  | atom : Affine → CountExpr
  | add : CountExpr → CountExpr → CountExpr
  deriving Repr

def CountExpr.value : CountExpr → Nat → Nat
  | .zero, _ => 0
  | .atom f, k => (f.eval k).toNat
  | .add e f, k => e.value k + f.value k

structure Piece where
  domain : Interval
  form : Affine
  deriving Repr

def CountExpr.pieces : CountExpr → List Piece
  | .zero => [⟨Interval.univ, Affine.zero⟩]
  | .atom f => [⟨leInterval Affine.zero f, f⟩,
      ⟨ltInterval f Affine.zero, Affine.zero⟩]
  | .add e f => e.pieces.flatMap (fun p => f.pieces.map (fun q =>
      ⟨p.domain.inter q.domain, p.form.add q.form⟩))

theorem CountExpr.pieces_sound (e : CountExpr) (p : Piece) (hp : p ∈ e.pieces)
    (k : Nat) (hk : p.domain.Contains k) : p.form.eval k = (e.value k : Int) := by
  induction e generalizing p with
  | zero =>
      simp only [CountExpr.pieces, List.mem_singleton] at hp
      subst p
      simp [CountExpr.value]
  | atom f =>
      simp only [CountExpr.pieces, List.mem_cons, List.not_mem_nil, or_false] at hp
      rcases hp with rfl | rfl
      · have hf := (contains_leInterval Affine.zero f k).mp hk
        have hf0 : 0 ≤ f.eval k := by simpa using hf
        exact (Int.toNat_of_nonneg hf0).symm
      · have hf := (contains_ltInterval f Affine.zero k).mp hk
        have hf0 : f.eval k ≤ 0 := by simpa using Int.le_of_lt hf
        simp [CountExpr.value, Int.toNat_of_nonpos hf0]
  | add e f ihe ihf =>
      obtain ⟨p₁, hp₁, hm⟩ := List.mem_flatMap.mp hp
      obtain ⟨p₂, hp₂, rfl⟩ := List.mem_map.mp hm
      have hparts := (Interval.contains_inter p₁.domain p₂.domain k).mp hk
      change (p₁.form.add p₂.form).eval k = ((e.value k + f.value k : Nat) : Int)
      rw [Affine.eval_add, ihe p₁ hp₁ hparts.1, ihf p₂ hp₂ hparts.2]
      simp

theorem CountExpr.pieces_cover (e : CountExpr) (k : Nat) :
    ∃ p ∈ e.pieces, p.domain.Contains k := by
  induction e with
  | zero =>
      refine ⟨⟨Interval.univ, Affine.zero⟩, by simp [CountExpr.pieces], ?_⟩
      simp [Interval.Contains, Interval.univ]
  | atom f =>
      by_cases hf : 0 ≤ f.eval k
      · refine ⟨⟨leInterval Affine.zero f, f⟩, by simp [CountExpr.pieces], ?_⟩
        exact (contains_leInterval Affine.zero f k).mpr (by simpa using hf)
      · refine ⟨⟨ltInterval f Affine.zero, Affine.zero⟩,
          by simp [CountExpr.pieces], ?_⟩
        exact (contains_ltInterval f Affine.zero k).mpr (by simpa using (show f.eval k < 0 by omega))
  | add e f ihe ihf =>
      obtain ⟨p, hp, hpk⟩ := ihe
      obtain ⟨q, hq, hqk⟩ := ihf
      refine ⟨⟨p.domain.inter q.domain, p.form.add q.form⟩, ?_, ?_⟩
      · exact List.mem_flatMap.mpr ⟨p, hp, List.mem_map.mpr ⟨q, hq, rfl⟩⟩
      · exact (Interval.contains_inter p.domain q.domain k).mpr ⟨hpk, hqk⟩

/-- Combine finite applicable pieces with an exact scalar relation interval. -/
def comparisonRegion (atom : Affine → Affine → Interval) (e f : CountExpr) : Region :=
  e.pieces.flatMap (fun p => f.pieces.map (fun q =>
    (p.domain.inter q.domain).inter (atom p.form q.form)))

theorem comparisonRegion_spec (atom : Affine → Affine → Interval)
    (R : Int → Int → Prop)
    (hatom : ∀ a b k, (atom a b).Contains k ↔ R (a.eval k) (b.eval k))
    (e f : CountExpr) (k : Nat) :
    holds (comparisonRegion atom e f) k ↔ R (e.value k : Int) (f.value k : Int) := by
  constructor
  · rintro ⟨I, hI, hk⟩
    obtain ⟨p, hp, hm⟩ := List.mem_flatMap.mp hI
    obtain ⟨q, hq, rfl⟩ := List.mem_map.mp hm
    have hboth := (Interval.contains_inter (p.domain.inter q.domain)
      (atom p.form q.form) k).mp hk
    have hpieces := (Interval.contains_inter p.domain q.domain k).mp hboth.1
    have hr := (hatom p.form q.form k).mp hboth.2
    rw [CountExpr.pieces_sound e p hp k hpieces.1,
      CountExpr.pieces_sound f q hq k hpieces.2] at hr
    exact hr
  · intro hr
    obtain ⟨p, hp, hpk⟩ := e.pieces_cover k
    obtain ⟨q, hq, hqk⟩ := f.pieces_cover k
    refine ⟨(p.domain.inter q.domain).inter (atom p.form q.form), ?_, ?_⟩
    · exact List.mem_flatMap.mpr ⟨p, hp, List.mem_map.mpr ⟨q, hq, rfl⟩⟩
    · apply (Interval.contains_inter (p.domain.inter q.domain) (atom p.form q.form) k).mpr
      refine ⟨(Interval.contains_inter p.domain q.domain k).mpr ⟨hpk, hqk⟩, ?_⟩
      apply (hatom p.form q.form k).mpr
      simpa only [CountExpr.pieces_sound e p hp k hpk,
        CountExpr.pieces_sound f q hq k hqk] using hr

def ltRegion (e f : CountExpr) : Region := comparisonRegion ltInterval e f

def leRegion (e f : CountExpr) : Region := comparisonRegion leInterval e f

def eqRegion (e f : CountExpr) : Region := inter (leRegion e f) (leRegion f e)

theorem holds_ltRegion (e f : CountExpr) (k : Nat) :
    holds (ltRegion e f) k ↔ e.value k < f.value k := by
  simpa [ltRegion] using comparisonRegion_spec ltInterval (fun a b => a < b)
    contains_ltInterval e f k

theorem holds_leRegion (e f : CountExpr) (k : Nat) :
    holds (leRegion e f) k ↔ e.value k ≤ f.value k := by
  simpa [leRegion] using comparisonRegion_spec leInterval (fun a b => a ≤ b)
    contains_leInterval e f k

theorem holds_eqRegion (e f : CountExpr) (k : Nat) :
    holds (eqRegion e f) k ↔ e.value k = f.value k := by
  simp only [eqRegion, holds_inter, holds_leRegion]
  omega

#print axioms CountExpr.pieces_sound
#print axioms CountExpr.pieces_cover
#print axioms comparisonRegion_spec
#print axioms holds_ltRegion
#print axioms holds_leRegion
#print axioms holds_eqRegion

end Agent102.ParameterSets
