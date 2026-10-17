import P196.Agent1PeriodicGuardedPath.Agent1PeriodicGuardedPath
import P196.Agent1PeriodicReturnClock.Agent1PeriodicReturnClock
import P196.Agent1PeriodicEighteenReturn.RunAncestry

/-!
Finite ancestry of one supplied maximal eighteen run along an exact guarded
quotient path. The original RunAncestry.descendant_step supplies successor
maximality. A fixed interior anchor prevents this selected run from becoming
empty during the finite horizon. No run population or birth classification
is asserted.
-/

namespace Agent1.Periodic
open Agent8

/-- Follow only the original descendant of the supplied initial run. -/
def quotientEighteenTrack (B H w : Nat → Word) (k : Nat → Nat)
    (a0 b0 : Nat) : Nat → Nat × Nat
  | 0 => (a0, b0)
  | t+1 =>
      let W := quotientPathWord B H w k t
      let p := quotientEighteenTrack B H w k a0 b0 t
      RunAncestry.descendant (fun j => (W[j]?).getD 0) W.length 18 p.1 p.2

private theorem eighteen_descendant_endpoint_bounds (q : Nat → Nat)
    (L a b : Nat) (ha : FoldedDecimal.Admissible L q) :
    (RunAncestry.descendant q L 18 a b).1 ≤ a+1 ∧
      b ≤ (RunAncestry.descendant q L 18 a b).2+1 ∧
      a + DecimalDigits.carry q L ≤ (RunAncestry.descendant q L 18 a b).1 := by
  have hc := RunAncestry.carry_le_one q L ha L (Nat.le_refl L)
  by_cases h0 : DecimalDigits.carry q L = 0
  · by_cases hleft : DecimalDigits.carry q a = RunAncestry.reset 18
    <;> by_cases hright : DecimalDigits.carry q (L-b) = RunAncestry.reset 18
    <;> simp only [RunAncestry.descendant, h0, if_pos, hleft, hright,
      if_false, Prod.fst, Prod.snd]
    <;> omega
  · simp only [RunAncestry.descendant, h0, if_false, Prod.fst, Prod.snd]
    omega

/-- Only in-range equality is used: the indexed successor may differ from
list getD outside the new width. -/
private theorem eighteen_run_stepWord (W : Word) (a b : Nat)
    (hr : RunAncestry.MaximalRun
      (FoldedDecimal.nextColumns (fun j => (W[j]?).getD 0) W.length)
      (FoldedDecimal.nextWidth (fun j => (W[j]?).getD 0) W.length) 18 a b) :
    RunAncestry.MaximalRun (fun j => ((stepWord W)[j]?).getD 0)
      (stepWord W).length 18 a b := by
  rw [← stepWord_length_nextWidth W] at hr
  obtain ⟨hab, hbL, hrun, hleft, hright⟩ := hr
  refine ⟨hab, hbL, ?_, ?_, ?_⟩
  · intro i hai hib
    change ((stepWord W)[i]?).getD 0 = 18
    rw [stepWord_getD_nextColumns W i (by omega)]
    exact hrun i hai hib
  · rcases hleft with hzero | hne
    · exact Or.inl hzero
    · right
      change ((stepWord W)[a-1]?).getD 0 ≠ 18
      rw [stepWord_getD_nextColumns W (a-1) (by omega)]
      exact hne
  · rcases hright with hend | hne
    · exact Or.inl hend
    · by_cases hend : b = (stepWord W).length
      · exact Or.inl hend
      · right
        change ((stepWord W)[b]?).getD 0 ≠ 18
        rw [stepWord_getD_nextColumns W b (by omega)]
        exact hne

