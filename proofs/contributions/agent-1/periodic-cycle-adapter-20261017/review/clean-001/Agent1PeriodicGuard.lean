import Agent1PeriodicSlices

/-!
Spatial guard extraction for a single original decimal pair-word transition.
The structural zipper lemmas use the original `Agent8.zipAdd` and `pair`.
No arithmetic copies, future interface returns, or safety invariants are used.
-/

namespace Agent1.Periodic

open Agent8 Agent1.RepeatedBlock

theorem pow_append (w : Word) (m n : Nat) :
    pow w (m + n) = pow w m ++ pow w n := by
  induction m with
  | zero => simp [pow]
  | succ m ih => simp [Nat.succ_add, pow, ih, List.append_assoc]

theorem pow_succ_right (w : Word) (n : Nat) :
    pow w (n + 1) = pow w n ++ w := by
  rw [pow_append]
  simp [pow]

theorem pow_reverse (w : Word) (n : Nat) :
    (pow w n).reverse = pow w.reverse n := by
  induction n with
  | zero => rfl
  | succ n ih => rw [pow, List.reverse_append, ih, pow_succ_right]

theorem zipAdd_append_eq (a a' b b' : Word) (h : a.length = b.length) :
    zipAdd (a ++ a') (b ++ b') = zipAdd a b ++ zipAdd a' b' := by
  simp only [zipAdd_eq_zipWith]
  exact List.zipWith_append h

theorem zipAdd_length_eq (a b : Word) (h : a.length = b.length) :
    (zipAdd a b).length = a.length := by
  simp [zipAdd_eq_zipWith, List.length_zipWith, h]

theorem zipAdd_comm_eq (a b : Word) : zipAdd a b = zipAdd b a := by
  simp only [zipAdd_eq_zipWith]
  rw [List.zipWith_comm]
  simp only [Nat.add_comm]

theorem zipAdd_reverse_eq (a b : Word) (h : a.length = b.length) :
    (zipAdd a b).reverse = zipAdd a.reverse b.reverse := by
  simp only [zipAdd_eq_zipWith]
  exact List.reverse_zipWith h

theorem zipAdd_pow (a b : Word) (n : Nat) (h : a.length = b.length) :
    zipAdd (pow a n) (pow b n) = pow (zipAdd a b) n := by
  induction n with
  | zero => rfl
  | succ n ih => rw [pow, pow, zipAdd_append_eq _ _ _ _ h, ih, pow]

/-- Moving a fixed prefix past any number of periods rotates that period. -/
theorem pow_rotate_append (p s : Word) (n : Nat) :
    pow (p ++ s) n ++ p = p ++ pow (s ++ p) n := by
  induction n with
  | zero => simp [pow]
  | succ n ih =>
    simp only [pow, List.append_assoc]
    rw [ih]

/-- Pairing three pieces with equally long exteriors leaves the middle paired
with itself and makes the right exterior the reverse of the left one. -/
theorem pair_three_parts (l m r : Word) (h : l.length = r.length) :
    pair (l ++ m ++ r) =
      zipAdd l r.reverse ++ pair m ++ (zipAdd l r.reverse).reverse := by
  have hl : l.length = r.reverse.length := by simpa using h
  have hm : m.length = m.reverse.length := by simp
  have hr : zipAdd r l.reverse = (zipAdd l r.reverse).reverse := by
    rw [zipAdd_reverse_eq l r.reverse hl, List.reverse_reverse, zipAdd_comm_eq]
  simp only [pair, List.reverse_append]
  rw [List.append_assoc l m r,
    zipAdd_append_eq l (m ++ r) r.reverse (m.reverse ++ l.reverse) hl,
    zipAdd_append_eq m r m.reverse l.reverse hm, hr]
  simp only [List.append_assoc]

/-- The fixed exterior after pairing the digit guards. -/
def zipperOuter (A V Z : Word) (g : Nat) : Word :=
  zipAdd A (Z.reverse ++ (V.drop g).reverse)

/-- The repeated paired block; the right digit period is rotated by the actual
terminal-carry displacement. -/
def zipperPeriod (U V : Word) (g : Nat) : Word :=
  zipAdd U ((V.take g).reverse ++ (V.drop g).reverse)

