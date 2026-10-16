import Agent10PrefixExclusion

/-!
Agent #10: exact three-column synchronized-carry refinement.
The extra high carry at L-1 is an actual observed coordinate. Without that
coordinate, the weaker finite graph still has thirteen eight-word starts.
The actual transport below includes widths three and four without disjointness
assumptions on the low and reflected prefixes.

Existing three-column projections include P196.Agent4.WholeWord.nextColumns_prefix3
and Agent113.TwoDigit.nextTriple/high_carries. This file rederives only the
needed arithmetic interface directly from the accepted standalone core to avoid
importing a second foundation definition. The finite exclusion is the new result.
-/

set_option maxHeartbeats 0
set_option maxRecDepth 100000

namespace Agent10ThreeColumnExclusion
open CarryObservability Agent10PrefixExclusion
open DifferenceObservability CarryObservabilityActual
open DecimalDigits FoldedDecimal OverflowCarryNormalization CarryHistory

abbrev State3 := Nat × Nat × Nat

def Valid3 (s : State3) : Prop :=
  1 ≤ s.1 ∧ s.1 ≤ 18 ∧ s.2.1 ≤ 18 ∧ s.2.2 ≤ 18

def state3Of (q : Nat → Nat) : State3 := (q 0, q 1, q 2)
def low1 (s : State3) : Nat := s.1 / 10
def low2 (s : State3) : Nat := (s.2.1 + low1 s) / 10
def low3 (s : State3) : Nat := (s.2.2 + low2 s) / 10
def highMiddle (s : State3) (v : Bool) : Nat := (s.2.2 + innerBit v) / 10
def highFirst (s : State3) (v : Bool) : Nat := (s.2.1 + highMiddle s v) / 10
def overflow3 (s : State3) (v : Bool) : Nat := (s.1 + highFirst s v) / 10

def next3 (s : State3) (v : Bool) : State3 :=
  if overflow3 s v = 0 then
    (2*s.1 + highFirst s v - 10*low1 s,
      2*s.2.1 + low1 s + highMiddle s v - 10*(low2 s + highFirst s v),
      2*s.2.2 + low2 s + innerBit v - 10*(low3 s + highMiddle s v))
  else
    (s.1 - 10*low1 s + 1,
      s.1 + s.2.1 + low1 s + highFirst s v - 10*(low2 s + overflow3 s v),
      s.2.1 + s.2.2 + low2 s + highMiddle s v - 10*(low3 s + highFirst s v))

def compatible3 (s r : State3) (v : Bool) : Bool :=
  decide (low1 s = low1 r ∧ low2 s = low2 r ∧ low3 s = low3 r ∧
    highFirst s v = highFirst r v ∧ overflow3 s v = overflow3 r v)

/-- Exact bounded-state coding forces each intermediate triple to normalize
before another transition; this changes no actual carry arithmetic. -/
def encode3 (s : State3) : Nat := 361*s.1 + 19*s.2.1 + s.2.2
def decode3 (n : Nat) : State3 := (n/361,n/19%19,n%19)
def nextCode (s : Nat) (v : Bool) : Nat := encode3 (next3 (decode3 s) v)
def compatibleCode (s r : Nat) (v : Bool) : Bool :=
  compatible3 (decode3 s) (decode3 r) v

def survivesCode : Nat → Nat → Nat → Bool
  | 0,_,_ => true
  | n+1,s,r =>
      (compatibleCode s r false && survivesCode n (nextCode s false) (nextCode r false)) ||
      (compatibleCode s r true && survivesCode n (nextCode s true) (nextCode r true))

def survives3 (n : Nat) (s r : State3) : Bool :=
  survivesCode n (encode3 s) (encode3 r)

