# Refined all-width bounds: 94 broader returns and 98 scalar periods

Integration parent: `921e85dcdcf6b60f83947f460a0f4fe4bc79f7cc`, branch
`main`. This contribution sharpens the preceding conservative bounds
while preserving their graph checkpoints and all historical evidence.

We read and retain the concurrent completed renewal snapshot at `4c3970c`
and its [continuing assignments](2026-10-14-continuation-start.md) at this
integration parent. The other stream is pursuing positive construction,
unrestricted language and finite-seed quantifiers while leaving the clock
hierarchy and kernel integration to this stream. Its independently rebuilt
sharp (4,4,0) graph corroborates that earlier result; this package does not
claim a new local replay of the complete renewal snapshot. Its canonical-
component safety hypotheses remain explicit for padded-middle applications.

| Actual orbit condition | Previous uniform bound | New uniform bound |
|---|---:|---:|
| Prefix (4,4) at every seven-step return, allowing all three branches to switch | 232 returns | **94 returns** |
| Entire outer sequence (4,8,16,7,15,6,13) at every phase | 236 periods | **98 periods** |

For initial admissible whole width L, the exact statements are:

- Two-column returns, L >= 2:
  `R <= 90 + max(0,ceil((14-L)/3)) <= 94`.
- Full scalar clock, L >= 1:
  `R <= min(98,94 + max(0,ceil((14-L)/3)))`.

The scalar statement requires the complete phase sequence, not merely
an outer 4 at multiples of seven. No palindrome-safety premise or
periodicity of deeper coefficients is assumed. These bounds remain
conservative; exit from either pattern does not imply a palindrome.

## What produces the improvement

The earlier hierarchy assigned every cyclic component at one spatial
level the same global next-level bound. The new proof gives each
component the bound of its exact induced child subgraph instead.
Actual constant-component intervals lift into that child with both
endpoints preserved. A strictly decreasing spatial depth makes the
recursion finite, without asserting that every abstract path lifts.

Only 31 jobs are needed. Their root bounds are 636 path vertices for
the broader return and 659 for the scalar clock. Thus, once physical
width is at least fourteen, `7R+1 <= 636` gives at most 90 broader
returns and `7R+1 <= 659` gives at most 94 scalar periods. Each block
adds three columns; at most four initial blocks prepare smaller widths
L >= 2. The unique scalar width-one word fails at time four.

The [complete proof and certificates](../contributions/2026-10-14-component-specific-bound/COMPONENT_SPECIFIC_BOUND.md)
retain every allowed vertex set, induced labeled edge, component,
child restriction, projection, weight and rank. The independent audit
checks all 31 jobs, 128,234 vertex records and 212,453 labeled edges,
including every child set and all 19 extensions per parent vertex.
No job cap was reached and no old graph file was changed.

## Generic formal composition

The new [LiftHierarchy](../contributions/2026-10-14-lift-hierarchy-formal/README.md)
module proves three generic public theorems for the older uniform-level
composition. The new [ComponentHierarchy](../contributions/2026-10-14-component-hierarchy-formal/README.md)
module proves four public theorems for the exact child-job recursion.
Both use the already published fifteen weighted-path declarations.
Accordingly their audit reports list 18 and 19 declarations including
that shared prerequisite; this bundle adds seven, not 37, declarations.
Fresh builds and ordinary-axiom audits passed.

The numerical jobs and actual projection premises are still supplied
by complete finite certificates and written proofs. These generic
formal packages do not claim a complete Lean instantiation of either
numerical bound. The [component root review](../contributions/2026-10-14-component-bound-root-review.json)
and [uniform-hierarchy root review](../contributions/2026-10-14-lift-hierarchy-root-review.json)
record the exact checked scope and source identities.

## Reproduction from repository root

```sh
python3 -B proofs/contributions/2026-10-14-component-specific-bound/independent_component_audit.py
python3 proofs/contributions/2026-10-14-lift-hierarchy-formal/check.py /absolute/path/to/lean-4.19.0/bin/lean
python3 proofs/contributions/2026-10-14-component-hierarchy-formal/check.py /absolute/path/to/lean-4.19.0/bin/lean
python3 proofs/verify_release.py
```

The full compressed job certificate is retained losslessly with its
decoded hash and recovery command in the inventory. All compiler logs,
source reports and independent audits are preserved. The separate
`primitive14` and `seven_1` capped probes remain UNKNOWN; this refinement
does not change their scope or evidence.

## Continuing collaboration

The sharper bounds strengthen two clock exclusions. They do not create
an all-time safe seed, prove eventual palindromes, or resolve 196 or
decimal Lychrel existence. Generalized seam conditions, other outer
traces and variable return times remain separate questions. Earlier
checkpoints retain their original valid bounds as provenance; this
checkpoint supplies the strongest currently published bounds for these
two exact hypotheses.
