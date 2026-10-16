import ScalarHierarchyData
import JobChecks0
import JobChecks1
import JobChecks2
import JobChecks3
import JobChecks4
import JobChecks5
import JobChecks6
import JobChecks7
import JobChecks8
import JobChecks9
import JobChecks10
import JobChecks11
import JobChecks12
import JobChecks13
import JobChecks14
import JobChecks15
namespace ScalarHierarchy
open ScalarFinite ScalarJobData ActualPrefixLift
set_option maxHeartbeats 0

def encode : Job → Nat → Nat × Fin 19 → Nat
  | .j0, c => if c=0 then ScalarFinite.encode lift_certificate1 else fun _ => 0
  | .j1, c => if c=52 then ScalarFinite.encode lift_certificate2 else fun _ => 0
  | .j2, c => if c=234 then ScalarFinite.encode lift_certificate3 else if c=278 then ScalarFinite.encode lift_certificate4 else fun _ => 0
  | .j3, c => fun _ => 0
  | .j4, c => if c=173 then ScalarFinite.encode lift_certificate5 else fun _ => 0
  | .j5, c => if c=459 then ScalarFinite.encode lift_certificate6 else fun _ => 0
  | .j6, c => if c=3079 then ScalarFinite.encode lift_certificate7 else fun _ => 0
  | .j7, c => if c=5241 then ScalarFinite.encode lift_certificate8 else fun _ => 0
  | .j8, c => if c=9643 then ScalarFinite.encode lift_certificate9 else fun _ => 0
  | .j9, c => if c=10716 then ScalarFinite.encode lift_certificate10 else fun _ => 0
  | .j10, c => if c=860 then ScalarFinite.encode lift_certificate11 else fun _ => 0
  | .j11, c => if c=3350 then ScalarFinite.encode lift_certificate12 else if c=4628 then ScalarFinite.encode lift_certificate15 else fun _ => 0
  | .j12, c => if c=3239 then ScalarFinite.encode lift_certificate13 else fun _ => 0
  | .j13, c => if c=10589 then ScalarFinite.encode lift_certificate14 else fun _ => 0
  | .j14, c => fun _ => 0
  | .j15, c => fun _ => 0

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
  · exact checked_rank15

theorem realizes (j : Job) (c : Nat) (hc : cyclic j c=true) :
    Realization (BoundedPrefixLift.bounded (ActualPrefixLift.lift (ActualPrefixLift.select (graph j) (fun v => component j v=c)))) (graph (child j c)) (encode j c) := by
  cases j
  · by_cases h0 : c=0
    · subst c
      exact lift_complete1
    · simp [cyclic, ranking, ranking0, childCode0, h0] at hc
  · by_cases h0 : c=52
    · subst c
      exact lift_complete2
    · simp [cyclic, ranking, ranking1, childCode1, h0] at hc
  · by_cases h0 : c=234
    · subst c
      exact lift_complete3
    · by_cases h1 : c=278
      · subst c
        exact lift_complete4
      · simp [cyclic, ranking, ranking2, childCode2, h0, h1] at hc
  · simp [cyclic, ranking, ranking3, childCode3] at hc
  · by_cases h0 : c=173
    · subst c
      exact lift_complete5
    · simp [cyclic, ranking, ranking4, childCode4, h0] at hc
  · by_cases h0 : c=459
    · subst c
      exact lift_complete6
    · simp [cyclic, ranking, ranking5, childCode5, h0] at hc
  · by_cases h0 : c=3079
    · subst c
      exact lift_complete7
    · simp [cyclic, ranking, ranking6, childCode6, h0] at hc
  · by_cases h0 : c=5241
    · subst c
      exact lift_complete8
    · simp [cyclic, ranking, ranking7, childCode7, h0] at hc
  · by_cases h0 : c=9643
    · subst c
      exact lift_complete9
    · simp [cyclic, ranking, ranking8, childCode8, h0] at hc
  · by_cases h0 : c=10716
    · subst c
      exact lift_complete10
    · simp [cyclic, ranking, ranking9, childCode9, h0] at hc
  · by_cases h0 : c=860
    · subst c
      exact lift_complete11
    · simp [cyclic, ranking, ranking10, childCode10, h0] at hc
  · by_cases h0 : c=3350
    · subst c
      exact lift_complete12
    · by_cases h1 : c=4628
      · subst c
        exact lift_complete15
      · simp [cyclic, ranking, ranking11, childCode11, h0, h1] at hc
  · by_cases h0 : c=3239
    · subst c
      exact lift_complete13
    · simp [cyclic, ranking, ranking12, childCode12, h0] at hc
  · by_cases h0 : c=10589
    · subst c
      exact lift_complete14
    · simp [cyclic, ranking, ranking13, childCode13, h0] at hc
  · simp [cyclic, ranking, ranking14, childCode14] at hc
  · simp [cyclic, ranking, ranking15, childCode15] at hc

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
    (hp : ActualPath (ScalarFinite.graph data0) q L 1 a s path n) : n ≤ 659 := by
  exact ActualJobFamily.actual_path_vertices_le graph width component cyclic child encode
    height bound rank q L ha height_decreases (width_valid L hL) realizes
    vertex_bounds edge_bounds Job.j0 a s path n hp

end ScalarHierarchy
