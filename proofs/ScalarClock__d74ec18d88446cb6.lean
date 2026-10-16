import Std

/-! The finite scalar boundary clock and its overflow arithmetic.
The whole-word bridge is proved separately in ActualScalar. -/

namespace ScalarClock

/-- One outside coefficient and the carry entering the high outside column. -/
def step (a : Nat) (c : Bool) : Nat × Nat :=
  let e := (a + c.toNat) / 10
  (if e = 0 then a % 10 + (a + c.toNat) % 10 else a % 10 + 1, e)

def phaseValue : Nat → Nat
  | 0 => 4 | 1 => 8 | 2 => 16 | 3 => 7 | 4 => 15 | 5 => 6 | _ => 13

def overflowValue : Nat → Nat
  | 2 => 1 | 4 => 1 | 6 => 1 | _ => 0

def phase (s : Nat) : Nat := phaseValue (s % 7)
def overflow (s : Nat) : Nat := overflowValue (s % 7)

def allowed (s : Nat) (c : Bool) : Prop :=
  match s % 7 with
  | 0 => c = false | 1 => c = false
  | 3 => c = true | 5 => c = true | _ => True

instance (s : Nat) (c : Bool) : Decidable (allowed s c) := by
  unfold allowed
  split <;> infer_instance

theorem phase_periodic (s : Nat) : phase (s + 7) = phase s := by
  unfold phase
  congr 1
  omega

theorem overflow_periodic (s : Nat) : overflow (s + 7) = overflow s := by
  unfold overflow
  congr 1
  omega

theorem finite_overflow : ∀ p : Fin 7, ∀ c : Bool,
    (step (phaseValue p.val) c).2 = overflowValue p.val := by decide

/-- The overflow at every clock phase is independent of the incoming bit. -/
theorem step_overflow_phase (s : Nat) (c : Bool) :
    (step (phase s) c).2 = overflow s :=
  finite_overflow ⟨s % 7, Nat.mod_lt _ (by decide)⟩ c

theorem finite_allowed : ∀ p : Fin 7, ∀ c : Bool,
    ((step (phaseValue p.val) c).1 = phaseValue ((p.val + 1) % 7)) ↔
      allowed p.val c := by decide

theorem step_follows_phase_iff (s : Nat) (c : Bool) :
    (step (phase s) c).1 = phase (s + 1) ↔ allowed s c := by
  have h := finite_allowed ⟨s % 7, Nat.mod_lt _ (by decide)⟩ c
  have hm : (s % 7 + 1) % 7 = (s + 1) % 7 := by omega
  simpa only [phase, allowed, Nat.mod_mod, hm] using h

/-- Every cyclic rotation has exactly three overflows in seven steps. -/
theorem seven_overflow_sum (s : Nat) :
    overflow s + overflow (s+1) + overflow (s+2) + overflow (s+3) +
      overflow (s+4) + overflow (s+5) + overflow (s+6) = 3 := by
  have hb : s % 7 < 7 := Nat.mod_lt _ (by decide)
  have hc : s % 7 = 0 ∨ s % 7 = 1 ∨ s % 7 = 2 ∨ s % 7 = 3 ∨
      s % 7 = 4 ∨ s % 7 = 5 ∨ s % 7 = 6 := by omega
  rcases hc with h | h | h | h | h | h | h <;>
    simp [overflow, Nat.add_mod, h, overflowValue]

end ScalarClock
