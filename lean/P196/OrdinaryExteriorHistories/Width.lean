import P196.OrdinaryExteriorHistories.Realization

/-!
# Decimal widths along equal finite observation histories

Each recorded terminal carry is the exact width increment of the ordinary
transition. Equal initial widths and equal observations through time `T`
therefore give equal widths through time `T + 1`, including zero seeds and
the zero spatial cutoff.
-/

namespace Agent5.OrdinaryExteriorHistories

/-- Equal finite histories preserve a common initial decimal width through
the successor of the last observed transition. -/
theorem digit_widths_of_same_history (cut T n m : Nat)
    (hinit : (Agent109.digits n).length = (Agent109.digits m).length)
    (hhistory : ∀ t, t ≤ T →
      ordinaryObservation cut n t = ordinaryObservation cut m t) :
    ∀ t, t ≤ T + 1 →
      (Agent109.digits (Lychrel196.orbit n t)).length =
        (Agent109.digits (Lychrel196.orbit m t)).length := by
  intro t
  induction t with
  | zero =>
    intro _
    exact hinit
  | succ t ih =>
    intro ht
    have hprevious := ih (by omega)
    have hcarry := congrArg Prod.fst (hhistory t (by omega))
    change (Agent109.norm (Agent109.pairWord (Lychrel196.orbit n t)) 0).2 =
      (Agent109.norm (Agent109.pairWord (Lychrel196.orbit m t)) 0).2 at hcarry
    change (Agent109.digits (Lychrel196.step (Lychrel196.orbit n t))).length =
      (Agent109.digits (Lychrel196.step (Lychrel196.orbit m t))).length
    rw [digits_step_length, digits_step_length, hprevious, hcarry]

#print axioms digit_widths_of_same_history

end Agent5.OrdinaryExteriorHistories
