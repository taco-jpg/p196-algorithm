import Agent107TransducerInput
import Agent107TransducerOutput

/-!
The literal folded transducer represents the ordinary natural-number
reverse-and-add step. The forward direction starts from a canonical decimal
integer. The reverse direction starts only from a complete accepting path;
it reconstructs the unread half of the input before invoking the original
finite realizability and representation-next theorems.
-/

namespace Agent107.FoldedTransducer

open DecimalDigits FoldedDecimal

/-- An accepting path on a represented admissible input emits precisely
the folded column sums of the actual integer `step n`. The stronger full
finite representation is retained for subsequent numeric composition. -/
theorem canonical_accepting_step (n : Nat) (d q : Nat → Nat) (L : Nat)
    (p : Nat → State) (hcan : Canonical n d L)
    (hrep : ∀ i, i < L → columnSum d L i = q i)
    (hAd : Admissible L q) (hp : Accepts L q p) :
    ∃ e, Canonical (Lychrel196.step n) e (nextWidth q L) ∧
      (∀ i, i < nextWidth q L →
        columnSum e (nextWidth q L) i = nextColumns q L i) ∧
      foldPrefix (nextWidth q L) (columnSum e (nextWidth q L)) =
        pathOutput L q p := by
  obtain ⟨e, he, hr⟩ := representation_next n d q L hcan hrep
  refine ⟨e, he, hr, ?_⟩
  exact (foldPrefix_congr (nextWidth q L)
    (columnSum e (nextWidth q L)) (nextColumns q L) hr).trans
      (accepting_output L q p hAd hp).symm

/-- Every canonical positive-width decimal integer has a complete folded
path whose output is a canonical representation of its genuine next step.
The input's admissibility follows from its digits, rather than being an
additional premise of this numeric-to-path direction. -/
theorem canonical_step_path (n : Nat) (d : Nat → Nat) (L : Nat)
    (hcan : Canonical n d L) :
    ∃ p e, Accepts L (columnSum d L) p ∧
      Canonical (Lychrel196.step n) e (nextWidth (columnSum d L) L) ∧
      foldPrefix (nextWidth (columnSum d L) L)
        (columnSum e (nextWidth (columnSum d L) L)) =
          pathOutput L (columnSum d L) p := by
  have ha := NormalizationBridge.canonical_admissible n d L hcan
  have hp := actual_accepts L (columnSum d L) ha
  obtain ⟨e, he, _, hout⟩ := canonical_accepting_step n d (columnSum d L) L
    (actualState L (columnSum d L)) hcan (fun _ _ => rfl) ha hp
  exact ⟨actualState L (columnSum d L), e, hp, he, hout⟩

/-- Every complete accepting path, with no assumed admissibility or
symmetry of the unread half, is exactly an actual positive integer step
on folded inputs and outputs. The width is the actual next width of the
reconstructed admissible input, not an arbitrary padded representation. -/
theorem accepting_numeric_realizable (L : Nat) (q : Nat → Nat)
    (p : Nat → State) (hp : Accepts L q p) :
    ∃ n d e, 0 < n ∧ Canonical n d L ∧
      Canonical (Lychrel196.step n) e (nextWidth (symmetrize L q) L) ∧
      (∀ i, i < L → columnSum d L i = symmetrize L q i) ∧
      foldPrefix L (columnSum d L) = foldPrefix L q ∧
      foldPrefix (nextWidth (symmetrize L q) L)
        (columnSum e (nextWidth (symmetrize L q) L)) =
          pathOutput L q p := by
  obtain ⟨n, d, hn, hc, hr, hp', hin, hout⟩ :=
    accepting_input_realizable L q p hp
  have ha := reconstructed_admissible L q p hp
  obtain ⟨e, he, _, heout⟩ :=
    canonical_accepting_step n d (symmetrize L q) L p hc hr ha hp'
  refine ⟨n, d, e, hn, hc, he, hr, ?_, heout.trans hout⟩
  exact (foldPrefix_congr L (columnSum d L) (symmetrize L q) hr).trans hin

#print axioms canonical_accepting_step
#print axioms canonical_step_path
#print axioms accepting_numeric_realizable

end Agent107.FoldedTransducer
