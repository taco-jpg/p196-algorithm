import ScalarOrbit
import PrefixExtension

/-! Actual orbit paths lift one spatial column by using their actual next
coefficient and actual deeper carry. Path lengths count vertices, so all
edges have both endpoints inside the interval. No disjointness is needed. -/

namespace ActualPrefixLift

open DecimalDigits FoldedDecimal OverflowCarryNormalization CarryHistory

structure Graph (V : Type) where
  valid : V → Prop
  phase : V → Nat
  last : V → Nat
  low : V → Nat
  edge : V → V → Nat → Prop

def Matches {V : Type} (G : Graph V) (q : Nat → Nat) (k s : Nat) (v : V) : Prop :=
  G.valid v ∧ G.phase v = s % 7 ∧ G.last v = q (k - 1) ∧ G.low v = carry q k

def state (q : Nat → Nat) (L a i : Nat) := iterPairs q L (a + i)

/-- The label at spatial width k is the actual carry entering its high block. -/
def label (q : Nat → Nat) (L k a i : Nat) : Nat :=
  carry (state q L a i).2 ((state q L a i).1 - k)

structure ActualPath {V : Type} (G : Graph V) (q : Nat → Nat)
    (L k a s : Nat) (path : Nat → V) (n : Nat) : Prop where
  clock : ∀ i, i < n → (state q L a i).2 0 = ScalarClock.phase (s + i)
  vertices : ∀ i, i < n → Matches G (state q L a i).2 k (s + i) (path i)
  edges : ∀ i, i + 1 < n → G.edge (path i) (path (i + 1)) (label q L k a i)

/-- This is the same local lift used by the stored finite graphs. -/
def lift {V : Type} (G : Graph V) : Graph (V × Fin 19) where
  valid v := G.valid v.1
  phase v := G.phase v.1
  last v := v.2.val
  low v := (v.2.val + G.low v.1) / 10
  edge x y deeper := ∃ gamma,
    G.edge x.1 y.1 gamma ∧
    PrefixExtension.ExtensionChoice (G.last x.1) x.2.val (G.low x.1) gamma
      (ScalarClock.overflowValue (G.phase x.1)) y.2.val
      ((x.2.val + G.low x.1) / 10) deeper

/-- Select a component by restricting vertices, retaining all internal edges. -/
def select {V : Type} (G : Graph V) (P : V → Prop) : Graph V :=
  { G with valid := fun v => G.valid v ∧ P v }

theorem state_admissible (q : Nat → Nat) (L a i : Nat) (ha : Admissible L q) :
    Admissible (state q L a i).1 (state q L a i).2 :=
  iterPairs_admissible q L (a + i) ha

theorem state_width (q : Nat → Nat) (L a i : Nat) : L ≤ (state q L a i).1 :=
  ScalarOrbit.widthAt_lower q L (a + i)

theorem actual_coefficient_bound (q : Nat → Nat) (L k a i : Nat)
    (ha : Admissible L q) (hk : k < L) : (state q L a i).2 k < 19 := by
  have had := state_admissible q L a i ha
  have hw := state_width q L a i
  have hb := had.2.2.1 k (by omega)
  omega

def childPath {V : Type} (q : Nat → Nat) (L k a : Nat) (path : Nat → V)
    (ha : Admissible L q) (hk : k < L) (i : Nat) : V × Fin 19 :=
  (path i, ⟨(state q L a i).2 k, actual_coefficient_bound q L k a i ha hk⟩)

theorem childPath_projection {V : Type} (q : Nat → Nat) (L k a : Nat)
    (path : Nat → V) (ha : Admissible L q) (hk : k < L) (i : Nat) :
    (childPath q L k a path ha hk i).1 = path i := rfl

/-- Construct the child path and every actual deeper-carry label. -/
theorem actual_path_lifts {V : Type} (G : Graph V) (q : Nat → Nat)
    (L k a s n : Nat) (path : Nat → V) (ha : Admissible L q)
    (hk0 : 1 ≤ k) (hk : k < L) (hp : ActualPath G q L k a s path n) :
    ActualPath (lift G) q L (k + 1) a s (childPath q L k a path ha hk) n := by
  refine ⟨hp.clock, ?_, ?_⟩
  · intro i hi
    obtain ⟨hv, hphase, hlast, hlow⟩ := hp.vertices i hi
    refine ⟨hv, hphase, ?_, ?_⟩
    · simp only [lift, childPath, Nat.add_sub_cancel]
    · change ((state q L a i).2 k + G.low (path i)) / 10 =
        carry (state q L a i).2 (k + 1)
      rw [hlow]
      rfl
  · intro i hi
    have had := state_admissible q L a i ha
    have hw := state_width q L a i
    have hchoice := PrefixExtension.actual_extension_choice
      (state q L a i).2 (state q L a i).1 k had hk0 (by omega)
    obtain ⟨_, hphase, hlast, hlow⟩ := hp.vertices i (by omega)
    have ho := ActualScalar.overflow_of_phase (state q L a i).2
      (state q L a i).1 (s + i) had (hp.clock i (by omega))
    refine ⟨label q L k a i, hp.edges i hi, ?_⟩
    change PrefixExtension.ExtensionChoice (G.last (path i)) ((state q L a i).2 k)
      (G.low (path i)) (label q L k a i)
      (ScalarClock.overflowValue (G.phase (path i)))
      ((state q L a (i + 1)).2 k)
      (((state q L a i).2 k + G.low (path i)) / 10)
      (label q L (k + 1) a i)
    rw [hlast, hlow, hphase]
    have hn : (state q L a (i + 1)).2 k =
        nextColumns (state q L a i).2 (state q L a i).1 k := by
      simp only [state, Nat.add_assoc, iterPairs]
      rfl
    rw [hn]
    have hd : (state q L a i).1 - (k + 1) = (state q L a i).1 - 1 - k := by omega
    simpa only [label, hd, ScalarClock.overflow, ho, carry] using hchoice

