import P196.Agent101ProtectedFamily.FamilyCardinality

namespace P196.Agent3.OverflowHorizon

open Agent8

set_option maxRecDepth 10000
set_option maxHeartbeats 2000000

/-- All coefficients avoid the carry-sensitive neutral residue nine. -/
def NoNeutral (w : Word) : Prop :=
  ∀ x ∈ w, x ≤ 18 ∧ x % 10 ≤ 8

def lowWord (w : Word) : Word := w.map (fun x => x % 10)
def highWord (w : Word) : Word := w.map (fun x => x / 10)
def rhoWord (w : Word) : Word := w.map (fun x => x % 10 + x / 10)

theorem stable_digit_carry (x e : Nat) (hx : x % 10 ≤ 8) (he : e ≤ 1) :
    (x + e) % 10 = x % 10 + e ∧ (x + e) / 10 = x / 10 := by
  omega

/-- Exact digit/carry decomposition, retaining a possibly zero final carry. -/
theorem padded_normalization (w : Word) (e : Nat)
    (hw : NoNeutral w) (he : e ≤ 1) :
    fixedDigits w e ++ [terminalCarry w e] =
      zipAdd (lowWord w ++ [0]) (e :: highWord w) := by
  induction w generalizing e with
  | nil => simp [fixedDigits, terminalCarry, lowWord, highWord, zipAdd]
  | cons x xs ih =>
    have hx := hw x (by simp)
    have ht : NoNeutral xs := by
      intro y hy
      exact hw y (by simp [hy])
    have hs := stable_digit_carry x e hx.2 he
    have hq : x / 10 ≤ 1 := by omega
    simp only [fixedDigits, terminalCarry, lowWord, highWord, List.map_cons,
      List.cons_append, zipAdd, hs.1, hs.2]
    exact congrArg (List.cons (x % 10 + e)) (ih (x / 10) ht hq)

theorem zipAdd_interchange (a b c d : Word) :
    zipAdd (zipAdd a b) (zipAdd c d) =
      zipAdd (zipAdd a d) (zipAdd b c) := by
  induction a generalizing b c d with
  | nil => simp [zipAdd]
  | cons x xs ih =>
    cases b <;> cases c <;> cases d <;>
      simp [zipAdd, ih, Nat.add_assoc, Nat.add_comm, Nat.add_left_comm]

theorem zipAdd_low_high (w : Word) :
    zipAdd (lowWord w) (highWord w) = rhoWord w := by
  induction w with
  | nil => rfl
  | cons x xs ih =>
    change (x % 10 + x / 10) :: zipAdd (lowWord xs) (highWord xs) =
      (x % 10 + x / 10) :: rhoWord xs
    rw [ih]

theorem zipAdd_high_low (w : Word) :
    zipAdd (highWord w) (lowWord w) = rhoWord w := by
  induction w with
  | nil => rfl
  | cons x xs ih =>
    change (x / 10 + x % 10) :: zipAdd (highWord xs) (lowWord xs) =
      (x % 10 + x / 10) :: rhoWord xs
    rw [ih, Nat.add_comm (x / 10)]

/-- Reusable exact overflow formula; the actual final carry is a premise.
The input symmetry is literal full-word symmetry, with no hidden width change. -/
theorem stepWord_noNeutral_overflow (w : Word) (hs : w.reverse = w)
    (hw : NoNeutral w) (hc : terminalCarry w 0 = 1) :
    stepWord w = zipAdd (rhoWord w ++ [0]) (0 :: rhoWord w) := by
  have hn : normalize w 0 = zipAdd (lowWord w ++ [0]) (0 :: highWord w) := by
    rw [normalize_decompose, hc]
    simpa [hc] using padded_normalization w 0 hw (by decide)
  have hrlo : (lowWord w).reverse = lowWord w := by
    simp [lowWord, ← List.map_reverse, hs]
  have hrhi : (highWord w).reverse = highWord w := by
    simp [highWord, ← List.map_reverse, hs]
  have hrev : (zipAdd (lowWord w ++ [0]) (0 :: highWord w)).reverse =
      zipAdd (0 :: lowWord w) (highWord w ++ [0]) := by
    simp only [zipAdd_eq_zipWith]
    rw [List.reverse_zipWith (by simp [lowWord, highWord])]
    simp [hrlo, hrhi]
  rw [stepWord, hn, pair, hrev, zipAdd_interchange]
  have hpad : zipAdd (lowWord w ++ [0]) (highWord w ++ [0]) =
      rhoWord w ++ [0] := by
    simp only [zipAdd_eq_zipWith]
    rw [List.zipWith_append (by simp [lowWord, highWord])]
    simp only [← zipAdd_eq_zipWith, zipAdd_low_high, zipAdd, Nat.add_zero]
  rw [hpad]
  simp only [zipAdd, Nat.zero_add, zipAdd_high_low]

