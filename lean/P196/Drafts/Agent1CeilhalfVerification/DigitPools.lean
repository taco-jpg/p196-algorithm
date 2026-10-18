import P196.Drafts.Agent1CeilhalfVerification.PalindromeDigits
import P196.Drafts.Agent1CeilhalfVerification.PairWeights

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

theorem positions_endpoint (s r n i : Nat)
    (hi : i ∈ positions s r n) : i + r ≤ s + r * n := by
  induction n generalizing s with
  | zero => simp [positions] at hi
  | succ n ih =>
    simp only [positions, List.mem_cons] at hi
    rw [Nat.mul_succ]
    rcases hi with rfl | hi
    · omega
    · have hb := ih (s + r) hi
      omega

theorem residuePool_bounds (k r a n q i : Nat) (hr : 0 < r)
    (hn : n ≤ q) (hi : i ∈ residuePool k r a n) :
    k ≤ i ∧ i < k + q * r := by
  have hb := positions_bounds (alignIndex k r a) r n i hr hi
  have he := positions_endpoint (alignIndex k r a) r n i hi
  have ha := alignIndex_bounds k r a hr
  have hm : r*n ≤ q*r := by
    simpa [Nat.mul_comm] using Nat.mul_le_mul_left r hn
  omega

def selectedPositions (k q r x y : Nat) : List Nat :=
  residuePool k r 0 x ++ residuePool (k + q*r) r 1 y

theorem selectedPositions_nodup (k q r x y : Nat) (hr : 0 < r)
    (hx : x ≤ q) : (selectedPositions k q r x y).Nodup := by
  change List.Pairwise (fun a b : Nat => a ≠ b) (_ ++ _)
  apply List.pairwise_append.mpr
  refine ⟨positions_nodup _ _ _ hr, positions_nodup _ _ _ hr, ?_⟩
  intro i hi j hj
  have hl := residuePool_bounds k r 0 x q i hr hx hi
  have hjb := positions_bounds (alignIndex (k+q*r) r 1) r y j hr hj
  have hja := alignIndex_bounds (k+q*r) r 1 hr
  omega

theorem selectedPositions_bounds (k q r x y L i : Nat) (hr : 0 < r)
    (hx : x ≤ q) (hy : y ≤ q) (hL : 2*k+4*q*r ≤ L)
    (hi : i ∈ selectedPositions k q r x y) :
    k ≤ i ∧ i < L-1-i := by
  have htwo : 4*q*r = 4*(q*r) := by simp [Nat.mul_assoc]
  simp only [selectedPositions, List.mem_append] at hi
  rcases hi with hi | hi
  · have hb := residuePool_bounds k r 0 x q i hr hx hi
    omega
  · have hb := residuePool_bounds (k+q*r) r 1 y q i hr hy hi
    omega

theorem selectedPositions_lower (k q r x y L : Nat) (hr : 0 < r)
    (hx : x ≤ q) (hy : y ≤ q) (hL : 2*k+4*q*r ≤ L) :
    LowerPositions k L (selectedPositions k q r x y) := by
  intro i hi
  exact selectedPositions_bounds k q r x y L i hr hx hy hL hi

/-- The explicit pools instantiate the genuine decimal realization theorem. -/
theorem residue_pools_realize (A k L u q r x y : Nat)
    (hk : 0 < k) (hr : 0 < r) (hL : 2*k+4*q*r ≤ L)
    (hA : A < 10^k) (hA0 : A%10 ≠ 0) (hu : u ∣ 10^k)
    (hx : x ≤ q) (hy : y ≤ q) (hperiod : 10^r%q=1%q) :
    ∃ P d, DecimalDigits.Canonical P d L ∧ Lychrel196.Palindrome P ∧
      P%u=A%u ∧ P%q=(outerValue A k L+x*pairWeight0 L+y*pairWeight1 L)%q := by
  have hL2 : 2 ≤ L := by omega
  have hlow := selectedPositions_lower k q r x y L hr hx hy hL
  have hnodup := selectedPositions_nodup k q r x y hr hx
  have hc0 : ∀ i, i ∈ residuePool k r 0 x → pairValue L i%q=pairWeight0 L%q := by
    intro i hi
    have hb := hlow i (List.mem_append_left _ hi)
    have hm := residuePool_mod k r 0 x i hr hi
    exact mirrored_weight_mod_zero q r L i (by omega) hperiod (by simpa using hm)
  have hc1 : ∀ i, i ∈ residuePool (k+q*r) r 1 y → pairValue L i%q=pairWeight1 L%q := by
    intro i hi
    have hb := hlow i (List.mem_append_right _ hi)
    exact mirrored_weight_mod_one q r L i hL2 (by omega) hperiod
      (residuePool_mod (k+q*r) r 1 y i hr hi)
  have ht := two_pool_realization A k L u q (pairWeight0 L) (pairWeight1 L)
    (residuePool k r 0 x) (residuePool (k+q*r) r 1 y) hk (by omega) hA hA0 hu
    hnodup hlow hc0 hc1
  simpa only [residuePool, positions_length] using ht

#print axioms alignIndex_bounds
#print axioms alignIndex_mod
#print axioms positions_length
#print axioms positions_bounds
#print axioms positions_mod
#print axioms positions_nodup
#print axioms residuePool_mod
#print axioms positions_endpoint
#print axioms residuePool_bounds
#print axioms selectedPositions_nodup
#print axioms selectedPositions_bounds
#print axioms selectedPositions_lower
#print axioms residue_pools_realize

end ExactLengthResidues
