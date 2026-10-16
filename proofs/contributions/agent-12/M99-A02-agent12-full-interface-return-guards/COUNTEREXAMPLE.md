# Agent #12 — M99-A02 full-interface return-guard preservation

Status: WIP / counterexample found. The proposed unconditional preservation of the seven-step return guard is false.

## Exact computational counterexample

Use the canonical symmetric pair word
`q = (4,4,0,1,3,16,3,1,0,4,4)`, whose middle is
`h = (1,3,16,3,1)`.

The first seven-step guard is satisfied with control word
`[0,0,0,0,0,0,1]` and overflow schedule
`[0,0,1,0,1,0,1]`. The resulting returned middle is
`h' = (3,5,9,15,15,9,5,3)`.

At the next attempted seven-step return, the controls begin
`[0,0,1,0,0,1]`; the required control at time 5 is 0, but the actual
control is 1. Thus the return guard fails at its sixth checked control.

The first middle is safe for the seven actual steps: the corresponding
ordinary seed is 44013800000, and its first seven iterates are:

0: 44013800000
1: 44014631044
2: 88028272088
3: 176055554176
4: 847511104847
5: 1595912220595
6: 7546134416546
7: 14002278733003

None of these eight values is a palindrome.

The next seven actual iterates continue without a palindrome through
time 14, but the return guard has already failed, so this is specifically
a refutation of guard preservation, not a P196 result.

## Interpretation

The existing SevenStepOrbit theorem proves a one-block equivalence:
a seven-step return occurs iff the five specified controls have the
required values. It does not prove those controls recur at the returned
interface. The exact counterexample above shows that recurrence cannot be
added as an unconditional invariant.

Acceptance level: WIP until the counterexample is independently encoded
and kernel-checked in Lean. No theorem is being upgraded from this report
alone. No `native_decide`, placeholder, or unsupported axiom is used.

## Next action

Formalize the concrete counterexample against the existing actual-orbit
definitions, preserving the exact seed, returned width, controls, and
failed next guard. Then request independent semantic review.
