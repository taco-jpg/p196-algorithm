import P196.Agent5OrdinaryStreamPrefix.ExteriorCore

/-! Elementary suffix-trimming lemmas for the original exterior map. -/
namespace Agent19.TwoStep

open P196.Agent6

private theorem drop_phase_spec (c : Nat) (raw : List Nat) :
    ∃ q, raw = List.replicate q c ++ raw.dropWhile (fun x => x == c) := by
  induction raw with
  | nil => exact ⟨0, rfl⟩
  | cons x xs ih =>
      by_cases hx : x = c
      · subst x
        obtain ⟨q, hq⟩ := ih
        refine ⟨q + 1, ?_⟩
        calc
          c :: xs = c :: (List.replicate q c ++ xs.dropWhile (fun x => x == c)) :=
            congrArg (List.cons c) hq
          _ = List.replicate (q + 1) c ++
              (c :: xs).dropWhile (fun x => x == c) := by
            simp [List.replicate_succ, List.dropWhile_cons]
      · exact ⟨0, by simp [List.dropWhile_cons, hx]⟩

private theorem drop_phase_head (c : Nat) (raw : List Nat) :
    (raw.dropWhile (fun x => x == c)).head? ≠ some c := by
  induction raw with
  | nil => simp
  | cons x xs ih =>
      by_cases hx : x = c
      · subst x
        simpa [List.dropWhile_cons] using ih
      · simp [List.dropWhile_cons, hx]

private theorem drop_phase_idempotent (c : Nat) (raw : List Nat) :
    (raw.dropWhile (fun x => x == c)).dropWhile (fun x => x == c) =
      raw.dropWhile (fun x => x == c) := by
  induction raw with
  | nil => rfl
  | cons x xs ih =>
      by_cases hx : x = c
      · subst x
        simpa [List.dropWhile_cons] using ih
      · simp [List.dropWhile_cons, hx]

/-- The deleted suffix consists only of copies of the phase. -/
theorem trim_spec (c : Nat) (raw : List Nat) :
    ∃ q, raw = trim c raw ++ List.replicate q c := by
  obtain ⟨q, hq⟩ := drop_phase_spec c raw.reverse
  refine ⟨q, ?_⟩
  have h := congrArg List.reverse hq
  simpa [trim] using h

/-- A trimmed word never has the phase as its final surviving entry. -/
theorem trim_last (c : Nat) (raw : List Nat) :
    (trim c raw).getLast? ≠ some c := by
  simpa [trim] using drop_phase_head c raw.reverse

/-- Trimming the same phase twice has no further effect. -/
theorem trim_idempotent (c : Nat) (raw : List Nat) :
    trim c (trim c raw) = trim c raw := by
  simp only [trim, List.reverse_reverse]
  rw [drop_phase_idempotent]

/-- The final entry of a nonempty trimmed word differs from the phase. -/
theorem trim_getLast (c : Nat) (raw : List Nat) (hne : trim c raw ≠ []) :
    (trim c raw).getLast hne ≠ c := by
  intro h
  apply trim_last c raw
  rw [List.getLast?_eq_getLast hne, h]

/-- Every surviving coefficient occurred in the untrimmed word. -/
theorem mem_of_mem_trim {c x : Nat} {raw : List Nat}
    (hx : x ∈ trim c raw) : x ∈ raw := by
  obtain ⟨q, hq⟩ := trim_spec c raw
  rw [hq]
  exact List.mem_append_left _ hx

/-- Trimming preserves any upper bound on all coefficients. -/
theorem trim_bounded (bound c : Nat) (raw : List Nat)
    (h : ∀ x ∈ raw, x ≤ bound) : ∀ x ∈ trim c raw, x ≤ bound := by
  intro x hx
  exact h x (mem_of_mem_trim hx)

/-- The suffix decomposition also records its exact length. -/
theorem trim_length (c : Nat) (raw : List Nat) (q : Nat)
    (h : raw = trim c raw ++ List.replicate q c) :
    raw.length = (trim c raw).length + q := by
  exact congrArg List.length h |>.trans (by simp)

/-- A two-step return whose raw lengths grow by one removes two entries total. -/
theorem trim_two_step_count (c d : Nat) (w raw₁ raw₂ : List Nat) (q r : Nat)
    (hlen₁ : raw₁.length = w.length + 1)
    (hlen₂ : raw₂.length = (trim c raw₁).length + 1)
    (hreturn : trim d raw₂ = w)
    (hq : raw₁ = trim c raw₁ ++ List.replicate q c)
    (hr : raw₂ = trim d raw₂ ++ List.replicate r d) : q + r = 2 := by
  have hq' := trim_length c raw₁ q hq
  have hr' := trim_length d raw₂ r hr
  rw [hreturn] at hr'
  omega

#print axioms trim_spec
#print axioms trim_last
#print axioms trim_idempotent
#print axioms trim_getLast
#print axioms mem_of_mem_trim
#print axioms trim_bounded
#print axioms trim_length
#print axioms trim_two_step_count

end Agent19.TwoStep
