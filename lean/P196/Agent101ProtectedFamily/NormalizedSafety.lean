import P196.Agent101ProtectedFamily.SafetyBridge

/-!
Interpret a normalized digit list using the original `DecimalDigits.value`.
The only compatibility lemma here identifies list pairing with the original
column sums. Normalization and the family transition remain the unchanged
`Agent8.normalize`, `Agent8.pair`, and `Agent8.stepWord` operations.
-/

namespace P196.Agent3.OverflowHorizon

open Lychrel196 DecimalDigits FoldedDecimal

/-- Digits from a finite least-significant-first list. -/
def digitColumn (ds : Agent8.Word) (i : Nat) : Nat := (ds[i]?).getD 0

/-- The ordinary integer represented by a finite decimal digit list. -/
def digitValue (ds : Agent8.Word) : Nat := value (digitColumn ds) ds.length

/-- A bounded digit list with a positive final digit is canonical for its
ordinary decimal value. The suffix witness also enforces nonemptiness. -/
theorem digitList_canonical (ds : Agent8.Word) (hb : Agent8.Bounded ds 9)
    (hpos : ∃ init last, ds = init ++ [last] ∧ 0 < last) :
    Canonical (digitValue ds) (digitColumn ds) ds.length := by
  refine ⟨?_, ?_, ?_, rfl⟩
  · obtain ⟨init, last, rfl, _⟩ := hpos
    simp
  · intro i hi
    simp only [digitColumn, List.getElem?_eq_getElem hi, Option.getD_some]
    exact hb _ (List.getElem_mem hi)
  · obtain ⟨init, last, rfl, hl⟩ := hpos
    simpa [digitColumn, List.getElem?_append] using hl

/-- The existing list pairing computes exactly the original mirrored
decimal column sum at every in-range position. -/
theorem digitColumn_pair (ds : Agent8.Word) (i : Nat) (hi : i < ds.length) :
    columnSum (digitColumn ds) ds.length i = ((Agent8.pair ds)[i]?).getD 0 := by
  have hr : ds.length - 1 - i < ds.length := by omega
  simp only [columnSum, reflected, digitColumn, Agent8.pair,
    Agent8.zipAdd_eq_zipWith, List.getElem?_zipWith, List.getElem?_reverse hi,
    List.getElem?_eq_getElem hi, List.getElem?_eq_getElem hr, Option.getD_some]

/-- A normalized list whose existing mirrored pair is the shared target
is an exact canonical decimal realization in the original core semantics. -/
theorem digitList_target_realization (ds : Agent8.Word) (m k : Nat)
    (hb : Agent8.Bounded ds 9)
    (hpos : ∃ init last, ds = init ++ [last] ∧ 0 < last)
    (hpair : Agent8.pair ds = target m k) :
    Canonical (digitValue ds) (digitColumn ds) (target m k).length ∧
      ∀ i, i < (target m k).length →
        columnSum (digitColumn ds) (target m k).length i = targetColumn m k i := by
  have hlen : ds.length = (target m k).length := by
    rw [← Agent8.pair_length ds, hpair]
  constructor
  · simpa only [hlen] using digitList_canonical ds hb hpos
  · intro i hi
    simpa only [hlen, hpair, targetColumn] using
      digitColumn_pair ds i (by omega)

/-- Every normalized family output is positive and avoids palindromes at
times `0, ..., k`, when its pair word is the common target. -/
theorem normalized_target_safe_prefix (ds : Agent8.Word) (m k : Nat)
    (hk : 0 < k) (hb : Agent8.Bounded ds 9)
    (hpos : ∃ init last, ds = init ++ [last] ∧ 0 < last)
    (hpair : Agent8.pair ds = target m k) :
    0 < digitValue ds ∧
      ∀ t, t ≤ k → ¬ Palindrome (orbit (digitValue ds) t) := by
  obtain ⟨hc, hrep⟩ := digitList_target_realization ds m k hb hpos hpair
  constructor
  · have hp := value_positive (digitColumn ds) (target m k).length hc.1 hc.2.2.1
    simpa only [hc.2.2.2] using hp
  · intro t ht
    cases t with
    | zero =>
        exact target_realization_nonpalindrome m k (digitValue ds)
          (digitColumn ds) hc hrep
    | succ t =>
        exact target_numeric_safe_prefix m k hk (digitValue ds)
          (digitColumn ds) hc hrep t (by omega)

/-- The next ordinary integer is independent of which normalized digit
list realizes the shared target. This is the existing exact core bridge. -/
theorem normalized_target_step_value (ds : Agent8.Word) (m k : Nat)
    (hb : Agent8.Bounded ds 9)
    (hpos : ∃ init last, ds = init ++ [last] ∧ 0 < last)
    (hpair : Agent8.pair ds = target m k) :
    step (digitValue ds) = value (targetColumn m k) (target m k).length := by
  obtain ⟨hc, hrep⟩ := digitList_target_realization ds m k hb hpos hpair
  exact step_eq_word_value (digitValue ds) (digitColumn ds) (targetColumn m k)
    (target m k).length hc hrep

end P196.Agent3.OverflowHorizon
