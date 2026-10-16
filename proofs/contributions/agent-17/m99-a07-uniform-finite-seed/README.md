# Agent #17 — M99-A07 finite-seed uniformity

Status: LEAN-CHECKED (official Lean 4.19.0, core + Std only). `finite_uniform_extraction` uses propext, Classical.choice, Quot.sound; the counterexample uses no axioms.

## Mathematical result

Let Safe x t mean that candidate seed x is safe at time t. Define PrefixSafe Safe x N := ∀ t ≤ N, Safe x t, and ForeverSafe Safe x := ∀ t, Safe x t.

The sufficient uniformity hypothesis is: there exists a fixed finite candidate set K, independent of the horizon, such that for every finite horizon N there is some x in K with PrefixSafe Safe x N.

Because K is finite, if every candidate failed at some finite time, the finitely many first failure times would have a maximum M. The hypothesis at horizon M would then choose a candidate that is safe through M, contradicting its failure time. Hence one fixed x in K is safe for every time.

For decimal reverse-add, a concrete sufficient hypothesis is therefore: fix one finite seed ensemble in advance (for example, all canonical seeds of one fixed decimal width), and prove that every finite horizon has at least one member of that same ensemble whose orbit avoids palindromes through the horizon. This is materially stronger than allowing the seed or its width to depend on the horizon.

## Quantifier boundary

The unrestricted statement ∀ N, ∃ x, ∀ t ≤ N, Safe(x,t) does not imply ∃ x, ∀ t, Safe(x,t). The seed can move as N grows. unrestricted_quantifier_swap_counterexample gives a fully formal elementary counterexample: for each N, choose x=N+1 and use t≤N → t<x; but no fixed natural x satisfies ∀t, t<x.

This complements Agent122's actual decimal countermap result. That result is much stronger as a research counterexample but has a different purpose and is not reimplemented here.

## Scope

This result is a logical extraction lemma only. It does not provide the required fixed finite seed for actual reverse-and-add, does not prove anything specific about 196, and does not assert that a fixed-width positive-survivor statement has been established in the repository.

The accepted theorem must retain exact Lean verification and axiom evidence. No sorry, admit, unsupported axiom, or native_decide is used by the target source.

## Formal interface (review correction)

The earlier source used Mathlib's `Fintype`/`Finset`, which this repository does not provide, and did not compile. The fixed finite ensemble is now a `List α` `K`:

`finite_uniform_extraction K Safe : (∀ N, ∃ x ∈ K, PrefixSafe Safe x N) → ∃ x ∈ K, ForeverSafe Safe x`,

proved via `common_failure_bound` (finitely many failing candidates fail by a common time, by induction on the list). The quantifier-swap counterexample's final step was also corrected (`hx x`, not `hx x le_rfl`).
