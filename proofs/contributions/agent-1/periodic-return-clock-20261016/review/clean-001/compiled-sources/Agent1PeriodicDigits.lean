import Agent1RepeatedBlockContext

/-!
The exact normalized two-band digit decomposition feeding the raw guard lemma.
All arithmetic is unchanged Agent8 arithmetic. These statements hold before
imposing symmetry/realizability and do not claim safe iteration.
-/
namespace Agent1.Periodic
open Agent8 Agent1.RepeatedBlock

def periodicWord (B H w : Word) (k : Nat) : Word :=
  B ++ pow w k ++ H ++ pow w.reverse k ++ B.reverse

def leftEntry (B : Word) : Nat := terminalCarry B 0
def leftCarry (B w : Word) : Nat := terminalCarry w (leftEntry B)
def rightEntry (B H w : Word) : Nat := terminalCarry H (leftCarry B w)
def rightCarry (B H w : Word) : Nat := terminalCarry w.reverse (rightEntry B H w)

def leftGuardDigits (B w : Word) : Word :=
  fixedDigits B 0 ++ fixedDigits w (leftEntry B)
def leftPeriodDigits (B w : Word) : Word := fixedDigits w (leftCarry B w)
def centerGuardDigits (B H w : Word) : Word :=
  fixedDigits H (leftCarry B w) ++ fixedDigits w.reverse (rightEntry B H w)
def rightPeriodDigits (B H w : Word) : Word := fixedDigits w.reverse (rightCarry B H w)
def rightGuardDigits (B H w : Word) : Word := normalize B.reverse (rightCarry B H w)

/-- One first-copy guard in each direction isolates both stable digit periods. -/
theorem normalize_periodicWord (B H w : Word) (k : Nat)
    (hB : Bounded B 18) (hH : Bounded H 18) (hw : Bounded w 18) :
    normalize (periodicWord B H w (k+3)) 0 =
      leftGuardDigits B w ++ pow (leftPeriodDigits B w) (k+2) ++
      centerGuardDigits B H w ++ pow (rightPeriodDigits B H w) (k+2) ++
      rightGuardDigits B H w := by
  have hb : leftEntry B ≤ 1 := terminalCarry_le_one B 0 hB (by omega)
  have hc : leftCarry B w ≤ 1 := terminalCarry_le_one w (leftEntry B) hw hb
  have hwr : Bounded w.reverse 18 := fun x hx => hw x (List.mem_reverse.mp hx)
  have hleft := normalize_context B w (H ++ pow w.reverse (k+3) ++ B.reverse)
    0 (k+2) hB hw (by omega)
  have hright := normalize_context H w.reverse B.reverse (leftCarry B w)
    (k+2) hH hwr hc
  unfold periodicWord
  rw [show B ++ pow w (k+3) ++ H ++ pow w.reverse (k+3) ++ B.reverse =
    B ++ pow w (k+3) ++ (H ++ pow w.reverse (k+3) ++ B.reverse) by
      simp only [List.append_assoc]]
  rw [hleft]
  change fixedDigits B 0 ++ fixedDigits w (leftEntry B) ++
    pow (fixedDigits w (leftCarry B w)) (k+2) ++
      normalize (H ++ pow w.reverse (k+3) ++ B.reverse) (leftCarry B w) = _
  rw [hright]
  simp only [leftGuardDigits, leftPeriodDigits, centerGuardDigits,
    rightPeriodDigits, rightGuardDigits, rightEntry, rightCarry, List.append_assoc]

theorem scan_carry_stable (B H w : Word) (k : Nat)
    (hB : Bounded B 18) (hH : Bounded H 18) (hw : Bounded w 18) :
    terminalCarry (periodicWord B H w (k+1)) 0 =
      terminalCarry (periodicWord B H w 3) 0 := by
  have hk := terminalCarry_symmetric_bands B w H 0 k hB hw hH (by omega)
  have h3 := terminalCarry_symmetric_bands B w H 0 2 hB hw hH (by omega)
  exact hk.trans h3.symm

theorem scan_carry_eq (B H w : Word)
    (hB : Bounded B 18) (hH : Bounded H 18) (hw : Bounded w 18) :
    terminalCarry (periodicWord B H w 3) 0 = terminalCarry B.reverse (rightCarry B H w) := by
  have h := terminalCarry_symmetric_bands B w H 0 2 hB hw hH (by omega)
  simpa only [periodicWord, terminalCarry_append, leftEntry, leftCarry,
    rightEntry, rightCarry] using h

theorem scan_carry_le_one (B H w : Word)
    (hB : Bounded B 18) (hH : Bounded H 18) (hw : Bounded w 18) :
    terminalCarry (periodicWord B H w 3) 0 ≤ 1 := by
  have hb := terminalCarry_le_one B 0 hB (by omega)
  have hc := terminalCarry_le_one w (leftEntry B) hw hb
  have hh := terminalCarry_le_one H (leftCarry B w) hH hc
  have hwr : Bounded w.reverse 18 := fun x hx => hw x (List.mem_reverse.mp hx)
  have hBr : Bounded B.reverse 18 := fun x hx => hB x (List.mem_reverse.mp hx)
  have hr := terminalCarry_le_one w.reverse (rightEntry B H w) hwr hh
  rw [scan_carry_eq B H w hB hH hw]
  exact terminalCarry_le_one B.reverse (rightCarry B H w) hBr hr

/-- Exact lengths of the five fixed digit blocks, including actual overflow. -/
theorem scan_block_lengths (B H w : Word)
    (hB : Bounded B 18) (hH : Bounded H 18) (hw : Bounded w 18) :
    (leftGuardDigits B w).length = B.length + w.length ∧
    (leftPeriodDigits B w).length = w.length ∧
    (centerGuardDigits B H w).length = H.length + w.length ∧
    (rightPeriodDigits B H w).length = w.length ∧
    (rightGuardDigits B H w).length = B.length + terminalCarry (periodicWord B H w 3) 0 := by
  have hb := terminalCarry_le_one B 0 hB (by omega)
  have hc := terminalCarry_le_one w (leftEntry B) hw hb
  have hh := terminalCarry_le_one H (leftCarry B w) hH hc
  have hwr : Bounded w.reverse 18 := fun x hx => hw x (List.mem_reverse.mp hx)
  have hBr : Bounded B.reverse 18 := fun x hx => hB x (List.mem_reverse.mp hx)
  have hr := terminalCarry_le_one w.reverse (rightEntry B H w) hwr hh
  simp only [leftGuardDigits, leftPeriodDigits, centerGuardDigits, rightPeriodDigits,
    rightGuardDigits, List.length_append, fixedDigits_length, List.length_reverse,
    normalize_length B.reverse (rightCarry B H w) hBr hr,
    scan_carry_eq B H w hB hH hw, and_self]

end Agent1.Periodic

#print axioms Agent1.Periodic.normalize_periodicWord
#print axioms Agent1.Periodic.scan_carry_stable
#print axioms Agent1.Periodic.scan_carry_eq
#print axioms Agent1.Periodic.scan_carry_le_one
#print axioms Agent1.Periodic.scan_block_lengths
