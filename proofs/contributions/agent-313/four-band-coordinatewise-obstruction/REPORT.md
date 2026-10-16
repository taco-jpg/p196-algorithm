# Agent #313 — Four-band coordinatewise gap-gain obstruction

## Scope

This report audits the exact decimal four-band quotient implemented in
`proofs/four_band__f923d34bb078f35f.py`. The state is

`B,9^g,A,9^h,C,9^h,reverse(A),9^g,reverse(B)`

with the actual final carry used as the clock. The target construction would
need a finite returned interface whose two total gap gains are each
nonnegative. A positive total gain alone is insufficient.

## Exact finite family checked

The published finite family has:

- B, A, C each one coefficient;
- B positive;
- C even;
- all relevant endpoints non-9;
- both complementary band pairs satisfying the mixed-carry condition;
- 765 initial interface states;
- 1,389 reachable quotient states;
- 708 ordinary quotient edges;
- 564 transitions losing the mixed condition;
- 45 outer/inner-band merges;
- 72 central-band merges;
- longest path 19 states;
- no configured state, path-length, or interface-width cap reached.

The archived result record reports an empty cycle list. The root review independently
re-executed the verifier and records PASS for the complete singleton-interface
initial family and all initial gaps g,h >= 10.

## Consequence for the previously assumed coordinatewise condition

For this exact finite family, there is no returned quotient interface at all.
Therefore there is, in particular, no returned interface whose two accumulated
gap gains satisfy

  Delta_g >= 0 and Delta_h >= 0.

This is stronger than merely observing a negative coordinate on a candidate
cycle: the exhaustive reachable graph contains no cycle.

The transition source also checks the exact length identity

  size(target) + 2*Delta_g + 2*Delta_h
    = size(source) + gamma,

and for a genuine cycle the established quotient architecture gives

  2*(Delta_g + Delta_h) = sum(gamma).

Thus the missing coordinatewise condition is a genuine construction bottleneck;
it cannot be inferred from the positive total gain identity.

## Status and limits

This is a scoped obstruction, not a universal obstruction to all decimal
finite-interface constructions. It covers only the specified singleton
initial-interface family and the exact four-band quotient represented by the
published verifier, for initial gaps at least 10. It does not exclude larger
interfaces, changing bulk coefficients, additional bands, or other
construction mechanisms.

The finite graph computation and its independent root replay are established
repository evidence. I am not labeling the mathematical obstruction
LEAN-CHECKED because the repository currently does not expose a Lean encoding
of this complete 1,389-state four-band graph. No unsupported Lean theorem is
being manufactured to upgrade the result.

## Next useful obligation

The immediate follow-up is to test whether the same coordinatewise obstruction
persists for the smallest non-singleton interface extension, while preserving
the exact four-band transition and distinguishing an actual graph exhaustion
from a search cap.
