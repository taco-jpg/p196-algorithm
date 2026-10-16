import ExteriorCoverage

/-!
Agent 110: a spatial-order-sensitive obstruction for the exact exterior map.

The observable below is a finite decimal evaluation relative to the constant
phase tail.  It is invariant under moving trailing phase letters into that tail,
but is NOT invariant under arbitrary reversal or positional-parity permutations.
An exact post-overflow path closes this observable without closing the exterior
state.  Consequently this observable is neither an autonomous factor nor a
source of an everywhere nondecreasing, overflow-strict potential.

This does not prove an exterior cycle exists, or that all exterior cycles are
impossible.  No statement about an infinite safe ordinary orbit is made.
-/

namespace Agent110.RadixExterior

open P196.Agent6

/-- Coefficient evaluation at ten, retaining spatial order. -/
def value10 : Word → Int
  | [] => 0
  | x :: xs => (x : Int) + 10 * value10 xs

/-- Evaluation of the coefficient defects relative to an infinite phase tail. -/
def centeredValue (c : Nat) : Word → Int
  | [] => 0
  | x :: xs => (x : Int) - (c : Int) + 10 * centeredValue c xs

/-- The centered recursion is the stated exact radix evaluation, for every word. -/
theorem centeredValue_formula (c : Nat) (B : Word) :
    9 * centeredValue c B =
      9 * value10 B - (c : Int) * ((10 : Int) ^ B.length - 1) := by
  induction B with
  | nil => simp [centeredValue, value10]
  | cons x xs ih =>
      have h := congrArg (fun z : Int => 10 * z) ih
      simp only [centeredValue, value10, List.length_cons, Int.pow_succ]
      simp only [Int.mul_add, Int.mul_sub, Int.mul_one, Int.mul_assoc] at h ⊢
      have hc : (c : Int) * (10 ^ xs.length * 10) =
          10 * ((c : Int) * 10 ^ xs.length) := by ac_rfl
      rw [hc]
      omega

/-- The integral version `9 eval(B) - c (10^length(B)-1)`. -/
def radixDefect (s : Exterior) : Int := 9 * centeredValue s.phase s.word

def observation (s : Exterior) : Nat × Int := (s.phase, radixDefect s)

/-- Repeated phase letters have no centered contribution. -/
theorem centeredValue_replicate (c j : Nat) :
    centeredValue c (List.replicate j c) = 0 := by
  induction j with
  | zero => rfl
  | succ j ih => simp [List.replicate_succ, centeredValue, ih]

/-- The observable respects every finite reassignment of tail phase letters. -/
theorem centeredValue_append_phase (c j : Nat) (B : Word) :
    centeredValue c (B ++ List.replicate j c) = centeredValue c B := by
  induction B with
  | nil => simp [centeredValue, centeredValue_replicate]
  | cons x xs ih => simp only [List.cons_append, centeredValue, ih]

theorem observation_append_phase (c j : Nat) (B : Word) :
    observation ⟨c, B ++ List.replicate j c⟩ = observation ⟨c, B⟩ := by
  simp only [observation, radixDefect, centeredValue_append_phase]

/-- Actual overflow in the imported, unchanged exterior dynamics. -/
def overflow (s : Exterior) : Nat :=
  (norm s.word.reverse (if 10 ≤ s.phase then 1 else 0)).2

/-- An actual finite ancestry following a computed overflow, not a free label. -/
def ReachedAfterOverflow (s : Exterior) : Prop :=
  ∃ a t, Canonical a ∧ overflow a = 1 ∧ s = iterate t (advance a)

def ancestor : Exterior := ⟨6, [13]⟩
def entered : Exterior := ⟨12, [4, 10]⟩
def source : Exterior := ⟨6, [9, 1]⟩
def middle : Exterior := ⟨12, [18, 2]⟩
def endpoint : Exterior := ⟨6, [9, 11, 5]⟩
def nextEndpoint : Exterior := ⟨12, [10, 1, 7, 11]⟩

/-- Every named state satisfies the existing exact canonical exterior predicate. -/
theorem witness_canonical :
    Canonical ancestor ∧ Canonical entered ∧ Canonical source ∧
    Canonical middle ∧ Canonical endpoint ∧ Canonical nextEndpoint := by
  simp [Canonical, trim, ancestor, entered, source, middle, endpoint, nextEndpoint]

