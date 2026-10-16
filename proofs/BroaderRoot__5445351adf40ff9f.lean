import BroaderClock
import ScalarRoot
import BoundedPrefixLift
import BJobData0

/-!
Agent #103. Root bridge for the broader two-column return hierarchy.

`root2` is the bit-bounded restriction of the lifted scalar root
(`ActualPrefixLift.lift ScalarRoot.root`, states `(phase, second coefficient)`)
to the fifteen states that occur on seven-step two-column returns to (4,4).
`root2_realization` checks, by kernel reduction, that it embeds into job 0 of
the generated broader certificate (`BroaderJobData.data0`, source job 16):
same phase/last/low fields, and every bounded edge is present. A second
kernel-checked classification (`returnIn_root`) shows that every state on a
return path lies in the fifteen-state set, so (`actual_broader_root_path`)
`R` consecutive returns from a word of width at least 2 give an actual path
of `7R+1` vertices in that finite graph at spatial width 2.
-/

namespace BroaderRoot

open DecimalDigits FoldedDecimal OverflowCarryNormalization CarryHistory ActualPrefixLift BroaderClock

/-- The fifteen (phase, second coefficient) states, in source-job-16 order. -/
def states : List (Nat × Nat) :=
  [(0, 4), (1, 8), (1, 9), (2, 16), (2, 18), (3, 14), (3, 16), (4, 8), (4, 12),
   (4, 13), (5, 9), (5, 10), (5, 14), (6, 0), (6, 9)]

def P (v : Fin 7 × Fin 19) : Prop := (v.1.val, v.2.val) ∈ states

instance : DecidablePred P := fun v => inferInstanceAs (Decidable ((v.1.val, v.2.val) ∈ states))

def root2 : Graph (Fin 7 × Fin 19) :=
  BoundedPrefixLift.bounded (select (lift ScalarRoot.root) P)

def encodeB (v : Fin 7 × Fin 19) : Nat := states.idxOf (v.1.val, v.2.val)

/-- Decidable form of a lifted-root edge: the hidden high carry is determined. -/
def liftEdgeB (u v : Fin 7 × Fin 19) (c : Nat) : Prop :=
  ((u.1.val, v.1.val, (u.2.val + c) / 10) ∈ ScalarRoot.rootEdges) ∧
  v.2.val = PrefixExtension.nextCoefficient (ScalarClock.phaseValue u.1.val) u.2.val
    (ScalarClock.phaseValue u.1.val / 10) ((u.2.val + c) / 10)
    (ScalarClock.overflowValue u.1.val) c

instance (u v : Fin 7 × Fin 19) (c : Nat) : Decidable (liftEdgeB u v c) := by
  unfold liftEdgeB; exact inferInstance

theorem lift_edge_iff (u v : Fin 7 × Fin 19) (c : Nat) :
    (lift ScalarRoot.root).edge u v c → liftEdgeB u v c := by
  rintro ⟨gamma, hroot, hg, hn, -⟩
  subst hg
  exact ⟨hroot, hn⟩

theorem fields_table_checked : ∀ (x : Fin 7) (y : Fin 19), P (x, y) →
    encodeB (x, y) < BroaderJobData.data0.size ∧
    BroaderJobData.data0.phase (encodeB (x, y)) = x.val ∧
    BroaderJobData.data0.last (encodeB (x, y)) = y.val ∧
    BroaderJobData.data0.low (encodeB (x, y)) = (y.val + ScalarClock.phaseValue x.val / 10) / 10 := by
  decide

theorem fields_checked (v : Fin 7 × Fin 19) (hv : P v) :
    encodeB v < BroaderJobData.data0.size ∧
    BroaderJobData.data0.phase (encodeB v) = v.1.val ∧
    BroaderJobData.data0.last (encodeB v) = v.2.val ∧
    BroaderJobData.data0.low (encodeB v) = (v.2.val + ScalarClock.phaseValue v.1.val / 10) / 10 :=
  fields_table_checked v.1 v.2 hv

theorem edges_table_checked : ∀ (x : Fin 7) (y : Fin 19), P (x, y) → ∀ (x' : Fin 7) (y' : Fin 19),
    P (x', y') → ∀ c : Fin 2, liftEdgeB (x, y) (x', y') c.val →
      BroaderJobData.data0.next (encodeB (x, y)) c.val = encodeB (x', y') + 1 := by
  decide

theorem edges_checked (u v : Fin 7 × Fin 19) (c : Fin 2) (hu : P u) (hv : P v)
    (he : liftEdgeB u v c.val) :
    BroaderJobData.data0.next (encodeB u) c.val = encodeB v + 1 :=
  edges_table_checked u.1 u.2 hu v.1 v.2 hv c he

theorem root2_realization : Realization root2 (ScalarFinite.graph BroaderJobData.data0) encodeB := by
  refine ⟨?_, ?_, ?_, ?_, ?_⟩
  · intro v hv; exact (fields_checked v hv.2).1
  · intro v hv; exact (fields_checked v hv.2).2.1
  · intro v hv; exact (fields_checked v hv.2).2.2.1
  · intro v hv
    have h := (fields_checked v hv.2).2.2.2
    change BroaderJobData.data0.low (encodeB v) = (v.2.val + ScalarClock.phaseValue v.1.val / 10) / 10
    exact h
  · rintro u v c hu hv ⟨hc, he⟩
    refine ⟨hc, ?_⟩
    exact edges_checked u v ⟨c, by omega⟩ hu.2 hv.2 (lift_edge_iff u v c he)

