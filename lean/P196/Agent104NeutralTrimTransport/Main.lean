import P196.Agent104NeutralTrimTransport.Schedule
import P196.Agent119NeutralCenterPadding.Main

/-!
# Complete neutral center-schedule transport

The concrete padding facts are Agent119's local formalization of the credited
Agent7/Agent107 covariance. This file instantiates the complete-chain argument
for the unchanged A120 checker. All center widths and natural trims are allowed.
-/

namespace Agent104.NeutralTrimTransport

open Agent120.Neutral

/-- Agent119's verified neutral padding supplies the exact local interface. -/
theorem neutralPaddingLaws (b : Nat) :
    PaddingLaws b (Agent119.NeutralCenterPadding.padC b) := by
  constructor
  · intro E he a a' w hb
    simpa only [Agent119.NeutralCenterPadding.transportEdge] using
      Agent119.NeutralCenterPadding.edgeOK_transport he a a' w hb
  · intro B C h a
    exact Agent119.NeutralCenterPadding.gam_padC (a := a) h

/-- The explicit transformed edge list, with initial reserve equal to sum(ws). -/
def retimeCenter (b : Nat) (es : List Edge) (ws : List Nat) : List Edge :=
  retime (Agent119.NeutralCenterPadding.padC b) 0 es ws

/-- Any equal-length, equal-total natural schedule preserves acceptance. -/
theorem cycleOK_retime (b : Nat) (es : List Edge) (ws : List Nat)
    (B C : List Nat) (hc : cycleOK b es B C = true)
    (hl : es.length = ws.length) (hs : ws.sum = sumV es) :
    cycleOK b (retimeCenter b es ws) B
      (Agent119.NeutralCenterPadding.padC b ws.sum C) = true := by
  exact cycleOK_retime_of_laws (neutralPaddingLaws b) es ws B C hc hl hs

theorem retimeCenter_v (b : Nat) (es : List Edge) (ws : List Nat)
    (hl : es.length = ws.length) :
    (retimeCenter b es ws).map (fun E => E.v) = ws := by
  exact retime_v _ 0 es ws hl

theorem retimeCenter_fields (b : Nat) (es : List Edge) (ws : List Nat)
    (hl : es.length = ws.length) :
    (retimeCenter b es ws).map (fun E => (E.B, E.B2, E.u)) =
      es.map (fun E => (E.B, E.B2, E.u)) := by
  exact retime_fields _ 0 es ws hl

theorem retimeCenter_streams (b : Nat) (es : List Edge) (ws : List Nat)
    (B C : List Nat) (hl : es.length = ws.length)
    (hc : chainOK b es B C = true) :
    (retimeCenter b es ws).map (fun E => (e1 b E.B, gam b E.B E.C)) =
      es.map (fun E => (e1 b E.B, gam b E.B E.C)) := by
  exact retime_streams (neutralPaddingLaws b) 0 es ws B C hl hc

theorem retimeCenter_sumGain (b : Nat) (es : List Edge) (ws : List Nat)
    (hl : es.length = ws.length) (hs : ws.sum = sumV es) :
    sumGain (retimeCenter b es ws) = sumGain es := by
  have h := retime_sumGain (Agent119.NeutralCenterPadding.padC b) 0 es ws hl
  change sumGain (retimeCenter b es ws) + sumV es = sumGain es + ws.sum at h
  omega

/-- At fixed exterior data and streams, unrestricted center existence depends
only on the listed schedule length and total. No width cap is preserved. -/
theorem schedule_realizable_iff (b : Nat) (B : List Nat)
    (exterior : List (List Nat × List Nat × Nat))
    (streams : List (Nat × Nat)) (ws zs : List Nat)
    (hl : ws.length = zs.length) (hs : ws.sum = zs.sum) :
    ScheduleRealizable b B exterior streams ws ↔
      ScheduleRealizable b B exterior streams zs := by
  exact schedule_realizable_iff_of_laws (neutralPaddingLaws b)
    B exterior streams ws zs hl hs

end Agent104.NeutralTrimTransport

#print axioms Agent104.NeutralTrimTransport.neutralPaddingLaws
#print axioms Agent104.NeutralTrimTransport.cycleOK_retime
#print axioms Agent104.NeutralTrimTransport.retimeCenter_v
#print axioms Agent104.NeutralTrimTransport.retimeCenter_fields
#print axioms Agent104.NeutralTrimTransport.retimeCenter_streams
#print axioms Agent104.NeutralTrimTransport.retimeCenter_sumGain
#print axioms Agent104.NeutralTrimTransport.schedule_realizable_iff
