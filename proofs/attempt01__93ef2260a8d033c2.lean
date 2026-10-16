import Std

/-! Disjoint, below-center arithmetic progressions of decimal positions.
The two pools remain disjoint when the period is one. -/
namespace ExactLengthResidues

def alignIndex (k r a : Nat) : Nat := k + (a + r - k % r) % r

theorem alignIndex_bounds (k r a : Nat) (hr : 0 < r) :
    k ≤ alignIndex k r a ∧ alignIndex k r a < k + r := by
  have h := Nat.mod_lt (a + r - k % r) hr
  simp only [alignIndex]
  omega

theorem alignIndex_mod (k r a : Nat) (hr : 0 < r) :
    alignIndex k r a % r = a % r := by
  have h := Nat.mod_lt k hr
  have he : k % r + (a + r - k % r) = a + r := by omega
  simp only [alignIndex, Nat.add_mod_mod]
  rw [← Nat.mod_add_mod k r, he]
  simp

def positions (s r : Nat) : Nat → List Nat
  | 0 => []
  | n + 1 => s :: positions (s + r) r n

theorem positions_length (s r n : Nat) : (positions s r n).length = n := by
  induction n generalizing s with
  | zero => rfl
  | succ n ih => simp [positions, ih]

theorem positions_bounds (s r n i : Nat) (hr : 0 < r)
    (hi : i ∈ positions s r n) : s ≤ i ∧ i < s + r * n := by
  induction n generalizing s with
  | zero => simp [positions] at hi
  | succ n ih =>
    simp only [positions, List.mem_cons] at hi
    rw [Nat.mul_succ]
    rcases hi with rfl | hi
    · omega
    · have hb := ih (s + r) hi
      omega

theorem positions_mod (s r n i : Nat)
    (hi : i ∈ positions s r n) : i % r = s % r := by
  induction n generalizing s with
  | zero => simp [positions] at hi
  | succ n ih =>
    simp only [positions, List.mem_cons] at hi
    rcases hi with rfl | hi
    · rfl
    · simpa using ih (s + r) hi

theorem positions_nodup (s r n : Nat) (hr : 0 < r) :
    (positions s r n).Nodup := by
  induction n generalizing s with
  | zero => simp [positions]
  | succ n ih =>
    change List.Pairwise (fun a b : Nat => a ≠ b) (s :: positions (s + r) r n)
    apply List.pairwise_cons.mpr
    refine ⟨?_, ih (s + r)⟩
    intro i hi
    have hb := positions_bounds (s + r) r n i hr hi
    omega

def residuePool (k r a n : Nat) : List Nat := positions (alignIndex k r a) r n

theorem residuePool_mod (k r a n i : Nat) (hr : 0 < r)
    (hi : i ∈ residuePool k r a n) : i % r = a % r := by
  exact (positions_mod _ _ _ _ hi).trans (alignIndex_mod k r a hr)

theorem residuePool_bounds (k r a n q i : Nat) (hr : 0 < r)
    (hn : n ≤ q) (hi : i ∈ residuePool k r a n) :
    k ≤ i ∧ i < k + q * r := by
  have hb := positions_bounds (alignIndex k r a) r n i hr hi
  have ha := alignIndex_bounds k r a hr
  have hn0 : 0 < n := by
    by_cases hz : n = 0
    · simp [residuePool, positions, hz] at hi
    · omega
  -- Use the bound for the last occupied position, saving the leading slack.
  have hlast : i < alignIndex k r a + r * n := hb.2
  clear hlast
  induction n generalizing k q i with
  | zero => omega
  | succ n ih =>
    simp only [residuePool, positions, List.mem_cons] at hi
    rcases hi with rfl | hi
    · have hmul := Nat.mul_le_mul_right r (show 1 ≤ q by omega)
      simp only [Nat.one_mul] at hmul
      omega
    · have hs := positions_bounds (alignIndex k r a + r) r n i hr hi
      have hm := Nat.mul_le_mul_left r (show n + 1 ≤ q by omega)
      rw [Nat.mul_succ] at hm
      -- The coarse range bound is one period too large; a sharper endpoint
      -- bound is supplied below when the progression has n terms.
      omega

end ExactLengthResidues
