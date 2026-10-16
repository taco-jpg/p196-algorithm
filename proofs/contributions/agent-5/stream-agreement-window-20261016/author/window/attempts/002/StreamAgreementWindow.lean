import OrdinaryStreamStep

/-!
Agent #5: the finite agreement window between an ordinary reverse-and-add
pair word and the two literal exterior coordinate streams.

The full normalization formula exposes `gap + 1` stable digits at each end.
The high prefix consumes one of these exactly when the outgoing carry is zero,
so the common guaranteed extension has length `gap + outgoingCarry`.
-/

namespace Agent5.OrdinaryStreamWindow

open P196.Agent6 Agent115.ExteriorFactorization Agent5.ExactDigitStreams
open Agent5.OrdinaryStreamPrefix

/-- A prefix followed by a sufficiently long constant band determines the
requested extended prefix independently of the remaining word. -/
theorem take_prefix_replicate (L M : List Nat) (t m q : Nat) (hq : q ≤ m) :
    (L ++ List.replicate m t ++ M).take (L.length + q) =
      L ++ List.replicate q t := by
  rw [List.append_assoc, List.take_append,
    List.take_append_of_le_length (by simpa using hq),
    List.take_replicate, Nat.min_eq_left hq]

/-- Two constant bands protect the paired prefix through the exact common
extension allowed by the possible final carry digit. -/
theorem paired_bands_window (L M R : List Nat) (t e gap q : Nat)
    (he : e ≤ 1) (hlen : L.length = R.length + 1) (hq : q ≤ gap + e) :
    (paired (L ++ List.replicate (gap + 1) t ++ M ++
      List.replicate (gap + 1) t ++ R ++ carryEnd e)).take
        (R.length + 1 + q) =
      List.zipWith Nat.add (L ++ List.replicate q t)
        ((if e == 0 then R.reverse ++ [t] else 1 :: R.reverse) ++
          List.replicate q t) := by
  have hlo :
      (L ++ List.replicate (gap + 1) t ++ M ++
        List.replicate (gap + 1) t ++ R ++ carryEnd e).take
          (R.length + 1 + q) = L ++ List.replicate q t := by
    rw [← hlen]
    simpa only [List.append_assoc] using
      take_prefix_replicate L
        (M ++ List.replicate (gap + 1) t ++ R ++ carryEnd e)
        t (gap + 1) q (by omega)
  have hhi :
      (L ++ List.replicate (gap + 1) t ++ M ++
        List.replicate (gap + 1) t ++ R ++ carryEnd e).reverse.take
          (R.length + 1 + q) =
        (if e == 0 then R.reverse ++ [t] else 1 :: R.reverse) ++
          List.replicate q t := by
    have hcases : e = 0 ∨ e = 1 := by omega
    rcases hcases with rfl | rfl
    · have htake := take_prefix_replicate R.reverse
        (M.reverse ++ List.replicate (gap + 1) t ++ L.reverse)
        t (gap + 1) (q + 1) (by omega)
      have htail : List.replicate (q + 1) t = t :: List.replicate q t := by
        rw [List.replicate_succ]
      rw [htail] at htake
      simpa only [carryEnd, beq_self_eq_true, if_true, List.append_nil,
        List.reverse_append, List.reverse_replicate, List.length_reverse,
        List.append_assoc, List.singleton_append,
        Nat.add_assoc, Nat.add_comm, Nat.add_left_comm] using htake
    · have htake := take_prefix_replicate (1 :: R.reverse)
        (M.reverse ++ List.replicate (gap + 1) t ++ L.reverse)
        t (gap + 1) q (by omega)
      simpa only [carryEnd, show (1 == 0) = false by decide, if_false,
        List.reverse_append, List.reverse_replicate, List.reverse_cons,
        List.reverse_nil, List.nil_append, List.length_cons, List.length_reverse,
        List.cons_append, List.append_assoc, List.singleton_append] using htake
  simp only [paired, List.take_zipWith, hlo, hhi]

/-- Actual normalization exposes the stable extension of both raw digit ends.
The middle is arbitrary subject to the original coefficient bound. -/
theorem surrounded_raw_exterior_window (B W : List Nat) (c gap q : Nat)
    (hc : Nonneutral c) (hB : Coefficients B) (hW : Coefficients W)
    (hq : q ≤ gap + (norm B.reverse (carryPhase c)).2) :
    (paired (normalizedDigits (surrounded B c gap W))).take
      (B.length + 1 + q) =
      List.zipWith Nat.add (lowEnd B c ++ List.replicate q (digitPhase c))
        ((if (norm B.reverse (carryPhase c)).2 == 0
          then (norm B.reverse (carryPhase c)).1.reverse ++ [digitPhase c]
          else 1 :: (norm B.reverse (carryPhase c)).1.reverse) ++
            List.replicate q (digitPhase c)) := by
  have hBr : Coefficients B.reverse := by
    intro x hx
    exact hB x (by simpa using hx)
  have he := norm_carry_bit B.reverse (carryPhase c) hBr (carryPhase_bit c)
  have hlen : (lowEnd B c).length =
      (norm B.reverse (carryPhase c)).1.length + 1 := by
    simp [lowEnd, norm_length]
  have hwindow := paired_bands_window (lowEnd B c)
    ((norm W (carryPhase c)).1 ++
      [c + (norm W (carryPhase c)).2 - 10 * carryPhase c])
    (norm B.reverse (carryPhase c)).1 (digitPhase c)
    (norm B.reverse (carryPhase c)).2 gap q he hlen hq
  simpa only [normalizedDigits, surrounded_normalization B W c gap hc hB hW,
    lowEnd, carryEnd, norm_length, List.length_reverse, List.append_assoc]
      using hwindow

#print axioms take_prefix_replicate
#print axioms paired_bands_window
#print axioms surrounded_raw_exterior_window

end Agent5.OrdinaryStreamWindow
