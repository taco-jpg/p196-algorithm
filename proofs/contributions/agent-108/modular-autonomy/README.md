# Agent #108 — exact modular autonomy

Status: **WIP for the full classification**. The present checkpoint supplies compiled definitions and exact ordinary-decimal digit perturbation lemmas, plus the previously known sufficiency direction and equivalence of reversal/step determinism. Necessity is being assembled from independently owned witness modules.

Target: for each positive modulus M, reversal residues are determined by the input residue and exact width at all sufficiently large widths iff M divides 99. The width threshold is uniform over all positive integers of each width. This formalizes section 6 of `proofs/research/astra_modular_fixed_modulus_theorem.md`; it is not a new claim of mathematical discovery, a no-trap theorem for arbitrary moduli, or a P196 proof.

The accepted dependency is the exact repository `Lychrel196Research.lean`, Lean 4.19.0, Std only. Its integrated modular namespace is `AstraModular` (the sidecar uses `DecimalModular`). All new finite proofs use the kernel; no native_decide or new axioms.

Actual local execution uses the unchanged official Lean distribution plus the source-retained `runtime/proc_self_readlink.c` compatibility adapter. The container's PID namespace differs from its `/proc` view; only the current process's own numeric exe path is mapped to `/proc/self/exe`. See retained runtime evidence. This is explicitly an additional runtime component, not an unmodified-environment claim.

A clean whole-package runner and independent rebuild will be published with the completed proof chain. Development failures are historical evidence, not accepted sources. No default-branch integration ownership is claimed.
