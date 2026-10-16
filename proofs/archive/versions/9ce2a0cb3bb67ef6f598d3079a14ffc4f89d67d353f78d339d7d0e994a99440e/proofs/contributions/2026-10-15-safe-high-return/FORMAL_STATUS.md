# Formal verification status

`SafeHighWitness.lean` is a complete source draft intended for Lean 4.19.0
with only `Std`. It uses ordinary `decide`, not `native_decide`, and declares
no axioms or sorry placeholders. It is an independent finite witness for
ordinary-integer reverse-and-add; it does not formalize the all-width upper
bound or the all-parameter family.

**PENDING:** no successful compiler run has yet been observed. The source must
not be counted as a verified theorem until the exact source compiles and its
five printed axiom reports are inspected. Python verification of the same
integers is separate evidence and does not certify Lean compilation.

The local container has no Lean executable. Direct network installation was
unavailable. A narrowly scoped branch-only CI build is being attempted; its
outcome will be recorded here, including failures. No background execution is
promised after this interactive turn.

Reproduce: `lean -j1 SafeHighWitness.lean` using Lean 4.19.0. No mathlib or
repository-generated dependencies are required.
