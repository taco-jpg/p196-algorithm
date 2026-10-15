# Agent 12: exact fixed-target ancestry

Status: **LEAN_CHECKED locally**, with a second fresh-source-directory rebuild. Not independently reviewed or integrated. The workflow now invokes the accepted-module verifier; its earlier bootstrap-only success did not certify these sources.

Pinned research source: `74df59c5ecb6cb30fb3c88b1d5b26fdb9526d6c4`.
Owned task: `agent12-fixed-target-census`, published on coordination in `d60607303822a2e9d1f41d0ae2bf4f2822edd004`.

For ordinary decimal reverse-and-add T, a positive a and T^t(a)=p, the module proves `a+t <= p`, `t <= p-1`, `1+floor(t/5) <= decimalLength(p)`, and the exact source bound `t <= min(p-1,5*decimalLength(p)-1)`. It also supplies an explicit finite list whose membership is equivalent, in both directions, to positive actual ancestry with its depth. All natural targets and zero time are handled; zero has no positive ancestor.

The source is `proofs/research/main_existence_attempt/continuation_pass/finite_seed/FINITE_SEED_OBSTRUCTIONS.md`, section 4, lines 325–341 (SHA-256 `85476e1defb0028abbc536c817f514f239da7fe5efdb2b1dcc4b57c0492cb874`). The existing width theorem in `FiniteAncestry.lean` is reused, not claimed as a new discovery. The separate stronger bound uses its existing `4*decimalLength(p)` estimate. No proof of 196 or decimal Lychrel existence follows.

## Proof contract

A. Source statement: the positive ancestry bounds and finite inverse tree asserted in that exact source section.

B. Proposition: `ancestor_depth_min_bound` and `mem_ancestorPairs`; the latter proves completeness of a finite enumeration of the original reachability relation, not merely a bounded substitute.

C. Definitions: unchanged `Lychrel196.reverse10`, `step`, `orbit`, and `DecimalQuantitativeMass.decimalLength`. Natural reversal discards leading zeros and iteration continues after palindromes.

D. Hypotheses: naturals a,p,t, `0<a`, and `orbit a t=p`; no postulated growth, safety, or target bound.

E. Quantifiers: all a,p,t for the bound; for every p one finite list covers all a,t.

F. Boundaries: time zero included, target zero impossible for positive ancestors, one-digit and trailing-zero inputs included, initial and intermediate palindromes allowed.

G. Source relationship: exact original bound; finite-tree conclusion strengthened from palindrome targets to every natural target. Mathematical provenance remains the original report and reused width proof.

H. Dependencies: unchanged source hashes in `accepted.json`, Lean 4.19.0 commit `6caaee842e94`, Std only. No missing substantive hypothesis is introduced.

I. Endpoints: `P196.Agent12.FixedTarget.ancestor_depth_min_bound`, `P196.Agent12.FixedTarget.mem_ancestorPairs`, and `P196.Agent12.FixedTarget.finite_inverse_tree`. The 14 listed supporting declarations cover three linked source claims, not 14 independent discoveries.

J. Verification: `python3 proofs/contributions/agent-12/verify.py --log-dir /tmp/agent12-audit` with pinned lean on PATH, or supply `--lean /absolute/path/to/lean`. Every dependency is copied as source into a fresh directory and rebuilt; every accepted export has transitive axiom output checked against the standard allowlist. The completed local audit uses only `propext` and `Quot.sound` for all 14 exports. Exact commands, exit codes and logs are retained; independent semantic review is still pending.

## Coverage boundary

The initial source capture contains 2,690 tracked entries, 2,199 included text-source hashes, and 243 Lean files. These are discovery counts, not a completed semantic census. Archive listings, unexamined branches, historical reports and other written-only claims remain gaps. No exhaustive-completion assertion is made. Fuller claim dispositions and retained development attempts follow as separate checkpoints.
