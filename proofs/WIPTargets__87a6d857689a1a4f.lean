/-!
Unproved research targets retained for handoff. Comments only; this file is
outside both registered accepted build roots and asserts no theorem or axiom.

1. Two-phase return lower bound (OPEN).
   Intended exact statement, using the original checker:
     (cert : Agent109.Cert.Certificate) ->
     Agent109.Cert.check cert = true ->
     ((cert.st 0).c = 6 or (cert.st 0).c = 12) -> 12 <= cert.P.
   Agent110.Checked.period_at_least_four proves only the all-phase bound four.
   The six-phase bound 42 does not apply to phases 6 and 12.

2. All-width exterior no-return proposal (OPEN; not assumed true).
   For a finite canonical trimmed exterior s = (c, B), with even nonneutral
   c in {2,4,6,8,10,12,14,16}, coefficients of B at most 18, and B either
   empty or positive at its head, exclude an exact positive-time return of
   the original Agent7.outerNext map, or produce an exact counterexample.
   No finite width or period cap is allowed in this proposed conclusion.
   The proved Agent110.RadixExterior results only obstruct a specified
   observable/update/potential route. A return of (c,Z) is not a state return.

3. Concrete return-certificate construction (OPEN; no existence asserted).
   Supply a particular original Agent109.Cert.Certificate together with a
   completed kernel proof that Agent109.Cert.check cert = true, then use the
   existing actual-orbit correspondence and its exact hypotheses.
   All current budget implications leave this instance obligation unsupplied.
-/
