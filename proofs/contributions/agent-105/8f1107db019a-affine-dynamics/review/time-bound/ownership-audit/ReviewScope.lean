import Agent105ReturnTimeBound

/-!
Independent scope checks by /root/ownership_audit, session 8f1107db019a.
The legacy CanonicalPair predicate admits [1], which cannot be pair w.
This is an interpretation boundary, not a defect in the list theorem.
-/

example : Agent8.CanonicalPair [1] := by
  simp [Agent8.CanonicalPair, Agent8.Bounded]

example (w : Agent8.Word) : Agent8.pair w ≠ [1] := by
  intro h
  have hl := congrArg List.length h
  rw [Agent8.pair_length] at hl
  cases w with
  | nil => simp at hl
  | cons x xs =>
    have hxlen : xs.length = 0 := by simp only [List.length_cons, List.length_nil] at hl; omega
    have hnil : xs = [] := List.length_eq_zero.mp hxlen
    subst xs
    have hx : x + x = 1 := by simpa [Agent8.pair, Agent8.zipAdd] using h
    omega

#check Agent105.ReturnTimeBound.orbit_width_potential_bound
#check Agent105.ReturnTimeBound.return_width_potential_bound
#check Agent105.ReturnTimeBound.return_time_bounds_of_width_gain
#check Agent105.ReturnTimeBound.positive_return_time_bound_of_width_gain
#check Agent105.ReturnTimeBound.return_time_bound_with_offset
#check Agent105.ReturnTimeBound.same_head_return_time_bound_with_offset
#check Agent105.ReturnTimeBound.word_family_return_time_bound
#check Agent105.ReturnTimeBound.affine_endpoint_return_time_bound
#check Agent105.ReturnTimeBound.affine_endpoint_return_time_bound_with_offset
