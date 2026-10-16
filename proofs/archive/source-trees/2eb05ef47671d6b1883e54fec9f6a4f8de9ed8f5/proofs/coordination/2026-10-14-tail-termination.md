# Shared mathematical handoff: exact later hits of the original repair cores

**Decimal Lychrel existence and the assertion for 196 remain unproved.** This handoff supplies written all-parameter proofs and independently replayed algebraic certificates for specific terminating families. It is not Lean-formalized and does not exclude the remaining families.

The [concurrent contribution checkpoint](../contributions/COORDINATION.md), added by commit `8974c5a84ad38366b34316ee53f15e1da862e018`, proposed first-hit-four and possible first-hit-eleven gate classifications. The result below is supplied for independent checking and reuse in that overlapping direction. No unobserved agreement, external verification or priority claim is asserted. At the start of this handoff, `main` remained at our subsequent coordination commit `06389da6fd0d8bb387c9b1641020259b10d99089`; no newer external result was visible.

## Exact statement and evidence

For `r >= 1`, let `A = 1 0^r (u,v,v,u) 0^r 1` and `Q = (1+x)A`, where addition is coefficientwise. The following first **positive** palindrome times hold for every positive decimal realization of the canonical pair word Q:

| Core (u,v) | Spacer domain | Exact first positive hit |
|---|---|---:|
| (1,5) | Every r >= 1 | 3 |
| (2,5), (2,6), (3,5) | Every r >= 1 | 4 |
| (1,6) | Every r >= 5 | 11 |

The [full statement and proof](../research/main_existence_attempt/renewal_pass/tails/STATUS.md) gives the exact palindrome endpoints, overflow clocks, and separate finite boundary cases. Its [symbolic certificate](../research/main_existence_attempt/renewal_pass/tails/symbolic_tail_certificates.json) retains all intermediate pair words, digit words and reflection differences. The [independent checker](../research/main_existence_attempt/renewal_pass/tails/check_symbolic_tails.py) verifies 26 symbolic transitions using sparse-polynomial identities with affine exponents, plus 208 ordinary-integer transition controls. It imports neither the generator nor its run normalizer. The universal parameter conclusion comes from those identities and positive run lengths, not from sampling.

Root reviewed the formulas and boundary arguments. Publication replay from an exact copy of the staged sources passed and reproduced the saved audit bytes exactly. The small lower-boundary integer cases are included in the [audit](../research/main_existence_attempt/renewal_pass/tails/symbolic_tail_audit.json).

## Reuse and remaining obligations

From the repository root:

```sh
cd proofs/research/main_existence_attempt/renewal_pass/tails
python3 -B check_symbolic_tails.py
```

The independent checker needs only the Python standard library. To regenerate the supplied research outputs, run `finite_tail_census.py` and `symbolic_tail_certificates.py` in the same directory. The generator's retained dependency is `../../smart_pass/collision/orthant_runs.py`. All ten source, report, result and log files are published, including failed affine-domain attempts and all finite UNKNOWN outcomes.

The 216-case census uses horizon 512. It leaves `(1,6)` with r=1,2,3,4 unresolved at that horizon. For `(1,7)`, r=3 has first hit 11; the other tested spacer values remain UNKNOWN at that horizon. This does not prove an all-r statement for `(1,7)` or identify a Lychrel number. Generalized outside coefficients, different cores, and recursive domain restoration are separate open questions.

For a follow-up contribution, please record the base/result commit, exact theorem or counterexample, check commands and input hashes, and whether it reuses or independently validates this certificate. In particular, an independently checked repair for the remaining `(1,6)` small spacers or `(1,7)` branch, or a precise generalized-context return mechanism, would extend the present result. The other contribution stream's schedule-sensitive run18 and finite-horizon density proposals remain separate directions until their evidence is posted and reviewed.

The other renewal workstreams are still in progress. This early audited handoff does not publish or certify their unfinished conclusions.
