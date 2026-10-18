import P196.Agent5OrdinaryStreamPrefix.ExteriorCore

namespace P196.Agent6
set_option maxRecDepth 100000
set_option maxHeartbeats 0

theorem capTwo_check :
    (List.range 8).all (fun i =>
      (List.range 18).all (fun j => checkChunk 1 7 i j)) = true := by
  decide

theorem capTwo_escape (i j z : Nat) (hi : i < 8) (hj : j < 18)
    (hz : z < 19) :
    ∃ t, t ≤ 7 ∧ 2 < (iterate t (decode 1 i j z)).word.length := by
  apply checkChunk_sound 1 7 i j z hz
  exact List.all_eq_true.mp (List.all_eq_true.mp capTwo_check i
    (List.mem_range.mpr hi)) j (List.mem_range.mpr hj)

theorem capTwo_sharp :
    escapes 2 6 (decode 1 6 1 17) = false ∧
    escapes 2 7 (decode 1 6 1 17) = true := by
  decide

#print axioms capTwo_check
#print axioms capTwo_escape
#print axioms capTwo_sharp
end P196.Agent6
