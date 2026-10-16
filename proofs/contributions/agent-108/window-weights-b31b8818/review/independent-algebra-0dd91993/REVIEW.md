# Independent review — fixed algebra interface

**Disposition: PASS for the stated algebraic and conditional interface.**

Reviewer: Agent #108 specialist claims_inventory, a separate non-author subagent in the same session and shared authenticated account. This is an internal independent review, not external peer review.

## Frozen sources and execution

- Agent108WindowObstruction.lean SHA-256: 0dd91993667dddac3740ccadd7b2764cc2e6122121f19bd0a8354a9e0507a90a.
- Agent108WindowDefs.lean SHA-256: 147ae208dce3b612c6eb23091eab123b77bd46c86d216ab8a6199913015f0aa0.

The exact byte copies in source/ were verified before execution. Defs and Obstruction were rebuilt into a newly created empty build/ using the pinned Lean 4.19.0/6caaee842e94 runtime and **--trust=0**. Both compilation commands and the independent audit command exited zero. Existing project compiled objects were not used; only pinned standard-library/Mathlib dependencies were imported.

All **20 public declarations** were audited: nine source definitions, binaryWeight, and ten algebra theorems. The Defs declarations have no axioms. choices_mem_length and choices_nodup report propext and Quot.sound. The real-valued declarations report only propext, Classical.choice, and Quot.sound. No unexpected axiom was reported. Complete names and commands are in build-results.json, and literal print output in logs/audit.stdout.log.

## Semantic review

| Declarations | Verified meaning and hypotheses |
|---|---|
| binaryWeight; binaryWeight_eq_prod | A false bit contributes 1, a true bit contributes beta; the empty list contributes 1. The product identity does not assume positivity. |
| binaryWeight_pos | Strict positivity follows from beta>0, including the empty choice. |
| choices_mem_length; choices_nodup | Every listed choice has the advertised length; different Boolean heads distinguish the two recursive lists. No duplicate multiplicities are hidden in the sum. |
| sum_map_real_mul | A generic finite real list-sum identity, including the empty list. |
| weighted_choices_sum | The exact sum is (1+beta)^r for every real beta and natural r. The r=0 value is 1. No positivity assumption is unnecessarily introduced into this algebraic identity. |
| weighted_family_total | Converts an explicitly assumed pointwise family formula, for every listed choice, into the total. C, targetWeight, and beta are arbitrary real values at this stage. This theorem does not assert that the pointwise formula has already been proved for the literal window family. |
| scaled_pow_unbounded | Requires fixed C>0 and beta>0. Thus 1+beta>1, and the same C and beta work for all r. The comparison constant K is arbitrary real, including zero and negative values. |
| incoming_exceeds_every_constant | Allows targetWeight(r) to vary with r but requires it to be positive at every r. Requires the geometric lower bound for every r. Multiplication by the selected positive target weight preserves the strict inequality. |
| no_uniform_bound_of_family_total | Requires an exact family-total identity and inclusion inequality for every r. Concludes no real K bounds the arbitrary incoming function by K times the arbitrary targetWeight function on all r. |

The type signatures keep C and beta outside the r-dependent functions, preserving the required fixed-potential/fixed-endpoint geometric growth. Width-only positive normalizations may vary with r through targetWeight, so this algebra does not accidentally require a uniform positive lower bound on the normalization.

## Scope and remaining composition

The module deliberately accepts **arbitrary** targetWeight, familyTotal, and incoming functions. It contains no definition of the original P196 safe incoming operator and no actual arithmetic family. Applying its final result to the full safe-state operator requires the literal family-weight formula, a positive target-weight calculation, and the genuine safe-family inclusion theorem. These premises are explicit and are not discharged by this module.

In particular, this review does not certify an unconditional actual buffered-family obstruction, an all-time palindrome-avoidance assertion, or a statement about 196. The module documentation accurately discloses this limitation.

The original definitions retain complete unpadded windows for the actual positive width d=b+1. Their helper behavior at d=0 is outside the claimed domain. No hidden classical axiom, admitted proof, compiler-evaluation oracle, or unsafe proof escape was found in the reviewed source.

## Evidence

- build-results.json: exact hashes, all three commands, exit codes, times, exhaustive declaration list.
- source/: exact frozen source copies plus the independent axiom audit.
- logs/: literal stdout/stderr for both rebuilt modules and the audit.
- REVIEW_MANIFEST.json: byte hashes for this review package.