/-- The center absorbs one full period and the reflected displacement. -/
def zipperCenter (U C V : Word) (g : Nat) : Word :=
  pair (U ++ C ++ V.take g)

/-- Exact spatial zipper identity. The five digit-block lengths determine the
guard widths; the displacement is retained explicitly instead of chosen freely. -/
theorem pair_periodic_digits (A U C V Z : Word) (b h g n : Nat)
    (hA : A.length = b + 4) (hU : U.length = 4)
    (hC : C.length = h + 4) (hV : V.length = 4)
    (hZ : Z.length = b + g) (hg : g ≤ 4) :
    pair (A ++ pow U (n+2) ++ C ++ pow V (n+2) ++ Z) =
      periodicWord (zipperOuter A V Z g) (zipperCenter U C V g)
        (zipperPeriod U V g) (n+1) := by
  let t := V.take g
  let d := V.drop g
  let l := A ++ pow U (n+1)
  let m := U ++ C ++ t
  let r := d ++ pow V (n+1) ++ Z
  have ht : t.length = g := by simp [t, hV, Nat.min_eq_left hg]
  have hd : d.length = 4 - g := by simp [d, hV]
  have hsplit : V = t ++ d := (List.take_append_drop g V).symm
  have hVpow : pow V (n+2) = (t ++ d) ++ pow V (n+1) :=
    congrArg (fun z => z ++ pow V (n+1)) hsplit
  have hsplitAll : A ++ pow U (n+2) ++ C ++ pow V (n+2) ++ Z = l ++ m ++ r := by
    rw [pow_succ_right U (n+1), hVpow]
    simp only [l, m, r, List.append_assoc]
  have hlr : l.length = r.length := by
    simp only [l, r, List.length_append, pow_length, hA, hU, hV, hZ, hd]
    omega
  have hVrev : V.reverse = d.reverse ++ t.reverse := by
    rw [hsplit, List.reverse_append]
  have hr : r.reverse = (Z.reverse ++ d.reverse) ++
      pow (t.reverse ++ d.reverse) (n+1) := by
    simp only [r, List.reverse_append, pow_reverse, hVrev, List.append_assoc]
    rw [pow_rotate_append]
  have hguard : A.length = (Z.reverse ++ d.reverse).length := by
    simp only [List.length_append, List.length_reverse, hA, hZ, hd]
    omega
  have hperiod : U.length = (t.reverse ++ d.reverse).length := by
    simp only [List.length_append, List.length_reverse, hU, ht, hd]
    omega
  have hz : zipAdd l r.reverse =
      zipperOuter A V Z g ++ pow (zipperPeriod U V g) (n+1) := by
    rw [hr]
    change zipAdd (A ++ pow U (n+1))
      ((Z.reverse ++ d.reverse) ++ pow (t.reverse ++ d.reverse) (n+1)) = _
    rw [zipAdd_append_eq _ _ _ _ hguard, zipAdd_pow _ _ _ hperiod]
    rfl
  rw [hsplitAll, pair_three_parts l m r hlr, hz]
  simp only [periodicWord, zipperCenter, m, t, List.reverse_append,
    pow_reverse, List.append_assoc]

/-- Exact lengths of the three extracted output blocks. -/
theorem zipper_block_lengths (A U C V Z : Word) (b h g : Nat)
    (hA : A.length = b + 4) (hU : U.length = 4)
    (hC : C.length = h + 4) (hV : V.length = 4)
    (hZ : Z.length = b + g) (hg : g ≤ 4) :
    (zipperOuter A V Z g).length = b + 4 ∧
    (zipperPeriod U V g).length = 4 ∧
    (zipperCenter U C V g).length = h + 8 + g := by
  have ht : (V.take g).length = g := by simp [hV, Nat.min_eq_left hg]
  have hd : (V.drop g).length = 4-g := by simp [hV]
  have hguard : A.length = (Z.reverse ++ (V.drop g).reverse).length := by
    simp only [List.length_append, List.length_reverse, hA, hZ, hd]
    omega
  have hperiod : U.length = ((V.take g).reverse ++ (V.drop g).reverse).length := by
    simp only [List.length_append, List.length_reverse, hU, ht, hd]
    omega
  constructor
  · exact (zipAdd_length_eq _ _ hguard).trans hA
  constructor
  · exact (zipAdd_length_eq _ _ hperiod).trans hU
  · simp only [zipperCenter, pair_length, List.length_append, hU, hC, ht]
    omega

