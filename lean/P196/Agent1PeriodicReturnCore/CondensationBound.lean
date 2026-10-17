import Std

/-! Weighted condensation bounds for finite paths.

The hypotheses are certificate conditions, not a formalized SCC algorithm:
each constant-component interval has its assigned vertex bound, and an
edge to a different component decreases the sink rank by at least the
source component's weight. Both endpoints count as path vertices.
-/

namespace CondensationBound

variable {C : Type} [DecidableEq C]

/-- Number of vertices in the current constant-component suffix. -/
def blockAge (component : Nat → C) : Nat → Nat
  | 0 => 1
  | t + 1 => if component (t + 1) = component t then blockAge component t + 1 else 1

/-- Every constant-component interval inside the `n`-vertex path fits its
component's weight. The interval includes both endpoints. -/
def IntervalBound (component : Nat → C) (weight : C → Nat) (n : Nat) : Prop :=
  ∀ a b, a ≤ b → b < n →
    (∀ i, a ≤ i → i ≤ b → component i = component b) →
    b + 1 - a ≤ weight (component b)

/-- Local conditions checked by a weighted condensation certificate. -/
def RankCertificate (component : Nat → C) (weight rank : C → Nat) (n : Nat) : Prop :=
  (∀ i, i < n → weight (component i) ≤ rank (component i)) ∧
  (∀ i, i + 1 < n → component i ≠ component (i + 1) →
    weight (component i) + rank (component (i + 1)) ≤ rank (component i))

theorem blockAge_pos (component : Nat → C) (t : Nat) :
    0 < blockAge component t := by
  induction t with
  | zero => simp [blockAge]
  | succ t ih =>
    simp only [blockAge]
    split <;> omega

theorem blockAge_le (component : Nat → C) (t : Nat) :
    blockAge component t ≤ t + 1 := by
  induction t with
  | zero => simp [blockAge]
  | succ t ih =>
    simp only [blockAge]
    split <;> omega

/-- The suffix counted by `blockAge` really has constant component. -/
theorem blockAge_constant (component : Nat → C) (t : Nat) :
    ∀ i, t + 1 - blockAge component t ≤ i → i ≤ t → component i = component t := by
  induction t with
  | zero =>
    intro i _ hi
    have : i = 0 := by omega
    simp [this]
  | succ t ih =>
    intro i hlo hhi
    by_cases he : component (t + 1) = component t
    · have hb := blockAge_le component t
      simp only [blockAge, he, if_true] at hlo
      by_cases hi : i ≤ t
      · have hc := ih i (by omega) hi
        exact hc.trans he.symm
      · have : i = t + 1 := by omega
        simp [this]
    · simp only [blockAge, he, if_false] at hlo
      have : i = t + 1 := by omega
      simp [this]

theorem blockAge_le_weight (component : Nat → C) (weight : C → Nat) (n t : Nat)
    (hinterval : IntervalBound component weight n) (ht : t < n) :
    blockAge component t ≤ weight (component t) := by
  have hp := blockAge_pos component t
  have hb := blockAge_le component t
  have h := hinterval (t + 1 - blockAge component t) t (by omega) ht
    (blockAge_constant component t)
  omega

/-- A subtraction-free residual-rank invariant for every visited vertex. -/
theorem residual_rank_bound (component : Nat → C) (weight rank : C → Nat) (n : Nat)
    (hinterval : IntervalBound component weight n)
    (hcert : RankCertificate component weight rank n) :
    ∀ t, t < n → t + rank (component t) + 1 ≤ rank (component 0) + blockAge component t := by
  intro t
  induction t with
  | zero =>
    intro _
    simp [blockAge]
  | succ t ih =>
    intro ht
    have hold := ih (by omega)
    have hage := blockAge_le_weight component weight n t hinterval (by omega)
    by_cases he : component (t + 1) = component t
    · simp only [blockAge, he, if_true]
      omega
    · have hdrop := hcert.2 t ht (Ne.symm he)
      simp only [blockAge, he, if_false]
      omega

