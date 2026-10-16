import FamilyCardinality

/-!
State-dependent finite binary word counts. The enumeration is the existing
Agent3 allBits list. The block-loss theorem is conditional on its explicit
uniform rejecting-word premise; a separate finite certificate must supply it.
-/

namespace P196.Agent3.PrefixContraction.BinaryCount

open P196.Agent3.OverflowHorizon

variable {Q : Type} [DecidableEq Q]

def runBits (delta : Q → Bool → Q) (q : Q) (bits : List Bool) : Q :=
  bits.foldl delta q

def survivingWords (delta : Q → Bool → Q) (dead q : Q) (n : Nat) :
    List (List Bool) :=
  (allBits n).filter (fun bits => decide (runBits delta q bits ≠ dead))

def survivorCount (delta : Q → Bool → Q) (dead q : Q) (n : Nat) : Nat :=
  (survivingWords delta dead q n).length

theorem runBits_nil (delta : Q → Bool → Q) (q : Q) :
    runBits delta q [] = q := rfl

theorem runBits_cons (delta : Q → Bool → Q) (q : Q) (b : Bool)
    (bits : List Bool) :
    runBits delta q (b :: bits) = runBits delta (delta q b) bits := rfl

theorem runBits_append (delta : Q → Bool → Q) (q : Q)
    (xs ys : List Bool) :
    runBits delta q (xs ++ ys) = runBits delta (runBits delta q xs) ys := by
  exact List.foldl_append

theorem runBits_dead (delta : Q → Bool → Q) (dead : Q)
    (hdead : ∀ b, delta dead b = dead) (bits : List Bool) :
    runBits delta dead bits = dead := by
  induction bits with
  | nil => rfl
  | cons b bits ih => rw [runBits_cons, hdead, ih]

theorem mem_survivingWords (delta : Q → Bool → Q) (dead q : Q)
    (n : Nat) (bits : List Bool) :
    bits ∈ survivingWords delta dead q n ↔
      bits.length = n ∧ runBits delta q bits ≠ dead := by
  simp [survivingWords, mem_allBits_iff]

theorem survivingWords_nodup (delta : Q → Bool → Q) (dead q : Q) (n : Nat) :
    (survivingWords delta dead q n).Nodup := by
  exact (allBits_nodup n).filter _

theorem survivorCount_zero (delta : Q → Bool → Q) (dead q : Q) :
    survivorCount delta dead q 0 = if q = dead then 0 else 1 := by
  by_cases h : q = dead <;> simp [survivorCount, survivingWords, allBits, runBits, h]

theorem survivorCount_succ (delta : Q → Bool → Q) (dead q : Q) (n : Nat) :
    survivorCount delta dead q (n + 1) =
      survivorCount delta dead (delta q false) n +
      survivorCount delta dead (delta q true) n := by
  simp [survivorCount, survivingWords, allBits, List.filter_map,
    Function.comp_def, runBits]

theorem survivorCount_dead (delta : Q → Bool → Q) (dead : Q)
    (hdead : ∀ b, delta dead b = dead) (n : Nat) :
    survivorCount delta dead dead n = 0 := by
  simp [survivorCount, survivingWords, runBits_dead delta dead hdead]

theorem survivorCount_le_power (delta : Q → Bool → Q) (dead q : Q) (n : Nat) :
    survivorCount delta dead q n ≤ 2 ^ n := by
  have h := List.length_filter_le
    (fun bits => decide (runBits delta q bits ≠ dead)) (allBits n)
  simpa [survivorCount, survivingWords, allBits_length] using h

theorem survivorCount_block_loss (delta : Q → Bool → Q) (dead q : Q)
    (k : Nat) (hkill : ∃ bits : List Bool,
      bits.length = k ∧ runBits delta q bits = dead) :
    survivorCount delta dead q k ≤ 2 ^ k - 1 := by
  rcases hkill with ⟨bits, hlen, hrun⟩
  have hlt :
      ((allBits k).filter (fun bs => decide (runBits delta q bs ≠ dead))).length <
        (allBits k).length := by
    apply List.length_filter_lt_length_iff_exists.mpr
    exact ⟨bits, (mem_allBits_iff bits k).mpr hlen, by simp [hrun]⟩
  rw [allBits_length] at hlt
  change survivorCount delta dead q k < 2 ^ k at hlt
  omega