/-- Every state on a continuation that returns to (4,4) lies in `states`. -/
def returnIn : Nat → Nat → Nat × Nat → Bool
  | 0, _, _ => true
  | r + 1, t, s => (!reaches (r + 1) s) ||
      (decide ((t, s.2) ∈ states) && (succs s).all (returnIn r (t + 1)))

theorem returnIn_root : returnIn 7 0 (4, 4) = true := by decide

theorem returnIn_sound (r t : Nat) (p : Nat → Nat × Nat)
    (hstep : ∀ i, i < r → p (i + 1) ∈ succs (p i)) (hend : p r = (4, 4))
    (hok : returnIn r t (p 0) = true) :
    ∀ i, i < r → (t + i, (p i).2) ∈ states := by
  induction r generalizing t p with
  | zero => intro i hi; omega
  | succ r ih =>
    have hr := reaches_of_path (r + 1) p hstep hend
    simp only [returnIn, hr, Bool.not_true, Bool.false_or, Bool.and_eq_true,
      decide_eq_true_eq, List.all_eq_true] at hok
    obtain ⟨h0, hall⟩ := hok
    intro i hi
    cases i with
    | zero => simpa using h0
    | succ j =>
      have hq := ih (t + 1) (fun k => p (k + 1)) (fun k hk => hstep (k + 1) (by omega)) hend
        (hall (p 1) (hstep 0 (by omega))) j (by omega)
      simpa [Nat.add_assoc, Nat.add_comm 1 j] using hq

/-- Along `R` consecutive returns, every (phase, second coefficient) is a root state. -/
theorem returns_in_states (q : Nat → Nat) (L a R : Nat) (ha : Admissible L q) (hL : 2 ≤ L)
    (hret : ∀ k, k ≤ R → pairAt q L (a + 7 * k) = (4, 4)) :
    ∀ i, i ≤ 7 * R → (i % 7, (iterPairs q L (a + i)).2 1) ∈ states := by
  intro i hi
  by_cases hR : i = 7 * R
  · have h := congrArg Prod.snd (hret R (Nat.le_refl R))
    simp only [pairAt] at h
    subst hR
    rw [h, Nat.mul_mod_right]
    decide
  · have hk : i / 7 < R := by omega
    have hs := returnIn_sound 7 0 (fun k => pairAt q L (a + 7 * (i / 7) + k))
      (fun k _ => by simpa [Nat.add_assoc] using pairAt_step q L (a + 7 * (i / 7) + k) ha hL)
      (by simpa [Nat.mul_succ, Nat.add_assoc] using hret (i / 7 + 1) (by omega))
      (by simpa [hret (i / 7) (by omega)] using returnIn_root) (i % 7) (Nat.mod_lt _ (by decide))
    have hi' : a + 7 * (i / 7) + i % 7 = a + i := by omega
    simpa [pairAt, hi'] using hs

theorem iterPairs_restart (q : Nat → Nat) (L a t : Nat) :
    iterPairs (iterPairs q L a).2 (iterPairs q L a).1 t = iterPairs q L (a + t) := by
  induction t with
  | zero => simp only [iterPairs, Nat.add_zero]
  | succ t ih =>
    simp only [iterPairs, Nat.add_succ, ih]
    rfl

/-- `R` consecutive returns, restarted at time `a`, give an actual path of
`7R+1` vertices in the finite broader root graph at spatial width 2. -/
theorem actual_broader_root_path (q : Nat → Nat) (L a R : Nat) (ha : Admissible L q) (hL : 2 ≤ L)
    (hret : ∀ k, k ≤ R → pairAt q L (a + 7 * k) = (4, 4)) :
    ∃ path, ActualPath (ScalarFinite.graph BroaderJobData.data0)
      (iterPairs q L a).2 (iterPairs q L a).1 2 0 0 path (7 * R + 1) := by
  have had := iterPairs_admissible q L a ha
  have hwa : 2 ≤ (iterPairs q L a).1 := by
    have := ScalarOrbit.widthAt_lower q L a
    unfold ScalarOrbit.widthAt at this; omega
  have hseg := returns_clock_segment q L a R ha hL hret
  have hc : ∀ i, i < 7 * R + 1 →
      (state (iterPairs q L a).2 (iterPairs q L a).1 0 i).2 0 = ScalarClock.phase (0 + i) := by
    intro i hi
    simp only [state, Nat.zero_add, iterPairs_restart]
    simpa [ScalarOrbit.outerAt] using hseg i (by omega)
  obtain ⟨path, hp, hproj⟩ := ScalarRoot.actual_two_column_path (iterPairs q L a).2
    (iterPairs q L a).1 0 0 (7 * R + 1) had hwa hc
  have hP : ∀ i, i < 7 * R + 1 → P (path i) := by
    intro i hi
    obtain ⟨h1, h2, -⟩ := hproj i
    have hm := returns_in_states q L a R ha hL hret i (by omega)
    unfold P
    rw [h1, h2]
    simpa [ScalarRoot.phasePath, state, iterPairs_restart] using hm
  have hsel := actual_path_select (lift ScalarRoot.root) P _ _ 2 0 0 _ path hp hP
  exact ⟨_, BoundedPrefixLift.actual_path_encode (select (lift ScalarRoot.root) P)
    (ScalarFinite.graph BroaderJobData.data0) encodeB root2_realization _ _ 2 0 0 _ path had hsel⟩

end BroaderRoot
