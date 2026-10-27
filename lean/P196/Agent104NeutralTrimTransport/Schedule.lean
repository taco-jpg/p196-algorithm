import P196.Agent104NeutralTrimTransport.Chain

/-!
# Prescribed center schedules have equivalent existence

At fixed exterior edge data, lower-carry/overflow streams and initial exterior,
any two center schedules of the same length and total are existence-equivalent
under the local padding laws. The center interfaces remain existential: their
widths may increase, and no fixed-width or primitive-period claim is made.
-/

namespace Agent104.NeutralTrimTransport

open Agent120.Neutral

/-- The recursive center trim total is the sum of the recorded schedule. -/
theorem sumV_eq_map_sum (es : List Edge) :
    sumV es = (es.map (fun E => E.v)).sum := by
  induction es with
  | nil => rfl
  | cons E es ih => simp [sumV, ih]

/-- A certificate with specified exterior edge data, carry/overflow streams,
initial exterior and center trim schedule. Center interfaces are unrestricted.
-/
def ScheduleRealizable (b : Nat) (B : List Nat)
    (exterior : List (List Nat × List Nat × Nat))
    (streams : List (Nat × Nat)) (ws : List Nat) : Prop :=
  ∃ (es : List Edge) (C : List Nat),
    cycleOK b es B C = true ∧
    es.map (fun E => (E.B, E.B2, E.u)) = exterior ∧
    es.map (fun E => (e1 b E.B, gam b E.B E.C)) = streams ∧
    es.map (fun E => E.v) = ws

/-- Construct a certificate with a prescribed schedule of the same length and
total, preserving the complete exterior data and carry/overflow streams. -/
theorem schedule_transport_of_laws {b : Nat}
    {pad : Nat → List Nat → List Nat} (laws : PaddingLaws b pad)
    {B : List Nat} {exterior : List (List Nat × List Nat × Nat)}
    {streams : List (Nat × Nat)} {ws zs : List Nat}
    (hr : ScheduleRealizable b B exterior streams ws)
    (hl : ws.length = zs.length) (hs : ws.sum = zs.sum) :
    ScheduleRealizable b B exterior streams zs := by
  obtain ⟨es, C, hc, hext, hstreams, hv⟩ := hr
  have hlen : es.length = zs.length := by
    have hm := congrArg List.length hv
    simp only [List.length_map] at hm
    exact hm.trans hl
  have hsum : zs.sum = sumV es := by
    rw [sumV_eq_map_sum, hv]
    exact hs.symm
  have hchain : chainOK b es B C = true := by
    have hh := hc
    simp only [cycleOK, Bool.and_eq_true, decide_eq_true_eq] at hh
    exact hh.1.1.1.2
  refine ⟨retime pad 0 es zs, pad zs.sum C,
    cycleOK_retime_of_laws laws es zs B C hc hlen hsum, ?_, ?_,
    retime_v pad 0 es zs hlen⟩
  · exact (retime_fields pad 0 es zs hlen).trans hext
  · exact (retime_streams laws 0 es zs B C hlen hchain).trans hstreams

/-- Schedule existence depends only on length and total once exterior data,
carry/overflow streams and initial exterior are fixed. Both directions use
forward padding; neither requires an inverse padding operation. -/
theorem schedule_realizable_iff_of_laws {b : Nat}
    {pad : Nat → List Nat → List Nat} (laws : PaddingLaws b pad)
    (B : List Nat) (exterior : List (List Nat × List Nat × Nat))
    (streams : List (Nat × Nat)) (ws zs : List Nat)
    (hl : ws.length = zs.length) (hs : ws.sum = zs.sum) :
    ScheduleRealizable b B exterior streams ws ↔
      ScheduleRealizable b B exterior streams zs := by
  constructor
  · intro hr
    exact schedule_transport_of_laws laws hr hl hs
  · intro hr
    exact schedule_transport_of_laws laws hr hl.symm hs.symm

end Agent104.NeutralTrimTransport

#print axioms Agent104.NeutralTrimTransport.sumV_eq_map_sum
#print axioms Agent104.NeutralTrimTransport.schedule_transport_of_laws
#print axioms Agent104.NeutralTrimTransport.schedule_realizable_iff_of_laws