/-- A weighted condensation rank bounds the total number of path vertices.
No finiteness of the ambient component type is needed once the finite
certificate conditions along this path are supplied. -/
theorem path_vertices_le_rank (component : Nat → C) (weight rank : C → Nat) (n : Nat)
    (hinterval : IntervalBound component weight n)
    (hcert : RankCertificate component weight rank n) :
    n ≤ rank (component 0) := by
  by_cases hn : n = 0
  · simp [hn]
  · have ht : n - 1 < n := by omega
    have h := residual_rank_bound component weight rank n hinterval hcert (n - 1) ht
    have ha := blockAge_le_weight component weight n (n - 1) hinterval ht
    have hr := hcert.1 (n - 1) ht
    omega

theorem path_vertices_le (component : Nat → C) (weight rank : C → Nat) (n M : Nat)
    (hinterval : IntervalBound component weight n)
    (hcert : RankCertificate component weight rank n)
    (hstart : rank (component 0) ≤ M) : n ≤ M :=
  Nat.le_trans (path_vertices_le_rank component weight rank n hinterval hcert) hstart

theorem rank_step_le (component : Nat → C) (weight rank : C → Nat) (n i : Nat)
    (hcert : RankCertificate component weight rank n) (hi : i + 1 < n) :
    rank (component (i + 1)) ≤ rank (component i) := by
  by_cases he : component i = component (i + 1)
  · simp [he]
  · have h := hcert.2 i hi he
    omega

theorem rank_antitone (component : Nat → C) (weight rank : C → Nat) (n a b : Nat)
    (hcert : RankCertificate component weight rank n) (hab : a ≤ b) (hb : b < n) :
    rank (component b) ≤ rank (component a) := by
  induction b generalizing a with
  | zero =>
    have : a = 0 := by omega
    simp [this]
  | succ b ih =>
    by_cases he : a = b + 1
    · simp [he]
    · have hprevious := ih a (by omega) (by omega)
      have hstep := rank_step_le component weight rank n b hcert hb
      omega

/-- Equal endpoint ranks force equality of the endpoint components when
every visited component has positive weight. -/
theorem same_component_of_equal_rank (component : Nat → C) (weight rank : C → Nat)
    (n a b : Nat) (hcert : RankCertificate component weight rank n)
    (hpositive : ∀ i, i < n → 0 < weight (component i))
    (hab : a ≤ b) (hb : b < n)
    (hequal : rank (component a) = rank (component b)) :
    component a = component b := by
  induction b generalizing a with
  | zero =>
    have : a = 0 := by omega
    simp [this]
  | succ b ih =>
    by_cases he : a = b + 1
    · simp [he]
    · have hbefore := rank_antitone component weight rank n a b hcert (by omega) (by omega)
      have hstep := rank_step_le component weight rank n b hcert hb
      have hr : rank (component a) = rank (component b) := by omega
      have hc := ih a (by omega) (by omega) hr
      by_cases hedge : component b = component (b + 1)
      · exact hc.trans hedge
      · have hdrop := hcert.2 b hb hedge
        have hp := hpositive b (by omega)
        omega

/-- A path cannot leave a component and later return to it: every
intermediate vertex between equal endpoint components has that component. -/
theorem component_interval (component : Nat → C) (weight rank : C → Nat)
    (n a b : Nat) (hcert : RankCertificate component weight rank n)
    (hpositive : ∀ i, i < n → 0 < weight (component i))
    (_hab : a ≤ b) (hb : b < n) (hequal : component a = component b) :
    ∀ i, a ≤ i → i ≤ b → component i = component a := by
  intro i hai hib
  have hleft := rank_antitone component weight rank n a i hcert hai (by omega)
  have hright := rank_antitone component weight rank n i b hcert hib hb
  have he : rank (component a) = rank (component b) := congrArg rank hequal
  have hr : rank (component a) = rank (component i) := by omega
  exact (same_component_of_equal_rank component weight rank n a i hcert hpositive
    hai (by omega) hr).symm