/-- One initially supplied maximal eighteen run stays maximal through the
finite horizon when the same fixed anchor has N positions of room on each
side. C records actual indexed overflow, not an independently chosen label.
No assumption is made that intermediate periodic phases are eighteen. -/
theorem quotient_eighteen_track (B H w : Nat → Word) (k C : Nat → Nat)
    (N a0 b0 I : Nat) (hp : QuotientPath B H w N)
    (hv : ValidPeriodic (B 0) (H 0) (w 0))
    (hguard : ∀ t, t < N → 3 ≤ k t)
    (hkstep : ∀ t, t < N → k (t+1) = (k t-2) +
      outerPeriods (B t) (H t) (w t) + centerPeriods (B t) (H t) (w t))
    (hC0 : C 0 = 0)
    (hCstep : ∀ t, t < N → C (t+1) = C t +
      DecimalDigits.carry
        (fun j => ((quotientPathWord B H w k t)[j]?).getD 0)
        (quotientPathWord B H w k t).length)
    (hr0 : RunAncestry.MaximalRun
      (fun j => ((quotientPathWord B H w k 0)[j]?).getD 0)
      (quotientPathWord B H w k 0).length 18 a0 b0)
    (hleft : a0+N ≤ I) (hright : I+N < b0) :
    ∀ t, t ≤ N →
      let p := quotientEighteenTrack B H w k a0 b0 t
      RunAncestry.MaximalRun
        (fun j => ((quotientPathWord B H w k t)[j]?).getD 0)
        (quotientPathWord B H w k t).length 18 p.1 p.2 ∧
      p.1 ≤ a0+t ∧ b0 ≤ p.2+t ∧ a0+C t ≤ p.1 ∧ p.1 ≤ I ∧ I < p.2 := by
  intro t
  induction t with
  | zero =>
      intro _
      simp only [quotientEighteenTrack, hC0, Nat.add_zero]
      exact ⟨hr0, Nat.le_refl _, Nat.le_refl _, Nat.le_refl _,
        by omega, by omega⟩
  | succ t ih =>
      intro ht
      have htN : t < N := by omega
      obtain ⟨hr, hAL, hBR, hAC, _, _⟩ := ih (by omega)
      let W := quotientPathWord B H w k t
      let p := quotientEighteenTrack B H w k a0 b0 t
      let d := RunAncestry.descendant (fun j => (W[j]?).getD 0) W.length 18 p.1 p.2
      have hva := periodicWord_admissible (B t) (H t) (w t) (k t)
        (quotient_path_valid B H w N hp hv t (by omega))
        (by have hg := hguard t htN; omega)
      have hb := eighteen_descendant_endpoint_bounds
        (fun j => (W[j]?).getD 0) W.length p.1 p.2 hva
      change d.1 ≤ p.1+1 ∧ p.2 ≤ d.2+1 ∧
        p.1 + DecimalDigits.carry (fun j => (W[j]?).getD 0) W.length ≤ d.1 at hb
      have hAL' : d.1 ≤ a0+(t+1) := by dsimp only [p] at hb; omega
      have hBR' : b0 ≤ d.2+(t+1) := by dsimp only [p] at hb; omega
      have hAC' : a0+C (t+1) ≤ d.1 := by
        rw [hCstep t htN]
        dsimp only [p, W] at hb
        omega
      have haI : d.1 ≤ I := by omega
      have hIb : I < d.2 := by omega
      have hdnonempty : d.1 < d.2 := by omega
      have hdmax := (RunAncestry.descendant_step
        (fun j => (W[j]?).getD 0) W.length 18 p.1 p.2 hva (Or.inr rfl) hr).2.1
        hdnonempty
      have hdword := eighteen_run_stepWord W d.1 d.2 hdmax
      have hstep := quotient_path_guarded_step B H w k N hp hguard hkstep t htN
      change stepWord W = quotientPathWord B H w k (t+1) at hstep
      rw [hstep] at hdword
      change RunAncestry.MaximalRun _ _ 18 d.1 d.2 ∧ _
      exact ⟨hdword, hAL', hBR', hAC', haI, hIb⟩

end Agent1.Periodic

#print axioms Agent1.Periodic.quotientEighteenTrack
#print axioms Agent1.Periodic.quotient_eighteen_track
