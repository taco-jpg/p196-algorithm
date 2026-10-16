# Exact zero-period quotient acyclicity — Agent #1

Status: **LEAN-CHECKED author compilation; independent fresh combined review pending.**

`Agent1.Periodic.zeroStateOrbit_no_cycle` proves that every original valid state `(B,H,[0,0,0,0])` has no positive-length return under the literal maximal quotient. No safety premise is used. The stronger intermediate `zeroStateOrbit_not_bounded` excludes a uniform bound on both interface width and coefficient mass.

The proof first establishes exact zero-period preservation and original validity. A hypothetical finite cycle gives bounded interfaces. Starting the literal exponent recursion at `M+3`, exact width balance supplies every `k>=3` guard before use. Periodic realizability supplies one positive ordinary integer at time zero; the new list/index bridge transports that same integer orbit at all later times. Zero-period words have mass entirely in their interfaces, which would bound the orbit's digit sums and contradict the existing unconditional `DecimalUnboundedMass.not_eventually_bounded_digitSum`.

This neither proves a palindrome hit nor termination of arbitrary quotient paths. Nonzero-period cycles and the status of196 remain outside scope. It does not take over the historical affirmative interface-lift/search lane.

Claims were published at d5786f691f77c606f7343b1182cc67643f058a8f. Foundation source checkpoint776f491e13287c3b2148d2dba73cd308590d459a remains preserved. The exact complete source registry is `proofs/Agent1PeriodicZeroCycle.registry.json` (24 modules). All seven new module authors performed actual strict Lean4.19.0 compilation and literal axiom audits; the final independent complete clean closure is pending. Author increments explicitly record reused pinned objects; a separate fresh19-module numeric bridge build also passed. All attempts, source snapshots, substantive logs and diagnostics are retained.

The parent authored Exponent/Cycle and is the sole Git writer. Genuine specialists authored Realizability/Mass, ZeroPeriod, ZeroState and ZeroNumeric in separate files. The final independent reviewer authored none of these seven files. No main-write slot is held.
