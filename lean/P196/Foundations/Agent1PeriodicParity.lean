import P196.Foundations.Agent1PeriodicQuotient

/-!
Literal indexed middle-coefficient parity for the original Agent8 pair map
and for the existing mirrored complete-block stripping operation.

The general fact that a paired word has an even middle is already present
in Agent112.Admissibility.pair_mirr, using Agent109.Cert.Mirr. This module
supplies the small original-Agent8 indexed interface without importing the
certificate closure. No arithmetic operation or validity predicate is replaced.
-/

namespace Agent1.Periodic

open Agent8 Agent1.RepeatedBlock

/-- At odd width, the middle coefficient of the paired word is twice the
middle input coefficient. In particular its parity is even. -/
theorem pair_middle_even (D : Word) (hodd : D.length % 2 = 1) :
    (((pair D)[D.length / 2]?).getD 0) % 2 = 0 := by
  have hm : D.length / 2 + D.length / 2 + 1 = D.length := by omega
  have hr : D.reverse[D.length / 2]? = D[D.length / 2]? :=
    List.getElem?_reverse' hm
  rw [pair, zipAdd_eq_zipWith, List.getElem?_zipWith, hr]
  cases D[D.length / 2]? with
  | none => rfl
  | some x => simp only [Option.getD_some]; omega

/-- Equally wide exterior pieces leave an odd center's middle coefficient
at the middle of the complete word. No exterior symmetry is required. -/
theorem middle_append_eq (P H S : Word) (hPS : P.length = S.length)
    (hodd : H.length % 2 = 1) :
    (P ++ H ++ S)[(P ++ H ++ S).length / 2]? = H[H.length / 2]? := by
  have hm : (P ++ H ++ S).length / 2 = P.length + H.length / 2 := by
    simp only [List.length_append]
    omega
  have hinside : H.length / 2 < H.length := by omega
  rw [hm, List.append_assoc, List.getElem?_append_right (by omega),
    Nat.add_sub_cancel_left, List.getElem?_append_left hinside]

/-- Removing complete mirrored period pairs preserves the original odd
center coefficient, hence its evenness. Empty periods are included. -/
theorem stripPeriodCenter_even (w H : Word)
    (heven : H.length % 2 = 1 → ((H[H.length / 2]?).getD 0) % 2 = 0) :
    (stripPeriodCenter w H).1.length % 2 = 1 →
      ((((stripPeriodCenter w H).1)[(stripPeriodCenter w H).1.length / 2]?).getD 0)
        % 2 = 0 := by
  intro hodd
  have hlen := stripPeriodCenter_length w H
  have hHodd : H.length % 2 = 1 := by omega
  have hp : (pow w (stripPeriodCenter w H).2).length =
      (pow w.reverse (stripPeriodCenter w H).2).length := by
    simp only [pow_length, List.length_reverse]
  have hm := middle_append_eq (pow w (stripPeriodCenter w H).2)
    (stripPeriodCenter w H).1 (pow w.reverse (stripPeriodCenter w H).2) hp hodd
  have heq : H[H.length / 2]? =
      ((stripPeriodCenter w H).1)[(stripPeriodCenter w H).1.length / 2]? :=
    (congrArg (fun K : Word => K[K.length / 2]?)
      (stripPeriodCenter_decomposition w H)).trans hm
  exact (congrArg (fun o : Option Nat => o.getD 0 % 2) heq).symm.trans (heven hHodd)

/-- The literal raw center is paired, so its odd middle coefficient is even.
This does not need input-center symmetry, parity, or positive exterior. -/
theorem raw_center_even (B H w : Word)
    (hB : Bounded B 18) (hH : Bounded H 18) (hw : Bounded w 18)
    (hlen : w.length = 4) :
    (rawCenter B H w).length % 2 = 1 →
      (((rawCenter B H w)[(rawCenter B H w).length / 2]?).getD 0) % 2 = 0 := by
  have hm := (raw_blocks_eq_zipper B H w hB hH hw hlen).2.2
  unfold zipperCenter at hm
  intro hodd
  rw [hm, pair_length] at hodd ⊢
  exact pair_middle_even _ hodd

end Agent1.Periodic

#print axioms Agent1.Periodic.pair_middle_even
#print axioms Agent1.Periodic.middle_append_eq
#print axioms Agent1.Periodic.stripPeriodCenter_even
#print axioms Agent1.Periodic.raw_center_even
