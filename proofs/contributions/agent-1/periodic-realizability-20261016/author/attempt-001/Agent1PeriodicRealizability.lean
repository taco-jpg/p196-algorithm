import Agent1PeriodicValidity

/-!
Pointwise ordinary-decimal realization of the unchanged valid period-four
template. The generic positive realization construction is the existing
FoldedDecimal.valid_word_realizable; this module only supplies its indexed
hypotheses from ValidPeriodic. CanonicalPair alone omits middle parity.
-/

namespace Agent1.Periodic

open Agent8 Agent1.RepeatedBlock

/-- Every positive exponent of a valid periodic tuple satisfies the original
indexed finite-word admissibility predicate, including odd-middle parity. -/
theorem periodicWord_admissible (B H w : Word) (k : Nat)
    (hv : ValidPeriodic B H w) (hk : 0 < k) :
    FoldedDecimal.Admissible (periodicWord B H w k).length
      (fun i => ((periodicWord B H w k)[i]?).getD 0) := by
  have hc := periodicWord_canonical B H w k hv hk
  refine ⟨List.length_pos_iff.mpr hc.1, ?_, ?_, ?_, ?_⟩
  · simpa only [List.headD_eq_head?_getD, List.head?_eq_getElem?] using hc.2.2.2
  · intro i hi
    simp only [List.getElem?_eq_getElem hi, Option.getD_some]
    exact hc.2.2.1 _ (List.getElem_mem hi)
  · intro i hi
    have hr := List.getElem?_reverse (l := periodicWord B H w k) hi
    rw [hc.2.1] at hr
    exact congrArg (fun o : Option Nat => o.getD 0) hr
  · intro i hi hfixed
    have hlen := periodicWord_length B H w k
    have hiMid : i = (periodicWord B H w k).length / 2 := by omega
    have hodd : H.length % 2 = 1 := by omega
    have hPS : (B ++ pow w k).length = (pow w.reverse k ++ B.reverse).length := by
      simp only [List.length_append, List.length_reverse, pow_length]
      omega
    have hm := middle_append_eq (B ++ pow w k) H
      (pow w.reverse k ++ B.reverse) hPS hodd
    have hmiddle :
        (periodicWord B H w k)[(periodicWord B H w k).length / 2]? =
          H[H.length / 2]? := by
      simpa only [periodicWord, List.append_assoc] using hm
    rw [hiMid, hmiddle]
    exact hv.center_even hodd

/-- Every positive exponent has a positive ordinary integer realization at
exactly the template width. The integer may depend on the exponent; this
asserts neither initial nonpalindromicity nor an infinite safe orbit. -/
theorem periodicWord_realizable (B H w : Word) (k : Nat)
    (hv : ValidPeriodic B H w) (hk : 0 < k) :
    ∃ n d, 0 < n ∧
      DecimalDigits.Canonical n d (periodicWord B H w k).length ∧
      ∀ i, i < (periodicWord B H w k).length →
        DecimalDigits.columnSum d (periodicWord B H w k).length i =
          ((periodicWord B H w k)[i]?).getD 0 := by
  obtain ⟨hL, houter, hbound, hsym, hcenter⟩ :=
    periodicWord_admissible B H w k hv hk
  exact FoldedDecimal.valid_word_realizable _ _ hL houter hbound hsym hcenter

end Agent1.Periodic

#print axioms Agent1.Periodic.periodicWord_admissible
#print axioms Agent1.Periodic.periodicWord_realizable
