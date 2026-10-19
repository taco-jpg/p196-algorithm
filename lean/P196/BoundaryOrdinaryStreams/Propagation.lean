import P196.BoundaryOrdinaryStreams.Normalization

/-!
# Ordinary propagation of boundary bands

The actual integer step is first normalized using the two surrounding
bands. The phase-free pairing theorem then places all dependence on the
middle word inside a new middle word. Removing a final run of the new
exterior phase only increases the protected gap. Consequently, a reserve
of two gap positions suffices for one ordinary transition.
-/

namespace Agent5.BoundaryOrdinaryStreams

open P196.Agent7.Finite (outerNext stripSuffix)

private theorem pair_two_bands (L M R : List Nat) (g t : Nat)
    (hlen : L.length = R.length) :
    Agent109.pair (L ++ List.replicate g t ++ M ++ List.replicate g t ++ R) =
      Agent109.zipAdd L R.reverse ++ List.replicate g (t + t) ++
        Agent109.pair M ++ List.replicate g (t + t) ++
        (Agent109.zipAdd L R.reverse).reverse := by
  simpa only [List.replicate_zero, List.nil_append, List.append_nil,
    Agent109.zipAdd, List.reverse_nil, List.append_assoc] using
    Agent109.pair_split L [] M [] R g 0 t 0 hlen rfl

private theorem boundary_stepWord_shape (c g : Nat) (B W : List Nat)
    (hc : c = 0 ∨ c = 18)
    (hB : Agent109.Bounded B) (hW : Agent109.Bounded W) :
    ∃ W', Agent109.stepWord (P196.Agent6.surrounded B c g W) =
      Agent109.Br c B [] [] ++
        List.replicate (g + (Agent109.norm B.reverse (Agent109.kOf c)).2) c ++
        W' ++
        List.replicate (g + (Agent109.norm B.reverse (Agent109.kOf c)).2) c ++
        (Agent109.Br c B [] []).reverse := by
  let k := Agent109.kOf c
  let t := Agent109.tOf c
  let L := (Agent109.norm B 0).1
  let R := (Agent109.norm B.reverse k).1
  let N := (Agent109.norm W k).1
  let u := c + (Agent109.norm B 0).2 - 10 * k
  let v := c + (Agent109.norm W k).2 - 10 * k
  let gamma := (Agent109.norm B.reverse k).2
  have hphase : t + t = c := by
    rcases hc with rfl | rfl <;> rfl
  have hL : L.length = B.length := Agent109.norm_length _ _
  have hR : R.length = B.length := by simp [R, Agent109.norm_length]
  have hgamma : gamma ≤ 1 :=
    Agent109.norm_carry_le _ _ (Agent109.bounded_reverse B hB)
      (Agent109.Outer.k_le c)
  have hn : Agent109.normalize (P196.Agent6.surrounded B c g W) 0 =
      L ++ [u] ++ List.replicate (g + 1) t ++ N ++ [v] ++
        List.replicate (g + 1) t ++ R ++ Agent109.carryWord gamma := by
    rw [Agent109.normalize_eq_norm,
      boundary_surrounded_normalization c g B W hc hB hW]
  change ∃ W', Agent109.pair
      (Agent109.normalize (P196.Agent6.surrounded B c g W) 0) =
    Agent109.Br c B [] [] ++ List.replicate (g + gamma) c ++ W' ++
      List.replicate (g + gamma) c ++ (Agent109.Br c B [] []).reverse
  rw [hn]
  rcases (by omega : gamma = 0 ∨ gamma = 1) with hg | hg
  · refine ⟨Agent109.pair ([t] ++ N ++ [v]), ?_⟩
    have hdigits :
        L ++ [u] ++ List.replicate (g + 1) t ++ N ++ [v] ++
          List.replicate (g + 1) t ++ R ++ Agent109.carryWord gamma =
        (L ++ [u]) ++ List.replicate g t ++ ([t] ++ N ++ [v]) ++
          List.replicate g t ++ ([t] ++ R) := by
      simp only [Agent109.carryWord, hg, ite_true, List.append_nil,
        List.replicate_succ', List.append_assoc, List.singleton_append,
        List.cons_append]
    have hBr : Agent109.Br c B [] [] =
        Agent109.zipAdd (L ++ [u]) (R.reverse ++ [t]) := by
      change (if gamma = 0 then
        Agent109.zipAdd (L ++ [u]) (R.reverse ++ [t]) else
        Agent109.zipAdd (L ++ [u]) ([1] ++ R.reverse)) = _
      rw [if_pos hg]
    rw [hdigits, pair_two_bands _ _ _ g t (by simp [hL, hR])]
    simp only [hphase, hg, Nat.add_zero, hBr, List.reverse_append,
      List.reverse_cons, List.reverse_nil, List.nil_append, List.append_assoc]
  · refine ⟨Agent109.pair (N ++ [v]), ?_⟩
    have hdigits :
        L ++ [u] ++ List.replicate (g + 1) t ++ N ++ [v] ++
          List.replicate (g + 1) t ++ R ++ Agent109.carryWord gamma =
        (L ++ [u]) ++ List.replicate (g + 1) t ++ (N ++ [v]) ++
          List.replicate (g + 1) t ++ (R ++ [1]) := by
      simp [Agent109.carryWord, hg, List.append_assoc]
    have hBr : Agent109.Br c B [] [] =
        Agent109.zipAdd (L ++ [u]) ([1] ++ R.reverse) := by
      change (if gamma = 0 then
        Agent109.zipAdd (L ++ [u]) (R.reverse ++ [t]) else
        Agent109.zipAdd (L ++ [u]) ([1] ++ R.reverse)) = _
      simp only [hg, Nat.one_ne_zero, ite_false]
    rw [hdigits, pair_two_bands _ _ _ (g + 1) t (by simp [hL, hR])]
    simp only [hphase, hg, hBr, List.reverse_append,
      List.reverse_cons, List.reverse_nil, List.nil_append, List.append_assoc]

