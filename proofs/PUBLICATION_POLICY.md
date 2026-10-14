# Research publication policy

Effective with the renewal pass on 14 October 2026, the user's standing instruction is: **“From now on publish everything.”** For this project, that authorizes publication of the ongoing research under `proofs/` in `taco-jpg/p196-algorithm`. Updates are published during active research work after evidence labels and audit records are consolidated. Repository visibility is unchanged.

## Complete research coverage

Retain every new substantive source, written proof, hypothesis, attempted construction, counterexample, negative result, search configuration, log, certificate, and raw generated research result. Failed attempts, abandoned approaches, solver failures, timeouts, and UNKNOWN outcomes are part of the record. Preserve the parameters, bounds, seeds, resource caps, and dependencies needed to interpret or reproduce each result.

Large genuine research outputs may be stored with lossless compression. The inventory must identify the original path, original byte count and SHA-256, stored path and compressed-byte hash, compression format, and exact recovery command. Compression must preserve the complete original bytes; it must not substitute a summary for the underlying result. Compact summaries and readable indexes accompany the retained raw evidence.

Compiled programs, duplicate dependency/build directories, runtime installations, caches, and operational publishing helpers are reproducible infrastructure rather than research findings. They may be excluded, with the reason recorded. Preserve original research sources, build/version instructions, substantive compiler and proof-audit logs, and all independently replayable snapshots. Earlier releases retain their explicitly documented historical coverage; this expanded rule governs new work from the renewal pass onward.

## Evidence labels

| Label | Required interpretation |
|---|---|
| Formal theorem | State the exact theorem and hypotheses, compiler version, dependency sources, and axiom audit. Distinguish ordinary logical axioms from `native_decide` / `Lean.ofReduceBool` finite computation. |
| Conditional theorem | The implication is proved; each unsupplied hypothesis remains explicit. It is not an instance, witness, or proof of the main conjecture. |
| Written proof | Preserve the argument and its exact domain. Identify internal audits separately from formal verification or external peer review. |
| Checked finite certificate or experiment | Preserve the checked object, independent checker, parameters, and verified finite scope. Do not extrapolate to an all-time conclusion. |
| Solver-reported outcome | Record the solver, configuration and output. Distinguish a reported SAT/UNSAT status from an independently checked certificate. |
| UNKNOWN or incomplete | State the timeout, cap, unfinished obligation or missing case. A missing result is not an exclusion. |
| Working hypothesis or heuristic | Mark the claim as conjectural and retain the evidence, motivation, and counterexamples. |

Corrections must identify the affected claim and evidence. Preserve superseded logs or hypotheses as historical records, with a clear correction or withdrawal, rather than silently treating them as current conclusions. Counts of theorem declarations, tested cases, or graph states are audit metadata, not counts of independent major results.

Decimal Lychrel existence and the claim for 196 remain **unproved** unless a later publication supplies and checks the missing all-time argument. A finite safe gate, conditional witness formula, failed ansatz, or long trajectory does not supply that argument. No novelty or external peer-review claim follows from publication here.

## Repository integrity

Keep unrelated repository files, production artifacts, and already published research intact. Use a fresh remote head and an atomic non-force update; reconcile concurrent changes before publishing. Update the overview, findings index, coverage inventory, file list, byte manifest and verification record so each release states exactly what was added or corrected. Verify compressed and uncompressed evidence identities as appropriate. No separate background-publishing service or schedule is created by this policy.
