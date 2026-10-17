import Saturated8CycleProfile

/-!
Agent #2 — proposed exact closure of Agent #215's two saturated-profile targets.

SOURCE PRESENT; NOT LEAN-CHECKED in the authoring environment.
Target source: PR #71, head adc0f66099f5743961d03e183cabd61b7c8fa66a.
The original cycleState and target definitions are imported, not replaced.
No claim of an unconditional closed orbit or a Lychrel witness is made.
-/

namespace Agent2.SaturatedProfile
open P196.Agent4.Saturation
open Agent215.Saturated8

/-- Arbitrary nonnegative weights: the edge inequalities telescope. -/
theorem weighted_budget_telescope (A B : Nat) (u g : Nat → Nat) (n : Nat) :
    (∀ i < n, A * g i + u (i + 1) ≤ B + u i) →
    A * total g n + u n ≤ B * n + u 0 := by
  induction n with
  | zero =>
      intro _
      simp [total]
  | succ n ih =>
      intro h
      have hp := ih (fun i hi => h i (by omega))
      have hs := h n (by omega)
      simp only [total, Nat.mul_add, Nat.mul_succ]
      omega

/-- Equality in the telescoped bound forces equality at every edge.
This derives local tightness rather than adding it as a hypothesis. -/
theorem weighted_all_edges_tight (A B : Nat) (u g : Nat → Nat) (n : Nat) :
    (∀ i < n, A * g i + u (i + 1) ≤ B + u i) →
    A * total g n + u n = B * n + u 0 →
    ∀ i < n, A * g i + u (i + 1) = B + u i := by
  induction n with
  | zero =>
      intro _ _ i hi
      omega
  | succ n ih =>
      intro h ht
      have hp := weighted_budget_telescope A B u g n
        (fun i hi => h i (by omega))
      have hs := h n (by omega)
      have hsplit : A * total g n + A * g n + u (n + 1) =
          B * n + B + u 0 := by
        simpa only [total, Nat.mul_add, Nat.mul_succ] using ht
      have hpre : A * total g n + u n = B * n + u 0 := by omega
      have hlast : A * g n + u (n + 1) = B + u n := by omega
      have hrest := ih (fun i hi => h i (by omega)) hpre
      intro i hi
      by_cases hin : i < n
      · exact hrest i hin
      · have hie : i = n := by omega
        simpa only [hie] using hlast

/-- The clock is bounded even on prefixes outside the finite Valid domain. -/
theorem clock_lt_eight (s : Prefix) : clock s < 8 := by
  rcases s with ⟨a, b, c⟩
  unfold clock
  split <;> omega

/-- Every nonzero clock class identifies its exact prefix, not just a residue. -/
theorem nonzero_clock_identifies_state (s : Prefix) (h : clock s ≠ 0) :
    s = cycleState (clock s) := by
  rcases s with ⟨a, b, c⟩
  unfold clock at h ⊢
  split at h <;> simp_all [cycleState]

theorem cycleState_mod (j : Nat) : cycleState (j % 8) = cycleState j := by
  simp [cycleState, Nat.mod_mod]

/-- The zero clock class contains other states. A clock-respecting incoming
edge removes that ambiguity: a predecessor with clock seven is unique. -/
theorem clock_step_output_identifies_state (s : Prefix) (e : Nat) (he : e ≤ 1)
    (hstep : clock (advance s e).1 = (clock s + 1) % 8) :
    (advance s e).1 = cycleState (clock (advance s e).1) := by
  by_cases hz : clock (advance s e).1 = 0
  · have h7 : clock s = 7 := by
      have hb := clock_lt_eight s
      omega
    have hshape := nonzero_clock_identifies_state s (by omega)
    rw [h7] at hshape
    have he01 : e = 0 ∨ e = 1 := by omega
    rcases he01 with rfl | rfl <;>
      simp [hshape, cycleState, advance, clock]
  · exact nonzero_clock_identifies_state (advance s e).1 hz

