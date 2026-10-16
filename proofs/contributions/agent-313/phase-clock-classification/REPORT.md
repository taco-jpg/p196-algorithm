# Agent #313 — Decimal phase-clock classification

For every admissible phase c in {1,...,17} excluding 9, the quotient phase
update is

  f(c) = 2c                 for 1 <= c <= 8,
  f(c) = 2(c-9)             for 10 <= c <= 17.

The complete transition table is:

1->2, 2->4, 3->6, 4->8, 5->10, 6->12, 7->14, 8->16,
10->2, 11->4, 12->6, 13->8, 14->10, 15->12, 16->14, 17->16.

Every image lies in the admissible set, so iteration is total on that set.

The directed functional graph has exactly two periodic components:

  2 -> 4 -> 8 -> 16 -> 14 -> 10 -> 2,

and

  6 -> 12 -> 6.

All other admissible phases enter one of these two cycles in finitely many
steps. In particular, any finite quotient cycle that returns to its original
phase has length divisible by 6 when it lies in the first component and by 2
when it lies in the second.

This matters for the four-band construction because its two complementary
bulk phases evolve under the same f. Therefore a purported persistent
coordinatewise-safe return cannot have an arbitrary temporal period: its phase
period is constrained to one of these two divisibility classes.

This is a finite classification of the phase subsystem only. It does not
prove or disprove a quotient cycle, and it does not imply anything about 196
by itself. Lean formalization remains WIP.
