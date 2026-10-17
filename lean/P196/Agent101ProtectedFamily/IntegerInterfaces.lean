import P196.Agent101ProtectedFamily.NormalizedSafety
import P196.Agent101ProtectedFamily.Compat

/-!
Exact ordinary-arithmetic interfaces for the two-history construction.
The list value and normalization operations are related to existing
accepted semantics; no history transition is assumed proved in this file.
Even-width realizability retains the finite-word center condition.
-/

namespace P196.Agent3.TwoHistory

open Lychrel196 DecimalDigits FoldedDecimal
open P196.Agent3.OverflowHorizon

/-- A positive canonical decimal realization of a full coefficient word. -/
def IntegerRealizes (n : Nat) (w : Agent8.Word) : Prop :=
  ∃ d, Canonical n d w.length ∧
    ∀ i, i < w.length → columnSum d w.length i = digitColumn w i

/-- The original fixed-width decimal value agrees with the already
formalized least-significant-first list evaluation. -/
theorem digitValue_eq_evalL (ds : Agent8.Word) :
    digitValue ds = Agent109.evalL ds := by
  induction ds with
  | nil => rfl
  | cons x xs ih =>
      change value (digitColumn (x :: xs)) (xs.length + 1) =
        x + 10 * Agent109.evalL xs
      rw [value_shift]
      change x + 10 * digitValue xs = x + 10 * Agent109.evalL xs
      rw [ih]

/-- Reuse the existing normalization-value theorem and its original-name
compatibility, rather than constructing a second normalization proof. -/
theorem digitValue_normalize (w : Agent8.Word) (e : Nat) :
    digitValue (Agent8.normalize w e) = digitValue w + e := by
  simp only [digitValue_eq_evalL, Agent109.Compat.normalize_eq, Agent109.evalL_norm]

theorem digitColumn_zero_eq_headD (w : Agent8.Word) :
    digitColumn w 0 = w.headD 0 := by
  cases w <;> rfl

theorem integer_realizes_positive (n : Nat) (w : Agent8.Word)
    (hr : IntegerRealizes n w) : 0 < n := by
  obtain ⟨d, hc, _⟩ := hr
  simpa only [hc.2.2.2] using value_positive d w.length hc.1 hc.2.2.1

/-- Any canonical realization takes exactly the ordinary step represented
by the existing normalization of its coefficient word. -/
theorem integer_step_of_realizes (n : Nat) (w : Agent8.Word)
    (hr : IntegerRealizes n w) :
    step n = digitValue (Agent8.normalize w 0) := by
  obtain ⟨d, hc, hrep⟩ := hr
  rw [digitValue_normalize, Nat.add_zero]
  exact step_eq_word_value n d (digitColumn w) w.length hc hrep

/-- The even-width hypothesis discharges the exact unpaired-center
condition; `CanonicalPair` alone does not supply it in odd width. -/
theorem even_canonical_admissible (w : Agent8.Word)
    (hw : Agent8.CanonicalPair w) (heven : w.length % 2 = 0) :
    Admissible w.length (digitColumn w) := by
  refine ⟨?_, ?_, ?_, ?_, ?_⟩
  · have hn := hw.1
    cases w <;> simp_all
  · rw [digitColumn_zero_eq_headD]
    exact hw.2.2.2
  · intro i hi
    simp only [digitColumn, List.getElem?_eq_getElem hi, Option.getD_some]
    exact hw.2.2.1 _ (List.getElem_mem hi)
  · intro i hi
    unfold digitColumn
    rw [← List.getElem?_reverse hi, hw.2.1]
  · intro i hi heq
    omega

/-- Every even canonical coefficient word has an ordinary positive
integer realization in the unchanged decimal semantics. -/
theorem even_canonical_realizable (w : Agent8.Word)
    (hw : Agent8.CanonicalPair w) (heven : w.length % 2 = 0) :
    ∃ n, 0 < n ∧ IntegerRealizes n w := by
  have ha := even_canonical_admissible w hw heven
  obtain ⟨n, d, hn, hc, hrep⟩ := valid_word_realizable (digitColumn w) w.length
    ha.1 ha.2.1 ha.2.2.1 ha.2.2.2.1 ha.2.2.2.2
  exact ⟨n, hn, d, hc, hrep⟩

theorem canonicalPair_lastPos (w : Agent8.Word) (hw : Agent8.CanonicalPair w) :
    Agent109.LastPos w := by
  intro a hlast
  rw [← hw.2.1, List.getLast?_reverse] at hlast
  cases w with
  | nil => simp at hlast
  | cons x xs =>
      simp only [List.head?_cons, Option.some.injEq] at hlast
      have hp := hw.2.2.2
      simpa only [List.headD_cons, hlast] using hp

