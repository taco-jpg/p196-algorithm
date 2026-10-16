# Agent #117: four-digit prefix 2641, k=7 finite rank pilot

**Status: CHECKED FINITE COMPUTATION (WIP; NOT LEAN-CHECKED).**

This extends the retained `research/agent-117/s20261015` seven-column
`PURE_PREFIX_CATALOGUE.md` §5 (2641: method bound 6). The historical
`prefix_cycles.py` is copied byte-for-byte as `legacy_prefix_cycles.py`.
It implements the finite relation of the Agent104 `prefixPredecessors`
calculation, already cross-checked in the historical work.

Run on Python 3.11+: `python3 -B verify_2641.py`.

This particular four-digit class has **1,000 long initial rows, no short
initial palindrome rows, 25,624 long states in its backward closure,
33,821 inverse edges, maximum rank 5 and method bound 6**. Each found
inverse edge was independently tested by applying the supplied forward
column formula, and Kahn ranks satisfy the strict-descent recurrence on
all rows. It reproduces the old whole-space catalogue bound.

The prior `rank_certificate.py` calls an initializer hard-coded to
`k-3` free digits, so it must *not* be used on a four-digit prefix without
correction. `verify_2641.py` explicitly uses `k-len(prefix)`.

**Remaining acceptance gates:** check inverse enumeration completeness
against the pinned Lean source; turn the 25,624-row rank result into a
concrete kernel-checked Lean certificate without `sorry` or
`native_decide`; prove/inspect the full short-boundary and arithmetic
orbit interpretation; audit axioms and independent clean rebuild.
Do not infer an actual 196 orbit restriction from the finite graph alone.

Task: `agent117-k7-four-digit-2641-20261016` on
`p196/coordination`. Owner is a research task label, not a GitHub account.
No main integration ownership is requested.
