import P196.Agent107FoldedTransducer.Agent107TransducerDefs

/-!
Independent semantic boundary checks by the Agent #107 semantic reviewer.
These are kernel-checked statements about the literal transducer definitions,
not an invariant certificate and not a claim concerning the 196 conjecture.
-/

namespace Agent107.FoldedTransducer.Boundary

open DecimalDigits FoldedDecimal

theorem initial_no_overflow_sentinel : (initial 0).delay = -1 := rfl

theorem initial_overflow_delay : (initial 1).delay = 1 := rfl

theorem no_overflow_preserves_sentinel (s : State) (q b : Nat)
    (h : s.overflow = 0) : (nextState s q b).delay = -1 := by
  simp [nextState, h]

theorem actual_no_overflow_sentinel (L : Nat) (q : Nat → Nat)
    (h : carry q L = 0) (i : Nat) : (actualState L q i).delay = -1 := by
  simp [actualState, h]

theorem first_pair_zero_rejected (h : Nat) (t : State) :
    ¬ Transition (initial h) 0 t := by
  simp [Transition, initial]

theorem odd_center_rejected (s : State) (c : Nat) (hc : c % 2 ≠ 0) :
    ¬ Terminal s (some c) := by
  intro ht
  exact hc ht.2.2.1

theorem oversized_center_rejected (s : State) (c : Nat) (hc : 18 < c) :
    ¬ Terminal s (some c) := by
  intro ht
  have := ht.2.1
  omega

theorem empty_input_rejected (q : Nat → Nat) (p : Nat → State) :
    ¬ Accepts 0 q p := by
  rintro ⟨⟨h, _, hp⟩, _, ht⟩
  simp only [Nat.zero_div, inputCenter, Nat.zero_mod, ite_true] at ht
  rw [hp] at ht
  simp [Terminal, initial] at ht

/-- The one-digit boundary includes the positive, even central column sum;
there are no pair transitions. Both possible overflow initials remain present.
-/
theorem one_digit_accepts_iff (q : Nat → Nat) (p : Nat → State) :
    Accepts 1 q p ↔
      ∃ h, h ≤ 1 ∧ p 0 = initial h ∧ 0 < q 0 ∧ q 0 ≤ 18 ∧
        q 0 % 2 = 0 ∧ q 0 / 10 = h := by
  constructor
  · rintro ⟨⟨h, hb, hp⟩, _, ht⟩
    refine ⟨h, hb, hp, ?_⟩
    simpa [inputCenter, hp, Terminal, initial] using ht
  · rintro ⟨h, hb, hp, hc⟩
    refine ⟨⟨h, hb, hp⟩, ?_, ?_⟩
    · intro i hi
      omega
    · simpa [inputCenter, hp, Terminal, initial] using hc

theorem one_digit_no_overflow_example :
    Accepts 1 (fun _ => 8) (fun _ => initial 0) ∧
      pathOutput 1 (fun _ => 8) (fun _ => initial 0) = ⟨[], some 16⟩ := by
  constructor
  · apply (one_digit_accepts_iff _ _).2
    exact ⟨0, by decide, rfl, by decide, by decide, by decide, by decide⟩
  · decide

theorem one_digit_overflow_example :
    Accepts 1 (fun _ => 10) (fun _ => initial 1) ∧
      pathOutput 1 (fun _ => 10) (fun _ => initial 1) = ⟨[1], none⟩ := by
  constructor
  · apply (one_digit_accepts_iff _ _).2
    exact ⟨1, by decide, rfl, by decide, by decide, by decide, by decide⟩
  · decide

theorem no_overflow_has_no_extra (s : State) (c : Option Nat)
    (h : s.overflow = 0) : terminalExtra s c = none := by
  simp [terminalExtra, h]

theorem even_overflow_has_center (s : State) (h : s.overflow ≠ 0) :
    terminalExtra s none = none ∧
      terminalCenter s none = some (2 * s.delay.toNat) := by
  simp [terminalExtra, terminalCenter, h]

theorem odd_overflow_has_extra_pair (s : State) (c : Nat)
    (h : s.overflow ≠ 0) :
    terminalExtra s (some c) = some ((c + s.low) % 10 + s.delay.toNat) ∧
      terminalCenter s (some c) = none := by
  simp [terminalExtra, terminalCenter, h]

/-- Acceptance constrains only the finite prefix. Replacing the tail can
change the function while preserving acceptance and its finite path.
-/
theorem accepted_tail_not_unique :
    ∃ p r : Nat → State,
      Accepts 1 (fun _ => 2) p ∧ Accepts 1 (fun _ => 2) r ∧
      finitePath 1 p = finitePath 1 r ∧ p ≠ r := by
  let p : Nat → State := fun _ => initial 0
  let r : Nat → State := fun i => if i = 0 then initial 0 else initial 1
  refine ⟨p, r, ?_, ?_, ?_, ?_⟩
  · apply (one_digit_accepts_iff _ _).2
    exact ⟨0, by decide, rfl, by decide, by decide, by decide, by decide⟩
  · apply (one_digit_accepts_iff _ _).2
    exact ⟨0, by decide, rfl, by decide, by decide, by decide, by decide⟩
  · rfl
  · intro h
    have hh := congrArg (fun f : Nat → State => (f 1).overflow) h
    have hbad : (0 : Nat) = 1 := hh
    omega

end Agent107.FoldedTransducer.Boundary
