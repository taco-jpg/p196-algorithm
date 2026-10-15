import BoundedPrefixLift
import ComponentHierarchy

/-! Component-specific finite certificates apply to actual orbit paths.
The path family, restriction closure, spatial lift, bit-label bound, and
edge-to-rank transfer are proved here. Remaining hypotheses are local graph
and finite table conditions, never the desired existence of lifted paths. -/

namespace ActualJobFamily

open DecimalDigits FoldedDecimal OverflowCarryNormalization CarryHistory ActualPrefixLift
open ComponentHierarchy CondensationBound

def family {J V : Type} (graph : J → Graph V) (width : J → Nat)
    (q : Nat → Nat) (L : Nat) : JobPathFamily J V where
  valid job path n := ∃ a s, ActualPath (graph job) q L (width job) a s path n
  restrict := by
    intro job path n hvalid start length hr
    obtain ⟨a, s, hp⟩ := hvalid
    exact ⟨a + start, s + start,
      actual_path_interval (graph job) q L (width job) a s n start length path hp hr⟩

theorem actual_path_valid {J V : Type} (graph : J → Graph V) (width : J → Nat)
    (q : Nat → Nat) (L a s n : Nat) (job : J) (path : Nat → V)
    (hp : ActualPath (graph job) q L (width job) a s path n) :
    (family graph width q L).valid job path n := ⟨a, s, hp⟩

/-- The generic hierarchy's lift premise follows from checked child maps
and the actual one-column construction; it is not an extra orbit assumption. -/
theorem constructive_child_lift {J V C : Type}
    (graph : J → Graph V) (width : J → Nat) (component : J → V → C)
    (cyclic : J → C → Bool) (child : J → C → J)
    (encode : J → C → V × Fin 19 → V) (q : Nat → Nat) (L : Nat)
    (ha : Admissible L q)
    (hwidth : ∀ job c, cyclic job c = true →
      1 ≤ width job ∧ width job < L ∧ width (child job c) = width job + 1)
    (hrealize : ∀ job c, cyclic job c = true →
      Realization (BoundedPrefixLift.bounded
        (lift (select (graph job) (fun v => component job v = c))))
        (graph (child job c)) (encode job c)) :
    ∀ job path n, (family graph width q L).valid job path n → 0 < n →
      cyclic job (component job (path 0)) = true →
      (∀ i, i < n → component job (path i) = component job (path 0)) →
      ∃ lifted, (family graph width q L).valid
        (child job (component job (path 0))) lifted n := by
  intro job path n hvalid _ hc hconstant
  obtain ⟨a, s, hp⟩ := hvalid
  obtain ⟨hk0, hk, hchild⟩ := hwidth job (component job (path 0)) hc
  obtain ⟨lifted, hlift, _⟩ := BoundedPrefixLift.actual_component_interval_lifts
    (graph job) (component job) (component job (path 0)) q L (width job) a s n 0 n
    path ha hk0 hk hp (by omega) (by simpa only [Nat.zero_add] using hconstant)
  have hencoded := ActualPrefixLift.actual_path_encode _ _ _
    (hrealize job (component job (path 0)) hc)
    q L (width job + 1) (a + 0) (s + 0) n lifted hlift
  refine ⟨fun i => encode job (component job (path 0)) (lifted i), a, s, ?_⟩
  simpa only [Nat.add_zero, hchild] using hencoded

/-- Local finite vertex/edge checks imply the full actual-path bound.
No SCC algorithm correctness theorem is required by these certificate
conditions; a suitable component partition and rank are enough. -/
theorem actual_path_vertices_le {J V C : Type} [DecidableEq C]
    (graph : J → Graph V) (width : J → Nat) (component : J → V → C)
    (cyclic : J → C → Bool) (child : J → C → J)
    (encode : J → C → V × Fin 19 → V)
    (height bound : J → Nat) (rank : J → C → Nat)
    (q : Nat → Nat) (L : Nat) (ha : Admissible L q)
    (hdecrease : ∀ job c, cyclic job c = true → height (child job c) < height job)
    (hwidth : ∀ job c, cyclic job c = true →
      1 ≤ width job ∧ width job < L ∧ width (child job c) = width job + 1)
    (hrealize : ∀ job c, cyclic job c = true →
      Realization (BoundedPrefixLift.bounded
        (lift (select (graph job) (fun v => component job v = c))))
        (graph (child job c)) (encode job c))
    (hvertex : ∀ job v, (graph job).valid v →
      jobWeight cyclic child bound job (component job v) ≤ rank job (component job v) ∧
      rank job (component job v) ≤ bound job)
    (hedge : ∀ job u v c, (graph job).valid u → (graph job).valid v →
      c ≤ 1 → (graph job).edge u v c →
      (cyclic job (component job u) = false → component job u ≠ component job v) ∧
      (component job u ≠ component job v →
        jobWeight cyclic child bound job (component job u) + rank job (component job v) ≤
          rank job (component job u))) :
    ∀ job a s path n, ActualPath (graph job) q L (width job) a s path n → n ≤ bound job := by
  have hacyclic : ∀ job path n, (family graph width q L).valid job path n →
      ∀ i, i + 1 < n → cyclic job (component job (path i)) = false →
      component job (path i) ≠ component job (path (i + 1)) := by
    intro job path n hvalid i hi hc
    obtain ⟨a, s, hp⟩ := hvalid
    exact (hedge job (path i) (path (i + 1)) (label q L (width job) a i)
      (hp.vertices i (by omega)).1 (hp.vertices (i + 1) hi).1
      (BoundedPrefixLift.actual_label_bound q L (width job) a i ha) (hp.edges i hi)).1 hc
  have hcert : ∀ job path n, (family graph width q L).valid job path n →
      RankCertificate (fun i => component job (path i))
        (jobWeight cyclic child bound job) (rank job) n := by
    intro job path n hvalid
    obtain ⟨a, s, hp⟩ := hvalid
    refine ⟨?_, ?_⟩
    · intro i hi
      exact (hvertex job (path i) (hp.vertices i hi).1).1
    · intro i hi hne
      exact (hedge job (path i) (path (i + 1)) (label q L (width job) a i)
        (hp.vertices i (by omega)).1 (hp.vertices (i + 1) hi).1
        (BoundedPrefixLift.actual_label_bound q L (width job) a i ha) (hp.edges i hi)).2 hne
  have hstart : ∀ job path n, (family graph width q L).valid job path n → 0 < n →
      rank job (component job (path 0)) ≤ bound job := by
    intro job path n hvalid hn
    obtain ⟨a, s, hp⟩ := hvalid
    exact (hvertex job (path 0) (hp.vertices 0 hn).1).2
  intro job a s path n hp
  exact component_hierarchy_path_vertices_le (family graph width q L)
    component cyclic child height bound rank hdecrease
    (constructive_child_lift graph width component cyclic child encode q L ha hwidth hrealize)
    hacyclic hcert hstart job path n ⟨a, s, hp⟩

end ActualJobFamily