/-- Actual carry of the single scanned exponent-three input. -/
def rawGamma (B H w : Word) : Nat := terminalCarry (periodicWord B H w 3) 0

/-- These three blocks are the literal slices in the preserved algorithm. -/
def rawOuter (B H w : Word) : Word :=
  (stepWord (periodicWord B H w 3)).take (B.length + 4)

def rawPeriod (B H w : Word) : Word :=
  ((stepWord (periodicWord B H w 3)).drop (B.length + 4)).take 4

def rawCenter (B H w : Word) : Word :=
  ((stepWord (periodicWord B H w 3)).drop (B.length + 8)).take
    (H.length + 8 + rawGamma B H w)

/-- The original valid-state domain, including genuine odd-center parity and
positive exterior. The stronger algebraic theorem below needs only the bounds
and the period length; this record preserves the original realization domain. -/
structure ValidPeriodic (B H w : Word) : Prop where
  outer_bounded : Bounded B 18
  center_bounded : Bounded H 18
  period_bounded : Bounded w 18
  period_length : w.length = 4
  center_symmetric : H.reverse = H
  center_even : H.length % 2 = 1 → ((H[H.length / 2]?).getD 0) % 2 = 0
  outside_positive : 0 < (B ++ w).headD 0

/-- Arithmetic supplies the five digit blocks; the spatial zipper supplies the
entire exact paired output at every exponent at least three. -/
theorem stepWord_periodic_form (B H w : Word) (n : Nat)
    (hB : Bounded B 18) (hH : Bounded H 18) (hw : Bounded w 18)
    (hlen : w.length = 4) :
    stepWord (periodicWord B H w (n+3)) =
      periodicWord
        (zipperOuter (leftGuardDigits B w) (rightPeriodDigits B H w)
          (rightGuardDigits B H w) (rawGamma B H w))
        (zipperCenter (leftPeriodDigits B w) (centerGuardDigits B H w)
          (rightPeriodDigits B H w) (rawGamma B H w))
        (zipperPeriod (leftPeriodDigits B w) (rightPeriodDigits B H w)
          (rawGamma B H w)) (n+1) := by
  unfold stepWord
  rw [normalize_periodicWord B H w n hB hH hw]
  obtain ⟨hA, hU, hC, hV, hZ⟩ := scan_block_lengths B H w hB hH hw
  apply pair_periodic_digits _ _ _ _ _ B.length H.length (rawGamma B H w) n
  · simpa only [hlen] using hA
  · exact hU.trans hlen
  · simpa only [hlen] using hC
  · exact hV.trans hlen
  · exact hZ
  · have := scan_carry_le_one B H w hB hH hw
    change rawGamma B H w ≤ 1 at this
    omega

