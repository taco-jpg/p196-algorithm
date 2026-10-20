import P196.Drafts.Agent103ResidualFiveFibers.ResidualFiveResidues
import P196.ResidualFivePredecessorCount.ScanSupport
import P196.Drafts.Agent19Session8ff2acAgent19Session8ff2ac.ResidualFivePredecessorFilter
import P196.Drafts.Agent3PrefixContraction.PathCounts

set_option autoImplicit false

/-!
The original numerical scanner filters the original complete enumeration of
complementary digit pairs. Its middle-word cardinality is transported to the
existing folded inverse-path enumeration and its proved Fibonacci count.
The words counted here are finite target digit words, not integer orbits.
-/

namespace P196.ResidualFivePredecessorCount

open Agent101
open Agent105DecoderLocal9df76b (Edge decodePair)
open Agent105DecoderScan9df76b (scan)
open Agent103.ResidualFiveResidues (rawNine rawNine_zero rawNine_succ)

private def accepted (a b : Nat) (ds : List Nat) : Bool :=
  (scan ds.length (digitFn ds) a b).isSome

/-- Complete middle digit words accepted from the two zero boundary carries. -/
def rawAcceptedWords (r : Nat) : List (List Nat) :=
  (Agent101.rawWords (List.replicate r 9) none).filter
    (fun ds => (Agent105DecoderScan9df76b.scan
      ds.length (Agent101.digitFn ds) 0 0).isSome)

private def rawScanCount (r a b : Nat) : Nat :=
  (rawNine r).countP (accepted a b)

private theorem wrapped_count (words : List (List Nat)) (u v a b : Nat) :
    (words.map (wrapDigits u v)).countP (accepted a b) =
      words.countP (fun ds =>
        match decodePair u v a b with
        | none => false
        | some E => accepted E.low E.high ds) := by
  rw [List.countP_map]
  apply List.countP_congr
  intro ds _
  simp only [Function.comp_apply, accepted, scan_wrap_isSome]
  rfl

/-- Outgoing carry pairs of the original decoder, retaining one entry for
each original digit-pair choice which it accepts. -/
private def decoderDestinations (ps : List (Nat × Nat)) (a b : Nat) :
    List (Nat × Nat) :=
  ps.filterMap (fun p =>
    (decodePair p.1 p.2 a b).map (fun E => (E.low, E.high)))

private theorem wrapped_grid_count (ps : List (Nat × Nat))
    (words : List (List Nat)) (a b : Nat) :
    (ps.flatMap (fun p => words.map (wrapDigits p.1 p.2))).countP
        (accepted a b) =
      ((decoderDestinations ps a b).map
        (fun st => words.countP (accepted st.1 st.2))).sum := by
  induction ps with
  | nil => simp [decoderDestinations]
  | cons p ps ih =>
    simp only [List.flatMap_cons, List.countP_append, wrapped_count]
    rw [ih]
    simp only [decoderDestinations, List.filterMap_cons]
    cases hd : decodePair p.1 p.2 a b with
    | none => simp [hd]
    | some E => simp [hd]

/- These four finite equalities are kernel evaluations of the original
decoder's list interface. They are compatible with the existing arithmetic
table in ResidualFivePredecessorFilter; no separate transition semantics
are used. -/
private theorem decoder_destinations_00 :
    decoderDestinations (pairChoices false 9) 0 0 = [(0, 1)] := by
  unfold decoderDestinations
  rw [Agent103.ResidualFiveResidues.pairChoices_nine]
  decide

private theorem decoder_destinations_01 :
    decoderDestinations (pairChoices false 9) 0 1 = [(1, 1), (0, 1)] := by
  unfold decoderDestinations
  rw [Agent103.ResidualFiveResidues.pairChoices_nine]
  decide

private theorem decoder_destinations_10 :
    decoderDestinations (pairChoices false 9) 1 0 = [(1, 0), (0, 0)] := by
  unfold decoderDestinations
  rw [Agent103.ResidualFiveResidues.pairChoices_nine]
  decide

private theorem decoder_destinations_11 :
    decoderDestinations (pairChoices false 9) 1 1 = [(1, 0)] := by
  unfold decoderDestinations
  rw [Agent103.ResidualFiveResidues.pairChoices_nine]
  decide

private theorem rawScanCount_step (r : Nat) :
    rawScanCount (r + 1) 0 0 = rawScanCount r 0 1 ∧
    rawScanCount (r + 1) 0 1 = rawScanCount r 1 1 + rawScanCount r 0 1 ∧
    rawScanCount (r + 1) 1 0 = rawScanCount r 1 0 + rawScanCount r 0 0 ∧
    rawScanCount (r + 1) 1 1 = rawScanCount r 1 0 := by
  refine ⟨?_, ?_, ?_, ?_⟩
  all_goals
    simp only [rawScanCount, rawNine_succ, wrapped_grid_count,
      decoder_destinations_00, decoder_destinations_01,
      decoder_destinations_10, decoder_destinations_11,
      List.map_cons, List.map_nil, List.sum_cons, List.sum_nil, Nat.add_zero]

