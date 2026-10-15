import ReturnCertificate

namespace Agent112.Admissibility
open Agent109 Agent109.Cert

theorem pair_wrap (a b : Nat) (w : Word) :
    pair ([a] ++ w ++ [b]) = [a + b] ++ pair w ++ [a + b] := by
  unfold pair
  simp only [List.reverse_append, List.reverse_cons, List.reverse_nil, List.nil_append, List.append_assoc]
  rw [zipAdd_append _ _ _ _ (by simp),
      zipAdd_append _ _ _ _ (by simp)]
  simp [zipAdd, Nat.add_comm]

theorem pair_mirr (w : Word) : Mirr (pair w) := by
  have aux : ∀ n, ∀ v : Word, v.length = n → Mirr (pair v) := by
    intro n
    induction n using Nat.strongRecOn with
    | ind n ih =>
      intro v hv
      cases v with
      | nil => exact Mirr.nil
      | cons a v =>
        cases he : v.reverse with
        | nil =>
          have hvnil : v = [] := by simpa using congrArg List.reverse he
          subst v
          exact Mirr.single (a + a) (by omega)
        | cons b r =>
          have hvr : v = r.reverse ++ [b] := by
            simpa using congrArg List.reverse he
          have hsmall : r.reverse.length < n := by
            simp only [List.length_cons, hvr, List.length_append,
              List.length_reverse, List.length_singleton, List.length_nil] at hv
            simp only [List.length_reverse]
            omega
          have hm := ih r.reverse.length hsmall r.reverse rfl
          rw [hvr]
          change Mirr (pair ([a] ++ r.reverse ++ [b]))
          rw [pair_wrap]
          exact Mirr.wrap (a + b) _ hm
  exact aux w.length w rfl

theorem mirr_unwrap (a : Nat) (w : Word)
    (h : Mirr ([a] ++ w ++ [a])) : Mirr w := by
  generalize he : [a] ++ w ++ [a] = v at h
  cases h with
  | nil => simp at he
  | single m hm =>
    have := congrArg List.length he
    simp at this
  | wrap b q hq =>
    have hc : a = b ∧ w ++ [a] = q ++ [b] := by simpa using he
    rcases hc with ⟨rfl, hc⟩
    have : w = q := List.append_cancel_right hc
    simpa [this] using hq

theorem mirr_trim (a k : Nat) (w : Word)
    (h : Mirr (List.replicate k a ++ w ++ List.replicate k a)) : Mirr w := by
  induction k with
  | zero => simpa using h
  | succ k ih =>
    apply ih
    apply mirr_unwrap a
    have he : List.replicate (k + 1) a ++ w ++ List.replicate (k + 1) a =
        [a] ++ (List.replicate k a ++ w ++ List.replicate k a) ++ [a] := by
      change (a :: List.replicate k a) ++ w ++ List.replicate (k + 1) a = _
      rw [List.replicate_succ']
      simp [List.append_assoc]
    rw [he] at h
    exact h

/-- The exact raw center of one step is always mirrored with an even middle,
regardless of the symmetry of the previous center. -/
theorem raw_center_mirr (c : Nat) (B A C : Word) : Mirr (Cr c B A C) := by
  unfold Cr
  split <;> exact pair_mirr _

/-- Every center in a nonempty accepted cyclic state list inherits the mirrored
shape from its predecessor. This is not an extra certificate hypothesis. -/
theorem valid_center_mirr (cert : Certificate) (hv : Valid cert)
    (i : Nat) (hi : i < cert.P) : Mirr (cert.st i).C := by
  have hpred : ∃ j, j < cert.P ∧ (j + 1) % cert.P = i := by
    cases i with
    | zero =>
      refine ⟨cert.P - 1, by omega, ?_⟩
      have hp : cert.P - 1 + 1 = cert.P := by omega
      rw [hp, Nat.mod_self]
    | succ i =>
      exact ⟨i, by omega, Nat.mod_eq_of_lt hi⟩
  obtain ⟨j, hj, hnext⟩ := hpred
  have hl := hv.2 j hj
  obtain ⟨_, _, _, _, _, _, _, hCr, _⟩ := hl
  have hm := raw_center_mirr (cert.st j).c (cert.st j).B (cert.st j).A (cert.st j).C
  rw [hCr] at hm
  have hs := mirr_trim (18 - (cert.st ((j + 1) % cert.P)).c) (cert.lk j).k
    (cert.st ((j + 1) % cert.P)).C hm
  simpa [hnext] using hs

/-- Reconstruct the exact finite split expected by the existing admissibility
checker from the inductive mirrored-word predicate. -/
theorem mirr_split (w : Word) (hw : Mirr w) :
    ∃ H M : Word, w = H ++ M ++ H.reverse ∧
      M.length ≤ 1 ∧ (∀ m ∈ M, m % 2 = 0) := by
  induction hw with
  | nil => exact ⟨[], [], rfl, by simp, by simp⟩
  | single m hm => exact ⟨[], [m], rfl, by simp, by simpa using hm⟩
  | wrap a q hq ih =>
    obtain ⟨H, M, he, hlen, heven⟩ := ih
    refine ⟨a :: H, M, ?_, hlen, heven⟩
    simp [he, List.append_assoc]

theorem valid_center_split (cert : Certificate) (hv : Valid cert)
    (i : Nat) (hi : i < cert.P) :
    ∃ H M : Word, (cert.st i).C = H ++ M ++ H.reverse ∧
      M.length ≤ 1 ∧ (∀ m ∈ M, m % 2 = 0) :=
  mirr_split _ (valid_center_mirr cert hv i hi)

/-- The center portion of Admissible0 is redundant. At this checkpoint the
positive-head premise remains explicit and has not yet been removed. -/
theorem admissible_of_valid_head (cert : Certificate) (hv : Valid cert)
    (hB : ∀ b, (cert.st 0).B.head? = some b → 0 < b) :
    ∃ H M, Admissible0 cert H M := by
  obtain ⟨H, M, he, hlen, heven⟩ := valid_center_split cert hv 0 hv.1
  exact ⟨H, M, he, hlen, heven, hB⟩

theorem certificate_existence_of_head (cert : Certificate) (hc : check cert = true)
    (hB : ∀ b, (cert.st 0).B.head? = some b → 0 < b) :
    ∃ m, ∀ k, ¬ Palindrome (orbit m k) := by
  obtain ⟨H, M, ha⟩ := admissible_of_valid_head cert (check_sound cert hc) hB
  exact certificate_existence cert hc H M (by simpa using ha)

end Agent112.Admissibility

#print axioms Agent112.Admissibility.pair_wrap
#print axioms Agent112.Admissibility.pair_mirr
#print axioms Agent112.Admissibility.mirr_unwrap
#print axioms Agent112.Admissibility.mirr_trim

#print axioms Agent112.Admissibility.raw_center_mirr
#print axioms Agent112.Admissibility.valid_center_mirr
#print axioms Agent112.Admissibility.mirr_split
#print axioms Agent112.Admissibility.valid_center_split
#print axioms Agent112.Admissibility.admissible_of_valid_head
#print axioms Agent112.Admissibility.certificate_existence_of_head
