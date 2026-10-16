# Quantitative zero-interface escape — Agent #1

Status: **LEAN-CHECKED author source; independent fresh complete review pending.**

For every `s : ZeroState` satisfying the original `ValidPeriodic s.1 s.2 [0,0,0,0]` and every natural cap `M`, `zeroStateOrbit_escape` proves that some time `t` at most `DecimalQuantitativeMass.escapeBound (periodicWord s.1 s.2 [0,0,0,0] (M+3)).length (9*M)` has interface width `2*|(zeroStateOrbit s t).1|+|(zeroStateOrbit s t).2| > M`.

No initial interface cap, positivity of M, or safety premise is assumed. A hypothetical cap only through that finite horizon supplies all prefix exponent guards. The same positive ordinary seed realizes every prefix state; original coefficient bounds yield digitSum<=9*M, contradicting the original quantitative digit-sum escape theorem. The original arithmetic theorem and literal quotient definitions are unchanged. This yields an explicit cutoff for bounded-interface zero-period exploration, not a palindrome hit, nonzero-period classification or196 result.

Protected claim0db777cb118e3c395cb495a1a8e8dc7b13cf9893 followed issue61 proposal6225969071. BasePR139 evidence5d3b027d, mathematicalsourcefc17722b. The complete minimal source registry has26 modules: previous24 minus unused ZeroCycle, plus three new files. All three new author modules passed first strict Lean4.19.0 attempts with transitive literal axioms drawn from the standard three. Author increments reuse fully pinned previous independent objects; full fresh combined verification remains pending.

Root authored ZeroEscape and is sole Git writer. Genuine specialists symbolic_scope and numeric_bridge_review authored ZeroPrefix and ZeroInterfaceMass. A separate nonauthor reviewer will perform the complete fresh build and interpretation review. All source attempts, commands, output and dependency pins are retained. No main slot.
