# Global-exterior research record

## Initial target and exclusions already known

The task was to investigate arbitrary finite canonical exterior words, not to
raise a complete-enumeration width cap. The baseline already excludes a strict
potential invariant under word reversal and, after an actual overflow, a strict
potential invariant under arbitrary permutations within each positional parity
class. Those arguments appear in Agent 6's `ExteriorPotentialObstruction.lean`
and `ExteriorAbsorbedObstruction.lean`. Repeating those potential searches was
therefore avoided.

The proposed new observable was the ordered radix defect
`Z=9 eval10(B)-c(10^|B|-1)`. Appending copies of the bulk phase leaves Z fixed,
so this is well adapted to the quotient's moving cut between finite exterior
and constant bulk. It is spatial-order-sensitive. The initial hope was a
closed arithmetic update or monotonic return constraint for this quantity.

## Rejected stronger guesses

Neither one-step nor phase-return monotonicity of `abs Z` is valid.
The exact small probes in `development/explore.py` and the recorded controls
show, for example:

- `(6,[15]) → (12,[6])`: `Z=81 → -54`, a decrease in absolute value.
- `(6,[4])` after two steps has phase 6 and exterior `[17,5]`:
  `Z=-18 → 9`, again a decrease in absolute value.
- `(12,[1,15])` after two steps has exterior `[7,2,13]`:
  `Z=171 → -45`.

These finite counterexamples reject those specific guesses; they say nothing
about global cycle existence. No monotonicity conjecture is left asserted.

## Exact projected return

The first projected two-cycle found with one-letter source exteriors was
`(6,[3]) → (12,[6]) → (6,[13,5])`, where the first and last observations are
`(6,-27)`. This already defeats strict progress of the radix observation but
has no overflow along those two transitions, so it was not used as the main
result.

The next small search restricted attention to states reached after a computed
overflow. From the one-letter ancestor `(6,[13])`, it found the fully contiguous
five-edge path in the README. Its two-edge observed return contains an actual
overflow. This yields the stronger obstruction allowing weak progress at
nonoverflow steps but requiring strict progress at overflow steps.

The observed alias is the elementary decimal carry identity

`9 + 10*1 - 6*(1+10) = 9 + 10*11 + 100*5 - 6*(1+10+100) = -47`.

Multiplying by nine gives Z=-423. The full words are different and have
different next observations. No autonomous scalar update can therefore be
inferred from Z and the phase. Keeping the whole radix value does not preserve
the bidirectional carry information needed by the actual exterior transition.

## Verification and scope

The new Lean module imports the exact existing `advance` and `Canonical`
definitions; it does not replace them with a surrogate relation. All listed
word transitions, overflow bits, observations, and the post-overflow ancestry
are kernel-checked. The generic obstruction is an ordinary logical proof from
those finite witnesses. Independent ordinary-integer controls use literal
addition and reversed decimal strings on three whole-word realizations.

No broad graph census or new width cap is reported. The discovery code stops
when it finds the finite witness and is not cited as an acyclicity proof.
The global no-return proposition remains open in this work.