/-- Only four input positions are forced. No odd-position balance premise
is imposed; the proposed odd-input sum-two law is false in the source. -/
theorem clock_step_forces_even_inputs (j e : Nat) (he : e ≤ 1)
    (hstep : clock (advance (cycleState j) e).1 = (j + 1) % 8) :
    (j % 8 = 0 → e = 1) ∧
    (j % 8 = 2 → e = 0) ∧
    (j % 8 = 4 → e = 0) ∧
    (j % 8 = 6 → e = 1) := by
  have he01 : e = 0 ∨ e = 1 := by omega
  refine ⟨?_, ?_, ?_, ?_⟩
  all_goals
    intro hj
    rcases he01 with rfl | rfl <;>
      simp_all [cycleState, advance, clock, Nat.add_mod]

/-- On the skeleton, overflow alternates, for either possible input bit. -/
theorem cycle_overflow (j e : Nat) (he : e ≤ 1) :
    (advance (cycleState j) e).2 = j % 2 := by
  have hjlt : j % 8 < 8 := Nat.mod_lt _ (by decide)
  have hj : j % 8 = 0 ∨ j % 8 = 1 ∨ j % 8 = 2 ∨ j % 8 = 3 ∨
      j % 8 = 4 ∨ j % 8 = 5 ∨ j % 8 = 6 ∨ j % 8 = 7 := by omega
  have he01 : e = 0 ∨ e = 1 := by omega
  rcases hj with hj | hj | hj | hj | hj | hj | hj | hj <;>
    rcases he01 with rfl | rfl <;>
    simp [cycleState, hj, advance] <;> omega

/-- Clock progression holds at every intermediate time, including the endpoint. -/
theorem clock_progression (s : Nat → Prefix) (n : Nat)
    (hstep : ∀ i < n, clock (s (i + 1)) = (clock (s i) + 1) % 8) :
    ∀ i ≤ n, clock (s i) = (clock (s 0) + i) % 8 := by
  intro i
  induction i with
  | zero =>
      intro _
      have hlt := clock_lt_eight (s 0)
      simp [Nat.mod_eq_of_lt hlt]
  | succ i ih =>
      intro hi
      have hp := ih (by omega)
      have hs := hstep i (by omega)
      omega

/-- Saturation plus closure discharges the source's EveryEdgeTight interface. -/
theorem closed_saturated_edges_tight (s : Nat → Prefix) (e : Nat → Nat) (n : Nat)
    (hv : ∀ i < n, Valid (s i)) (he : ∀ i < n, e i ≤ 1)
    (hs : ∀ i < n, (advance (s i) (e i)).1 = s (i + 1))
    (hclose : s n = s 0)
    (hsat : 2 * total (fun i => (advance (s i) (e i)).2) n = n) :
    EveryEdgeTight s e n := by
  have hb : ∀ i < n,
      82 * (advance (s i) (e i)).2 + potential (s (i + 1)) ≤
        41 + potential (s i) := by
    intro i hi
    have h := (prefix_certificate (s i) (e i) (hv i hi) (he i hi)).1
    simpa only [hs i hi] using h
  have ht : 82 * total (fun i => (advance (s i) (e i)).2) n +
      potential (s n) = 41 * n + potential (s 0) := by
    rw [hclose]
    omega
  exact weighted_all_edges_tight 82 41 (fun i => potential (s i))
    (fun i => (advance (s i) (e i)).2) n hb ht

