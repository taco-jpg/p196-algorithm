import P196.Drafts.Agent9NooverflowHorizon.Agent9HorizonDefinitions
import P196.Agent1Pr104Repair.DecimalSafeRuns

/-!
Agent #9: finite numeric safety of the protected no-overflow target family.
Source: final no-overflow horizon section of persist_inverse_fibers_proof.txt
at archived source snapshot 2eb05ef47671d6b1883e54fec9f6a4f8de9ed8f5.
Pinned current repository snapshot: 4b4edf976b2c7a9ba1dad80636c0e21c66350325.

The target is a coefficient word. Its canonical decimal realizations have
this word as their pair sums; positive orbit time one is the next numeric
reverse-and-add operation. The imported finite-run theorem and realization
bridge are reused unchanged. The finite seed may depend on both parameters.

Exact original imported source blobs:
DecimalSafeRuns: 5013589f2ad97f111a9b9e1885152990a1fe8e78.
LychrelDigitSums: 8a865176625283648a8a20dd2411ed77670eb0a2.
- No claim about a single seed with infinite avoidance is made here.
-/

namespace P196.Agent9.NoOverflowHorizon

open InverseFibers Lychrel196 DecimalDigits FoldedDecimal DecimalSafeRuns

/-- The finite target word, extended by zero outside its actual width. -/
def targetColumns (m k : Nat) (i : Nat) : Nat :=
  (targetWord m k).getD i 0

theorem protected_half_values (m k : Nat) :
    (targetHalf m k).map Fin.val =
      11 :: (List.replicate m 9 ++ List.replicate k 18) := by
  simp [targetHalf, show (11 : Symbol).val = 11 from rfl,
    show (9 : Symbol).val = 9 from rfl,
    show (18 : Symbol).val = 18 from rfl]

/-- The central eighteen block is literally of length `2 * k`, with
equal length exterior blocks on its two sides. -/
theorem protected_target_blocks (m k : Nat) :
    targetWord m k = (11 :: List.replicate m 9) ++
      (List.replicate (2 * k) 18 ++ (List.replicate m 9 ++ [11])) := by
  rw [targetWord, protected_half_values]
  simp only [mirror, List.reverse_cons, List.reverse_append,
    List.reverse_replicate, List.cons_append, List.append_assoc,
    show 2 * k = k + k by omega, InverseFibers.replicate_add]

theorem protected_target_length (m k : Nat) :
    (targetWord m k).length = 2 * (m + k + 1) := by
  simp only [targetWord, mirror, List.length_append, List.length_reverse,
    List.length_map, targetHalf, List.length_cons, List.length_replicate]
  omega

theorem protected_target_even (m k : Nat) :
    (targetWord m k).length % 2 = 0 := by
  rw [protected_target_length]
  omega

theorem protected_target_reverse (m k : Nat) :
    (targetWord m k).reverse = targetWord m k := by
  simp only [targetWord, mirror, List.reverse_append, List.reverse_reverse]

theorem protected_target_outer (m k : Nat) : targetColumns m k 0 = 11 := by
  simp [targetColumns, protected_target_blocks]

theorem protected_target_bounded (m k i : Nat)
    (hi : i < (targetWord m k).length) : targetColumns m k i ≤ 18 := by
  have hbound : ∀ x, x ∈ targetWord m k → x ≤ 18 := by
    intro x hx
    rw [protected_target_blocks] at hx
    simp only [List.mem_append, List.mem_cons, List.mem_replicate,
      List.mem_singleton, List.not_mem_nil, or_false] at hx
    omega
  have hmem : (targetWord m k)[i] ∈ targetWord m k := List.getElem_mem hi
  have hval : targetColumns m k i = (targetWord m k)[i] := by
    simp [targetColumns, List.getElem?_eq_getElem hi]
  rw [hval]
  exact hbound _ hmem

theorem protected_target_symmetric (m k i : Nat)
    (hi : i < (targetWord m k).length) :
    targetColumns m k i =
      targetColumns m k ((targetWord m k).length - 1 - i) := by
  have he := List.getElem?_reverse (l := targetWord m k) hi
  rw [protected_target_reverse] at he
  exact congrArg (fun x : Option Nat => x.getD 0) he

/-- Even width eliminates the self-reflected center parity obligation. -/
theorem protected_target_center (m k i : Nat)
    (hi : i < (targetWord m k).length)
    (he : i = (targetWord m k).length - 1 - i) :
    targetColumns m k i % 2 = 0 := by
  rw [protected_target_length] at hi he
  omega

/-- These are the exact positive, bounded, symmetric finite-word
conditions required by the existing canonical decimal realization bridge. -/
theorem protected_target_admissible (m k : Nat) :
    Admissible (targetWord m k).length (targetColumns m k) := by
  refine ⟨?_, ?_, protected_target_bounded m k,
    protected_target_symmetric m k, protected_target_center m k⟩
  · rw [protected_target_length]
    omega
  · rw [protected_target_outer]
    decide