/-- A uniform local block loss gives a count bound from every starting state.
The rejecting word is allowed to depend on that state. -/
theorem survivorCount_add_block (delta : Q → Bool → Q) (dead : Q)
    (hdead : ∀ b, delta dead b = dead) (k : Nat)
    (hkill : ∀ q, ∃ bits : List Bool,
      bits.length = k ∧ runBits delta q bits = dead) (q : Q) (n : Nat) :
    survivorCount delta dead q (n + k) ≤
      (2 ^ k - 1) * survivorCount delta dead q n := by
  induction n generalizing q with
  | zero =>
    by_cases h : q = dead
    · subst q
      simp [survivorCount_dead delta dead hdead]
    · simpa [survivorCount_zero, h] using
        survivorCount_block_loss delta dead q k (hkill q)
  | succ n ih =>
    rw [Nat.succ_add, survivorCount_succ, survivorCount_succ]
    calc
      _ ≤ (2 ^ k - 1) * survivorCount delta dead (delta q false) n +
          (2 ^ k - 1) * survivorCount delta dead (delta q true) n :=
        Nat.add_le_add (ih (delta q false)) (ih (delta q true))
      _ = _ := (Nat.mul_add _ _ _).symm

theorem survivorCount_blocks (delta : Q → Bool → Q) (dead : Q)
    (hdead : ∀ b, delta dead b = dead) (k : Nat)
    (hkill : ∀ q, ∃ bits : List Bool,
      bits.length = k ∧ runBits delta q bits = dead) (q : Q) (b r : Nat) :
    survivorCount delta dead q (k * b + r) ≤ (2 ^ k - 1) ^ b * 2 ^ r := by
  induction b with
  | zero => simpa using survivorCount_le_power delta dead q r
  | succ b ih =>
    have h := survivorCount_add_block delta dead hdead k hkill q (k * b + r)
    have heq : k * (b + 1) + r = (k * b + r) + k := by omega
    rw [heq]
    calc
      _ ≤ (2 ^ k - 1) * survivorCount delta dead q (k * b + r) := h
      _ ≤ (2 ^ k - 1) * ((2 ^ k - 1) ^ b * 2 ^ r) := Nat.mul_le_mul_left _ ih
      _ = (2 ^ k - 1) ^ (b + 1) * 2 ^ r := by
        simp [Nat.pow_succ, Nat.mul_assoc, Nat.mul_comm, Nat.mul_left_comm]

theorem survivorCount_div_mod (delta : Q → Bool → Q) (dead : Q)
    (hdead : ∀ b, delta dead b = dead) (k : Nat)
    (hkill : ∀ q, ∃ bits : List Bool,
      bits.length = k ∧ runBits delta q bits = dead) (q : Q) (n : Nat) :
    survivorCount delta dead q n ≤ (2 ^ k - 1) ^ (n / k) * 2 ^ (n % k) := by
  have h := survivorCount_blocks delta dead hdead k hkill q (n / k) (n % k)
  simpa [Nat.div_add_mod] using h

#print axioms runBits
#print axioms survivingWords
#print axioms survivorCount
#print axioms runBits_nil
#print axioms runBits_cons
#print axioms runBits_append
#print axioms runBits_dead
#print axioms mem_survivingWords
#print axioms survivingWords_nodup
#print axioms survivorCount_zero
#print axioms survivorCount_succ
#print axioms survivorCount_dead
#print axioms survivorCount_le_power
#print axioms survivorCount_block_loss
#print axioms survivorCount_add_block
#print axioms survivorCount_blocks
#print axioms survivorCount_div_mod

end P196.Agent3.PrefixContraction.BinaryCount