/-- One actual ordinary step follows the prescribed exterior map at phase
zero or eighteen. A gap reserve of two leaves at least the requested gap;
the returned exterior and the new middle remain coefficient-bounded. -/
theorem boundary_pairWord_propagation (n c g : Nat) (B W : List Nat)
    (hc : c = 0 ∨ c = 18)
    (hB : Agent109.Bounded B) (hW : Agent109.Bounded W)
    (hrep : Agent109.pairWord n = P196.Agent6.surrounded B c (g + 2) W) :
    ∃ g' W', g ≤ g' ∧ Agent109.Bounded W' ∧
      Agent109.Bounded (outerNext ⟨c, B⟩).B ∧
      Agent109.pairWord (Lychrel196.step n) =
        P196.Agent6.surrounded (outerNext ⟨c, B⟩).B
          (outerNext ⟨c, B⟩).c g' W' := by
  let gamma := (Agent109.norm B.reverse (Agent109.kOf c)).2
  obtain ⟨W', hraw⟩ := boundary_stepWord_shape c (g + 2) B W hc hB hW
  have hstep : Agent109.pairWord (Lychrel196.step n) =
      Agent109.Br c B [] [] ++ List.replicate (g + 2 + gamma) c ++ W' ++
        List.replicate (g + 2 + gamma) c ++ (Agent109.Br c B [] []).reverse := by
    rw [Agent109.Compat.step_eq, Agent109.pairWord_step, hrep]
    exact hraw
  have hphase : Agent109.tOf c + Agent109.tOf c = c := by
    rcases hc with rfl | rfl <;> rfl
  have hnext := Agent109.Outer.outerNext_eq c B [] []
  rw [hphase] at hnext
  obtain ⟨j, hj⟩ := Agent109.Outer.stripSuffix_spec c (Agent109.Br c B [] [])
  have htrim :
      Agent109.Br c B [] [] ++ List.replicate (g + 2 + gamma) c ++ W' ++
        List.replicate (g + 2 + gamma) c ++ (Agent109.Br c B [] []).reverse =
      P196.Agent6.surrounded (stripSuffix c (Agent109.Br c B [] [])) c
        (g + gamma + j) W' := by
    have ht := Agent109.Cert.template_trim c
      (stripSuffix c (Agent109.Br c B [] [])) [] W' j 0 0 0
      (g + 2 + gamma) 0
    simp only [List.replicate_zero, List.nil_append, List.append_nil,
      Nat.add_zero] at ht
    rw [← hj] at ht
    simpa [Agent109.template, P196.Agent6.surrounded, List.append_assoc,
      Nat.add_assoc, Nat.add_comm, Nat.add_left_comm] using ht
  have hshape : Agent109.pairWord (Lychrel196.step n) =
      P196.Agent6.surrounded (outerNext ⟨c, B⟩).B
        (outerNext ⟨c, B⟩).c (g + gamma + j) W' := by
    rw [hnext]
    exact hstep.trans htrim
  have hbounded := Agent109.bounded_pair_digits (Lychrel196.step n)
  refine ⟨g + gamma + j, W', by omega, ?_, ?_, hshape⟩
  · intro x hx
    apply hbounded x
    rw [hshape]
    simp [P196.Agent6.surrounded, hx]
  · intro x hx
    apply hbounded x
    rw [hshape]
    simp [P196.Agent6.surrounded, hx]

#print axioms boundary_pairWord_propagation

end Agent5.BoundaryOrdinaryStreams
