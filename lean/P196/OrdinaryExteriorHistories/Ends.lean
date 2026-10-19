import P196.OrdinaryExteriorHistories.Numeric

/-!
# Separate ordinary digit ends from a protected exterior

The existing full template normalization supplies its actual terminal carry
and its two normalized exterior blocks. Taking a prefix inside those blocks
identifies the low and high digits separately through the existing literal
stream interfaces.

For an arbitrary requested cutoff, phase letters are first absorbed into the
specified exterior using the existing template identity. Phase padding leaves
both original streams and their actual high carry unchanged. This gives the
one-step observation interface without reconstructing a paired sum or proving
a second whole-word normalization formula.
-/

namespace Agent5.OrdinaryExteriorHistories

open P196.Agent7.Finite Agent115.ExteriorFactorization
open Agent5.ExactDigitStreams Agent5.TrimmedStreamObservation
open Agent5.UniversalPhasePrefixes Agent5.FiniteExteriorHistories

private theorem normalized_template_observation_of_cut_le
    (c cut : Nat) (B I C : List Nat) (g h : Nat)
    (hc : nonneutralPhase c)
    (hB : Agent109.Bounded B) (hI : Agent109.Bounded I)
    (hC : Agent109.Bounded C) (hcut : cut ≤ B.length) :
    ((Agent109.norm (Agent109.template c B I C (g + 1) (h + 1)) 0).2,
      (Agent109.normalize
        (Agent109.template c B I C (g + 1) (h + 1)) 0).take cut,
      (Agent109.normalize
        (Agent109.template c B I C (g + 1) (h + 1)) 0).reverse.take cut) =
      observation cut { c := c, B := B } := by
  let R := (Agent109.norm B.reverse (Agent109.kOf c)).1
  let gamma := (Agent109.norm B.reverse (Agent109.kOf c)).2
  let M :=
    (Agent109.u0 c B I C :: List.replicate g (Agent109.tOf c)) ++
      (Agent109.data c B I C).DA ++
      (Agent109.u1 c B I C :: List.replicate h (Agent109.tOf (18 - c))) ++
      (Agent109.data c B I C).DC ++
      (Agent109.u2 c B I C :: List.replicate h (Agent109.tOf (18 - c))) ++
      (Agent109.data c B I C).DRA ++
      (Agent109.u3 c B I C :: List.replicate g (Agent109.tOf c))
  have hshape :
      Agent109.normalize (Agent109.template c B I C (g + 1) (h + 1)) 0 =
        (Agent109.norm B 0).1 ++ M ++ R ++ Agent109.carryWord gamma := by
    rw [Agent109.normalize_template c B I C g h
      (phase_of_nonneutral c hc) hB hI hC]
    simp only [Agent109.digitWord, Agent109.data, M, R, gamma,
      List.append_assoc]
  have hcarry :
      (Agent109.norm (Agent109.template c B I C (g + 1) (h + 1)) 0).2 =
        (normalize B.reverse (if 10 ≤ c then 1 else 0)).2 := by
    rw [Agent109.norm_template c B I C g h
      (phase_of_nonneutral c hc) hB hI hC]
    simp only [Agent109.data, Agent109.Outer.normalize7_eq, Agent109.kOf]
  have hlo :
      (Agent109.normalize
        (Agent109.template c B I C (g + 1) (h + 1)) 0).take cut =
        (normalize B 0).1.take cut := by
    rw [hshape]
    have htake :
        ((Agent109.norm B 0).1 ++ (M ++ R ++ Agent109.carryWord gamma)).take cut =
          (Agent109.norm B 0).1.take cut :=
      List.take_append_of_le_length (by
        simpa only [Agent109.norm_length] using hcut)
    simpa only [List.append_assoc, Agent109.Outer.normalize7_eq] using htake
  have hR : R.length = B.length := by
    simp only [R, Agent109.norm_length, List.length_reverse]
  have hhi :
      (Agent109.normalize
        (Agent109.template c B I C (g + 1) (h + 1)) 0).reverse.take cut =
        ((Agent109.carryWord gamma).reverse ++ R.reverse).take cut := by
    rw [hshape]
    have hlen : cut ≤ ((Agent109.carryWord gamma).reverse ++ R.reverse).length := by
      simp only [List.length_append, List.length_reverse, hR]
      omega
    have htake :
        (((Agent109.carryWord gamma).reverse ++ R.reverse) ++
          (M.reverse ++ (Agent109.norm B 0).1.reverse)).take cut =
            ((Agent109.carryWord gamma).reverse ++ R.reverse).take cut :=
      List.take_append_of_le_length hlen
    simpa only [List.reverse_append, List.append_assoc] using htake
  have hlow_stream :
      (normalize B 0).1.take cut =
        adicNumeratorDigits cut (zValue c B - (c : Int)) := by
    rw [← low_prefix_normalized c B]
    have hp := adicNumeratorDigits_prefix cut (B.length - cut)
      (zValue c B - (c : Int))
    rw [Nat.add_sub_of_le hcut] at hp
    exact hp
  have hgamma : gamma ≤ 1 := Agent109.gamma_le c B I C hB
  have hfront :
      (Agent109.carryWord gamma).reverse ++ R.reverse =
        if (normalize B.reverse (if 10 ≤ c then 1 else 0)).2 == 0 then
          (normalize B.reverse (if 10 ≤ c then 1 else 0)).1.reverse
        else [1] ++ (normalize B.reverse (if 10 ≤ c then 1 else 0)).1.reverse := by
    rw [Agent109.Outer.normalize7_eq]
    change (Agent109.carryWord gamma).reverse ++ R.reverse =
      if gamma == 0 then R.reverse else [1] ++ R.reverse
    by_cases hz : gamma = 0
    · simp [hz, Agent109.carryWord]
    · have hone : gamma = 1 := by omega
      simp [hone, Agent109.carryWord]
  rw [hfront] at hhi
  have hhigh_stream := high_prefix_normalized c cut B hc hB hcut
  apply Prod.ext
  · exact hcarry
  · apply Prod.ext
    · exact hlo.trans hlow_stream
    · exact hhi.trans hhigh_stream.symm

