import Std

/-!
# Finite returns of an endpoint map

A finite list containing every iterate supplies an explicit transient/return
bound. The list may contain duplicates. This is a finite dynamical-system
lemma; it does not assert that a particular exterior or center cycle exists.
-/

namespace Agent108.CyclicQuotientLift

universe u
variable {α : Type u}

/-- Apply `f` exactly `n` times, adding each new step at the output. -/
def iter (f : α → α) : Nat → α → α
  | 0, x => x
  | n + 1, x => f (iter f n x)

@[simp] theorem iter_zero (f : α → α) (x : α) : iter f 0 x = x := rfl

@[simp] theorem iter_succ (f : α → α) (n : Nat) (x : α) :
    iter f (n + 1) x = f (iter f n x) := rfl

/-- A prefix of `r` steps followed by `m` further steps. -/
theorem iter_add (f : α → α) (r m : Nat) (x : α) :
    iter f (r + m) x = iter f m (iter f r x) := by
  induction m with
  | zero => simp
  | succ m ih => simpa only [Nat.add_succ, iter_succ] using congrArg f ih

/-- Move one initial application of `f` into the iteration count. -/
theorem iter_shift (f : α → α) (n : Nat) (x : α) :
    iter f n (f x) = iter f (n + 1) x := by
  induction n with
  | zero => rfl
  | succ n ih => simpa only [iter_succ] using congrArg f ih

/-- Equality of two iterates persists under every common further iteration. -/
theorem iter_add_eq_of_eq (f : α → α) (x : α) {r s : Nat}
    (h : iter f r x = iter f s x) (n : Nat) :
    iter f (r + n) x = iter f (s + n) x := by
  rw [iter_add, iter_add, h]

-- Erasing the first value reduces the enumeration budget by one. This uses
-- only the standard list erase lemmas and needs no Nodup carrier hypothesis.
private theorem finite_injective_bound (carrier : List α) (a : Nat → α) (n : Nat)
    (hmem : ∀ i, i < n → a i ∈ carrier)
    (hinj : ∀ i j, i < n → j < n → a i = a j → i = j) :
    n ≤ carrier.length := by
  classical
  induction n generalizing carrier a with
  | zero => exact Nat.zero_le _
  | succ n ih =>
    have hzero : a 0 ∈ carrier := hmem 0 (by omega)
    have htail : ∀ i, i < n → a (i + 1) ∈ carrier.erase (a 0) := by
      intro i hi
      have hne : a (i + 1) ≠ a 0 := by
        intro he
        have heq := hinj (i + 1) 0 (by omega) (by omega) he
        omega
      exact (List.mem_erase_of_ne hne).mpr (hmem (i + 1) (by omega))
    have htail_inj : ∀ i j, i < n → j < n → a (i + 1) = a (j + 1) → i = j := by
      intro i j hi hj he
      have heq := hinj (i + 1) (j + 1) (by omega) (by omega) he
      omega
    have hbound := ih (carrier.erase (a 0)) (fun i => a (i + 1)) htail htail_inj
    have herase := List.length_erase_of_mem hzero
    have hpositive := List.length_pos_of_mem hzero
    omega

/-- Among the first `carrier.length + 1` iterates, two distinct indices agree. -/
theorem finite_orbit_collision (f : α → α) (x : α) (carrier : List α)
    (hmem : ∀ n, iter f n x ∈ carrier) :
    ∃ i j, i < j ∧ j ≤ carrier.length ∧ iter f j x = iter f i x := by
  classical
  apply Classical.byContradiction
  intro hcollision
  have hinj : ∀ i j, i < carrier.length + 1 → j < carrier.length + 1 →
      iter f i x = iter f j x → i = j := by
    intro i j hi hj he
    apply Classical.byContradiction
    intro hne
    by_cases hij : i < j
    · exact hcollision ⟨i, j, hij, by omega, he.symm⟩
    · exact hcollision ⟨j, i, by omega, by omega, he⟩
  have hbound := finite_injective_bound carrier (fun n => iter f n x)
    (carrier.length + 1) (fun n _ => hmem n) hinj
  omega

/-- A positive return period after a transient, bounded by the carrier length. -/
theorem finite_orbit_return (f : α → α) (x : α) (carrier : List α)
    (hmem : ∀ n, iter f n x ∈ carrier) :
    ∃ r m, 0 < m ∧ r + m ≤ carrier.length ∧ iter f (r + m) x = iter f r x := by
  obtain ⟨i, j, hij, hj, he⟩ := finite_orbit_collision f x carrier hmem
  refine ⟨i, j - i, by omega, by omega, ?_⟩
  have hindex : i + (j - i) = j := by omega
  simpa only [hindex] using he

/-- The state after the transient is periodic for the same positive period. -/
theorem finite_orbit_periodic_state (f : α → α) (x : α) (carrier : List α)
    (hmem : ∀ n, iter f n x ∈ carrier) :
    ∃ r m, 0 < m ∧ r + m ≤ carrier.length ∧
      iter f m (iter f r x) = iter f r x := by
  obtain ⟨r, m, hm, hbound, he⟩ := finite_orbit_return f x carrier hmem
  exact ⟨r, m, hm, hbound, by simpa only [iter_add] using he⟩

end Agent108.CyclicQuotientLift
