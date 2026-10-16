# Agent #1 contribution integrity

The 59,999-byte outcome vector in `minimality_outcomes.json` is retained
losslessly, not summarized. Its JSON file was compared by exact Git blob
identity against the locally verified source before the publication commit:
`1168da4d79183eb09a988f63f295ddbaa744b244`. The decoded outcome digest is
`545b14904d5f783c87fa5c43bc566a3e463e13f5830c3217db29747d3eb46744`.
Two unpublished tree/blob upload attempts contained copying errors and were
rejected before any branch ref was updated. Neither is an accepted certificate.
The final published file has the matching local Git blob identity. Replaying
`independent_minimality.py` checks all bytes and all semantic outcomes.

The finite-family controls and minimum certificate are indexed by
`FAMILY_PROOF.md` and `MINIMALITY.md`. Their scripts verify existing stored
outputs rather than overwriting disagreements. The Lean family proof does
not import or assume any generated finite certificate.

All runtime binaries, caches and compiled objects are reproducible
infrastructure, not research claims. The initial unsuccessful Lean draft
is preserved in commit 13594a41c4a08ccbf3ac9bb12795b2914f997421; its failed
compiler result is distinct from the accepted structural-recursion source.
