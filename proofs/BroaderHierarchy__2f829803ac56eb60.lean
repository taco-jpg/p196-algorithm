import BroaderHierarchyData
import BJobChecks0
import BJobChecks1
import BJobChecks2
import BJobChecks3
import BJobChecks4
import BJobChecks5
import BJobChecks6
import BJobChecks7
import BJobChecks8
import BJobChecks9
import BJobChecks10
import BJobChecks11
import BJobChecks12
import BJobChecks13
import BJobChecks14
namespace BroaderHierarchy
open ScalarFinite BroaderJobData ActualPrefixLift
set_option maxHeartbeats 0

def encode : Job → Nat → Nat × Fin 19 → Nat
  | .j0, c => if c=0 then ScalarFinite.encode lift_certificate1 else fun _ => 0
  | .j1, c => if c=153 then ScalarFinite.encode lift_certificate2 else if c=180 then ScalarFinite.encode lift_certificate3 else fun _ => 0
  | .j2, c => fun _ => 0
  | .j3, c => if c=117 then ScalarFinite.encode lift_certificate4 else fun _ => 0
  | .j4, c => if c=459 then ScalarFinite.encode lift_certificate5 else fun _ => 0
  | .j5, c => if c=3079 then ScalarFinite.encode lift_certificate6 else fun _ => 0
  | .j6, c => if c=5241 then ScalarFinite.encode lift_certificate7 else fun _ => 0
  | .j7, c => if c=9643 then ScalarFinite.encode lift_certificate8 else fun _ => 0
  | .j8, c => if c=10716 then ScalarFinite.encode lift_certificate9 else fun _ => 0
  | .j9, c => if c=860 then ScalarFinite.encode lift_certificate10 else fun _ => 0
  | .j10, c => if c=3350 then ScalarFinite.encode lift_certificate11 else if c=4628 then ScalarFinite.encode lift_certificate14 else fun _ => 0
  | .j11, c => if c=3239 then ScalarFinite.encode lift_certificate12 else fun _ => 0
  | .j12, c => if c=10589 then ScalarFinite.encode lift_certificate13 else fun _ => 0
  | .j13, c => fun _ => 0
  | .j14, c => fun _ => 0

theorem checked (j : Job) : CheckedRank (data j) (ranking j) := by
  cases j
  · exact checked_rank0
  · exact checked_rank1
  · exact checked_rank2
  · exact checked_rank3
  · exact checked_rank4
  · exact checked_rank5
  · exact checked_rank6
  · exact checked_rank7
  · exact checked_rank8
  · exact checked_rank9
  · exact checked_rank10
  · exact checked_rank11
  · exact checked_rank12
  · exact checked_rank13
  · exact checked_rank14

theorem realizes (j : Job) (c : Nat) (hc : cyclic j c=true) :
    Realization (BoundedPrefixLift.bounded (ActualPrefixLift.lift (ActualPrefixLift.select (graph j) (fun v => component j v=c)))) (graph (child j c)) (encode j c) := by
  cases j
  · by_cases h0 : c=0
    · subst c
      exact lift_complete1
    · simp [cyclic, ranking, ranking0, childCode0, h0] at hc
  · by_cases h0 : c=153
    · subst c
      exact lift_complete2
    · by_cases h1 : c=180
      · subst c
        exact lift_complete3
      · simp [cyclic, ranking, ranking1, childCode1, h0, h1] at hc
  · simp [cyclic, ranking, ranking2, childCode2] at hc
  · by_cases h0 : c=117
    · subst c
      exact lift_complete4
    · simp [cyclic, ranking, ranking3, childCode3, h0] at hc
  · by_cases h0 : c=459
    · subst c
      exact lift_complete5
    · simp [cyclic, ranking, ranking4, childCode4, h0] at hc
  · by_cases h0 : c=3079
    · subst c
      exact lift_complete6
    · simp [cyclic, ranking, ranking5, childCode5, h0] at hc
  · by_cases h0 : c=5241
    · subst c
      exact lift_complete7
    · simp [cyclic, ranking, ranking6, childCode6, h0] at hc
  · by_cases h0 : c=9643
    · subst c
      exact lift_complete8
    · simp [cyclic, ranking, ranking7, childCode7, h0] at hc
  · by_cases h0 : c=10716
    · subst c
      exact lift_complete9
    · simp [cyclic, ranking, ranking8, childCode8, h0] at hc
  · by_cases h0 : c=860
    · subst c
      exact lift_complete10
    · simp [cyclic, ranking, ranking9, childCode9, h0] at hc
  · by_cases h0 : c=3350
    · subst c
      exact lift_complete11
    · by_cases h1 : c=4628
      · subst c
        exact lift_complete14
      · simp [cyclic, ranking, ranking10, childCode10, h0, h1] at hc
  · by_cases h0 : c=3239
    · subst c
      exact lift_complete12
    · simp [cyclic, ranking, ranking11, childCode11, h0] at hc
  · by_cases h0 : c=10589
    · subst c
      exact lift_complete13
    · simp [cyclic, ranking, ranking12, childCode12, h0] at hc
  · simp [cyclic, ranking, ranking13, childCode13] at hc
  · simp [cyclic, ranking, ranking14, childCode14] at hc

theorem vertex_bounds (j : Job) (v : Nat) (hv : (graph j).valid v) :
    ComponentHierarchy.jobWeight cyclic child bound j (component j v) ≤ rank j (component j v) ∧
    rank j (component j v) ≤ bound j := by
  rw [weight_eq, ← bound_eq]
  exact checked_vertex_bounds (checked j) v hv

theorem edge_bounds (j : Job) (u v bit : Nat)
    (hu : (graph j).valid u) (hv : (graph j).valid v)
    (_hb : bit ≤ 1) (he : (graph j).edge u v bit) :
    (cyclic j (component j u)=false → component j u ≠ component j v) ∧
    (component j u ≠ component j v →
      ComponentHierarchy.jobWeight cyclic child bound j (component j u)+rank j (component j v) ≤
      rank j (component j u)) := by
  rw [weight_eq]
  exact checked_edge_bounds (checked j) u v bit hu hv he

open DecimalDigits FoldedDecimal OverflowCarryNormalization CarryHistory

theorem finite_root_bound (q : Nat → Nat) (L a s n : Nat) (path : Nat → Nat)
    (ha : Admissible L q) (hL : 14 ≤ L)
    (hp : ActualPath (ScalarFinite.graph data0) q L 2 a s path n) : n ≤ 636 := by
  exact ActualJobFamily.actual_path_vertices_le graph width component cyclic child encode
    height bound rank q L ha height_decreases (width_valid L hL) realizes
    vertex_bounds edge_bounds Job.j0 a s path n hp

end BroaderHierarchy
