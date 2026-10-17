import Agent107DFAHorn

/-!
Conditional arithmetic consequences of the finite Horn closure certificate.
These statements use the actual folded column update and the ordinary
natural-number reverse-and-add step. No safety or nonempty-language premise
is silently supplied, and no particular DFA model is asserted to exist.
-/

namespace Agent107.FoldedDFA

open Agent107.FoldedTransducer DecimalDigits FoldedDecimal

/-- Finite Horn conditions suffice for all-width closure under the exact
column update, including its actual overflow-dependent width. -/
theorem horn_next_closed {N : Nat} (M : DFA N)
    (R : State → Fin N → Fin N → Prop) (cert : Horn M R)
    (L : Nat) (q : Nat → Nat) (hAd : Admissible L q)
    (ha : M.accepts (foldPrefix L q)) :
    M.accepts (foldPrefix (nextWidth q L) (nextColumns q L)) := by
  have hp := actual_accepts L q hAd
  have hout := horn_accepting_output M R cert L q (actualState L q) hp ha
  rw [accepting_output L q (actualState L q) hAd hp] at hout
  exact hout

/-- Every represented integer whose folded column word is DFA-accepted
has an actually represented next integer with a DFA-accepted folded word.
The next width is the genuine width, rather than an arbitrary padding. -/
theorem horn_canonical_step {N : Nat} (M : DFA N)
    (R : State → Fin N → Fin N → Prop) (cert : Horn M R)
    (n : Nat) (d : Nat → Nat) (L : Nat) (hcan : Canonical n d L)
    (ha : M.accepts (foldPrefix L (columnSum d L))) :
    ∃ e, Canonical (Lychrel196.step n) e (nextWidth (columnSum d L) L) ∧
      M.accepts (foldPrefix (nextWidth (columnSum d L) L)
        (columnSum e (nextWidth (columnSum d L) L))) := by
  obtain ⟨p, e, hp, he, hout⟩ := canonical_step_path n d L hcan
  refine ⟨e, he, ?_⟩
  rw [hout]
  exact horn_accepting_output M R cert L (columnSum d L) p hp ha

#print axioms horn_next_closed
#print axioms horn_canonical_step

end Agent107.FoldedDFA