theorem actual_path_select {V : Type} (G : Graph V) (P : V → Prop)
    (q : Nat → Nat) (L k a s n : Nat) (path : Nat → V)
    (hp : ActualPath G q L k a s path n) (hP : ∀ i, i < n → P (path i)) :
    ActualPath (select G P) q L k a s path n := by
  refine ⟨hp.clock, ?_, hp.edges⟩
  intro i hi
  obtain ⟨hv, hphase, hlast, hlow⟩ := hp.vertices i hi
  exact ⟨⟨hv, hP i hi⟩, hphase, hlast, hlow⟩

/-- Finite intervals restrict with their endpoint and phase correspondence. -/
theorem actual_path_interval {V : Type} (G : Graph V) (q : Nat → Nat)
    (L k a s n start length : Nat) (path : Nat → V)
    (hp : ActualPath G q L k a s path n) (hr : start + length ≤ n) :
    ActualPath G q L k (a + start) (s + start)
      (fun i => path (start + i)) length := by
  refine ⟨?_, ?_, ?_⟩
  · intro i hi
    simpa only [state, Nat.add_assoc] using hp.clock (start + i) (by omega)
  · intro i hi
    simpa only [state, Nat.add_assoc] using hp.vertices (start + i) (by omega)
  · intro i hi
    simpa only [label, state, Nat.add_assoc] using hp.edges (start + i) (by omega)

/-- Constant-component intervals construct a path in the exact induced lift.
No premise asserting the existence of a lifted path is used. -/
theorem actual_component_interval_lifts {V C : Type} (G : Graph V)
    (component : V → C) (c : C) (q : Nat → Nat) (L k a s n start length : Nat)
    (path : Nat → V) (ha : Admissible L q) (hk0 : 1 ≤ k) (hk : k < L)
    (hp : ActualPath G q L k a s path n) (hr : start + length ≤ n)
    (hc : ∀ i, i < length → component (path (start + i)) = c) :
    ∃ lifted, ActualPath (lift (select G (fun v => component v = c)))
      q L (k + 1) (a + start) (s + start) lifted length ∧
      ∀ i, (lifted i).1 = path (start + i) := by
  have hinterval := actual_path_interval G q L k a s n start length path hp hr
  have hselected := actual_path_select G (fun v => component v = c) q L k
    (a + start) (s + start) length (fun i => path (start + i)) hinterval hc
  exact ⟨childPath q L k (a + start) (fun i => path (start + i)) ha hk,
    actual_path_lifts _ q L k (a + start) (s + start) length _ ha hk0 hk hselected,
    fun _ => rfl⟩

/-- The remaining finite-ID obligations are vertex fields and forward edge
completeness. No converse realizability of finite graph edges is needed. -/
structure Realization {V W : Type} (G : Graph V) (H : Graph W) (encode : V → W) : Prop where
  valid : ∀ v, G.valid v → H.valid (encode v)
  phase : ∀ v, G.valid v → H.phase (encode v) = G.phase v
  last : ∀ v, G.valid v → H.last (encode v) = G.last v
  low : ∀ v, G.valid v → H.low (encode v) = G.low v
  edges : ∀ u v c, G.valid u → G.valid v → G.edge u v c →
    H.edge (encode u) (encode v) c

theorem actual_path_encode {V W : Type} (G : Graph V) (H : Graph W)
    (encode : V → W) (hr : Realization G H encode)
    (q : Nat → Nat) (L k a s n : Nat) (path : Nat → V)
    (hp : ActualPath G q L k a s path n) :
    ActualPath H q L k a s (fun i => encode (path i)) n := by
  refine ⟨hp.clock, ?_, ?_⟩
  · intro i hi
    obtain ⟨hv, hphase, hlast, hlow⟩ := hp.vertices i hi
    exact ⟨hr.valid _ hv, (hr.phase _ hv).trans hphase,
      (hr.last _ hv).trans hlast, (hr.low _ hv).trans hlow⟩
  · intro i hi
    exact hr.edges _ _ _ (hp.vertices i (by omega)).1
      (hp.vertices (i + 1) hi).1 (hp.edges i hi)

end ActualPrefixLift
