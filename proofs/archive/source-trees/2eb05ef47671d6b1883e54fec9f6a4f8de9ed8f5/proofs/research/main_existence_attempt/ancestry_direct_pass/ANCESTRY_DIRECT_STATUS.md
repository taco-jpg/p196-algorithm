# Direct ancestry pass and algorithm review — 14 October 2026

**Decimal Lychrel existence and the claim about 196 remain unproved.**
This checkpoint contains new checked supporting mathematics and exact
exclusions of specified proof-certificate families. It does not claim a
solution, novelty, external peer review, or a verified production GPU run.

## New unconditional Lean result

For a positive integer n and r reverse-and-add steps, the new module proves

    width(T^r(n)) >= width(n) + floor(r/5).

More sharply, if a positive integer reaches a fixed width-L target after r
steps, then r <= 4L. The same bound holds for admissible finite pair-word
ancestors. Therefore the intersection of all ordinary ancestry sets of a
fixed finite target is empty; any safe restriction has empty intersection
as well. This is a backward statement with a fixed target. It does not
exclude an infinite forward orbit whose width grows.

`lean/FiniteAncestry.lean` proves these statements against the unchanged
standalone `continuation/LychrelDigitSums.lean`. The dependency and module
were rebuilt with Lean 4.19.0; root independently compiled the new module
against that fresh dependency. All eleven audited declarations use only
`propext` and `Quot.sound`. There are no admitted proofs or unproved growth
hypotheses in these declarations. The safety predicates and their relation
to the language search are distinguished in `lean/STATUS.md`.

## Direct NFA certificate search, without determinization

The saved 6,680-state NFA for safe two-step ancestry has 8,396 terminal
acceptance flags. Every flag now has a concrete accepted pair word whose
ordinary reverse-and-add orbit reaches a palindrome. Hence no nonempty
choice of those flags yields a safe forward-closed language. This is a
complete exclusion of this fixed terminal-component family, not of every
language expressible by refining states or tracking NFA configurations.

The largest first hit among the witnesses is 72 steps; the largest input
has 29 digits. The independent branch checker and root's separately written
`root_nfa_audit.py` verified every NFA path and ordinary integer trajectory,
with complete coverage of all 8,396 flags. Neither checker imports the
search code or carry transducer. See `language/STATUS.md`.

## Exact scope of finite safe ancestry

Let B be the pair words whose next output is palindromic, S_0 the canonical
words, S_(r+1)=G(S_r minus B), and K_r=S_r minus B. Then S_r is descending,
and G(K_r)=S_(r+1). The set S_r intersects B exactly when some positive
integer first reaches a palindrome at positive step r+1. K_r fails forward
closure exactly when such a first hit occurs at step r+2. The positive-step
convention permits an initially palindromic seed; the report explains the
one-step adjustment for requiring a nonpalindromic starting seed.

The published nonpalindromic seed 13968441660506503386020 was independently
recomputed and first hits at step 289. Thus S_r intersects B for r<=288,
and K_r is not closed for r<=287. This does not prove the all-depth claim.
The source-described delay-extension method has unextendable branches;
no uniform induction follows from it. See `delay/STATUS.md`, the verifier,
and its full 289-step trajectory.

Long surviving 18-runs provide arbitrarily long finite safe segments. A
universal finite upper bound on terminating first-hit times would therefore
imply an explicit finite Lychrel witness. Neither that upper bound nor
unbounded finite terminating delays has been proved here.

## Review of the supplied computing algorithms

The user supplied https://github.com/taco-jpg/p196-algorithm. The inspected
revision is 8219522a02d46fbb72a6ee38819e5723b8c8fc9f. Scope includes the root
README, explainer, math_v6 package and v8 source archive. Retrieved files
were checked against their Git blob hashes. The larger v9 archive was not
retrieved through the connector, so neither v9 implementation correctness
nor reported GPU throughput is independently verified here.

The mathematical checks pass: all 176 local CRT cases, and 100,000 growth
steps against ordinary big integers. The independent v8 CPU core oracle
passes on 1,000,579 inputs, including every positive integer below one
million and long carry-chain cases. A strict 88-case integration matrix
checks exact output, earliest palindrome time, materialized palindrome
contents, intermediate snapshots, certification failures and exact replay.
It includes J=8/16 and K=7/33/64. The CPU matrix reports no discrepancy.
The detailed reports distinguish arithmetic correctness from command-line
validation issues, weaknesses in the supplied test assertions, and an
unconfirmed GPU concurrency concern.

The engine accelerates exact finite iteration by folded pairs, bit planes
and certified time blocks. The carry model matches the existing mathematical
representation. Its finite-interval certification is relevant to designing
sound local computations; it does not supply an invariant proving avoidance
at every future time. Faster iteration alone does not remove the NFA
configuration-growth bottleneck of the current proof search.

See `repository_review/` for pinned provenance, independently written test
harnesses, results and the audit. Upstream engine files and production
checkpoints were not modified. Generated binaries and scratch cases are
not publication deliverables.

## Reproduction and publication scope

Branch status files give exact commands and limits. Keep original source
dependencies and evidence hashes. Earlier `return_pass/` results remain
unchanged, including the UNKNOWN status of full two-step-ancestry
determinization. The direct terminal-flag exclusion is a different family;
it must not be used to relabel that earlier UNKNOWN result as impossible.

All statements above are supporting results or explicitly scoped exclusions.
The required nonempty family closed under reverse-and-add and avoiding
palindromes at every future step has not been obtained.