theorem inputWord_noNeutral (xs : List Bool) (k : Nat) :
    NoNeutral (inputWord xs k) := by
  intro x hx
  simp only [inputWord, List.mem_append, List.mem_reverse] at hx
  have hh : x ∈ inputHalf xs k := hx.elim id id
  simp only [inputHalf, List.mem_append, List.mem_singleton, List.mem_map,
    List.mem_replicate] at hh
  rcases hh with (rfl | ⟨b, _, rfl⟩) | ⟨_, rfl⟩
  · decide
  · cases b <;> decide
  · decide

theorem inputWord_final_carry (xs : List Bool) (k : Nat) :
    terminalCarry (inputWord xs k) 0 = 1 := by
  let tail : Word := xs.map choice ++ List.replicate k 18
  have hw : inputWord xs k = (14 :: tail) ++ tail.reverse ++ [14] := by
    simp [inputWord, inputHalf, tail, List.reverse_append, List.append_assoc]
  have hb : Bounded ((14 :: tail) ++ tail.reverse) 18 := by
    intro x hx
    have hm : x ∈ inputWord xs k := by
      rw [hw]
      exact List.mem_append_left [14] hx
    exact (inputWord_noNeutral xs k x hm).1
  have he := terminalCarry_le_one ((14 :: tail) ++ tail.reverse) 0 hb (by decide)
  rw [hw, terminalCarry_append]
  simp only [terminalCarry]
  omega

private theorem replicate_join (m n x : Nat) :
    List.replicate m x ++ List.replicate n x = List.replicate (m + n) x := by
  induction m with
  | zero => simp
  | succ m ih => simp [List.replicate_succ, ih, Nat.succ_add]

theorem rho_inputWord (xs : List Bool) (k : Nat) :
    rhoWord (inputWord xs k) =
      List.replicate (xs.length + 1) 5 ++ List.replicate (2 * k) 9 ++
        List.replicate (xs.length + 1) 5 := by
  have hm : rhoWord (xs.map choice) = List.replicate xs.length 5 := by
    induction xs with
    | nil => rfl
    | cons b bs ih =>
      cases b <;> simp [rhoWord, choice, List.replicate_succ, ← ih]
  simp only [inputWord, inputHalf, rhoWord, List.map_append, List.map_reverse,
    List.map_cons, List.map_nil, List.map_replicate]
  change (5 :: rhoWord (xs.map choice) ++ List.replicate k 9) ++
      (5 :: rhoWord (xs.map choice) ++ List.replicate k 9).reverse = _
  rw [hm]
  simp only [List.reverse_append, List.reverse_cons, List.reverse_replicate]
  have hk : List.replicate k 9 ++ List.replicate k 9 =
      List.replicate (2 * k) 9 := by rw [replicate_join]; congr 1; omega
  simp only [List.cons_append, List.append_assoc]
  rw [← List.append_assoc (List.replicate k 9), hk]
  have hm5 : List.replicate xs.length 5 ++ [5] =
      List.replicate (xs.length + 1) 5 := replicate_join xs.length 1 5
  rw [hm5]
  simp [List.replicate_succ, List.append_assoc]

/-- Adjacent sums with explicit zero padding on both sides. -/
def overlap (p : Nat) : Word → Word
  | [] => [p]
  | x :: xs => (p + x) :: overlap x xs

theorem zipAdd_padded_overlap (w : Word) (p : Nat) :
    zipAdd (w ++ [0]) (p :: w) = overlap p w := by
  induction w generalizing p with
  | nil => simp [zipAdd, overlap]
  | cons x xs ih => simp [zipAdd, overlap, ih, Nat.add_comm]

theorem overlap_replicate (p x n : Nat) (tail : Word) :
    overlap p (List.replicate (n + 1) x ++ tail) =
      (p + x) :: (List.replicate n (2 * x) ++ overlap x tail) := by
  induction n generalizing p with
  | zero => simp [List.replicate_succ, overlap]
  | succ n ih =>
    rw [List.replicate_succ, List.cons_append, overlap, ih]
    simp [List.replicate_succ, Nat.two_mul]

/-- All Boolean choices have one exact overflow image for every k > 0. -/
theorem inputWord_step (xs : List Bool) (k : Nat) (hk : 0 < k) :
    stepWord (inputWord xs k) = target xs.length k := by
  rw [stepWord_noNeutral_overflow _ (inputWord_canonical xs k).2.1
    (inputWord_noNeutral xs k) (inputWord_final_carry xs k)]
  rw [rho_inputWord, zipAdd_padded_overlap]
  have hk2 : 2 * k = (2 * k - 1) + 1 := by omega
  rw [List.append_assoc, overlap_replicate]
  rw [hk2, overlap_replicate]
  have hend := overlap_replicate 9 5 xs.length []
  simp only [List.append_nil] at hend
  rw [hend]
  simp [target, overlap, List.append_assoc]

#print axioms padded_normalization
#print axioms stepWord_noNeutral_overflow
#print axioms inputWord_final_carry
#print axioms inputWord_step

end P196.Agent3.OverflowHorizon
