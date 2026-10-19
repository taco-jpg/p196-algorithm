import P196.BoundaryOrdinaryStreams.Normalization
import P196.BoundaryOrdinaryStreams.Coherence

/-!
# Separate ordinary digit windows at the boundary phases

The protected bands determine both decimal ends separately. A zero final
carry consumes one extra high band digit; a final one supplies that digit
itself. The original low stream and the complete corrected high window then
identify the two ends, retaining the calculated carry as a separate output.
-/

namespace Agent5.BoundaryOrdinaryStreams

open P196.Agent7.Finite Agent115.ExteriorFactorization
open Agent5.ExactDigitStreams Agent5.BoundedStreamCandidates
open Agent5.CompleteExteriorFibers Agent5.OriginalStreamSuccessor
open Agent5.OrdinaryExteriorHistories Agent5.OrdinaryStreamWindow

private theorem digit_bands_ends (L M R : List Nat) (t e gap q : Nat)
    (he : e ≤ 1) (hlen : L.length = R.length + 1) (hq : q ≤ gap + e) :
    (L ++ List.replicate (gap + 1) t ++ M ++
      List.replicate (gap + 1) t ++ R ++ Agent109.carryWord e).take
        (R.length + 1 + q) = L ++ List.replicate q t ∧
    (L ++ List.replicate (gap + 1) t ++ M ++
      List.replicate (gap + 1) t ++ R ++ Agent109.carryWord e).reverse.take
        (R.length + 1 + q) =
      (if e == 0 then R.reverse ++ [t] else [1] ++ R.reverse) ++
        List.replicate q t := by
  constructor
  · rw [← hlen]
    simpa only [List.append_assoc] using
      take_prefix_replicate L
        (M ++ List.replicate (gap + 1) t ++ R ++ Agent109.carryWord e)
        t (gap + 1) q (by omega)
  · have hecases : e = 0 ∨ e = 1 := by omega
    rcases hecases with rfl | rfl
    · have htake := take_prefix_replicate R.reverse
        (M.reverse ++ List.replicate (gap + 1) t ++ L.reverse)
        t (gap + 1) (q + 1) (by omega)
      have htail : List.replicate (q + 1) t = t :: List.replicate q t := by
        rw [List.replicate_succ]
      rw [htail] at htake
      simpa only [Agent109.carryWord, beq_self_eq_true, if_true,
        List.append_nil, List.reverse_append, List.reverse_replicate,
        List.length_reverse, List.append_assoc, List.singleton_append,
        Nat.add_assoc, Nat.add_comm, Nat.add_left_comm] using htake
    · have htake := take_prefix_replicate (1 :: R.reverse)
        (M.reverse ++ List.replicate (gap + 1) t ++ L.reverse)
        t (gap + 1) q (by omega)
      simpa only [Agent109.carryWord, show (1 : Nat) ≠ 0 by decide,
        show (1 == 0) = false by decide, if_false, List.reverse_append,
        List.reverse_replicate, List.reverse_cons, List.reverse_nil,
        List.nil_append, List.length_cons, List.length_reverse,
        List.cons_append, List.append_assoc, List.singleton_append] using htake

