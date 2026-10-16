# Exact zero-period quotient acyclicity — Agent #1

Status: **INDEPENDENTLY-REVIEWED; integration pending.**

`Agent1.Periodic.zeroStateOrbit_no_cycle` proves that every original valid state `(B,H,[0,0,0,0])` has no positive-length return under the literal maximal quotient. No safety premise is used. The stronger intermediate `zeroStateOrbit_not_bounded` excludes a uniform bound on both interface width and coefficient mass.

The proof first establishes exact zero-period preservation and original validity. A hypothetical finite cycle gives bounded interfaces. Starting the literal exponent recursion at `M+3`, exact width balance supplies every `k>=3` guard before use. Periodic realizability supplies one positive ordinary integer at time zero; the new list/index bridge transports that same integer orbit at all later times. Zero-period words have mass entirely in their interfaces, which would bound the orbit's digit sums and contradict the existing unconditional `DecimalUnboundedMass.not_eventually_bounded_digitSum`.

This neither proves a palindrome hit nor termination of arbitrary quotient paths. Nonzero-period cycles and the status of196 remain outside scope. It does not take over the historical affirmative interface-lift/search lane.

Claims were published at d5786f691f77c606f7343b1182cc67643f058a8f. Foundation source checkpoint776f491e13287c3b2148d2dba73cd308590d459a remains preserved. The exact complete source registry is `proofs/Agent1PeriodicZeroCycle.registry.json` (24 modules). All seven new module authors performed actual strict Lean4.19.0 compilation and literal axiom audits. The separate nonauthor fresh24-module trust0 build passed all25 commands, 1,446 theorem constants,241 safe definitions and108 named theorem types (30new). The parent unchanged canonical fresh24 build also passed with source_tree_clean=true atfc17722b; its command does not explicitly set trust0, unlike the independent and author commands. Author increments explicitly record reused pinned objects; a separate fresh19-module numeric bridge build also passed. All attempts, source snapshots, substantive logs and diagnostics are retained.

The parent authored Exponent/Cycle and is the sole Git writer. Genuine specialists authored Realizability/Mass, ZeroPeriod, ZeroState and ZeroNumeric in separate files. The final independent reviewer authored none of these seven files. No main-write slot is held.

The theorem dependency union is exactly `propext`, `Classical.choice`, `Quot.sound`. The independent inventory separately records14 generated unsafe implementation axioms, including ZeroState's generated List.sum helper; none enters any audited theorem or safe definition. This is not a claim that the compiler environment contains no implementation axioms.

See `review/final-semantic-review.md` for exact interpretation and `review/README.md` for the portable full trust0 replay command. `verification/parent-clean-001/` preserves the separate parent run, including every compiled source snapshot. The source registry retains its historical checkpoint wording; current acceptance status is this evidence and the eventual actual PR review, not that earlier label. This package is scoped and does not certify the entire repository.
