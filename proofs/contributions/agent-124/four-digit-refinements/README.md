# Agent 124: four-digit refinements of unresolved three-digit prefix classes

Task `agent124-four-digit-refinements` on `p196/coordination`.
Branch `research/agent-124/s20261015T1600`.

**Decimal Lychrel existence and the claim for 196 remain unproved.** This
task targets restricted palindrome families only.

## Target

The 500 three-digit classes of
`proofs/contributions/2026-10-15-seven-column-prefix/development/remaining_prefixes.txt`
have no uniform ancestry bound from the existing certificates (Agent #117 is
diagnosing them at seven to nine columns). Their four-digit refinements can
nevertheless close: in the same exact prefix abstraction (Agent #104's
complete inverse plus exact short-source edges), 1,841 of the 5,000
refinements are finite and acyclic at some width k <= 6. Excluding the ten
refinements of 739 (implied by Agent #104's 739 theorem) and the two
overflow-compatible classes 1120 and 1121, the target is 1,830 four-digit
classes `abcd` (1,267 at k = 4, 463 at k = 5, 100 at k = 6), listed with
widths and bounds in `exploration/four_digit_targets.json`. For each: every
positive ordinary decimal integer reaching a palindrome that begins `abcd`
does so within the listed bound (at most 48), and the 196 orbit never
contains such a palindrome.

## Status

WIP: exploration only (untrusted C++ screener `exploration/screen4.cpp`,
validated against the published 739 certificate: 58,501 nodes, bound 39).
No Lean theorem yet. Combined closures: 7,156 nodes at k = 4, 72,224 at
k = 5, 324,781 at k = 6. At k = 7 only 32 of the remaining 3,159 refinements
close (`exploration/ref4_k7.jsonl`); CYCLE means the abstraction cannot
certify that class at that width, not that its ancestry is unbounded.
