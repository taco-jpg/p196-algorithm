import P196.Agent1PeriodicNineCenter.Agent1PeriodicNinesCenter
import P196.Agent1PeriodicNineExcursion.Agent1PeriodicNinesPath

/-!
Natural length accounting for the actual additional center strips in a
mixed-entry nine transition, and along a finite path returning to the nine
phase. Empty centers and zero transitions are included. No original validity,
positive clock sum, center descent, or full tuple return is assumed.
-/

namespace Agent1.Periodic
open Agent8

/-- Additional mirrored period pairs removed inside the exact paired residual.
This retains the original maximal strip count and the actual computed carry. -/
def ninesExtraStrips (B H : Word) : Nat :=
  (stripPeriodCenter [9,9,9,9]
    (pair (fixedDigits H (leftEntry B) ++
      List.replicate (rawGamma B H [9,9,9,9]) (9 * leftEntry B)))).2

/-- Cumulative actual additional stripping, over the used source states. -/
def ninesExtraSum (B H : Nat → Word) : Nat → Nat
  | 0 => 0
  | N+1 => ninesExtraSum B H N + ninesExtraStrips (B N) (H N)

/-- Exact natural center-length balance for one mixed actual nine transition. -/
theorem quotientCenter_nines_length_balance (B H : Word)
    (hB : Bounded B 18) (hH : Bounded H 18)
    (hmix : leftEntry B + rightEntry B H [9,9,9,9] = 1) :
    (quotientCenter B H [9,9,9,9]).length + 8 * ninesExtraStrips B H =
      H.length + rawGamma B H [9,9,9,9] := by
  rw [quotientCenter_nines_mixed B H hB hH hmix]
  have h := stripPeriodCenter_length [9,9,9,9]
    (pair (fixedDigits H (leftEntry B) ++
      List.replicate (rawGamma B H [9,9,9,9]) (9 * leftEntry B)))
  simp only [pair_length, List.length_append, fixedDigits_length,
    List.length_replicate, List.length_cons, List.length_nil] at h
  unfold ninesExtraStrips
  omega

/-- The local natural ledger telescopes along every exact path whose initial
and final phases are nine; no center or exterior return is required. -/
theorem quotient_path_nines_center_balance (B H w : Nat → Word) (N : Nat)
    (hp : QuotientPath B H w N) (hw0 : w 0 = [9,9,9,9])
    (hwN : w N = [9,9,9,9]) :
    (H N).length + 8 * ninesExtraSum B H N =
      (H 0).length + quotientClockSum B H w N := by
  induction N with
  | zero => simp [ninesExtraSum, quotientClockSum]
  | succ N ih =>
      have hprefix : QuotientPath B H w N := fun i hi => hp i (by omega)
      have hphase := quotient_path_nines_phase B H w (N+1) hp hw0 hwN
      have hmid : w N = [9,9,9,9] := hphase N (by omega)
      have hprevious := ih hprefix hmid
      obtain ⟨hB, hH, _, _, _, hnextH, _⟩ := hp N (by omega)
      have hmix := quotient_path_nines_entry_sum B H w (N+1) hp hw0 hwN N (by omega)
      have hlocal := quotientCenter_nines_length_balance (B N) (H N) hB hH hmix
      rw [hmid] at hnextH
      rw [← hnextH] at hlocal
      simp only [ninesExtraSum, quotientClockSum, hmid]
      omega

end Agent1.Periodic

#print axioms Agent1.Periodic.ninesExtraStrips
#print axioms Agent1.Periodic.ninesExtraSum
#print axioms Agent1.Periodic.quotientCenter_nines_length_balance
#print axioms Agent1.Periodic.quotient_path_nines_center_balance
