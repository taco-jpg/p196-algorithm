import P196.Drafts.Agent120NeutralBandCalibration.A120Certificate

/-!
# Structural transport of center trim schedules

The padding operation is a parameter. These identities concern edge records,
their chain endpoints and their total trim counts only. Checking transported
edges requires a separate padding covariance theorem for the original checker.
-/

namespace Agent104.NeutralTrimTransport

open Agent120.Neutral

/-- Total number of symmetric center pairs trimmed by a chain. -/
def sumV : List Edge → Nat
  | [] => 0
  | E :: es => E.v + sumV es

/-- Replace the center trim schedule using nonnegative padding reserves.

For matching list lengths, the source reserve is the accumulated old trim
plus the remaining new trim. Every target reserve is the next source reserve.
The empty mismatched cases are deliberately inert; the structural theorems
below require matching list lengths.
-/
def retime (pad : Nat → List Nat → List Nat) :
    Nat → List Edge → List Nat → List Edge
  | q, E :: es, w :: ws =>
      { E with
        C := pad (q + w + ws.sum) E.C
        C2 := pad (q + E.v + ws.sum) E.C2
        v := w } :: retime pad (q + E.v) es ws
  | _, _, _ => []

/-- The transported center trims are exactly the requested schedule. -/
theorem retime_v (pad : Nat → List Nat → List Nat) (q : Nat)
    (es : List Edge) (ws : List Nat) (hl : es.length = ws.length) :
    (retime pad q es ws).map (fun E => E.v) = ws := by
  induction es generalizing q ws with
  | nil =>
      have hw : ws = [] := List.length_eq_zero_iff.mp (by simpa using hl.symm)
      subst ws
      rfl
  | cons E es ih =>
      cases ws with
      | nil => simp at hl
      | cons w ws =>
          have ht : es.length = ws.length := by simpa using hl
          simp [retime, ih (q + E.v) ws ht]

/-- Both exterior interfaces and every exterior trim are unchanged. -/
theorem retime_fields (pad : Nat → List Nat → List Nat) (q : Nat)
    (es : List Edge) (ws : List Nat) (hl : es.length = ws.length) :
    (retime pad q es ws).map (fun E => (E.B, E.B2, E.u)) =
      es.map (fun E => (E.B, E.B2, E.u)) := by
  induction es generalizing q ws with
  | nil =>
      have hw : ws = [] := List.length_eq_zero_iff.mp (by simpa using hl.symm)
      subst ws
      rfl
  | cons E es ih =>
      cases ws with
      | nil => simp at hl
      | cons w ws =>
          have ht : es.length = ws.length := by simpa using hl
          simp [retime, ih (q + E.v) ws ht]

/-- Transport preserves the number of edges. -/
theorem retime_length (pad : Nat → List Nat → List Nat) (q : Nat)
    (es : List Edge) (ws : List Nat) (hl : es.length = ws.length) :
    (retime pad q es ws).length = es.length := by
  have hv := congrArg List.length (retime_v pad q es ws hl)
  simp only [List.length_map] at hv
  omega

/-- The final exterior interface is unchanged. -/
theorem retime_endB (pad : Nat → List Nat → List Nat) (q : Nat)
    (es : List Edge) (ws : List Nat) (B : List Nat)
    (hl : es.length = ws.length) :
    endB (retime pad q es ws) B = endB es B := by
  induction es generalizing q ws B with
  | nil =>
      have hw : ws = [] := List.length_eq_zero_iff.mp (by simpa using hl.symm)
      subst ws
      rfl
  | cons E es ih =>
      cases ws with
      | nil => simp at hl
      | cons w ws =>
          have ht : es.length = ws.length := by simpa using hl
          simpa only [retime, endB] using ih (q + E.v) ws E.B2 ht

/-- The terminal reserve uses the old total trim, while the initial reserve
uses the new total trim. -/
theorem retime_endC (pad : Nat → List Nat → List Nat) (q : Nat)
    (es : List Edge) (ws : List Nat) (C : List Nat)
    (hl : es.length = ws.length) :
    endC (retime pad q es ws) (pad (q + ws.sum) C) =
      pad (q + sumV es) (endC es C) := by
  induction es generalizing q ws C with
  | nil =>
      have hw : ws = [] := List.length_eq_zero_iff.mp (by simpa using hl.symm)
      subst ws
      rfl
  | cons E es ih =>
      cases ws with
      | nil => simp at hl
      | cons w ws =>
          have ht : es.length = ws.length := by simpa using hl
          simpa only [retime, endC, sumV, Nat.add_assoc] using
            ih (q + E.v) ws E.C2 ht

/-- The transported center trim total equals the new schedule sum. -/
theorem retime_sumV (pad : Nat → List Nat → List Nat) (q : Nat)
    (es : List Edge) (ws : List Nat) (hl : es.length = ws.length) :
    sumV (retime pad q es ws) = ws.sum := by
  induction es generalizing q ws with
  | nil =>
      have hw : ws = [] := List.length_eq_zero_iff.mp (by simpa using hl.symm)
      subst ws
      rfl
  | cons E es ih =>
      cases ws with
      | nil => simp at hl
      | cons w ws =>
          have ht : es.length = ws.length := by simpa using hl
          simp [retime, sumV, ih (q + E.v) ws ht]

/-- Exterior gains stay fixed; replacing center trims changes total gain by
exactly the difference between the new and old center trim totals. -/
theorem retime_sumGain (pad : Nat → List Nat → List Nat) (q : Nat)
    (es : List Edge) (ws : List Nat) (hl : es.length = ws.length) :
    sumGain (retime pad q es ws) + sumV es = sumGain es + ws.sum := by
  induction es generalizing q ws with
  | nil =>
      have hw : ws = [] := List.length_eq_zero_iff.mp (by simpa using hl.symm)
      subst ws
      rfl
  | cons E es ih =>
      cases ws with
      | nil => simp at hl
      | cons w ws =>
          have ht : es.length = ws.length := by simpa using hl
          have hi := ih (q + E.v) ws ht
          simp only [retime, sumGain, sumV, List.sum_cons]
          omega

end Agent104.NeutralTrimTransport

#print axioms Agent104.NeutralTrimTransport.retime_v
#print axioms Agent104.NeutralTrimTransport.retime_fields
#print axioms Agent104.NeutralTrimTransport.retime_length
#print axioms Agent104.NeutralTrimTransport.retime_endB
#print axioms Agent104.NeutralTrimTransport.retime_endC
#print axioms Agent104.NeutralTrimTransport.retime_sumV
#print axioms Agent104.NeutralTrimTransport.retime_sumGain
