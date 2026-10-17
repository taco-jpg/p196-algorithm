import P196.Agent102AffineScalar.Agent102RunDefs
import P196.Foundations.ActualWordBridge

/-!
Agent #105, session 8f1107db019a. Shared actual-word interfaces for the
affine-run dynamics proof. `RunSpec` and `wordAt` are imported unchanged
from Agent #102; all decimal operations are the original Agent #8 ones.
-/

namespace Agent105.AffineDynamics

open Agent102

/-- A bound on the literal symbols of a finite run specification. -/
def SpecBound (rs : List RunSpec) (b : Nat) : Prop :=
  ∀ r ∈ rs, r.digit ≤ b

/-- Actual words with a bounded-symbol affine-run representation on a tail. -/
def HasAffineRuns (w : Nat → List Nat) (b : Nat) : Prop :=
  ∃ rs : List RunSpec, SpecBound rs b ∧
    ∃ K : Nat, ∀ k, K ≤ k → w k = wordAt rs k

def constRun (digit count : Nat) : RunSpec :=
  ⟨digit, ⟨0, (count : Int)⟩⟩

def minusOne (f : Affine) : Affine :=
  ⟨f.slope, f.intercept - 1⟩

@[simp] theorem wordAt_nil (k : Nat) : wordAt [] k = [] := rfl

@[simp] theorem wordAt_cons (r : RunSpec) (rs : List RunSpec) (k : Nat) :
    wordAt (r :: rs) k =
      List.replicate (r.length.eval k).toNat r.digit ++ wordAt rs k := by
  simp [wordAt, runsAt, word]

@[simp] theorem wordAt_append (rs ss : List RunSpec) (k : Nat) :
    wordAt (rs ++ ss) k = wordAt rs k ++ wordAt ss k := by
  simp [wordAt, runsAt, word]

@[simp] theorem wordAt_singleton (r : RunSpec) (k : Nat) :
    wordAt [r] k = List.replicate (r.length.eval k).toNat r.digit := by
  simp

@[simp] theorem wordAt_constRun (digit count k : Nat) :
    wordAt [constRun digit count] k = List.replicate count digit := by
  simp [constRun, Affine.eval]

theorem wordAt_reverse (rs : List RunSpec) (k : Nat) :
    wordAt rs.reverse k = (wordAt rs k).reverse := by
  induction rs with
  | nil => rfl
  | cons r rs ih =>
    simp [List.reverse_cons, ih, List.reverse_append]

@[simp] theorem minusOne_eval (f : Affine) (k : Nat) :
    (minusOne f).eval k = f.eval k - 1 := by
  simp [minusOne, Affine.eval, Int.sub_eq_add_neg, Int.add_assoc]

theorem minusOne_toNat (f : Affine) (k : Nat) :
    ((minusOne f).eval k).toNat = (f.eval k).toNat - 1 := by
  rw [minusOne_eval]
  exact Int.toNat_sub' _ 1

theorem specBound_nil (b : Nat) : SpecBound [] b := by
  intro r hr
  simp at hr

theorem specBound_cons {r : RunSpec} {rs : List RunSpec} {b : Nat}
    (hr : r.digit ≤ b) (hs : SpecBound rs b) : SpecBound (r :: rs) b := by
  intro s h
  rcases List.mem_cons.mp h with h | h
  · simpa [h] using hr
  · exact hs s h

theorem specBound_reverse {rs : List RunSpec} {b : Nat}
    (h : SpecBound rs b) : SpecBound rs.reverse b := by
  intro r hr
  exact h r (by simpa using hr)

theorem wordAt_bounded (rs : List RunSpec) (b k : Nat)
    (h : SpecBound rs b) : Agent8.Bounded (wordAt rs k) b := by
  induction rs with
  | nil => intro x hx; simp at hx
  | cons r rs ih =>
    intro x hx
    rw [wordAt_cons] at hx
    rcases List.mem_append.mp hx with hx | hx
    · have he : x = r.digit := (List.mem_replicate.mp hx).2
      subst x
      exact h r (by simp)
    · exact ih (fun s hs => h s (by simp [hs])) x hx

theorem hasAffineRuns_wordAt (rs : List RunSpec) (b : Nat)
    (h : SpecBound rs b) : HasAffineRuns (wordAt rs) b := by
  exact ⟨rs, h, 0, fun _ _ => rfl⟩

end Agent105.AffineDynamics

#print axioms Agent105.AffineDynamics.wordAt_cons
#print axioms Agent105.AffineDynamics.wordAt_append
#print axioms Agent105.AffineDynamics.wordAt_reverse
#print axioms Agent105.AffineDynamics.minusOne_toNat
#print axioms Agent105.AffineDynamics.wordAt_bounded
#print axioms Agent105.AffineDynamics.hasAffineRuns_wordAt
