import OuterBridge

namespace Agent116.Exterior
open Agent109
open P196.Agent7.Finite (Outer outerNext stripSuffix)
set_option maxHeartbeats 0

/-- Moving one final phase letter into the band appends precisely one new phase
letter to the untrimmed returned exterior. -/
theorem Br_append_phase (c : Nat) (B A C : Word) (hc : Phase c) (hB : Bounded B) :
    Br c (B ++ [c]) A C = Br c B A C ++ [tOf c + tOf c] := by
  have hc18 : c ≤ 18 := by have := hc.2.1; omega
  have hcnine := hc.2.2
  have he := norm_carry_le B 0 hB (by decide)
  have hleft : norm (B ++ [c]) 0 =
      ((norm B 0).1 ++ [c + (norm B 0).2 - 10 * kOf c], kOf c) := by
    rw [norm_append]
    have hb := norm_band c 0 (norm B 0).2 hc18 hcnine he
    simpa using congrArg (fun p : Word × Nat => ((norm B 0).1 ++ p.1, p.2)) hb
  have hr0 : norm [c] (kOf c) = ([tOf c], kOf c) := by
    exact norm_band_tail c 1 hc18
  have hright : norm (B ++ [c]).reverse (kOf c) =
      ([tOf c] ++ (norm B.reverse (kOf c)).1, (norm B.reverse (kOf c)).2) := by
    rw [List.reverse_append]
    simp only [List.reverse_cons, List.reverse_nil, List.nil_append]
    rw [norm_append, hr0]
  have hut : c + kOf c - 10 * kOf c = tOf c := by
    unfold tOf kOf; split <;> omega
  simp only [Br, data, u0]
  simp only [data, hleft, hright]
  simp only [List.reverse_append, List.reverse_cons, List.reverse_nil,
    List.nil_append, hut]
  by_cases hγ : (norm B.reverse (kOf c)).2 = 0
  · simp only [hγ, if_true]
    rw [zipAdd_append _ _ _ _ (by simp [norm_length])]
    rfl
  · simp only [hγ, if_false]
    rw [← List.append_assoc [1] _ [tOf c]]
    rw [zipAdd_append _ _ _ _ (by simp [norm_length])]
    rfl

#print axioms Br_append_phase
end Agent116.Exterior
