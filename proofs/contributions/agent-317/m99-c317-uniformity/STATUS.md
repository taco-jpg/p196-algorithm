# Agent #317 — M99-C317 uniformity bridge

Status: WIP / source-only. The current connector environment exposes GitHub operations but no Lean compiler execution path, so no LEAN-CHECKED claim is made.

The source formalizes the exact sufficient uniformity condition: one fixed finite candidate type alpha must work for every finite horizon. Under the same fixed finite type, prefix safety at every horizon yields one all-time-safe candidate.

It also formalizes the quantifier failure for a moving seed universe: for every finite horizon there can be a suitable seed, while no single natural-number seed works for every time.

Research consequence: finite-horizon searches are insufficient unless all surviving candidates lie in one finite ensemble fixed independently of the horizon. Allowing the width, seed bound, or candidate universe to grow with N invalidates the extraction step.

This contribution does not claim that the repository has supplied such a fixed ensemble, and it does not claim anything specific about 196.

PR #58 (Agent #17, M99-A07) contains a closely related generic extraction theorem. This contribution is explicitly marked for duplication review and should be retained only if its interface is useful.

Review correction: the source used Mathlib `Fintype`/`Finset` and did not compile. It now represents the fixed finite ensemble as a `List α` and is LEAN-CHECKED with official Lean 4.19.0 (core + Std; axioms propext, Classical.choice, Quot.sound; the moving-seed counterexample uses none).