theorem decode_encode3 (s : State3) (hs : Valid3 s) : decode3 (encode3 s) = s := by
  rcases s with ⟨p,q,r⟩
  rcases hs with ⟨hp,hp',hq,hr⟩
  dsimp only at hp hp' hq hr
  simp only [encode3,decode3]
  apply Prod.ext
  · dsimp only; omega
  · apply Prod.ext <;> dsimp only <;> omega

/-- The full finite check is partitioned by the eighteen exterior values
to bound kernel reduction memory. Every one of the 5,184 starts is covered. -/
abbrev EightExcludedAt (p : Nat) : Prop :=
  ∀ q : Fin 18, ∀ r : Fin 16,
    survives3 8 (p+1,q.val+1,r.val) (p+1,q.val,r.val+3) = false

theorem exclusion_p0 : EightExcludedAt 0 := by decide +kernel
#print axioms exclusion_p0

theorem exclusion_p1 : EightExcludedAt 1 := by decide +kernel
#print axioms exclusion_p1

theorem exclusion_p2 : EightExcludedAt 2 := by decide +kernel
#print axioms exclusion_p2

theorem exclusion_p3 : EightExcludedAt 3 := by decide +kernel
#print axioms exclusion_p3

theorem exclusion_p4 : EightExcludedAt 4 := by decide +kernel
#print axioms exclusion_p4

theorem exclusion_p5 : EightExcludedAt 5 := by decide +kernel
#print axioms exclusion_p5

theorem exclusion_p6 : EightExcludedAt 6 := by decide +kernel
#print axioms exclusion_p6

theorem exclusion_p7 : EightExcludedAt 7 := by decide +kernel
#print axioms exclusion_p7

theorem exclusion_p8 : EightExcludedAt 8 := by decide +kernel
#print axioms exclusion_p8

theorem exclusion_p9 : EightExcludedAt 9 := by decide +kernel
#print axioms exclusion_p9

theorem exclusion_p10 : EightExcludedAt 10 := by decide +kernel
#print axioms exclusion_p10

theorem exclusion_p11 : EightExcludedAt 11 := by decide +kernel
#print axioms exclusion_p11

theorem exclusion_p12 : EightExcludedAt 12 := by decide +kernel
#print axioms exclusion_p12

theorem exclusion_p13 : EightExcludedAt 13 := by decide +kernel
#print axioms exclusion_p13

theorem exclusion_p14 : EightExcludedAt 14 := by decide +kernel
#print axioms exclusion_p14

theorem exclusion_p15 : EightExcludedAt 15 := by decide +kernel
#print axioms exclusion_p15

theorem exclusion_p16 : EightExcludedAt 16 := by decide +kernel
#print axioms exclusion_p16

theorem exclusion_p17 : EightExcludedAt 17 := by decide +kernel
#print axioms exclusion_p17

theorem eight_three_prefix_exclusion_fin :
    ∀ p : Fin 18, ∀ q : Fin 18, ∀ r : Fin 16,
      survives3 8 (p.val+1,q.val+1,r.val) (p.val+1,q.val,r.val+3) = false := by
  intro p q r
  have hp := p.isLt
  have hcases : p.val = 0 ∨ p.val = 1 ∨ p.val = 2 ∨ p.val = 3 ∨ p.val = 4 ∨ p.val = 5 ∨ p.val = 6 ∨ p.val = 7 ∨ p.val = 8 ∨ p.val = 9 ∨ p.val = 10 ∨ p.val = 11 ∨ p.val = 12 ∨ p.val = 13 ∨ p.val = 14 ∨ p.val = 15 ∨ p.val = 16 ∨ p.val = 17 := by omega
  rcases hcases with h | h | h | h | h | h | h | h | h | h | h | h | h | h | h | h | h | h
  · simpa only [h] using exclusion_p0 q r
  · simpa only [h] using exclusion_p1 q r
  · simpa only [h] using exclusion_p2 q r
  · simpa only [h] using exclusion_p3 q r
  · simpa only [h] using exclusion_p4 q r
  · simpa only [h] using exclusion_p5 q r
  · simpa only [h] using exclusion_p6 q r
  · simpa only [h] using exclusion_p7 q r
  · simpa only [h] using exclusion_p8 q r
  · simpa only [h] using exclusion_p9 q r
  · simpa only [h] using exclusion_p10 q r
  · simpa only [h] using exclusion_p11 q r
  · simpa only [h] using exclusion_p12 q r
  · simpa only [h] using exclusion_p13 q r
  · simpa only [h] using exclusion_p14 q r
  · simpa only [h] using exclusion_p15 q r
  · simpa only [h] using exclusion_p16 q r
  · simpa only [h] using exclusion_p17 q r