/-- Normalizing a canonical coefficient word gives bounded digits with
a positive final digit, using the existing `canon_normalize` theorem. -/
theorem canonicalPair_normalized_digits (w : Agent8.Word)
    (hw : Agent8.CanonicalPair w) :
    Agent8.Bounded (Agent8.normalize w 0) 9 ∧
      ∃ init last, Agent8.normalize w 0 = init ++ [last] ∧ 0 < last := by
  have hc : Agent109.Canon (Agent8.normalize w 0) := by
    rw [Agent109.Compat.normalize_eq]
    exact Agent109.canon_normalize w 0 hw.2.2.1 (by decide) (canonicalPair_lastPos w hw)
  have hn : Agent8.normalize w 0 ≠ [] := by
    intro hnil
    have hp := (Agent8.canonical_step w hw).1.1
    apply hp
    simp [Agent8.stepWord, hnil, Agent8.pair, Agent8.zipAdd]
  refine ⟨Agent8.normalized_digits_bounded w 0 hw.2.2.1 (by decide), ?_⟩
  obtain ⟨init, last, hsplit⟩ :
      ∃ init last, Agent8.normalize w 0 = init ++ [last] := by
    cases hrev : (Agent8.normalize w 0).reverse with
    | nil =>
        have hz : Agent8.normalize w 0 = [] := by
          rw [← List.reverse_reverse (Agent8.normalize w 0), hrev]
          rfl
        exact False.elim (hn hz)
    | cons last init =>
        refine ⟨init.reverse, last, ?_⟩
        rw [← List.reverse_reverse (Agent8.normalize w 0), hrev]
        simp
  refine ⟨init, last, hsplit, ?_⟩
  exact ((Agent109.canon_iff _).mp hc).2 last (by rw [hsplit]; simp)

/-- The existing digit-list canonical and pairing bridges apply to an
arbitrary normalized word, with no new normalization semantics. -/
theorem digitList_realizes_pair (ds : Agent8.Word)
    (hb : Agent8.Bounded ds 9)
    (hpos : ∃ init last, ds = init ++ [last] ∧ 0 < last) :
    IntegerRealizes (digitValue ds) (Agent8.pair ds) := by
  refine ⟨digitColumn ds, ?_, ?_⟩
  · simpa only [Agent8.pair_length] using digitList_canonical ds hb hpos
  · intro i hi
    simpa only [Agent8.pair_length] using
      digitColumn_pair ds i (by simpa only [Agent8.pair_length] using hi)

theorem normalized_realizes_stepWord (w : Agent8.Word)
    (hw : Agent8.CanonicalPair w) :
    IntegerRealizes (digitValue (Agent8.normalize w 0)) (Agent8.stepWord w) := by
  obtain ⟨hb, hp⟩ := canonicalPair_normalized_digits w hw
  exact digitList_realizes_pair (Agent8.normalize w 0) hb hp

/-- Actual canonical realizations propagate through the unchanged whole-word
step. This corollary only combines the preceding exact interfaces. -/
theorem integer_realizes_next (n : Nat) (w : Agent8.Word)
    (hw : Agent8.CanonicalPair w) (hr : IntegerRealizes n w) :
    IntegerRealizes (step n) (Agent8.stepWord w) := by
  rw [integer_step_of_realizes n w hr]
  exact normalized_realizes_stepWord w hw

theorem normalized_integer_next (w : Agent8.Word) (hw : Agent8.CanonicalPair w) :
    step (digitValue (Agent8.normalize w 0)) =
      digitValue (Agent8.normalize (Agent8.stepWord w) 0) :=
  integer_step_of_realizes _ _ (normalized_realizes_stepWord w hw)

/-- An odd mirrored digit sum excludes a palindrome in every realization. -/
theorem integer_nonpalindrome_of_odd_column (n : Nat) (w : Agent8.Word)
    (hr : IntegerRealizes n w) (i : Nat) (hi : i < w.length)
    (hodd : digitColumn w i % 2 = 1) : ¬ Palindrome n := by
  obtain ⟨d, hc, hrep⟩ := hr
  intro hp
  rw [← hc.2.2.2] at hp
  have hs := (palindrome_value_iff d w.length hc.2.1 (Or.inr hc.2.2.1)).mp hp
  have hiq := hrep i hi
  have hsym := hs i hi
  simp only [columnSum, reflected] at hiq
  omega

theorem integer_nonpalindrome_of_odd_outer (n : Nat) (w : Agent8.Word)
    (hr : IntegerRealizes n w) (hodd : w.headD 0 % 2 = 1) : ¬ Palindrome n := by
  obtain ⟨d, hc, hrep⟩ := hr
  exact integer_nonpalindrome_of_odd_column n w ⟨d, hc, hrep⟩ 0 hc.1
    (by simpa only [digitColumn_zero_eq_headD] using hodd)

/-- A single eighteen column supplies the existing one-step central-run
safety certificate for any ordinary realization of the word. -/
theorem integer_step_nonpalindrome_of_eighteen (n : Nat) (w : Agent8.Word)
    (hr : IntegerRealizes n w) (hm : 18 ∈ w) : ¬ Palindrome (step n) := by
  obtain ⟨d, hc, hrep⟩ := hr
  have ha : Admissible w.length (digitColumn w) :=
    NormalizationBridge.admissible_congr _ _ _
      (NormalizationBridge.canonical_admissible n d w.length hc) hrep
  obtain ⟨i, hi, heq⟩ := List.mem_iff_getElem.mp hm
  have h18 : digitColumn w i = 18 := by
    simp only [digitColumn, List.getElem?_eq_getElem hi, Option.getD_some, heq]
  have hrun : DecimalSafeRuns.HasRun18 (digitColumn w) w.length 1 := by
    refine ⟨i, by omega, ?_⟩
    intro j hj hji
    have hji' : j = i := by omega
    simpa only [hji'] using h18
  exact DecimalSafeRuns.iter_not_palindrome_of_run n d (digitColumn w) w.length 0
    hc hrep ha hrun

end P196.Agent3.TwoHistory