/-- A sufficiently long actual complementary template has the prescribed
terminal carry and the two separate digit prefixes after one ordinary step.
Both digit lists are taken from the canonical digits of the actual successor.
The exterior observations keep their original numerators, widths, and actual
carry-dependent high denominators. -/
theorem ordinary_step_observation_of_template
    (n c cut : Nat) (B I C : List Nat) (g h : Nat)
    (hc : nonneutralPhase c)
    (hB : Agent109.Bounded B) (hI : Agent109.Bounded I)
    (hC : Agent109.Bounded C)
    (hrep : Agent109.pairWord n = Agent109.template c B I C g h)
    (hg : cut + 2 ≤ g) (hh : cut + 2 ≤ h) :
    ordinaryObservation cut n 0 = observation cut { c := c, B := B } := by
  let P := B ++ List.replicate cut c
  have hP : Agent109.Bounded P := by
    intro x hx
    rcases List.mem_append.mp hx with hx | hx
    · exact hB x hx
    · have hxc : x = c := List.eq_of_mem_replicate hx
      rw [hxc]
      have hc17 := (phase_of_nonneutral c hc).2.1
      omega
  obtain ⟨g', hg'⟩ : ∃ g', g = (g' + 1) + cut :=
    ⟨g - cut - 1, by omega⟩
  obtain ⟨h', hh'⟩ : ∃ h', h = h' + 1 := ⟨h - 1, by omega⟩
  have htrim :
      Agent109.template c P I C (g' + 1) (h' + 1) =
        Agent109.template c B I C g h := by
    have ht := Agent109.Cert.template_trim c B I C cut 0 0 0 (g' + 1) (h' + 1)
    simpa only [P, List.replicate_zero, List.nil_append, List.append_nil,
      Nat.add_zero, ← hg', ← hh'] using ht
  have hwhole :
      Agent109.pairWord n = Agent109.template c P I C (g' + 1) (h' + 1) :=
    hrep.trans htrim.symm
  have hn : ordinaryObservation cut n 0 =
      ((Agent109.norm (Agent109.template c P I C (g' + 1) (h' + 1)) 0).2,
        (Agent109.normalize
          (Agent109.template c P I C (g' + 1) (h' + 1)) 0).take cut,
        (Agent109.normalize
          (Agent109.template c P I C (g' + 1) (h' + 1)) 0).reverse.take cut) := by
    simp only [ordinaryObservation, Lychrel196.orbit,
      digits_step_eq_normalize, hwhole]
  have hcutP : cut ≤ P.length := by
    simp only [P, List.length_append, List.length_replicate]
    omega
  have hnormalized := normalized_template_observation_of_cut_le
    c cut P I C g' h' hc hP hI hC hcutP
  have hpadding : observation cut { c := c, B := P } =
      observation cut { c := c, B := B } := by
    apply Prod.ext
    · exact phase_padding_carry c B cut hc
    · apply Prod.ext
      · exact phase_padding_low c cut B cut
      · exact phase_padding_high c cut B cut hc
  exact hn.trans (hnormalized.trans hpadding)

#print axioms ordinary_step_observation_of_template

end Agent5.OrdinaryExteriorHistories