theorem seven_three_prefix_survival :
    survives3 7 (16,6,0) (16,5,3) = true := by decide +kernel

theorem eight_three_prefix_exclusion (s r : State3)
    (hs : Valid3 s) (hr : Valid3 r)
    (hp : s.1 = r.1) (hq : s.2.1 = r.2.1 + 1)
    (hr' : r.2.2 = s.2.2 + 3) : survives3 8 s r = false := by
  rcases s with ⟨p,q,z⟩
  rcases r with ⟨p',q',z'⟩
  rcases hs with ⟨hp0,hp1,hq1,hz1⟩
  rcases hr with ⟨hp0',hp1',hq1',hz1'⟩
  dsimp only at hp hq hr' hp0 hp1 hq1 hz1 hp0' hp1' hq1' hz1'
  have h := eight_three_prefix_exclusion_fin
    ⟨p-1,by omega⟩ ⟨q',by omega⟩ ⟨z,by omega⟩
  have he : p-1+1=p := by omega
  simpa only [he, ←hp, ←hq, ←hr'] using h

def observedBit3 (q : Nat → Nat) (L : Nat) : Bool :=
  decide (carry q (L-3) = 1)

theorem observedBit3_value (q : Nat → Nat) (L : Nat)
    (hq : ∀ i, i < L → q i ≤ 18) :
    innerBit (observedBit3 q L) = carry q (L-3) := by
  have hb := carry_bounded q L hq (L-3) (by omega)
  by_cases h : carry q (L-3) = 1
  · simp [innerBit,observedBit3,h]
  · have hz : carry q (L-3) = 0 := by omega
    simp [innerBit,observedBit3,hz]

theorem state3_valid (q : Nat → Nat) (L : Nat)
    (hq : Admissible L q) (hL : 3 ≤ L) : Valid3 (state3Of q) := by
  change 1 ≤ q 0 ∧ q 0 ≤ 18 ∧ q 1 ≤ 18 ∧ q 2 ≤ 18
  have h0 := hq.2.2.1 0 hq.1
  have h1 := hq.2.2.1 1 (by omega)
  have h2 := hq.2.2.1 2 (by omega)
  have hp := hq.2.1
  exact ⟨by omega,h0,h1,h2⟩

/-- The high coordinates are derived by exact symmetry, including overlap. -/
theorem prefix_carries3_exact (q : Nat → Nat) (L : Nat)
    (hq : Admissible L q) (hL : 3 ≤ L) :
    low1 (state3Of q) = carry q 1 ∧
    low2 (state3Of q) = carry q 2 ∧
    low3 (state3Of q) = carry q 3 ∧
    highMiddle (state3Of q) (observedBit3 q L) = carry q (L-2) ∧
    highFirst (state3Of q) (observedBit3 q L) = carry q (L-1) ∧
    overflow3 (state3Of q) (observedBit3 q L) = carry q L := by
  have hbit := observedBit3_value q L hq.2.2.1
  have h0 := (folded_carry_transition q L 0 hq.1 hq.2.2.2.1).2
  have h1 := (folded_carry_transition q L 1 (by omega) hq.2.2.2.1).2
  have h2 := (folded_carry_transition q L 2 (by omega) hq.2.2.2.1).2
  have hi1 : L-1-1=L-2 := by omega
  have hi2 : L-1-2=L-3 := by omega
  simp only [Nat.sub_zero] at h0
  rw [hi1] at h1
  rw [hi2] at h2
  have hm : highMiddle (state3Of q) (observedBit3 q L) = carry q (L-2) := by
    change (q 2 + innerBit (observedBit3 q L)) / 10 = _
    rw [hbit]
    exact h2.symm
  have hf : highFirst (state3Of q) (observedBit3 q L) = carry q (L-1) := by
    change (q 1 + highMiddle (state3Of q) (observedBit3 q L)) / 10 = _
    rw [hm]
    exact h1.symm
  refine ⟨?_,?_,?_,hm,hf,?_⟩
  · simp [low1,state3Of,carry]
  · simp [low2,low1,state3Of,carry]
  · simp [low3,low2,low1,state3Of,carry]
  · change (q 0 + highFirst (state3Of q) (observedBit3 q L)) / 10 = _
    rw [hf]
    exact h0.symm

/-- The next triple is exactly the repository's current normalization. -/
theorem prefix_step3_exact (q : Nat → Nat) (L : Nat)
    (hq : Admissible L q) (hL : 3 ≤ L) :
    state3Of (nextColumns q L) = next3 (state3Of q) (observedBit3 q L) := by
  rcases prefix_carries3_exact q L hq hL with ⟨ha,hb,hc,hu,hv,hh⟩
  have hbit := observedBit3_value q L hq.2.2.1
  have h0 : carry q 0 = 0 := rfl
  have hc2 : carry q (1+1) = carry q 2 := rfl
  have hc3 : carry q (2+1) = carry q 3 := rfl
  have hq1 : q (2-1) = q 1 := rfl
  have hfirst : carry q 1 = q 0 / 10 := by simp [carry]
  have hfirst_bound : 10*carry q 1 ≤ q 0 := by rw [hfirst]; omega
  unfold next3
  rw [ha,hb,hc,hu,hv,hh,hbit]
  simp only [state3Of]
  by_cases ho : carry q L = 0
  · rw [if_pos ho]
    have he0 := next_column_no_overflow q L 0 hq.1 hq.2.2.2.1 ho
    have he1 := next_column_no_overflow q L 1 (by omega) hq.2.2.2.1 ho
    have he2 := next_column_no_overflow q L 2 (by omega) hq.2.2.2.1 ho
    have hi1 : L-1-1=L-2 := by omega
    have hi2 : L-1-2=L-3 := by omega
    simp only [Nat.zero_add,Nat.sub_zero,h0,ho,hi1,hi2,hc2,hc3] at he0 he1 he2
    apply Prod.ext
    · dsimp only; omega
    · apply Prod.ext <;> dsimp only <;> omega
  · rw [if_neg ho]
    have hb' := carry_bounded q L hq.2.2.1 L (Nat.le_refl L)
    have hc' : carry q L = 1 := by omega
    have he0 := next_column_overflow_outer q L hq.1 hc'
    have he1 := next_column_overflow_interior q L 1 (by decide) (by omega) hq.2.2.2.1 hc'
    have he2 := next_column_overflow_interior q L 2 (by decide) (by omega) hq.2.2.2.1 hc'
    have hi1 : L-1+1=L := by omega
    have hi2 : L-2+1=L-1 := by omega
    simp only [Nat.zero_add,Nat.sub_zero,Nat.sub_self,h0,hc',hi1,hi2,hc2,hc3,hq1] at he0 he1 he2
    apply Prod.ext
    · dsimp only; omega
    · apply Prod.ext <;> dsimp only <;> omega

#print axioms eight_three_prefix_exclusion_fin
#print axioms decode_encode3
#print axioms seven_three_prefix_survival
#print axioms eight_three_prefix_exclusion
#print axioms prefix_carries3_exact
#print axioms prefix_step3_exact

end Agent10ThreeColumnExclusion
