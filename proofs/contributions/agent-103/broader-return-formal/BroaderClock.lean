import ActualScalar
import PrefixExtension
import ScalarOrbit

/-!
Agent #103. Two-column seven-step returns to the prefix (4,4) force the
scalar clock on the outside coefficient.

`nextPair x y v` is the exact actual update of the first two pair
coefficients `(q 0, q 1)`, given the actual deeper carry `v = carry q (L-2)`
entering the high two-column block (`two_column_step`, valid for every
admissible width `L >= 2`, including the overlapping widths 2 and 3).
A kernel-checked finite search (`returnOK_root`) shows that every seven-step
path of this relation from (4,4) back to (4,4) has outside coefficients
4,8,16,7,15,6,13. Hence (`return_forces_clock`) an actual orbit whose first two
coefficients are (4,4) at times `a` and `a+7` follows `ScalarClock.phase` at
every intermediate time. No palindrome or 196 statement is made.
-/

namespace BroaderClock

open DecimalDigits FoldedDecimal OverflowCarryNormalization CarryHistory

/-- Exact local update of the first two pair coefficients. -/
def nextPair (x y v : Nat) : Nat × Nat :=
  let c := (y + v) / 10
  let st := ScalarClock.step x (decide (c = 1))
  (st.1, PrefixExtension.nextCoefficient x y (x / 10) c st.2 v)

def succs (s : Nat × Nat) : List (Nat × Nat) :=
  [nextPair s.1 s.2 0, nextPair s.1 s.2 1]

/-- The actual pair-word update moves the first two coefficients by `nextPair`
with the actual deeper carry. -/
theorem two_column_step (q : Nat → Nat) (L : Nat) (ha : Admissible L q) (hL : 2 ≤ L) :
    (nextColumns q L 0, nextColumns q L 1) = nextPair (q 0) (q 1) (carry q (L - 2)) ∧
      carry q (L - 2) ≤ 1 := by
  have hs := ActualScalar.actual_scalar_step q L ha
  have hx := PrefixExtension.actual_extension_formula q L 1 ha (by omega) (by omega)
  have hv : carry q (L - 2) ≤ 1 := carry_bounded q L ha.2.2.1 _ (by omega)
  have h1 : L - 1 - 1 = L - 2 := by omega
  rw [h1] at hx
  obtain ⟨hc, hn, -⟩ := hx
  have hcarry1 : carry q 1 = q 0 / 10 := by simp [carry]
  have hctl : ActualScalar.actualControl q L = decide ((q 1 + carry q (L - 2)) / 10 = 1) := by
    unfold ActualScalar.actualControl
    rw [hc]
  refine ⟨?_, hv⟩
  have hs0 := congrArg Prod.fst hs
  have hs1 := congrArg Prod.snd hs
  simp only at hs0 hs1
  rw [hctl] at hs0 hs1
  simp only [nextPair, Prod.mk.injEq]
  refine ⟨hs0, ?_⟩
  rw [hn, hcarry1, hc, hs1]

/-- Some continuation with `r` more steps from `s` reaches (4,4). -/
def reaches : Nat → Nat × Nat → Bool
  | 0, s => s == (4, 4)
  | r + 1, s => (succs s).any (reaches r)

/-- With `r` steps remaining at time `t`, every state on a continuation that
reaches (4,4) after those `r` steps has the scalar-clock outside value. -/
def returnOK : Nat → Nat → Nat × Nat → Bool
  | 0, _, _ => true
  | r + 1, t, s => (!reaches (r + 1) s) ||
      (s.1 == ScalarClock.phaseValue t && (succs s).all (returnOK r (t + 1)))

/-- The finite classification, checked by kernel reduction. -/
theorem returnOK_root : returnOK 7 0 (4, 4) = true := by decide

theorem reaches_of_path (r : Nat) (p : Nat → Nat × Nat)
    (hstep : ∀ i, i < r → p (i + 1) ∈ succs (p i)) (hend : p r = (4, 4)) :
    reaches r (p 0) = true := by
  induction r generalizing p with
  | zero => simp [reaches, hend]
  | succ r ih =>
    have h1 := ih (fun k => p (k + 1)) (fun i hi => hstep (i + 1) (by omega)) hend
    simp only [reaches, List.any_eq_true]
    exact ⟨p 1, hstep 0 (by omega), h1⟩