/-- The exponent-three slices equal the same fixed zipper blocks used at all
larger exponents. No existential output decomposition is assumed. -/
theorem raw_blocks_eq_zipper (B H w : Word)
    (hB : Bounded B 18) (hH : Bounded H 18) (hw : Bounded w 18)
    (hlen : w.length = 4) :
    rawOuter B H w = zipperOuter (leftGuardDigits B w) (rightPeriodDigits B H w)
      (rightGuardDigits B H w) (rawGamma B H w) ∧
    rawPeriod B H w = zipperPeriod (leftPeriodDigits B w) (rightPeriodDigits B H w)
      (rawGamma B H w) ∧
    rawCenter B H w = zipperCenter (leftPeriodDigits B w) (centerGuardDigits B H w)
      (rightPeriodDigits B H w) (rawGamma B H w) := by
  let O := zipperOuter (leftGuardDigits B w) (rightPeriodDigits B H w)
    (rightGuardDigits B H w) (rawGamma B H w)
  let W := zipperPeriod (leftPeriodDigits B w) (rightPeriodDigits B H w) (rawGamma B H w)
  let M := zipperCenter (leftPeriodDigits B w) (centerGuardDigits B H w)
    (rightPeriodDigits B H w) (rawGamma B H w)
  have hf : stepWord (periodicWord B H w 3) = periodicWord O M W 1 :=
    stepWord_periodic_form B H w 0 hB hH hw hlen
  obtain ⟨hA, hU, hC, hV, hZ⟩ := scan_block_lengths B H w hB hH hw
  have hg : rawGamma B H w ≤ 4 := by
    have := scan_carry_le_one B H w hB hH hw
    change rawGamma B H w ≤ 1 at this
    omega
  have hl := zipper_block_lengths (leftGuardDigits B w) (leftPeriodDigits B w)
    (centerGuardDigits B H w) (rightPeriodDigits B H w) (rightGuardDigits B H w)
    B.length H.length (rawGamma B H w)
    (by simpa only [hlen] using hA) (hU.trans hlen)
    (by simpa only [hlen] using hC) (hV.trans hlen) hZ hg
  change O.length = B.length + 4 ∧ W.length = 4 ∧
    M.length = H.length + 8 + rawGamma B H w at hl
  change (stepWord (periodicWord B H w 3)).take (B.length+4) = O ∧
    ((stepWord (periodicWord B H w 3)).drop (B.length+4)).take 4 = W ∧
    ((stepWord (periodicWord B H w 3)).drop (B.length+8)).take
      (H.length+8+rawGamma B H w) = M
  rw [hf]
  constructor
  · rw [← hl.1]
    exact take_outer_one O M W
  constructor
  · rw [← hl.1, ← hl.2.1]
    exact take_period_one O M W
  · have hc : B.length+8 = O.length + W.length := by omega
    rw [hc, ← hl.2.2]
    exact take_center_one O M W

/-- Literal period-four guard extraction for every bounded input. This
algebraic strengthening requires neither symmetry nor realizability of H. -/
theorem raw_guard_bounded (B H w : Word) (k : Nat)
    (hB : Bounded B 18) (hH : Bounded H 18) (hw : Bounded w 18)
    (hlen : w.length = 4) (hk : 3 ≤ k) :
    stepWord (periodicWord B H w k) =
      periodicWord (rawOuter B H w) (rawCenter B H w) (rawPeriod B H w) (k-2) := by
  have hf := stepWord_periodic_form B H w (k-3) hB hH hw hlen
  rw [show k-3+3 = k by omega, show k-3+1 = k-2 by omega] at hf
  obtain ⟨hO, hW, hM⟩ := raw_blocks_eq_zipper B H w hB hH hw hlen
  rw [← hO, ← hW, ← hM] at hf
  exact hf

/-- The same exact guard lemma on the full original valid-state domain. -/
theorem raw_guard (B H w : Word) (k : Nat) (hv : ValidPeriodic B H w) (hk : 3 ≤ k) :
    stepWord (periodicWord B H w k) =
      periodicWord (rawOuter B H w) (rawCenter B H w) (rawPeriod B H w) (k-2) :=
  raw_guard_bounded B H w k hv.outer_bounded hv.center_bounded hv.period_bounded
    hv.period_length hk

end Agent1.Periodic

#print axioms Agent1.Periodic.pow_append
#print axioms Agent1.Periodic.pow_succ_right
#print axioms Agent1.Periodic.pow_reverse
#print axioms Agent1.Periodic.zipAdd_append_eq
#print axioms Agent1.Periodic.zipAdd_length_eq
#print axioms Agent1.Periodic.zipAdd_comm_eq
#print axioms Agent1.Periodic.zipAdd_reverse_eq
#print axioms Agent1.Periodic.zipAdd_pow
#print axioms Agent1.Periodic.pow_rotate_append
#print axioms Agent1.Periodic.pair_three_parts
#print axioms Agent1.Periodic.pair_periodic_digits
#print axioms Agent1.Periodic.zipper_block_lengths
#print axioms Agent1.Periodic.stepWord_periodic_form
#print axioms Agent1.Periodic.raw_blocks_eq_zipper
#print axioms Agent1.Periodic.raw_guard_bounded
#print axioms Agent1.Periodic.raw_guard
