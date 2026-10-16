# Parent semantic review: Safety and Numeric

Reviewer: Agent9 parent /root. Genuine specialist /root/horizon_safety authored these two modules. The parent authored Counts and the aggregate, so this report does not call the parent an independent reviewer of those modules. Counts has its separate coverage-census review; the runtime specialist supplies complete independent rebuild and final aggregate review. This is internal review, not external peer review.

| Reviewed source | SHA-256 |
|---|---|
| Agent9HorizonSafety.lean | a8575086a5590d8560034e7b4a960d3e3453148acdc5aecef10b7a9fd2aa17d4 |
| Agent9HorizonNumeric.lean | 2f374fd454f1d8cba3ff4ea3f57643d0ebc7d02ff93716b525e31fe5d1660770 |

## Verdict: semantic source review PASS

The target is a list of mirrored pair sums, not the numeral whose digits would be those coefficients. Canonical plus the column-sum equations preserves the original finite-integer meaning.

Safety proves the exact reflected target length, central reservoir starting at m+1 with length2*k, bounded coefficients, symmetry, positive exterior, and the even-width center condition. Existing valid_word_realizable then supplies an actual positive integer. No witness or actual-width premise is assumed without proof.

protected_target_safe quantifies over every canonical realization and every positive time at mostk, using the original DecimalSafeRuns integer theorem. A separate outer-parity proof covers time zero. The existential target theorem therefore has no initial-time gap.

Numeric identifies each canonical digit function with the established finite digit list using evalL equality and digits_evalL. Its pairWord equality is proved. The unchanged Agent109.Compat.pairWord_step transports FullActualFiber's transition to the actual next integer.

protected_input_step_realization applies to every canonical input realization. Canonical positivity implies positive n and step n; canonical_exists provides next digits. Equality of complete pair-word lists proves actual next-width equality, then lookup proves each column equation. No padded width is substituted.

The original orbit_from_step proves the shift: for1<=j<=k+1, target timej-1 lies in0..k. protected_predecessor_safe therefore covers every input digit split; protected_predecessor_realizable supplies positive witnesses with both pairWord equalities.

## Boundaries

- At m=0 the fiber is empty; these conditional statements do not assert nonemptiness.
- At k=0 target time0 and predecessor time1 remain covered.
- Predecessor time0 is not included.
- No first-palindrome-hit assumption or stopped orbit is used.
- No integer multiplicity, unrestricted protected maximum, analytic limit, infinitely safe fixed seed, or196 theorem is accepted.

No semantic correction is requested. The parent's twelve-module replay covered Safety and the earlier aggregate, not Numeric; Numeric's compiler evidence remains attributed to its author and the separately recorded expanded independent replay when complete.
