import Agent1RepeatedBlock

/-!
Exact fixed-context and two-band consequences of repeated-block normalization.
The prefix and repeated blocks contain decimal pair coefficients (at most 18).
The incoming carry is a bit. No symmetry or nonempty-block assumption is hidden.
These identities concern one normalization, not recurrence of reverse-add states.
-/

namespace Agent1.RepeatedBlock
open Agent8

theorem pow_length (w : Word) (k : Nat) :
    (pow w k).length = k * w.length := by
  induction k with
  | zero => simp [pow]
  | succ k ih => simp [pow, ih, Nat.succ_mul, Nat.add_comm]

theorem bounded_pow (w : Word) (k b : Nat) (hw : Bounded w b) :
    Bounded (pow w k) b := by
  induction k with
  | zero => simp [pow, Bounded]
  | succ k ih =>
    intro x hx
    simp only [pow, List.mem_append] at hx
    exact hx.elim (hw x) (ih x)

/-- The exact normalized output in arbitrary fixed context. The suffix may be
unbounded: its full original normalization at the stabilized carry is retained. -/
theorem normalize_context (B w H : Word) (e k : Nat)
    (hB : Bounded B 18) (hw : Bounded w 18) (he : e ≤ 1) :
    normalize (B ++ pow w (k+1) ++ H) e =
      fixedDigits B e ++ fixedDigits w (terminalCarry B e) ++
      pow (fixedDigits w (terminalCarry w (terminalCarry B e))) k ++
      normalize H (terminalCarry w (terminalCarry B e)) := by
  have hb := terminalCarry_le_one B e hB he
  simp only [normalize_append, fixedDigits_append, terminalCarry_append]
  rw [fixedDigits_pow_succ w (terminalCarry B e) k hw hb,
      terminalCarry_pow_succ w (terminalCarry B e) k hw hb]
  simp only [List.append_assoc]

/-- All positive repetition counts have the same actual outgoing carry. -/
theorem terminalCarry_context (B w H : Word) (e k : Nat)
    (hB : Bounded B 18) (hw : Bounded w 18) (he : e ≤ 1) :
    terminalCarry (B ++ pow w (k+1) ++ H) e =
      terminalCarry (B ++ w ++ H) e := by
  have hb := terminalCarry_le_one B e hB he
  simp only [terminalCarry_append]
  rw [terminalCarry_pow_succ w (terminalCarry B e) k hw hb]

/-- Two separated repeated bands may vary independently. A bounded middle
ensures that the second band also receives a bit carry. The final suffix is arbitrary. -/
theorem terminalCarry_two_bands (B w H v T : Word) (e k l : Nat)
    (hB : Bounded B 18) (hw : Bounded w 18) (hH : Bounded H 18)
    (hv : Bounded v 18) (he : e ≤ 1) :
    terminalCarry (B ++ pow w (k+1) ++ H ++ pow v (l+1) ++ T) e =
      terminalCarry (B ++ w ++ H ++ v ++ T) e := by
  have hb := terminalCarry_le_one B e hB he
  have hc := terminalCarry_le_one w (terminalCarry B e) hw hb
  have hh := terminalCarry_le_one H (terminalCarry w (terminalCarry B e)) hH hc
  simp only [terminalCarry_append]
  rw [terminalCarry_pow_succ w (terminalCarry B e) k hw hb,
      terminalCarry_pow_succ v (terminalCarry H (terminalCarry w (terminalCarry B e))) l hv hh]

/-- In particular, the terminal carry of symmetric repeated bands does not
depend on their positive common copy count. No palindromicity of H is required. -/
theorem terminalCarry_symmetric_bands (B w H : Word) (e k : Nat)
    (hB : Bounded B 18) (hw : Bounded w 18) (hH : Bounded H 18) (he : e ≤ 1) :
    terminalCarry (B ++ pow w (k+1) ++ H ++ pow w.reverse (k+1) ++ B.reverse) e =
      terminalCarry (B ++ w ++ H ++ w.reverse ++ B.reverse) e := by
  apply terminalCarry_two_bands B w H w.reverse B.reverse e k k hB hw hH _ he
  intro x hx
  exact hw x (List.mem_reverse.mp hx)

/-- Exact output width: only the repeated block length grows with k; the
possible final carry is that of the single-copy context. -/
theorem normalize_context_length (B w H : Word) (e k : Nat)
    (hB : Bounded B 18) (hw : Bounded w 18) (hH : Bounded H 18) (he : e ≤ 1) :
    (normalize (B ++ pow w (k+1) ++ H) e).length =
      B.length + (k+1) * w.length + H.length + terminalCarry (B ++ w ++ H) e := by
  have hwhole : Bounded (B ++ pow w (k+1) ++ H) 18 := by
    intro x hx
    simp only [List.mem_append] at hx
    rcases hx with (hx | hx) | hx
    · exact hB x hx
    · exact bounded_pow w (k+1) 18 hw x hx
    · exact hH x hx
  rw [normalize_length _ _ hwhole he, terminalCarry_context B w H e k hB hw he]
  simp only [List.length_append, pow_length]

/-- Exact width for symmetric repeated bands: their outgoing carry is fixed
by one copy, so only the explicit repeated coefficient width grows. -/
theorem normalize_symmetric_bands_length (B w H : Word) (e k : Nat)
    (hB : Bounded B 18) (hw : Bounded w 18) (hH : Bounded H 18) (he : e ≤ 1) :
    (normalize (B ++ pow w (k+1) ++ H ++ pow w.reverse (k+1) ++ B.reverse) e).length =
      2 * B.length + 2 * ((k+1) * w.length) + H.length +
      terminalCarry (B ++ w ++ H ++ w.reverse ++ B.reverse) e := by
  have hwr : Bounded w.reverse 18 := fun x hx => hw x (List.mem_reverse.mp hx)
  have hBr : Bounded B.reverse 18 := fun x hx => hB x (List.mem_reverse.mp hx)
  have hwhole : Bounded
      (B ++ pow w (k+1) ++ H ++ pow w.reverse (k+1) ++ B.reverse) 18 := by
    intro x hx
    simp only [List.mem_append] at hx
    rcases hx with (((hx | hx) | hx) | hx) | hx
    · exact hB x hx
    · exact bounded_pow w (k+1) 18 hw x hx
    · exact hH x hx
    · exact bounded_pow w.reverse (k+1) 18 hwr x hx
    · exact hBr x hx
  rw [normalize_length _ _ hwhole he,
      terminalCarry_symmetric_bands B w H e k hB hw hH he]
  simp only [List.length_append, pow_length, List.length_reverse]
  omega

end Agent1.RepeatedBlock

#print axioms Agent1.RepeatedBlock.pow_length
#print axioms Agent1.RepeatedBlock.bounded_pow
#print axioms Agent1.RepeatedBlock.normalize_context
#print axioms Agent1.RepeatedBlock.terminalCarry_context
#print axioms Agent1.RepeatedBlock.terminalCarry_two_bands
#print axioms Agent1.RepeatedBlock.terminalCarry_symmetric_bands
#print axioms Agent1.RepeatedBlock.normalize_context_length

#print axioms Agent1.RepeatedBlock.normalize_symmetric_bands_length
