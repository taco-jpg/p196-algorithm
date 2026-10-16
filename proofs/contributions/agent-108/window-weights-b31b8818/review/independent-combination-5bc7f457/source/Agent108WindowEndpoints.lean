import Agent108WindowProducts

/-!
Agent #108, session b31b8818, endpoint window bookkeeping for the existing
fixed-window incoming-weight obstruction.  Complete unpadded windows are
retained, including every short-center and empty-buffer case.
-/

namespace Agent108.WindowWeights

/-- Windows still meeting the distinguished endpoint letter, with the exact
number of terminal eighteens available in the unpadded word. -/
theorem endpoint_window_cross (b k a j : Nat) (hjb : j ≤ b) (hjk : j ≤ k) :
    ((endpoint b k a).drop j).take (b+1) =
      List.replicate (b-j) 9 ++ [a] ++ List.replicate j 18 := by
  simp only [endpoint, buffer, List.append_assoc, List.singleton_append]
  rw [List.drop_append_of_le_length (by simpa using hjb), List.drop_replicate,
    List.take_append_eq_append_take]
  simp only [List.take_replicate, List.length_replicate]
  have hmin : min (b+1) (b-j) = b-j := Nat.min_eq_right (by omega)
  have hsub : b+1-(b-j) = j+1 := by omega
  rw [hmin, hsub, List.take_succ_cons, List.take_replicate, Nat.min_eq_left hjk]

/-- Every later complete window lies wholly in the terminal eighteen block. -/
theorem endpoint_window_tail (b k a j : Nat) (hjb : b < j) (hjk : j ≤ k) :
    ((endpoint b k a).drop j).take (b+1) = List.replicate (b+1) 18 := by
  have he : endpoint b k a = (buffer b ++ [a]) ++ List.replicate k 18 := by
    simp [endpoint]
  have hj : j = (buffer b ++ [a]).length + (j-(b+1)) := by
    simp only [buffer, List.length_append, List.length_replicate,
      List.length_cons, List.length_nil]
    omega
  rw [he, hj, List.drop_append, List.drop_replicate, List.take_replicate]
  have hb : b+1 ≤ k-(j-(b+1)) := by omega
  rw [Nat.min_eq_left hb]

/-- Exact endpoint-window decomposition for every buffer and terminal length.
No hypothesis k>=b is inserted: min k b and k-b retain both short-center cases. -/
theorem endpoint_windows (b k a : Nat) :
    windows (b+1) (endpoint b k a) =
      (List.range (min k b + 1)).map
        (fun j => List.replicate (b-j) 9 ++ [a] ++ List.replicate j 18) ++
      List.replicate (k-b) (List.replicate (b+1) 18) := by
  rw [windows_eq_range_map]
  have hn : (endpoint b k a).length - b = k+1 := by
    simp only [endpoint, buffer, List.length_append, List.length_replicate,
      List.length_cons, List.length_nil]
    omega
  rw [hn]
  have hs : k+1 = (min k b + 1) + (k-b) := by omega
  rw [hs, List.range_add, List.map_append, List.map_map]
  congr 1
  · apply List.map_congr_left
    intro j hj
    have hh := List.mem_range.mp hj
    exact endpoint_window_cross b k a j (by omega) (by omega)
  · calc
      (List.range (k-b)).map
          ((fun j => ((endpoint b k a).drop j).take (b+1)) ∘
            (fun j => min k b + 1 + j)) =
          (List.range (k-b)).map (fun _ => List.replicate (b+1) 18) := by
        apply List.map_congr_left
        intro j hj
        have hh := List.mem_range.mp hj
        exact endpoint_window_tail b k a (min k b + 1 + j) (by omega) (by omega)
      _ = List.replicate (k-b) (List.replicate (b+1) 18) := by
        rw [List.map_const', List.length_range]

#print axioms endpoint_window_cross
#print axioms endpoint_window_tail
#print axioms endpoint_windows

end Agent108.WindowWeights
