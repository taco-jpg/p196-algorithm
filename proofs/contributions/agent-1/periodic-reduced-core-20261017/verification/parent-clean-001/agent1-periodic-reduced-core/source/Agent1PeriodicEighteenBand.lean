import Agent1PeriodicQuotient
import RunAncestry

/-!
Static geometry of the left constant-eighteen band in the original periodic
word. Only one maximal run meeting this band is selected. No run population,
ancestry enumeration, validity assumption, or quotient dynamics is asserted.
-/

namespace Agent1.Periodic
open Agent8 Agent1.RepeatedBlock

private theorem eighteen_pow (k : Nat) :
    pow [18,18,18,18] k = List.replicate (4*k) 18 := by
  induction k with
  | zero => rfl
  | succ k ih =>
      rw [pow, ih, Nat.mul_succ, Nat.add_comm (4*k) 4]
      change List.replicate 4 18 ++ List.replicate (4*k) 18 = _
      exact List.replicate_append_replicate

private theorem eighteen_prefix (B H : Word) (k j : Nat) (hj : j < B.length) :
    ((periodicWord B H [18,18,18,18] k)[j]?).getD 0 = (B[j]?).getD 0 := by
  simp only [periodicWord, List.append_assoc]
  rw [List.getElem?_append_left hj]

private theorem eighteen_band (B H : Word) (k j : Nat)
    (hj : B.length ≤ j) (hjk : j < B.length+4*k) :
    ((periodicWord B H [18,18,18,18] k)[j]?).getD 0 = 18 := by
  simp only [periodicWord, List.append_assoc]
  rw [List.getElem?_append_right hj, eighteen_pow]
  have hsub : j-B.length < 4*k := by omega
  rw [List.getElem?_append_left (by simpa only [List.length_replicate] using hsub),
    List.getElem?_replicate_of_lt hsub]
  rfl

private theorem eighteen_least (P : Nat → Prop) (n : Nat) (hn : P n) :
    ∃ m, P m ∧ ∀ r, r < m → ¬ P r := by
  classical
  induction n using Nat.strongRecOn with
  | ind n ih =>
      by_cases hex : ∃ r, r < n ∧ P r
      · obtain ⟨r, hr, hPr⟩ := hex
        exact ih r hr hPr
      · exact ⟨n, hn, fun r hr hPr => hex ⟨r, hr, hPr⟩⟩

/-- A maximal eighteen run covers the entire nonempty left repeated band.
Both adjoining blocks may be empty or all eighteen, so the run may extend
through the center and the right band. -/
theorem periodic_eighteen_band_run (B H : Word) (k : Nat) (hk : 0 < k) :
    ∃ a b, RunAncestry.MaximalRun
      (fun j => ((periodicWord B H [18,18,18,18] k)[j]?).getD 0)
      (periodicWord B H [18,18,18,18] k).length 18 a b ∧
      a ≤ B.length ∧ B.length+4*k ≤ b := by
  classical
  let W := periodicWord B H [18,18,18,18] k
  let q := fun (j : Nat) => (W[j]?).getD 0
  let e := B.length+4*k
  have heL : e ≤ W.length := by
    dsimp [e, W]
    rw [periodicWord_length]
    simp only [List.length_cons, List.length_nil]
    omega
  have hband : ∀ j, B.length ≤ j → j < e → q j = 18 :=
    eighteen_band B H k
  let P := fun a => a ≤ B.length ∧ ∀ j, a ≤ j → j < e → q j = 18
  have hP : P B.length := ⟨Nat.le_refl _, hband⟩
  obtain ⟨a, ha, hamin⟩ := eighteen_least P B.length hP
  have haB : a ≤ B.length := ha.1
  have hae : a < e := by dsimp [e]; omega
  have hleft : a = 0 ∨ q (a-1) ≠ 18 := by
    by_cases ha0 : a = 0
    · exact Or.inl ha0
    · right
      intro hq
      apply hamin (a-1) (by omega)
      refine ⟨by omega, ?_⟩
      intro j haj hje
      by_cases hja : a ≤ j
      · exact ha.2 j hja hje
      · have heq : j = a-1 := by omega
        simpa only [heq] using hq
  let R := fun b => e ≤ b ∧ (b = W.length ∨ q b ≠ 18)
  have hR : R W.length := ⟨heL, Or.inl rfl⟩
  obtain ⟨b, hb, hbmin⟩ := eighteen_least R W.length hR
  have hbL : b ≤ W.length := by
    by_cases h : b ≤ W.length
    · exact h
    · exact False.elim (hbmin W.length (by omega) hR)
  have heb : e ≤ b := hb.1
  refine ⟨a, b, ⟨by omega, hbL, ?_, hleft, hb.2⟩, haB, heb⟩
  intro j haj hjb
  by_cases hje : j < e
  · exact ha.2 j haj hje
  · by_cases hq : q j = 18
    · exact hq
    · exact False.elim (hbmin j hjb ⟨by omega, Or.inr hq⟩)

/-- Two maximal runs meeting the same position in the two left bands have
identical left endpoints. The shared exterior is the only shared block;
centers and positive band lengths may differ. -/
theorem periodic_eighteen_band_left_eq (B H H' : Word)
    (k k' i a b a' b' : Nat)
    (hr : RunAncestry.MaximalRun
      (fun j => ((periodicWord B H [18,18,18,18] k)[j]?).getD 0)
      (periodicWord B H [18,18,18,18] k).length 18 a b)
    (hr' : RunAncestry.MaximalRun
      (fun j => ((periodicWord B H' [18,18,18,18] k')[j]?).getD 0)
      (periodicWord B H' [18,18,18,18] k').length 18 a' b')
    (hBi : B.length ≤ i) (hik : i < B.length+4*k)
    (hik' : i < B.length+4*k')
    (hai : a ≤ i) (hib : i < b) (hai' : a' ≤ i) (hib' : i < b') :
    a = a' := by
  have hprefix : ∀ j, j ≤ i →
      ((periodicWord B H [18,18,18,18] k)[j]?).getD 0 =
      ((periodicWord B H' [18,18,18,18] k')[j]?).getD 0 := by
    intro j hji
    by_cases hjB : j < B.length
    · rw [eighteen_prefix B H k j hjB, eighteen_prefix B H' k' j hjB]
    · rw [eighteen_band B H k j (by omega) (by omega),
        eighteen_band B H' k' j (by omega) (by omega)]
  apply Nat.le_antisymm
  · by_cases h : a ≤ a'
    · exact h
    · exfalso
      have hne := hr.2.2.2.1.resolve_left (by omega)
      apply hne
      dsimp only
      rw [hprefix (a-1) (by omega)]
      exact hr'.2.2.1 (a-1) (by omega) (by omega)
  · by_cases h : a' ≤ a
    · exact h
    · exfalso
      have hne := hr'.2.2.2.1.resolve_left (by omega)
      apply hne
      dsimp only
      rw [← hprefix (a'-1) (by omega)]
      exact hr.2.2.1 (a'-1) (by omega) (by omega)

end Agent1.Periodic

#print axioms Agent1.Periodic.periodic_eighteen_band_run
#print axioms Agent1.Periodic.periodic_eighteen_band_left_eq
