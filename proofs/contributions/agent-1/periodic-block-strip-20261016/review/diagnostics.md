# Finite diagnostic controls

Agent #1's separate `research_status` reviewer ran `diagnostic_controls.py` once successfully. Attempt `diagnostics-001/` preserves the exact script, standard output, standard error and process receipt. No Lean source was written by this reviewer.

The script pins the preserved Python quotient source by SHA256 and imports it without executing its discovery `main`. It compares the literal two stripping loops against an independently enumerated finite specification of removable counts, checks reconstruction and final stopping, and checks absorption at exponents 0, 1, 2, 3 and 7.

Twelve targeted generic cases cover empty/short words, complete nonconstant blocks, short residuals, suffix mismatch, the seven-column overlapping-center boundary, constant and zero periods, nonprimitive periods, and a palindromic period. Fourteen actual raw-slice cases check exponents 3, 4, 5, 7 and 12: 70 sampled transitions, both actual carry values, and signed deltas -2, -1 and 0. Six valid-and-safe cases also execute the preserved `transition`. Cases beyond that function's domain use only its underlying finite `image` operation and are labeled in the JSON.

The smallest observed target exponent is one. This is an explicit diagnostic reminder that a single edge need not remain in the guard theorem's source domain `k ≥ 3`. Full validity, numeral realization, safety preservation, finite-interface returns, and iteration are not checked or inferred.

These are finite execution controls, not universally quantified proofs or formally proved counterexamples. The Lean source review and fresh final closure audit are separate evidence.

Result: PASS, Python process exit 0, approximately 0.045 seconds. Script SHA256 `1f1d43bbc85fd8e253f0560c57644e48e3bae2296a0298d2619c9b1b0f08512c`.
