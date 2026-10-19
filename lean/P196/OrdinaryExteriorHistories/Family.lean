import P196.OrdinaryExteriorHistories.History
import P196.OrdinaryExteriorHistories.Width

/-!
# Ordinary realizations of simultaneous all-phase finite histories

First choose one exterior word that works at all eight nonneutral phases.
Then realize each phase's template by a positive ordinary integer. The
initial widths agree because the exterior and band lengths are common.
The seeds differ because the first phase-band coefficient differs.

All observations come from the accepted integer orbits. Each seed depends
on the prescribed finite cutoff and horizon. No single seed realizing an
infinite exterior history or any palindrome-avoidance assertion is supplied.
-/

namespace Agent5.OrdinaryExteriorHistories

open P196.Agent7.Finite Agent115.ExteriorFactorization
open Agent5.FiniteExteriorHistories Agent6.ExteriorCoordinates

private theorem head_pos_of_valid (c : Nat) (B : List Nat)
    (hv : validOuter { c := c, B := B } = true) :
    ∀ b, B.head? = some b → 0 < b := by
  intro b hb
  cases B with
  | nil => simp at hb
  | cons a tail =>
      have hba : a = b := by simpa using hb
      simp only [validOuter, Bool.and_eq_true, decide_eq_true_eq] at hv
      simpa only [hba] using hv.1.2

/-- Every valid exterior target has one arbitrarily wide canonical word
whose realizations at all eight initial phases reproduce its prescribed
finite history. The positive ordinary seeds have a common initial width. -/
theorem arbitrarily_wide_all_phase_ordinary_history
    (c cut T W : Nat) (B : List Nat)
    (hc : nonneutralPhase c)
    (hv : validOuter { c := c, B := B } = true) :
    let g := 2 * T + cut + 2
    ∃ A : List Nat,
      max B.length W < A.length ∧
      ∀ d, nonneutralPhase d →
        validOuter { c := d, B := A } = true ∧
        stripSuffix d A = A ∧
        ∃ n, 0 < n ∧
          (Agent109.digits n).length = 2 * A.length + 4 * g ∧
          Agent109.pairWord n = Agent109.template d A [] [] g g ∧
          ∀ t, t ≤ T →
            ordinaryObservation cut n t =
              observation cut (outerIter t { c := c, B := B }) := by
  dsimp only
  obtain ⟨A, hwidth, hA⟩ :=
    arbitrarily_wide_all_phase_same_history c cut T W B hc hv
  refine ⟨A, hwidth, ?_⟩
  intro d hd
  obtain ⟨hvA, hcanonical, hhistory⟩ := hA d hd
  have hbound : Agent109.Bounded A := entries_le_of_valid d A hvA
  obtain ⟨n, hnpos, hlen, hrep⟩ := positive_template_realized d A
    (2 * T + cut + 2) (phase_of_nonneutral d hd) (by omega) hbound
    (head_pos_of_valid d A hvA)
  refine ⟨hvA, hcanonical, n, hnpos, hlen, hrep, ?_⟩
  have hordinary := ordinary_history_of_template n d cut T A [] []
    (2 * T + cut + 2) (2 * T + cut + 2) hd hbound
    (by simp [Agent109.Bounded]) (by simp [Agent109.Bounded]) hrep
    (Nat.le_refl _) (Nat.le_refl _)
  intro t ht
  apply (hordinary t ht).trans
  have hobs := hhistory t ht
  exact Prod.ext hobs.1 (Prod.ext hobs.2.1 hobs.2.2)

/-- Eight distinct positive ordinary seeds, indexed by the eight phases,
realize the same finite target history with a common initial exterior.
Their full decimal widths agree through time `T + 1`, since every recorded
terminal carry agrees as well as both digit ends. -/
theorem eight_phase_ordinary_family
    (c cut T W : Nat) (B : List Nat)
    (hc : nonneutralPhase c)
    (hv : validOuter { c := c, B := B } = true) :
    let g := 2 * T + cut + 2
    ∃ A : List Nat, ∃ seed : Fin 8 → Nat,
      max B.length W < A.length ∧
      (∀ i j, seed i = seed j → i = j) ∧
      (∀ i,
        validOuter { c := 2 * (i.val + 1), B := A } = true ∧
        stripSuffix (2 * (i.val + 1)) A = A ∧
        0 < seed i ∧
        (Agent109.digits (seed i)).length = 2 * A.length + 4 * g ∧
        Agent109.pairWord (seed i) =
          Agent109.template (2 * (i.val + 1)) A [] [] g g ∧
        ∀ t, t ≤ T →
          ordinaryObservation cut (seed i) t =
            observation cut (outerIter t { c := c, B := B })) ∧
      ∀ i j t, t ≤ T + 1 →
        (Agent109.digits (Lychrel196.orbit (seed i) t)).length =
          (Agent109.digits (Lychrel196.orbit (seed j) t)).length := by
  classical
  dsimp only
  obtain ⟨A, hwidth, hA⟩ :=
    arbitrarily_wide_all_phase_ordinary_history c cut T W B hc hv
  have hphase (i : Fin 8) : nonneutralPhase (2 * (i.val + 1)) := by
    have hi := i.isLt
    simp [nonneutralPhase]
    omega
  let witnesses := fun i : Fin 8 => (hA (2 * (i.val + 1)) (hphase i)).2.2
  let seed : Fin 8 → Nat := fun i => Classical.choose (witnesses i)
  have hseed (i : Fin 8) := Classical.choose_spec (witnesses i)
  refine ⟨A, seed, hwidth, ?_, ?_, ?_⟩
  · intro i j hij
    have hphaseeq : 2 * (i.val + 1) = 2 * (j.val + 1) :=
      template_phase_injective _ _ A _ _ (by omega)
        ((hseed i).2.2.1.symm.trans
          ((congrArg Agent109.pairWord hij).trans (hseed j).2.2.1))
    apply Fin.ext
    omega
  · intro i
    exact ⟨(hA _ (hphase i)).1, (hA _ (hphase i)).2.1, hseed i⟩
  · intro i j
    apply digit_widths_of_same_history cut T (seed i) (seed j)
      ((hseed i).2.1.trans (hseed j).2.1.symm)
    intro t ht
    exact ((hseed i).2.2.2 t ht).trans ((hseed j).2.2.2 t ht).symm

#print axioms arbitrarily_wide_all_phase_ordinary_history
#print axioms eight_phase_ordinary_family

end Agent5.OrdinaryExteriorHistories
