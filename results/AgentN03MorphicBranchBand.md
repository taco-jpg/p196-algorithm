# N03 uniform-substitution decimal bulk (Fibonacci / Thue–Morse)
Label: **PAPER PROOF** for the branch-loop bulk composition and aperiodicity; **COMPUTED** for the finite 20,000-step ordinary-decimal replays. **Not LEAN-VERIFIED.**
Scope: base 10, eight-phase overflow `10101010`, reachable cut-state graph (244,785 vertices, 263,584 edges), one branching SCC of 1,104 vertices and 1,168 internal edges; loop lengths 119 and 48 at state `(242,226,22595)`.
New construction: equal-length 167-column blocks `U=A||B`, `V=B||A` encode a genuinely aperiodic Fibonacci or Thue–Morse spatial band satisfying every eight-phase bulk carry equation.
Finite replay: both 66,854-digit seeds survive 20,000 reverse-and-add steps without a palindrome, with exact outer pairword shape at every step and at least 30,743 matching columns at step 20,000; central discrepancy moves outward.
Not claimed: full-width template closure, infinite persistence, a decimal Lychrel number, a complete centre, or a Lean proof.
Reproduce: `calculation/new_structures/agent-N03/README.md` (commands, exact semantics, checker, data, and replay logs).
Files: `calculation/new_structures/agent-N03/{automaton.cpp,witness.txt,check.py,replay.cpp,README.md}`.
Next: attach a finite-state centre-acceptance transducer to the branching recurrent state, retaining both macro paths.