theorem protected_target_central_run (m k : Nat) :
    Run18 (targetColumns m k) (targetWord m k).length (m + 1) (2 * k) := by
  constructor
  · rw [protected_target_length]
    omega
  · intro i hlow hupp
    unfold targetColumns
    rw [protected_target_blocks]
    simp only [List.getD_eq_getElem?_getD]
    rw [List.getElem?_append_right (by simpa using hlow)]
    simp only [List.length_cons, List.length_replicate]
    rw [List.getElem?_append_left (by simp; omega),
      List.getElem?_replicate_of_lt (by omega)]
    rfl

/-- Each requested positive index uses only a prefix of the central run.
The exact imported rule concludes time `t + 1` from `1 + 2 * t` eighteens. -/
theorem protected_target_safe (m k n : Nat) (d : Nat → Nat)
    (hc : Canonical n d (targetWord m k).length)
    (hr : ∀ i, i < (targetWord m k).length →
      columnSum d (targetWord m k).length i = targetColumns m k i)
    (j : Nat) (hj : 1 ≤ j) (hjk : j ≤ k) :
    ¬ Palindrome (orbit n j) := by
  have hrun := protected_target_central_run m k
  have hsub : HasRun18 (targetColumns m k) (targetWord m k).length
      (1 + 2 * (j - 1)) := by
    refine ⟨m + 1, ?_, ?_⟩
    · have := hrun.1
      omega
    · intro i hi him
      exact hrun.2 i hi (by omega)
  have hsafe := iter_not_palindrome_of_run n d (targetColumns m k)
    (targetWord m k).length (j - 1) hc hr
    (protected_target_admissible m k) hsub
  simpa only [show j - 1 + 1 = j by omega] using hsafe

/-- The odd outer pair sum eleven also forbids a palindrome at time zero. -/
theorem protected_target_not_palindrome (m k n : Nat) (d : Nat → Nat)
    (hc : Canonical n d (targetWord m k).length)
    (hr : ∀ i, i < (targetWord m k).length →
      columnSum d (targetWord m k).length i = targetColumns m k i) :
    ¬ Palindrome n := by
  intro hp
  have hpv : Palindrome (value d (targetWord m k).length) := by
    simpa only [hc.2.2.2] using hp
  have hs := (palindrome_value_iff d (targetWord m k).length
    hc.2.1 (Or.inr hc.2.2.1)).mp hpv 0 hc.1
  have hsum := hr 0 hc.1
  rw [protected_target_outer] at hsum
  simp only [columnSum, reflected, Nat.sub_zero] at hsum hs
  omega

/-- Every member of this target family has a positive canonical finite
integer realization at exactly the target's actual width. -/
theorem protected_target_realizable (m k : Nat) :
    ∃ n d, 0 < n ∧ Canonical n d (targetWord m k).length ∧
      ∀ i, i < (targetWord m k).length →
        columnSum d (targetWord m k).length i = targetColumns m k i := by
  have ha := protected_target_admissible m k
  exact valid_word_realizable _ _ ha.1 ha.2.1 ha.2.2.1
    ha.2.2.2.1 ha.2.2.2.2

/-- A finite integer with this target pair word exists and avoids
palindromes at every time from zero through the chosen finite horizon. -/
theorem protected_target_safe_realization (m k : Nat) :
    ∃ n d, 0 < n ∧ Canonical n d (targetWord m k).length ∧
      (∀ i, i < (targetWord m k).length →
        columnSum d (targetWord m k).length i = targetColumns m k i) ∧
      ∀ j, j ≤ k → ¬ Palindrome (orbit n j) := by
  obtain ⟨n, d, hn, hc, hr⟩ := protected_target_realizable m k
  refine ⟨n, d, hn, hc, hr, ?_⟩
  intro j hj
  cases j with
  | zero => exact protected_target_not_palindrome m k n d hc hr
  | succ j => exact protected_target_safe m k n d hc hr (j + 1) (by omega) hj

#print axioms targetColumns
#print axioms protected_half_values
#print axioms protected_target_blocks
#print axioms protected_target_length
#print axioms protected_target_even
#print axioms protected_target_reverse
#print axioms protected_target_outer
#print axioms protected_target_bounded
#print axioms protected_target_symmetric
#print axioms protected_target_center
#print axioms protected_target_admissible
#print axioms protected_target_central_run
#print axioms protected_target_safe
#print axioms protected_target_not_palindrome
#print axioms protected_target_realizable
#print axioms protected_target_safe_realization

end P196.Agent9.NoOverflowHorizon
