import P196.Foundations.LychrelDigitSums

namespace Agent13FoldedFamily
open DecimalDigits FoldedDecimal Lychrel196

/-- The two four-column alternatives from the source, not transition assumptions. -/
def blockDigit (e : Bool) (j : Nat) : Nat := if e then (if j < 2 then 14 else 4) else 9
def blockLow (e : Bool) (j : Nat) : Nat := if e && (j = 1 || j = 2) then 1 else 0
def blockHigh (e : Bool) (j : Nat) : Nat := if e then (if j < 2 ∨ j = 4 then 1 else 0) else 1

theorem block_start (e : Bool) : blockLow e 0 = 0 ∧ blockHigh e 0 = 1 := by
  cases e <;> decide

theorem block_finish (e : Bool) : blockLow e 4 = 0 ∧ blockHigh e 4 = 1 := by
  cases e <;> decide

/-- Seven concrete arithmetic edges, checked by ordinary kernel reduction. -/
theorem block_edges (e : Bool) (j : Nat) (hj : j < 4) :
    blockLow e (j+1) = (blockDigit e j + blockLow e j)/10 ∧
    blockHigh e j = (blockDigit e j + blockHigh e (j+1))/10 ∧
    (blockDigit e j + blockLow e j)%10 +
      (blockDigit e j + blockHigh e (j+1))%10 = 9 := by
  have hc : j = 0 ∨ j = 1 ∨ j = 2 ∨ j = 3 := by omega
  rcases hc with rfl | rfl | rfl | rfl <;> cases e <;> decide

def halfWidth (r k : Nat) : Nat := 4*r+k+2

def inputHalf (e : Nat → Bool) (r i : Nat) : Nat :=
  if i=0 then 5
  else if i < 4*r+1 then blockDigit (e ((i-1)/4)) ((i-1)%4)
  else if i=4*r+1 then 14 else 18

def targetHalf (r i : Nat) : Nat := if i=0 then 11 else if i ≤ 4*r+1 then 9 else 18

def lowTrace (e : Nat → Bool) (r i : Nat) : Nat :=
  if i=0 then 0 else if i ≤ 4*r+1 then blockLow (e ((i-1)/4)) ((i-1)%4) else 1

def highTrace (e : Nat → Bool) (r i : Nat) : Nat :=
  if i=0 then 0 else if i ≤ 4*r+1 then blockHigh (e ((i-1)/4)) ((i-1)%4) else 1

/-- Consecutive block-boundary states match even when the next bit changes. -/
theorem block_join (e : Nat → Bool) (n : Nat) :
    blockLow (e ((n+1)/4)) ((n+1)%4) = blockLow (e (n/4)) (n%4+1) ∧
    blockHigh (e ((n+1)/4)) ((n+1)%4) = blockHigh (e (n/4)) (n%4+1) := by
  have hm : n%4 < 4 := Nat.mod_lt _ (by decide)
  by_cases h : n%4=3
  · have h0 : (n+1)%4 = 0 := by omega
    rw [h0, h]
    constructor
    · exact (block_start _).1.trans (block_finish _).1.symm
    · exact (block_start _).2.trans (block_finish _).2.symm
  · have hd : (n+1)/4=n/4 := by omega
    have hr : (n+1)%4=n%4+1 := by omega
    rw [hd,hr]
    exact ⟨rfl,rfl⟩

theorem outer_trace (e : Nat → Bool) (r : Nat) :
    lowTrace e r 0 = 0 ∧ highTrace e r 0 = 0 ∧
    lowTrace e r 1 = 0 ∧ highTrace e r 1 = 1 := by
  simp [lowTrace, highTrace, blockLow, blockHigh]

theorem terminal_boundary (e : Nat → Bool) (r : Nat) :
    lowTrace e r (4*r+1) = 0 ∧ highTrace e r (4*r+1) = 1 := by
  simp [lowTrace, highTrace, blockLow, blockHigh]

theorem trace_edges (e : Nat → Bool) (r i : Nat) :
    lowTrace e r (i+1) = (inputHalf e r i + lowTrace e r i)/10 ∧
    highTrace e r i = (inputHalf e r i + highTrace e r (i+1))/10 ∧
    (inputHalf e r i + lowTrace e r i)%10 +
      (inputHalf e r i + highTrace e r (i+1))%10 = targetHalf r i := by
  by_cases hz : i=0
  · subst i
    have h := outer_trace e r
    simp only [inputHalf, targetHalf, if_pos rfl]
    rw [h.1, h.2.1, h.2.2.1, h.2.2.2]
    simp
  · by_cases hi : i < 4*r+1
    · have hj := block_join e (i-1)
      have he := block_edges (e ((i-1)/4)) ((i-1)%4) (Nat.mod_lt _ (by decide))
      have hn : i-1+1=i := by omega
      rw [hn] at hj
      simp only [inputHalf, lowTrace, highTrace, targetHalf, hz,
        show i+1 ≠ 0 by omega, if_false, hi, show i ≤ 4*r+1 by omega,
        show i+1 ≤ 4*r+1 by omega, if_true, Nat.add_sub_cancel]
      rw [hj.1,hj.2]
      exact he
    · by_cases heq : i=4*r+1
      · subst i
        have h := terminal_boundary e r
        have hlow : lowTrace e r (4*r+1+1)=1 := by simp [lowTrace, show ¬ 4*r+1+1 ≤ 4*r+1 by omega]
        have hhigh : highTrace e r (4*r+1+1)=1 := by simp [highTrace, show ¬ 4*r+1+1 ≤ 4*r+1 by omega]
        simp only [inputHalf, targetHalf, hz, if_false, Nat.lt_irrefl,
          if_pos rfl, Nat.le_refl, if_true]
        rw [h.1,h.2,hlow,hhigh]
        decide
      · have hgt : 4*r+1 < i := by omega
        simp [inputHalf, lowTrace, highTrace, targetHalf, hz, hi, heq,
          show ¬ i ≤ 4*r+1 by omega, show ¬ i+1 ≤ 4*r+1 by omega,
          show i+1 ≠ 0 by omega]

end Agent13FoldedFamily
