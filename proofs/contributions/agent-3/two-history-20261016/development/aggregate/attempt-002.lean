import HistoryFamily
import HistorySafety

/-!
The complete finite-horizon two-history family. Cardinalities count
canonical coefficient words. The ordinary-integer conclusion applies to
every canonical realization of each initial word and includes existence.
The free family and its central reservoir depend on the prescribed horizon.
-/

namespace P196.Agent3.TwoHistory

open Agent8 Lychrel196
open P196.Agent3.OverflowHorizon

theorem mirrored_eighteen_reservoir (prefix : List Nat) (k : Nat) :
    P196.Agent9.InverseFibers.mirror (prefix ++ List.replicate k 18) =
      prefix ++ List.replicate (2 * k) 18 ++ prefix.reverse := by
  rw [show 2 * k = k + k by omega, List.replicate_add]
  simp only [P196.Agent9.InverseFibers.mirror, List.reverse_append,
    List.reverse_replicate, List.append_assoc]

/-- The initial history retains the literal central block of `2*k`
eighteens, between equally long mirrored outer parts. -/
theorem historyWord0_reservoir (xs : List Bool) (k : Nat) :
    ∃ prefix : List Nat, prefix.length = xs.length + 7 ∧
      historyWord0 xs k =
        prefix ++ List.replicate (2 * k) 18 ++ prefix.reverse := by
  refine ⟨(secondLabels (0, 0) (historyBits xs)).map Fin.val, ?_, ?_⟩
  · simp only [List.length_map, secondLabels_length, historyBits_length]
  · exact mirrored_eighteen_reservoir _ k

/-- The first predecessor has the same literal central reservoir. -/
theorem historyWord1_reservoir (xs : List Bool) (k : Nat) :
    ∃ prefix : List Nat, prefix.length = xs.length + 7 ∧
      historyWord1 xs k =
        prefix ++ List.replicate (2 * k) 18 ++ prefix.reverse := by
  refine ⟨(firstLabels (0, 0) (historyBits xs)).map Fin.val, ?_, ?_⟩
  · simp only [List.length_map, firstLabels_length, historyBits_length]
  · exact mirrored_eighteen_reservoir _ k

/-- All three explicit coefficient words are canonical, have the same
even width, and take the asserted two zero-carry steps and one overflow
step in the unchanged full-word dynamics. -/
theorem history_word_chain (xs : List Bool) (k : Nat) (hk : 0 < k) :
    CanonicalPair (historyWord0 xs k) ∧
    CanonicalPair (historyWord1 xs k) ∧
    CanonicalPair (historyWord2 xs k) ∧
    (historyWord0 xs k).length = 2 * (xs.length + k + 7) ∧
    (historyWord1 xs k).length = 2 * (xs.length + k + 7) ∧
    (historyWord2 xs k).length = 2 * (xs.length + k + 7) ∧
    (historyWord0 xs k).length % 2 = 0 ∧
    (historyWord1 xs k).length % 2 = 0 ∧
    (historyWord2 xs k).length % 2 = 0 ∧
    (historyWord0 xs k).headD 0 = 3 ∧
    (historyWord1 xs k).headD 0 = 7 ∧
    terminalCarry (historyWord0 xs k) 0 = 0 ∧
    terminalCarry (historyWord1 xs k) 0 = 0 ∧
    terminalCarry (historyWord2 xs k) 0 = 1 ∧
    stepWord (historyWord0 xs k) = historyWord1 xs k ∧
    stepWord (historyWord1 xs k) = historyWord2 xs k ∧
    stepWord (historyWord2 xs k) = target (xs.length + 6) k := by
  exact ⟨historyWord0_canonical xs k, historyWord1_canonical xs k,
    historyWord2_canonical xs k, historyWord0_length xs k,
    historyWord1_length xs k, historyWord2_length xs k,
    historyWord0_even xs k, historyWord1_even xs k, historyWord2_even xs k,
    historyWord0_head xs k, historyWord1_head xs k,
    historyWord0_final_carry xs k, historyWord1_final_carry xs k,
    historyWord2_final_carry xs k, historyWord0_step xs k,
    historyWord1_step xs k, historyWord2_step xs k hk⟩

/-- Exactly `2^m` distinct canonical initial coefficient words support
the two incoming histories. Every ordinary realization is positive,
avoids palindromes through time `k + 3`, and shares the time-four value.
Each initial coefficient word has at least one such realization. -/
theorem finite_horizon_two_history_family (m k : Nat) (hk : 0 < k) :
    (historyFamily0 m k).length = 2 ^ m ∧
    (historyFamily0 m k).Nodup ∧
    (historyFamily2 m k).length = 2 ^ m ∧
    (historyFamily2 m k).Nodup ∧
    (historyFamily0 m k).map (fun w => stepWord (stepWord w)) =
      historyFamily2 m k ∧
    ∀ w ∈ historyFamily0 m k,
      CanonicalPair w ∧ w.length = 2 * (m + k + 7) ∧ w.length % 2 = 0 ∧
      (∃ xs : List Bool, xs.length = m ∧ historyWord0 xs k = w ∧
        stepWord w = historyWord1 xs k ∧
        stepWord (historyWord1 xs k) = historyWord2 xs k ∧
        terminalCarry w 0 = 0 ∧
        terminalCarry (historyWord1 xs k) 0 = 0 ∧
        terminalCarry (historyWord2 xs k) 0 = 1 ∧
        stepWord (historyWord2 xs k) = target (m + 6) k) ∧
      (∃ n, 0 < n ∧ IntegerRealizes n w) ∧
      (∀ n, IntegerRealizes n w →
        0 < n ∧ (∀ t, t ≤ k + 3 → ¬ Palindrome (orbit n t)) ∧
        orbit n 4 = digitValue (target (m + 6) k)) := by
  refine ⟨historyFamily0_length m k, historyFamily0_nodup m k,
    historyFamily2_length m k, historyFamily2_nodup m k,
    historyFamilies_two_step m k, ?_⟩
  intro w hw
  obtain ⟨xs, hlen, rfl⟩ := (mem_historyFamily0_iff w m k).mp hw
  refine ⟨historyWord0_canonical xs k,
    by rw [historyWord0_length, hlen], historyWord0_even xs k, ?_, ?_, ?_⟩
  · exact ⟨xs, hlen, rfl, historyWord0_step xs k, historyWord1_step xs k,
      historyWord0_final_carry xs k, historyWord1_final_carry xs k,
      historyWord2_final_carry xs k,
      by simpa only [hlen] using historyWord2_step xs k hk⟩
  · exact even_canonical_realizable _ (historyWord0_canonical xs k)
      (historyWord0_even xs k)
  · intro n hr
    simpa only [hlen] using history_integer_realization_package xs k hk n hr

end P196.Agent3.TwoHistory