/-- Exact proof of the original abstract target, with its original quantifiers.
The n=0 case is vacuous; no positivity premise is silently added. -/
theorem saturatedEightCycleTarget : SaturatedEightCycleTarget := by
  intro s e n hv he hs hclose hsat
  have ht := closed_saturated_edges_tight s e n hv he hs hclose hsat
  have hstep : ∀ i < n, clock (s (i + 1)) = (clock (s i) + 1) % 8 := by
    intro i hi
    have hc := (prefix_certificate (s i) (e i) (hv i hi) (he i hi)).2
    have htight : 82 * (advance (s i) (e i)).2 +
        potential (advance (s i) (e i)).1 = 41 + potential (s i) := by
      rw [hs i hi]
      exact ht i hi
    simpa only [hs i hi] using hc htight
  have hclock := clock_progression s n hstep
  have hsucc : ∀ i < n, s (i + 1) = cycleState (clock (s (i + 1))) := by
    intro i hi
    have hlocal : clock (advance (s i) (e i)).1 = (clock (s i) + 1) % 8 := by
      rw [hs i hi]
      exact hstep i hi
    have h := clock_step_output_identifies_state (s i) (e i) (he i hi) hlocal
    simpa only [hs i hi] using h
  have hshape : ∀ i < n, s i = cycleState (clock (s i)) := by
    intro i hi
    by_cases hi0 : i = 0
    · subst i
      have hlast := hsucc (n - 1) (by omega)
      have hn : n - 1 + 1 = n := by omega
      simpa only [hn, hclose] using hlast
    · have hprev := hsucc (i - 1) (by omega)
      have hi' : i - 1 + 1 = i := by omega
      simpa only [hi'] using hprev
  let r : Fin 8 := ⟨clock (s 0), clock_lt_eight (s 0)⟩
  have hprofile : ∀ i < n, s i = cycleState (r.val + i) := by
    intro i hi
    calc
      s i = cycleState (clock (s i)) := hshape i hi
      _ = cycleState ((clock (s 0) + i) % 8) :=
        congrArg cycleState (hclock i (by omega))
      _ = cycleState (r.val + i) := cycleState_mod _
  have hinput : ∀ i < n,
      ((r.val + i) % 8 = 0 → e i = 1) ∧
      ((r.val + i) % 8 = 2 → e i = 0) ∧
      ((r.val + i) % 8 = 4 → e i = 0) ∧
      ((r.val + i) % 8 = 6 → e i = 1) := by
    intro i hi
    apply clock_step_forces_even_inputs (r.val + i) (e i) (he i hi)
    rw [← hprofile i hi, hs i hi]
    have hh := hclock (i + 1) (by omega)
    simpa only [r, Nat.add_assoc] using hh
  refine ⟨r, hprofile, ?_, ?_, ?_, ?_⟩
  · intro i hi hmod
    exact (hinput i hi).1 (by omega)
  · intro i hi hmod
    exact (hinput i hi).2.1 (by omega)
  · intro i hi hmod
    exact (hinput i hi).2.2.1 (by omega)
  · intro i hi hmod
    exact (hinput i hi).2.2.2 (by omega)

/-- A stronger derived consequence: the actual overflow bits alternate. -/
theorem saturated_overflow_profile (s : Nat → Prefix) (e : Nat → Nat) (n : Nat)
    (hv : ∀ i < n, Valid (s i)) (he : ∀ i < n, e i ≤ 1)
    (hs : ∀ i < n, (advance (s i) (e i)).1 = s (i + 1))
    (hclose : s n = s 0)
    (hsat : 2 * total (fun i => (advance (s i) (e i)).2) n = n) :
    ∃ r : Fin 8, ∀ i < n,
      s i = cycleState (r.val + i) ∧
      (advance (s i) (e i)).2 = (r.val + i) % 2 := by
  obtain ⟨r, hp, _⟩ := saturatedEightCycleTarget s e n hv he hs hclose hsat
  refine ⟨r, ?_⟩
  intro i hi
  refine ⟨hp i hi, ?_⟩
  rw [hp i hi]
  exact cycle_overflow _ _ (he i hi)

open DecimalDigits FoldedDecimal OverflowCarryNormalization
open P196.Agent4.WholeWord

/-- Exact proof of the original actual-whole-word target. Its transition,
validity and carry-bound premises are derived from the existing arithmetic
bridge; they are not supplied as surrogate-dynamics assumptions. -/
theorem actualSaturatedEightCycleTarget : ActualSaturatedEightCycleTarget := by
  intro q L n ha hL hreturn hwidth
  let s := fun i => prefix3 (iterPairs q L i).2
  let e := fun i => carry (iterPairs q L i).2 ((iterPairs q L i).1 - 3)
  have hv : ∀ i < n, Valid (s i) := by
    intro i _
    have had := CarryHistory.iterPairs_admissible q L i ha
    have hw := iterPairs_width_ge q L i
    exact ⟨had.2.1, had.2.2.1 0 (by omega), had.2.2.1 1 (by omega),
      had.2.2.1 2 (by omega)⟩
  have he : ∀ i < n, e i ≤ 1 := by
    intro i _
    have had := CarryHistory.iterPairs_admissible q L i ha
    exact carry_bounded (iterPairs q L i).2 (iterPairs q L i).1
      had.2.2.1 ((iterPairs q L i).1 - 3) (by omega)
  have hs : ∀ i < n, (advance (s i) (e i)).1 = s (i + 1) := by
    intro i _
    exact congrArg Prod.fst (iterPairs_prefix_evolution q L i ha hL)
  have hg : (fun i => (advance (s i) (e i)).2) = overflowAt q L := by
    funext i
    exact congrArg Prod.snd (iterPairs_prefix_evolution q L i ha hL)
  have hclose : s n = s 0 := by simpa [s, iterPairs] using hreturn
  have hid := actual_width_overflow_identity q L n ha
  have hsat : 2 * total (fun i => (advance (s i) (e i)).2) n = n := by
    rw [hg]
    omega
  exact saturatedEightCycleTarget s e n hv he hs hclose hsat

/-- Ordinary-integer specialization with an actual canonical representative
at every intermediate time. This does not assert that a saturated return exists. -/
theorem numeric_saturated_prefix_profile
    (seed : Nat) (d : Nat → Nat) (L P : Nat)
    (hc : Canonical seed d L) (hL : 3 ≤ L) :
    ∃ final W, Canonical (Lychrel196.orbit seed P) final W ∧
      (prefix3 (columnSum final W) = prefix3 (columnSum d L) →
        2 * W = 2 * L + P →
        ∃ r : Fin 8, ∀ i < P,
          ∃ digits width, Canonical (Lychrel196.orbit seed i) digits width ∧
            prefix3 (columnSum digits width) = cycleState (r.val + i)) := by
  let q := columnSum d L
  have ha := NormalizationBridge.canonical_admissible seed d L hc
  obtain ⟨final, hf, hrf⟩ :=
    iterPairs_representation seed d q L P hc (fun _ _ => rfl)
  refine ⟨final, (iterPairs q L P).1, hf, ?_⟩
  intro hp hw
  have hge := iterPairs_width_ge q L P
  have hpf : prefix3 (columnSum final (iterPairs q L P).1) =
      prefix3 (iterPairs q L P).2 := by
    unfold prefix3
    rw [hrf 0 (by omega), hrf 1 (by omega), hrf 2 (by omega)]
  rw [hpf] at hp
  obtain ⟨r, hprofile, _⟩ := actualSaturatedEightCycleTarget q L P ha hL hp hw
  refine ⟨r, ?_⟩
  intro i hi
  obtain ⟨digits, hd, hrd⟩ :=
    iterPairs_representation seed d q L i hc (fun _ _ => rfl)
  refine ⟨digits, (iterPairs q L i).1, hd, ?_⟩
  have hgi := iterPairs_width_ge q L i
  have hpi : prefix3 (columnSum digits (iterPairs q L i).1) =
      prefix3 (iterPairs q L i).2 := by
    unfold prefix3
    rw [hrd 0 (by omega), hrd 1 (by omega), hrd 2 (by omega)]
  exact hpi.trans (hprofile i hi)

#print axioms weighted_budget_telescope
#print axioms weighted_all_edges_tight
#print axioms clock_lt_eight
#print axioms nonzero_clock_identifies_state
#print axioms cycleState_mod
#print axioms clock_step_output_identifies_state
#print axioms clock_step_forces_even_inputs
#print axioms cycle_overflow
#print axioms clock_progression
#print axioms closed_saturated_edges_tight
#print axioms saturatedEightCycleTarget
#print axioms saturated_overflow_profile
#print axioms actualSaturatedEightCycleTarget
#print axioms numeric_saturated_prefix_profile

end Agent2.SaturatedProfile
