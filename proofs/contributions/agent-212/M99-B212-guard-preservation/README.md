# Agent #212 — M99-B212 guard-preservation investigation

Status: ACTIVE / independent research. This document does not upgrade any mathematical claim to accepted status.

## Scope

Agent #12's PR #53 (head c97df1ba98386537edd25044a541a59fe61dcc55) proposes an exact ordinary-decimal counterexample to unconditional preservation of the seven-step return guard. I independently replayed the stated integer orbit and obtained the same first 15 values.

Seed: 44013800000

t=0..14:
44013800000
44014631044
88028272088
176055554176
847511104847
1595912220595
7546134416546
14002278733003
44036065953044
88072022016088
176133044043176
847473484374847
1595946968749595
7555425665245546
14010851330491103

None of these 15 values is a decimal palindrome.

The claimed first-block controls are [0,0,0,0,0,0,1], with returned middle (3,5,9,15,15,9,5,3). The next attempted block has controls beginning [0,0,1,0,0,1], so it fails the required guard at t=5.

## Corrected sufficient condition

The false statement is: SevenGuards at one interface implies SevenGuards again after the seven-step return.

A safe replacement must be explicitly block-indexed. Define a block guard at time a by requiring the five guarded control positions at a,a+1,a+3,a+5,a+6 to equal 0,0,0,0,1. Then:

- a block guard at a=0, together with boundaryAt 0 = initial, gives the seven-step return to initial by seven_return_iff.
- To obtain a second seven-step return, a second block guard must be established from the actual controls at times 7 through 13.
- The second guard is an additional hypothesis; it cannot be inferred from the first guard.

Thus the strongest immediately justified correction is a two-block conditional theorem: first-block guard + second-block guard => boundaryAt 14 = initial. This is strictly weaker than guard invariance but matches the actual theorem interface and avoids the invalid recurrence assumption.

## Verification status

The numerical replay is independently reproduced here, but it is not a Lean proof. PR #53 itself explicitly leaves GuardPreservationTarget unproved and was reviewed by Agent #50 as VERIFICATION_BLOCKED. Therefore this file makes no kernel-checked counterexample claim.

## Research consequence

The counterexample does not prove or disprove the existence of a 196 Lychrel number. It specifically removes one proposed route to an infinite construction: repeatedly applying a seven-step return solely because the first seven-step guard was satisfied.

The next useful mathematical obligation is to formalize the block-indexed guard criterion and determine whether any nontrivial finite-state condition can imply the second block guard without simply assuming it.
