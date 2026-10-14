# Independent review of the concurrent contributions

The source reviewed here was published in commit
`b7fa911dc4ca943528f5d28b67f3fbd87c9404ca` of `taco-jpg/p196-algorithm`.
The external author's files remain in `proofs/contributions/` with their
original bytes. This directory contains our additional review evidence.

## Rebuilt formal results

`check_contributions.py` freshly rebuilt all four dependencies and both
new modules, then generated a separate complete axiom audit. All 24 new
supporting declarations passed under Lean 4.19.0. Source hashes were
compared to the published verification records before compilation and
checked again afterward. Only `propext`, `Classical.choice`, and
`Quot.sound` occur in the audited axiom lists.

The strongest unconditional explicit result is: for every natural R,

\[
C_R=2\bigl(10^{\lfloor7R/4\rfloor+1}-1\bigr)
\]

has nonpalindromic actual decimal iterates at every index 0 through R.
The candidate changes with R. The second module proves the deterministic
mirrored-nine-block implication used in the written counting proof.
No global finite-delay bound or finite Lychrel witness is supplied.

From this directory in the published layout, run

```sh
python -B check_contributions.py /absolute/path/to/lean-4.19.0
```

The two root overrides support separate local research and contribution
checkouts; they do not alter the mathematics or select different hashes.

## Written proofs and arithmetic controls

Root read the finite-width probability calculation, its growing-horizon
limit, and the separated-block theorem. The independence of the chosen
digit blocks, exclusion of the leading digit, exact initial-palindrome
intersection, actual final overflow, and one-zero-gap boundary are explicit.
Their stated quantifiers do not imply an infinite safe orbit for one seed.

The external density replay passed 99,999 exhaustive small integers and
22,016 planted-block controls. The separation replay passed all 36 outer
potential cases, 3,000 block examples and 18 complete trajectories up to
gap exhaustion. `root_density_replay.log` and `root_separation_replay.json`
record these independent replays. They are implementation controls, not
replacements for the universal proofs.

The external separation bound for the remaining (1,7) family is
\(\tau(r)\le4r-3\) for \(r\ge2\). Our new exact arbitrary-block seam
identity and local Lean incoming-carry lemma are a response to its stated
post-collision obligation. Neither contribution provides the repeatable
safe reset required to prove existence.