/-- A contiguous orbit of the exact map, including both computed overflow steps. -/
theorem witness_path :
    advance ancestor = entered ∧ advance entered = source ∧
    advance source = middle ∧ advance middle = endpoint ∧
    advance endpoint = nextEndpoint := by decide

theorem witness_overflows :
    overflow ancestor = 1 ∧ overflow entered = 0 ∧ overflow source = 0 ∧
    overflow middle = 1 ∧ overflow endpoint = 1 := by decide

/-- Both edges used in the obstruction start after an actual earlier overflow. -/
theorem witness_after_overflow :
    ReachedAfterOverflow source ∧ ReachedAfterOverflow middle ∧
    ReachedAfterOverflow endpoint := by
  constructor
  · exact ⟨ancestor, 1, witness_canonical.1, witness_overflows.1, by decide⟩
  constructor
  · exact ⟨ancestor, 2, witness_canonical.1, witness_overflows.1, by decide⟩
  · exact ⟨ancestor, 3, witness_canonical.1, witness_overflows.1, by decide⟩

/-- Same phase and same full radix defect, despite genuinely different words. -/
theorem witness_observation_return :
    observation source = (6, -423) ∧ observation middle = (12, -846) ∧
    observation endpoint = observation source := by decide

/-- The observable return is not a returned exterior state. -/
theorem witness_not_state_return : endpoint ≠ source := by decide

/-- Equal observations already have unequal next observations. -/
theorem witness_nonautonomy :
    observation source = observation endpoint ∧
    observation (advance source) ≠ observation (advance endpoint) := by decide

/-- There is no deterministic update of `(phase, radixDefect)` even on the
canonical states which have already experienced a genuine overflow. -/
theorem no_autonomous_radix_factor
    (F : (Nat × Int) → (Nat × Int))
    (hF : ∀ s, Canonical s → ReachedAfterOverflow s →
      observation (advance s) = F (observation s)) : False := by
  have hs := hF source witness_canonical.2.2.1 witness_after_overflow.1
  have he := hF endpoint witness_canonical.2.2.2.2.1 witness_after_overflow.2.2
  apply witness_nonautonomy.2
  rw [hs, he, witness_nonautonomy.1]

/-- General relational form: no function of this observable can weakly advance
on all canonical post-overflow steps and strictly advance on every overflow.
Only mixed transitivity and strict irreflexivity of the target relations are
needed; the target is not restricted to integers. -/
theorem no_overflow_strict_radix_observable {α : Type}
    (P : (Nat × Int) → α) (weak strict : α → α → Prop)
    (htrans : ∀ a b c, weak a b → strict b c → strict a c)
    (hirr : ∀ a, ¬ strict a a)
    (hweak : ∀ s, Canonical s → ReachedAfterOverflow s →
      weak (P (observation s)) (P (observation (advance s))))
    (hstrict : ∀ s, Canonical s → ReachedAfterOverflow s → overflow s = 1 →
      strict (P (observation s)) (P (observation (advance s)))) : False := by
  have h0 := hweak source witness_canonical.2.2.1 witness_after_overflow.1
  have h1 := hstrict middle witness_canonical.2.2.2.1
    witness_after_overflow.2.1 witness_overflows.2.2.2.1
  rw [witness_path.2.2.1] at h0
  rw [witness_path.2.2.2.1] at h1
  have h := htrans _ _ _ h0 h1
  rw [witness_observation_return.2.2] at h
  exact hirr _ h

/-- Integer-valued version, with nondecrease allowed at nonoverflow steps. -/
theorem no_overflow_strict_radix_potential
    (P : Nat → Int → Int)
    (hweak : ∀ s, Canonical s → ReachedAfterOverflow s →
      P s.phase (radixDefect s) ≤ P (advance s).phase (radixDefect (advance s)))
    (hstrict : ∀ s, Canonical s → ReachedAfterOverflow s → overflow s = 1 →
      P s.phase (radixDefect s) < P (advance s).phase (radixDefect (advance s))) :
    False := by
  apply no_overflow_strict_radix_observable (fun o => P o.1 o.2) (· ≤ ·) (· < ·)
  · intro a b c hab hbc; omega
  · intro a h; omega
  · exact hweak
  · exact hstrict

/-- This observable retains information discarded by reversal-invariant scores. -/
theorem radix_observation_is_order_sensitive :
    radixDefect ⟨6, [1, 5]⟩ ≠ radixDefect ⟨6, [5, 1]⟩ := by decide

end Agent110.RadixExterior