private theorem preimages_step_length
    (ss : List P196.Agent9.InverseFibers.Symbol)
    (p : P196.Agent9.InverseFibers.State) :
    (P196.Agent9.InverseFibers.preimages (9 :: ss) p).length =
      P196.Agent9.InverseFibers.weight 9 p 0 *
          (P196.Agent9.InverseFibers.preimages ss 0).length +
      (P196.Agent9.InverseFibers.weight 9 p 1 *
          (P196.Agent9.InverseFibers.preimages ss 1).length +
      (P196.Agent9.InverseFibers.weight 9 p 2 *
          (P196.Agent9.InverseFibers.preimages ss 2).length +
      P196.Agent9.InverseFibers.weight 9 p 3 *
          (P196.Agent9.InverseFibers.preimages ss 3).length)) := by
  simp only [P196.Agent9.InverseFibers.preimages,
    P196.Agent9.InverseFibers.states, List.flatMap_cons, List.flatMap_nil,
    List.length_append, List.length_nil,
    P196.Agent9.InverseFibers.length_extend, Nat.add_zero]
  rfl

/-- The original scanner's four boundary-state counts are the counts of
the already proved complete folded inverse-path enumeration. -/
private theorem rawScanCount_eq_preimages (r : Nat) :
    ∀ p : P196.Agent9.InverseFibers.State,
      rawScanCount r (P196.Agent9.InverseFibers.low p)
        (P196.Agent9.InverseFibers.high p) =
      (P196.Agent9.InverseFibers.preimages (List.replicate r 9) p).length := by
  induction r with
  | zero => decide
  | succ r ih =>
    intro p
    have hstep := rawScanCount_step r
    have h0 := ih 0
    have h1 := ih 1
    have h2 := ih 2
    have h3 := ih 3
    have hp : p = 0 ∨ p = 1 ∨ p = 2 ∨ p = 3 := by
      have hv : p.val = 0 ∨ p.val = 1 ∨ p.val = 2 ∨ p.val = 3 := by omega
      rcases hv with hv | hv | hv | hv
      · exact Or.inl (Fin.ext hv)
      · exact Or.inr (Or.inl (Fin.ext hv))
      · exact Or.inr (Or.inr (Or.inl (Fin.ext hv)))
      · exact Or.inr (Or.inr (Or.inr (Fin.ext hv)))
    rcases hp with rfl | rfl | rfl | rfl
    all_goals
      simp only [P196.Agent9.InverseFibers.low,
        P196.Agent9.InverseFibers.high] at h0 h1 h2 h3 ⊢
      rw [List.replicate_succ, preimages_step_length]
      simp only [P196.Agent9.InverseFibers.weight_eq_table]
      simp [P196.Agent9.InverseFibers.table,
        show (9 : P196.Agent9.InverseFibers.Symbol).val = 9 from rfl,
        show (0 : P196.Agent9.InverseFibers.State).val = 0 from rfl,
        show (1 : P196.Agent9.InverseFibers.State).val = 1 from rfl,
        show (2 : P196.Agent9.InverseFibers.State).val = 2 from rfl,
        show (3 : P196.Agent9.InverseFibers.State).val = 3 from rfl]
          at h0 h1 h2 h3 ⊢
      omega

theorem rawAcceptedWords_zero : rawAcceptedWords 0 = [[]] := by
  rfl

/-- Exact all-parameter middle-word count, reusing the existing Fibonacci
theorem for the original folded inverse-path enumeration. -/
theorem rawAcceptedWords_length_succ (r : Nat) :
    (rawAcceptedWords (r + 1)).length =
      P196.Agent9.InverseFibers.fib r := by
  have hcount := rawScanCount_eq_preimages (r + 1) 0
  have hnines := (P196.Agent9.InverseFibers.nines_exact r).1
  rw [P196.Agent9.InverseFibers.preimages_length] at hcount
  change rawScanCount (r + 1) 0 0 =
    P196.Agent9.InverseFibers.inverseCount (List.replicate (r + 1) 9) at hcount
  calc
    (rawAcceptedWords (r + 1)).length = rawScanCount (r + 1) 0 0 := by
      exact List.countP_eq_length_filter.symm
    _ = P196.Agent9.InverseFibers.inverseCount (List.replicate (r + 1) 9) := hcount
    _ = P196.Agent9.InverseFibers.fib r := hnines

end P196.ResidualFivePredecessorCount

#print axioms P196.ResidualFivePredecessorCount.rawAcceptedWords_zero
#print axioms P196.ResidualFivePredecessorCount.rawAcceptedWords_length_succ