def componentWeight (cyclic : C → Bool) (B : Nat) (c : C) : Nat :=
  if cyclic c then B else 1

omit [DecidableEq C] in
/-- Cyclic-component interval bounds and the absence of an internal edge
in every acyclic component give the weights used by the condensation DP. -/
theorem interval_bound_of_cyclic (component : Nat → C) (cyclic : C → Bool) (B n : Nat)
    (hcyclic : ∀ a b, a ≤ b → b < n → cyclic (component b) = true →
      (∀ i, a ≤ i → i ≤ b → component i = component b) → b + 1 - a ≤ B)
    (hacyclic : ∀ i, i + 1 < n → cyclic (component i) = false →
      component i ≠ component (i + 1)) :
    IntervalBound component (componentWeight cyclic B) n := by
  intro a b hab hb hconstant
  by_cases hc : cyclic (component b) = true
  · simpa only [componentWeight, hc, if_true] using hcyclic a b hab hb hc hconstant
  · have hf : cyclic (component b) = false := by
      cases hx : cyclic (component b) <;> simp_all
    have he : a = b := by
      by_cases heq : a = b
      · exact heq
      · have hstart := hconstant a (Nat.le_refl a) hab
        have hnext := hconstant (a + 1) (by omega) (by omega)
        have hfalse : cyclic (component a) = false := by rw [hstart]; exact hf
        have hne := hacyclic a (by omega) hfalse
        exact False.elim (hne (hstart.trans hnext.symm))
    simp only [componentWeight, hf, Bool.false_eq_true, if_false]
    omega

theorem cyclic_path_vertices_le_rank (component : Nat → C) (cyclic : C → Bool)
    (rank : C → Nat) (B n : Nat)
    (hcyclic : ∀ a b, a ≤ b → b < n → cyclic (component b) = true →
      (∀ i, a ≤ i → i ≤ b → component i = component b) → b + 1 - a ≤ B)
    (hacyclic : ∀ i, i + 1 < n → cyclic (component i) = false →
      component i ≠ component (i + 1))
    (hcert : RankCertificate component (componentWeight cyclic B) rank n) :
    n ≤ rank (component 0) :=
  path_vertices_le_rank component (componentWeight cyclic B) rank n
    (interval_bound_of_cyclic component cyclic B n hcyclic hacyclic) hcert

/-- Instantiation for an actual directed-graph path. A graph-wide local
rank certificate supplies the sequence certificate automatically. -/
theorem graph_path_vertices_le_rank {V : Type} (edge : V → V → Prop)
    (component : V → C) (weight rank : C → Nat) (path : Nat → V) (n : Nat)
    (hpath : ∀ i, i + 1 < n → edge (path i) (path (i + 1)))
    (hbase : ∀ v, weight (component v) ≤ rank (component v))
    (hcross : ∀ u v, edge u v → component u ≠ component v →
      weight (component u) + rank (component v) ≤ rank (component u))
    (hinterval : IntervalBound (fun i => component (path i)) weight n) :
    n ≤ rank (component (path 0)) := by
  apply path_vertices_le_rank (fun i => component (path i)) weight rank n hinterval
  constructor
  · intro i _
    exact hbase (path i)
  · intro i hi hne
    exact hcross (path i) (path (i + 1)) (hpath i hi) hne

/-- The arithmetic conversion used for seven-step return counts. The
1600-vertex bound remains an explicit hypothesis, not a computed graph fact. -/
theorem seven_returns_le_228 (n returns : Nat)
    (hvertices : n ≤ 1600) (hreturns : 7 * returns + 1 ≤ n) :
    returns ≤ 228 := by omega

end CondensationBound
