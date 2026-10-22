import P196.Sprint.Agent20.PrefixFidelity

/-!
# Red team (sprint agent 20): delay witnesses beyond the 100-step base check

The prefix method excludes a family only through a uniform ancestry bound
`t ≤ bound + 1 ≤ 100` (`no_196_of_entries`).  Each row `(pre, seed, t, r)` below is
an actual orbit: `orbit seed t` is a palindrome in `[num pre · 10^r, (num pre + 1) · 10^r)`.
So any uniform ancestry bound for `pre` is at least `t`, and since every listed `t`
exceeds 100, **no certificate of the current pipeline exists for these prefixes at
any width** (`no_entry_certificate`).  The rows were found by the forward scans in
`sprint/agent-20/scripts/fwdscan.c` (seeds < 10^7, 2,000,000 random seeds below
10^13, record seeds); the Lean proof re-evaluates every orbit in the kernel.
These are statements about the method, not about the orbit of 196.
-/

namespace Sprint.Agent20.Delay

open Lychrel196 Agent124.PrefixL Sprint.Agent20

/-- Kernel-checkable delay witness. -/
def witnessOK (w : List Nat × Nat × Nat × Nat) : Bool :=
  let (pre, seed, t, r) := w
  let P := orbit seed t
  decide (WellFormed pre) && decide (0 < seed) && decide (100 < t) &&
    (reverse10 P == P) && Nat.ble (num pre * 10 ^ r) P && Nat.blt P ((num pre + 1) * 10 ^ r)

theorem witness_sound (w : List Nat × Nat × Nat × Nat) (h : witnessOK w = true) (B : Nat)
    (hB : ∀ A P t, 0 < A → PalStartsL w.1 P → orbit A t = P → t ≤ B) : w.2.2.1 ≤ B := by
  obtain ⟨pre, seed, t, r⟩ := w
  simp only [witnessOK, Bool.and_eq_true, decide_eq_true_eq, beq_iff_eq, Nat.ble_eq,
    Nat.blt_eq] at h
  obtain ⟨⟨⟨⟨⟨hw, hs⟩, _⟩, hp⟩, hlo⟩, hhi⟩ := h
  exact hB seed (orbit seed t) t hs ⟨hp, startsL_of_decStarts pre hw _ ⟨r, hlo, hhi⟩⟩ rfl

/-- `(prefix, seed, steps, r)`. -/
def witnesses : List (List Nat × Nat × Nat × Nat) :=
  [([1,2,2], 4802083327646, 103, 48),
   ([1,2,2,2], 4802083327646, 103, 47),
   ([1,3,3], 623031087358, 102, 53),
   ([1,3,3,2], 623031087358, 102, 52),
   ([1,3,5], 525853994724, 102, 53),
   ([1,3,5,4], 525853994724, 102, 52),
   ([1,3,6], 16364749691, 113, 53),
   ([1,3,6,5], 16364749691, 113, 52),
   ([1,4,4], 18788256210, 101, 48),
   ([1,4,4,3], 18788256210, 101, 47),
   ([1,4,6], 80523117705, 107, 47),
   ([1,4,6,9], 80523117705, 107, 46),
   ([1,4,8], 2495407672183, 109, 54),
   ([1,4,8,5], 2495407672183, 109, 53),
   ([1,5,7], 894868733627, 103, 47),
   ([1,5,7,3], 894868733627, 103, 46),
   ([1,5,9], 7087743853354, 109, 53),
   ([1,5,9,9], 7087743853354, 109, 52),
   ([2,2,1], 3453984598754, 116, 55),
   ([2,2,1,2], 3453984598754, 116, 54),
   ([2,3,4], 340023930894, 108, 50),
   ([2,3,4,4], 340023930894, 108, 49),
   ([3,5,9], 21217819763, 101, 46),
   ([3,5,9,9], 21217819763, 101, 45),
   ([3,6,7], 998117314580, 102, 48),
   ([3,6,7,4], 998117314580, 102, 47),
   ([3,8,7], 2960671726311, 102, 48),
   ([3,8,7,8], 2960671726311, 102, 47),
   ([4,4,5], 1186060307891929990, 261, 116),
   ([4,4,5,6], 1186060307891929990, 261, 115),
   ([4,4,7], 284829704, 116, 47),
   ([4,4,7,9], 284829704, 116, 46),
   ([4,6,1], 114560080449, 121, 55),
   ([4,6,1,8], 114560080449, 121, 54),
   ([4,8,6], 125224832174, 103, 51),
   ([4,8,6,2], 125224832174, 103, 50),
   ([5,5,5], 1702190, 101, 45),
   ([5,5,5,4], 1702190, 101, 44),
   ([5,8,3], 1469644083, 105, 46),
   ([5,8,3,1], 1469644083, 105, 45),
   ([6,6,3], 13968441660506503386020, 289, 139),
   ([6,6,3,3], 1026588326, 109, 49),
   ([6,6,3,4], 13968441660506503386020, 289, 138),
   ([6,8,4], 65687233278, 105, 53),
   ([6,8,4,2], 65687233278, 105, 52),
   ([8,9,3], 588518634474, 106, 53),
   ([8,9,3,8], 588518634474, 106, 52)]

set_option maxRecDepth 100000 in
theorem witnesses_ok : witnesses.all witnessOK = true := by
  decide +kernel

theorem witnesses_length : witnesses.length = 47 := by decide

/-- For every listed prefix, every uniform ancestry bound exceeds 100. -/
theorem no_bound_le_100 : ∀ w ∈ witnesses, ∀ B,
    (∀ A P t, 0 < A → PalStartsL w.1 P → orbit A t = P → t ≤ B) → 100 < B := by
  intro w hw B hB
  have hok := List.all_eq_true.mp witnesses_ok w hw
  have h1 := witness_sound w hok B hB
  have h2 : 100 < w.2.2.1 := by
    obtain ⟨pre, seed, t, r⟩ := w
    simp only [witnessOK, Bool.and_eq_true, decide_eq_true_eq] at hok
    exact hok.1.1.1.2
  omega

/-- Hence no `entryOK` certificate with `bound + 1 ≤ 100` exists for any listed prefix,
whatever the width `k` and rank function `R`. -/
theorem no_entry_certificate : ∀ w ∈ witnesses, ∀ (k : Nat) (R : List Nat → Option Nat),
    Agent124.PrefixR.RowsClosed k R → Agent124.PrefixR.ShortClosed k R →
    ∀ bound, entryOK k R (w.1, bound) = true → 100 ≤ bound := by
  intro w hw k R rows short bound h
  have hall := ancestry_of_entries k R rows short [(w.1, bound)] (by simp [h]) (w.1, bound)
    (by simp)
  have := no_bound_le_100 w hw (bound + 1) hall
  omega

end Sprint.Agent20.Delay

#print axioms Sprint.Agent20.Delay.witnesses_ok
#print axioms Sprint.Agent20.Delay.no_bound_le_100
#print axioms Sprint.Agent20.Delay.no_entry_certificate