/-- A protected ordinary transition has the exact original low window,
the complete corrected high window, and the original calculated carry.
The common extension is `q ≤ gap + actualCarry`, including both carry cases. -/
theorem ordinary_boundary_window (n c gap q : Nat) (B W : List Nat)
    (hc : c = 0 ∨ c = 18)
    (hB : Agent109.Bounded B) (hW : Agent109.Bounded W)
    (hrep : Agent109.pairWord n = P196.Agent6.surrounded B c gap W)
    (hq : q ≤ gap + actualCarry ⟨c, B⟩) :
    let K := B.length + 1 + q
    ordinaryObservation K n 0 =
      (actualCarry ⟨c, B⟩, originalLow K ⟨c, B⟩,
        correctedHigh c K (originalHigh K ⟨c, B⟩)) := by
  let k := Agent109.kOf c
  let t := Agent109.tOf c
  let L := (Agent109.norm B 0).1 ++
    [c + (Agent109.norm B 0).2 - 10 * k]
  let M := (Agent109.norm W k).1 ++
    [c + (Agent109.norm W k).2 - 10 * k]
  let R := (Agent109.norm B.reverse k).1
  let gamma := (Agent109.norm B.reverse k).2
  have hnorm : Agent109.norm (P196.Agent6.surrounded B c gap W) 0 =
      (L ++ List.replicate (gap + 1) t ++ M ++
        List.replicate (gap + 1) t ++ R, gamma) := by
    simpa only [L, M, R, gamma, k, t, List.append_assoc] using
      boundary_surrounded_normalization c gap B W hc hB hW
  have hdigits : Agent109.digits (Lychrel196.step n) =
      L ++ List.replicate (gap + 1) t ++ M ++
        List.replicate (gap + 1) t ++ R ++ Agent109.carryWord gamma := by
    rw [digits_step_eq_normalize n, Agent109.normalize_eq_norm, hrep, hnorm]
  have hactual : actualCarry ⟨c, B⟩ = gamma := by
    simp only [actualCarry, Agent109.Outer.normalize7_eq, gamma, k, Agent109.kOf]
  have hcarry : (Agent109.norm (Agent109.pairWord n) 0).2 =
      actualCarry ⟨c, B⟩ := by
    rw [hrep, hnorm]
    exact hactual.symm
  have hgamma : gamma ≤ 1 :=
    Agent109.norm_carry_le B.reverse k (Agent109.bounded_reverse B hB)
      (Agent109.Outer.k_le c)
  have hlength : L.length = R.length + 1 := by
    simp only [L, R, List.length_append, List.length_singleton,
      Agent109.norm_length, List.length_reverse]
  have hq' : q ≤ gap + gamma := by simpa only [hactual] using hq
  have hends := digit_bands_ends L M R t gamma gap q hgamma hlength hq'
  have hcTen : c ∈ [0, 2, 4, 6, 8, 10, 12, 14, 16, 18] := by
    rcases hc with rfl | rfl <;> decide
  have hlow : originalLow (B.length + 1 + q) ⟨c, B⟩ =
      L ++ List.replicate q t := by
    simpa only [originalLow, Agent109.Outer.normalize7_eq, L, k, t,
      Agent109.kOf, Agent109.tOf] using low_prefix_even_phase c B q hcTen hB
  have hhigh : correctedHigh c (B.length + 1 + q)
      (originalHigh (B.length + 1 + q) ⟨c, B⟩) =
      (if gamma == 0 then R.reverse ++ [t] else [1] ++ R.reverse) ++
        List.replicate q t := by
    simpa only [Agent109.Outer.normalize7_eq, R, gamma, k, t,
      Agent109.kOf, Agent109.tOf] using boundary_high_reconstruction c q B hc hB
  have hleft : (Agent109.digits (Lychrel196.step n)).take
      (B.length + 1 + q) = originalLow (B.length + 1 + q) ⟨c, B⟩ := by
    rw [hdigits, hlow]
    simpa only [R, Agent109.norm_length, List.length_reverse] using hends.1
  have hright : (Agent109.digits (Lychrel196.step n)).reverse.take
      (B.length + 1 + q) = correctedHigh c (B.length + 1 + q)
        (originalHigh (B.length + 1 + q) ⟨c, B⟩) := by
    rw [hdigits, hhigh]
    simpa only [R, Agent109.norm_length, List.length_reverse] using hends.2
  change ((Agent109.norm (Agent109.pairWord n) 0).2,
      (Agent109.digits (Lychrel196.step n)).take (B.length + 1 + q),
      (Agent109.digits (Lychrel196.step n)).reverse.take (B.length + 1 + q)) = _
  exact Prod.ext hcarry (Prod.ext hleft hright)

/-- Every requested cutoff inside the protected gap agrees with the
coherent observation, even when it is shorter than the exterior itself. -/
theorem ordinary_boundary_observation (n c cut gap : Nat) (B W : List Nat)
    (hc : c = 0 ∨ c = 18)
    (hB : Agent109.Bounded B) (hW : Agent109.Bounded W)
    (hrep : Agent109.pairWord n = P196.Agent6.surrounded B c gap W)
    (hgap : cut ≤ gap) :
    ordinaryObservation cut n 0 = coherentObservation cut ⟨c, B⟩ := by
  have hwindow := ordinary_boundary_window n c gap cut B W hc hB hW hrep
    (by omega : cut ≤ gap + actualCarry ⟨c, B⟩)
  have htake := congrArg (fun p : Nat × List Nat × List Nat =>
    (p.1, p.2.1.take cut, p.2.2.take cut)) hwindow
  have hcut : cut ≤ B.length + 1 + cut := by omega
  have hlow : (originalLow (B.length + 1 + cut) ⟨c, B⟩).take cut =
      originalLow cut ⟨c, B⟩ := by
    simpa only [originalLow, Nat.add_assoc, Nat.add_comm, Nat.add_left_comm] using
      adicNumeratorDigits_prefix cut (B.length + 1) (zValue c B - (c : Int))
  have hhigh := complete_high_window_take c cut cut B hc hB hcut
  simpa only [ordinaryObservation, coherentObservation, List.take_take,
    Nat.min_eq_left hcut, hlow, hhigh] using htake

#print axioms ordinary_boundary_window
#print axioms ordinary_boundary_observation

end Agent5.BoundaryOrdinaryStreams
