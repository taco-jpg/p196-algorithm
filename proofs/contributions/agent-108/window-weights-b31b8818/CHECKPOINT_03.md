# Agent #108 — complete literal family ratio and actual family embedding

This source checkpoint extends `bd576412b228ab60156ce1759a54af69dbbdb9f6`
on the existing contribution branch and draft PR #98.

## New proved interfaces

`Agent108WindowFamilyProducts.lean`, SHA256
`d4449500c98887a82dca222af318e8d99e8ef0d1ad5e58719658406c1650fdc8`,
decouples window width `b+1` and buffer length `b+c`. Its
`inputHalf_product` and `targetHalf_product` give the exact literal
products for all natural `b,c,k,r`, including short and empty tails.
The author build and nine-declaration audit passed with `--trust=0`.
Independent reviewer `semantic_scout` then rebuilt its four-module chain
from an empty directory, audited 32 public declarations, and reviewed
the complete extra-buffer exponent accounting. See
`review/independent-family-products-d4449500/`.

`Agent108WindowFamilyRatio.lean`, SHA256
`051dcb42849d9cffb2fec0de77af138b6d7d6c415ff27d65725dcdf9cfcf7afc`,
defines the strictly positive local insertion ratio `localBeta`.
`inputHalf_product_ratio` and `inputHalf_exact_total` prove the exact
pointwise ratio and the finite total
`C * targetProduct * (1+beta)^r`. The constant `C` is the previously
proved explicit endpoint constant; neither it nor beta depends on `r`
or the extra-buffer length `c`. Author compilation and a distinct
reviewer root's fresh eight-module build passed. The latter audited all
63 public declarations, including the `localBeta` definition. See
`review/independent-family-ratio-051dcb4/`.

`Agent108WindowEmbedding.lean`, SHA256
`1acb5964188bcb7828bec58cbd8b5328ff9d68467e5951eb3a4bf87d78eb4e7f`,
embeds the long-buffer family into the original verified Agent13 binary
family. `expandBits`, `expandFin`, and their injectivity/coordinate
theorems prove the exact restriction. `embeddedState_spec` reuses the
original safety and arithmetic transition; `embeddedState_half` and
`embeddedTarget_half` identify every coordinate of the complete literal
half-words. The source and target have the same actual finite width.
Author `--trust=0` compilation and all 41 public declaration audits
passed. Independent statement and execution review of this module is
still in progress at this checkpoint. See `embedding/README.md` and
`embedding/attempts/006/` for the fixed source and evidence.

All reported mathematical axiom audits use only subsets of
`{propext, Classical.choice, Quot.sound}`. Generated compiler internals
from the separate exhaustive core environment inspection are classified
and retained without expanding this logical allowlist.

## Remaining actual incoming theorem

The actual family is available. The final module must still combine its
injective safe-fiber inclusion, equal-width normalization and the exact
window total with unbounded positive geometric growth. The owned
`Agent108WindowIncoming.lean` is being developed separately and is not
included as a checked module in this checkpoint. The full canonical
safe incoming operator and its original decimal interpretation are
reused from Agent13, including predecessors of every possible width.

No claim of an infinite palindrome-avoiding orbit or a conclusion about
the orbit of 196 follows from the present weight calculation.
