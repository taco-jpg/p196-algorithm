import AllRows4
import Short4
import Table4

/-!
# Four-column three-digit prefix ancestry bounds: concrete endpoints

Agent #119, task `agent119-four-column-prefix-kernel`.

All finite premises of `FourColumnKernel.ancestry_bound_of_checks` are
discharged by kernel reduction for the concrete rank tree `ranks4`:

* `allRows`        — every row of the tree against the complete proved inverse
                     (`AllRows4`, assembled from `decide +kernel` chunks);
* `shortDescent4`  — exact short-transition descent for all 207 short words;
* `table4_checked` — every listed prefix is outside the growth prefixes, its
                     bound lies in `1..100`, and every member of its root family
                     has checked rank at most `bound - 1`.

Main results (no remaining hypotheses besides membership in `table4`):

* `ancestry_bound` : for `(a, b, c, B) ∈ table4`, every positive ordinary
  decimal `A`, every time `t` and every palindrome `P` whose canonical numeral
  begins `a b c` (any width ≥ 3, any interior digits) with
  `Lychrel196.orbit A t = P` satisfy `t ≤ B`.
* `no_196` : for `(a, b, c, B) ∈ table4` and every `t`, `orbit 196 t` is not a
  palindrome beginning `a b c`.
* `ancestry_bound_33`, `no_196_33` : the complete two-digit class 33
  (every width ≥ 2), bound 5, with the sharp example `sharp_33`.

These exclude restricted palindrome families only.  They do not prove that
196 is a Lychrel number, and no optimality of the listed bounds is asserted
(except that 5 is attained in the class 33).
-/

namespace FourColumnKernel.Certificate

open DecimalDigits FoldedDecimal Lychrel196
open SevenColumn.Certificate SevenColumn.ShortBoundary
open SevenColumnKernel.PalindromeBridge FourColumnKernel

/-- Decidable acceptance test for one table entry. -/
def entryOK (tree : RankTree) : Nat × Nat × Nat × Nat → Bool
  | (a, b, c, B) =>
    !(decide (GrowthPrefix a b c)) && decide (1 ≤ B) && decide (B ≤ 100) &&
      (rootWords a b c).all (checkInitial tree (B - 1))

set_option maxRecDepth 100000 in
set_option maxHeartbeats 100000000 in
theorem table4_checked : table4.all (entryOK ranks4) = true := by decide +kernel

theorem table4_length : table4.length = 229 := by decide +kernel

theorem entry_sound {a b c B : Nat} (h : (a, b, c, B) ∈ table4) :
    ¬ GrowthPrefix a b c ∧ 1 ≤ B ∧ B ≤ 100 ∧
      ∀ p ∈ rootWords a b c, checkInitial ranks4 (B - 1) p = true := by
  have hok := List.all_eq_true.mp table4_checked _ h
  simp only [entryOK, Bool.and_eq_true, Bool.not_eq_true', decide_eq_true_eq,
    decide_eq_false_iff_not, List.all_eq_true] at hok
  obtain ⟨⟨⟨hng, h1⟩, h100⟩, hinit⟩ := hok
  exact ⟨hng, h1, h100, hinit⟩

/-- Ancestry bound for every listed three-digit palindrome prefix. -/
theorem ancestry_bound {a b c B : Nat} (h : (a, b, c, B) ∈ table4) :
    ∀ A P t, 0 < A → PalindromeStarts3 a b c P → orbit A t = P → t ≤ B := by
  obtain ⟨hng, h1, _, hinit⟩ := entry_sound h
  intro A P t hA hP hreach
  have ht := ancestry_bound_of_checks ranks4 allRows shortDescent4 a b c (B - 1)
    hng hinit A P t hA hP hreach
  omega

/-- The ordinary orbit of 196 never reaches a palindrome with a listed prefix. -/
theorem no_196 {a b c B : Nat} (h : (a, b, c, B) ∈ table4) :
    ∀ t, ¬ PalindromeStarts3 a b c (orbit 196 t) := by
  obtain ⟨_, _, h100, _⟩ := entry_sound h
  exact no_196_target_of_ancestry_bound (PalindromeStarts3 a b c) B h100
    (fun _ hp => hp.1) (ancestry_bound h)

