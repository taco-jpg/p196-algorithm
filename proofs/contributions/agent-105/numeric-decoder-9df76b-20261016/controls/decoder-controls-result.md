# Decoder boundary controls: kernel result

**PASS:** the six closed controls in `proofs/Agent105DecoderControls9df76b.lean` compiled successfully with explicit `--trust=0 -j1 -DElab.async=false`. Frozen source SHA-256: `3159c9ddfe55b141e56d5181240bd696b3677d3061a2f8aaf317b6bce5c8b7c5`.

The targeted replay freshly compiled Local, the final frozen Scan, and Controls, in that order. Every command exited zero on attempt 001. The foundation, four Agent101 modules, and old witness module were reused from the previously successful explicit-trust-zero dependency build. Their source and imported-object hashes are recorded in `kernel-attempt-001/receipt.json`. This small targeted run does not claim the forthcoming complete decoder registry has already been rebuilt.

| Control | Kernel-checked result |
| --- | --- |
| `five_to_ten` | `step 5 = 10`; the short overflow candidate returns `[10]`; the equal-width candidate returns none. |
| `one_to_two` | `step 1 = 2`; the one-column no-overflow candidate returns `[2]`; the zero-width candidate returns none. |
| `boundary_121` | Actual steps from 29 and 110 both equal 121; candidates return `[11,11]` and `[1,2,1]`. |
| `retained_nonpalindromic_1197801` | Actual steps from 200799 and 1098900 both equal the nonpalindrome 1197801; candidates return `[11,9,7,7,9,11]` and `[1,0,18,16,18,0,1]`. |
| `truncated_subtraction_rejects` | Pair and center calls that would require a negative coefficient both return none. |
| `output_digit_bound_contract` | The raw out-of-domain digit10 call returns `[10]`, while actual normalized output is digit0 and carry1, demonstrating why physical correctness requires the stated digit bound. |

The 121 control accepts the legitimate empty interior with carries one and one. The 1197801 control accepts a nonpalindromic target with odd center output digit7 and even source coefficient16. The old palindrome-target parity obstruction has therefore not been mistakenly imposed on all numerical targets.

Four control theorems have no axiom dependencies. The two that reuse the established ordinary-integer reversal witnesses depend only on `propext` and `Quot.sound`. Large numeric reversals are proved by the old witness module, not by unfolding large reverseFuel literals here.

The original note records the two nonpalindromic coefficient profiles and their output; the concrete integer realizations were supplied by the already verified witness contribution. This control packet makes no new counterexample-discovery claim.