/-- Soundness of the finite classification for every path of the local relation. -/
theorem returnOK_sound (r t : Nat) (p : Nat → Nat × Nat)
    (hstep : ∀ i, i < r → p (i + 1) ∈ succs (p i)) (hend : p r = (4, 4))
    (hok : returnOK r t (p 0) = true) :
    ∀ i, i < r → (p i).1 = ScalarClock.phaseValue (t + i) := by
  induction r generalizing t p with
  | zero => intro i hi; omega
  | succ r ih =>
    have hr := reaches_of_path (r + 1) p hstep hend
    simp only [returnOK, hr, Bool.not_true, Bool.false_or, Bool.and_eq_true,
      beq_iff_eq, List.all_eq_true] at hok
    obtain ⟨h0, hall⟩ := hok
    intro i hi
    cases i with
    | zero => simpa using h0
    | succ j =>
      have hq := ih (t + 1) (fun k => p (k + 1)) (fun k hk => hstep (k + 1) (by omega)) hend
        (hall (p 1) (hstep 0 (by omega))) j (by omega)
      simpa [Nat.add_assoc, Nat.add_comm 1 j] using hq

/-- The first two coefficients of the actual pair-word orbit. -/
def pairAt (q : Nat → Nat) (L t : Nat) : Nat × Nat :=
  ((iterPairs q L t).2 0, (iterPairs q L t).2 1)

theorem pairAt_step (q : Nat → Nat) (L t : Nat) (ha : Admissible L q) (hL : 2 ≤ L) :
    pairAt q L (t + 1) ∈ succs (pairAt q L t) := by
  have had := iterPairs_admissible q L t ha
  have hw := ScalarOrbit.widthAt_lower q L t
  have hw' : 2 ≤ (iterPairs q L t).1 := by
    change L ≤ ScalarOrbit.widthAt q L t at hw
    unfold ScalarOrbit.widthAt at hw
    omega
  obtain ⟨he, hv⟩ := two_column_step (iterPairs q L t).2 (iterPairs q L t).1 had hw'
  have hn : pairAt q L (t + 1) =
      (nextColumns (iterPairs q L t).2 (iterPairs q L t).1 0,
       nextColumns (iterPairs q L t).2 (iterPairs q L t).1 1) := rfl
  rw [hn, he]
  have hv2 : carry (iterPairs q L t).2 ((iterPairs q L t).1 - 2) = 0 ∨
      carry (iterPairs q L t).2 ((iterPairs q L t).1 - 2) = 1 := by omega
  rcases hv2 with h | h <;> simp [succs, pairAt, h]

/-- **L1.** A seven-step two-column return to (4,4) forces the scalar clock on
the outside coefficient at every intermediate time. -/
theorem return_forces_clock (q : Nat → Nat) (L a : Nat) (ha : Admissible L q) (hL : 2 ≤ L)
    (h0 : pairAt q L a = (4, 4)) (h7 : pairAt q L (a + 7) = (4, 4)) :
    ∀ i, i ≤ 7 → (iterPairs q L (a + i)).2 0 = ScalarClock.phase i := by
  intro i hi
  by_cases h : i = 7
  · subst h
    have := congrArg Prod.fst h7
    simpa [pairAt, ScalarClock.phase, ScalarClock.phaseValue] using this
  · have hs := returnOK_sound 7 0 (fun k => pairAt q L (a + k))
      (fun k _ => by simpa [Nat.add_assoc] using pairAt_step q L (a + k) ha hL)
      h7 (by simpa [h0] using returnOK_root) i (by omega)
    have hm : i % 7 = i := Nat.mod_eq_of_lt (by omega)
    simpa [pairAt, ScalarClock.phase, hm] using hs

/-- `R` consecutive seven-step two-column returns give a scalar-clock segment
of `7R` steps (both endpoints included), starting at phase 0. -/
theorem returns_clock_segment (q : Nat → Nat) (L a R : Nat) (ha : Admissible L q) (hL : 2 ≤ L)
    (hret : ∀ k, k ≤ R → pairAt q L (a + 7 * k) = (4, 4)) :
    ScalarOrbit.ClockSegment q L a 0 (7 * R) := by
  intro i hi
  by_cases hR : i = 7 * R
  · have h := congrArg Prod.fst (hret R (Nat.le_refl R))
    simp only [pairAt] at h
    subst hR
    have hp : ScalarClock.phase (0 + 7 * R) = 4 := by
      simp [ScalarClock.phase, Nat.mul_mod_right, ScalarClock.phaseValue]
    rw [hp]
    exact h
  · have hk : i / 7 < R := by omega
    have hj : i % 7 < 7 := Nat.mod_lt _ (by decide)
    have hc := return_forces_clock q L (a + 7 * (i / 7)) ha hL (hret (i / 7) (by omega))
      (by simpa [Nat.mul_succ, Nat.add_assoc] using hret (i / 7 + 1) (by omega)) (i % 7) (by omega)
    have hi' : a + 7 * (i / 7) + i % 7 = a + i := by omega
    rw [hi'] at hc
    have hp : ScalarClock.phase (0 + i) = ScalarClock.phase (i % 7) := by
      simp [ScalarClock.phase, Nat.mod_mod]
    unfold ScalarOrbit.outerAt
    rw [hp]
    exact hc

end BroaderClock
