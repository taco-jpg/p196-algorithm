# Independent semantic review of ArithmeticCRT

Reviewer: `/root/agent111_coefficients/period` (author of the period lemmas and period-existence development, not of either source reviewed below).

## Pinned source versions

Paths are relative to `p196/proofs/contributions/agent-111/exact-length-residues/`.

| Source | SHA-256 |
| --- | --- |
| `ArithmeticCRT.lean` | `c5709b1de255e43d84a4d323257b13f9a314872d77cae955ac9c0c088ced59a5` |
| `ModularSpan.lean` | `1cad197771ad6a4a9577ac08d3e1a4afe143e354a96a261b8ebaa2c687c09754` |

## Scope and independence

This is a read-only mathematical and source-level review of `crt_mod_eq_of_coprime`, its positive-modulus wrapper `crt_mod_eq`, and `shifted_modular_span`, including the directly used statements and constructions in `ModularSpan.lean`. The reviewer did not author or modify either reviewed file. The period lemmas written by this reviewer are outside this review's scope and are not being self-certified here.

No independent Lean or kernel-checker execution was performed for these two sources in this review. No new tests were run, and no independent `#print axioms` result is claimed. Compilation success communicated by the author is not treated as independent execution evidence. The pinned hashes identify the sources that received this semantic review; this record does not certify the entire project or its transitive dependency closure.

## Mathematical checks

- In the CRT proof, let `d = p - a` in the integers. The remainder equalities give `d = u*k` and `d = q*l`. The integer Bezout identity `s*u + t*q = 1` then gives `d = (u*q)*(s*l + t*k)`. The subtraction direction, placement of `k` and `l`, and final divisibility witness agree throughout the Lean proof.
- Integer arithmetic avoids natural subtraction truncation in the CRT argument. The final cast returns precisely equality of the natural remainders modulo `u*q`.
- The general CRT interface legitimately includes zero moduli. If `u = 0`, coprimality forces `q = 1`, and equality modulo zero directly says `p = a`. The case `q = 0` is symmetric. Both moduli cannot be zero under the coprimality assumption. The positive-modulus wrapper intentionally has stronger, unused positivity assumptions.
- For the shifted span, write `g = gcd q (gcd c0 c1)` and `b = a + q - C % q`. Since `q > 0`, one has `C % q < q`, so the subtraction defining `b` cannot truncate and `C % q + b = a + q`.
- From `g | q` and `g | C`, the proof correctly obtains `g | C % q`; together with `g | a`, this gives `g | b`. Applying `modular_span` therefore provides both required bounds `x < q`, `y < q` and the correct residual target modulo `q`.
- The final remainder calculation adds the fixed contribution `C` back with the correct sign and yields exactly `(C + x*c0 + y*c1) % q = a % q`.
- At `q = 1`, the coefficient bounds force `x = y = 0` and both target remainders are zero; all statements remain valid. At `c0 = c1 = 0`, the hypotheses reduce to the required divisibility of `a` and `C` by `q`, again giving the claimed conclusion.
- In `ModularSpan.lean`, the Euclidean recurrence constructs an integer Bezout representation; multiplying the two nested representations gives the stated three-generator combination. Reducing the two free integer coefficients modulo the positive `q` supplies nonnegative natural representatives below `q` and preserves the required residue.

## Conclusion

No semantic defect, reversed difference, missing positivity requirement, or uncovered boundary case was found within the scope above. This conclusion is an independent source review only; independent execution remains outstanding for this reviewer.