/-- Uniform form: no palindrome in the 196 orbit has any listed prefix. -/
theorem no_196_listed_prefix (t : Nat) (hpal : Palindrome (orbit 196 t)) :
    ∀ a b c B, (a, b, c, B) ∈ table4 → ¬ Starts3 a b c (orbit 196 t) :=
  fun _ _ _ _ h hs => no_196 h t ⟨hpal, hs⟩

/-! ## The complete two-digit class 33 -/

/-- The canonical numeral of `P` has at least two digits and begins `a b`. -/
def Starts2 (a b P : Nat) : Prop :=
  ∃ e W, Canonical P e W ∧ 2 ≤ W ∧ e (W - 1) = a ∧ e (W - 2) = b

theorem table4_has_33 : ∀ c, c < 10 → (3, 3, c, 5) ∈ table4 := by decide

theorem root33_checked : checkInitial ranks4 4 [3, 3] = true := by decide +kernel

/-- Every palindrome beginning 33, of any width at least two (including 33
itself), has ancestry depth at most 5. -/
theorem ancestry_bound_33 :
    ∀ A P t, 0 < A → Palindrome P → Starts2 3 3 P → orbit A t = P → t ≤ 5 := by
  intro A P t hA hpal hs hreach
  obtain ⟨e, W, htarget, hW, h1, h2⟩ := hs
  by_cases hW3 : 3 ≤ W
  · have hc := htarget.2.1 (W - 3) (by omega)
    have hmem := table4_has_33 (e (W - 3)) (by omega)
    exact ancestry_bound hmem A P t hA ⟨hpal, e, W, htarget, hW3, h1, h2, rfl⟩ hreach
  · have hW2 : W = 2 := by omega
    subst hW2
    cases t with
    | zero => omega
    | succ t =>
      have ht : t ≤ 4 := by
        apply time_bound_of_root allRows shortDescent4 hA (roots := [[3, 3]])
        · intro n d L hcan hstep
          have hlead : 1 < e (2 - 1) := by omega
          obtain ⟨hwidth, _, hpair, _⟩ :=
            canonical_last_step hcan htarget (hstep.trans hreach) hpal hlead
          subst hwidth
          have q0 : columnSum d 2 0 = 3 := by
            rw [hpair 0 (by omega)]
            simpa using h2
          have q1 : columnSum d 2 1 = 3 := by
            rw [hpair 1 (by omega)]
            simpa using h1
          have hproj : project4 (columnSum d 2) 2 = [3, 3] := by
            rw [project4_short _ _ (by omega)]
            simp [wordOf, List.range_succ, q0, q1]
          simp [hproj]
        · intro p hp
          simp only [List.mem_singleton] at hp
          subst hp
          exact root33_checked
      omega

theorem no_196_33 : ∀ t, ¬ (Palindrome (orbit 196 t) ∧ Starts2 3 3 (orbit 196 t)) :=
  no_196_target_of_ancestry_bound (fun P => Palindrome P ∧ Starts2 3 3 P) 5 (by decide)
    (fun _ hp => hp.1) (fun A P t hA hP hr => ancestry_bound_33 A P t hA hP.1 hP.2 hr)

/-- The bound 5 is attained in the class 33: a first palindrome at time 5. -/
theorem sharp_33 :
    orbit 1109090 5 = 33266233 ∧ Palindrome (orbit 1109090 5) ∧
      (∀ k, k < 5 → ¬ Palindrome (orbit 1109090 k)) := by
  decide

theorem sharp_33_starts : Starts2 3 3 33266233 := by
  refine ⟨fun i => (33266233 / 10 ^ i) % 10, 8, ⟨by decide, ?_, by decide, by decide⟩,
    by decide, by decide, by decide⟩
  intro i _
  exact Nat.le_of_lt_succ (Nat.mod_lt _ (by decide))

#print axioms table4_checked
#print axioms entry_sound
#print axioms ancestry_bound
#print axioms no_196
#print axioms no_196_listed_prefix
#print axioms ancestry_bound_33
#print axioms no_196_33
#print axioms sharp_33
#print axioms sharp_33_starts

end FourColumnKernel.Certificate
