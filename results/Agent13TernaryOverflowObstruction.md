# Agent13TernaryOverflowObstruction

**PAPER PROOF.** For the primitive 3-letter length-two substitution `0→01,1→02,2→00`, an interior eight-letter source factor encoded with three distinct nonneutral pair coefficients cannot map at any overflow-one ordinary reverse-and-add step to an injectively recoded six-letter factor of the same substitution, in any base `b>=2`.
The source and target may be arbitrarily shifted; the coefficient values may vary, and normalization may collapse source distinctions.
Exact finite factor languages have `|L8|=20`, `|L6|=16`; all five partitions of the three neighbor-pair types fail for all 20 source factors (100 finite cases).
Independent prefix-based checker: 540 raw mappings fail; 2,500 ordinary big-integer checks agree.
Existing positive exterior controls: base 9 `g=1100011000` with `|B|=61`; base 13 `g=1010010000` with `|B|=75,55`.
Full proof: `reports/Agent13TernaryOverflowObstruction.md`.
Reproduction: `calculation/decimal_frontier/ternary_overflow/proof.py` and `calculation/decimal_frontier/ternary_overflow/independent.py`.
Commands: `python3 calculation/decimal_frontier/ternary_overflow/proof.py` and `python3 calculation/decimal_frontier/ternary_overflow/independent.py`.
Scope excludes only a single overflowing step and nonneutral ternary input; no assertion about overflow-zero, neutral coefficients, unconstrained intermediates, or all F1 formats.
Not LEAN-VERIFIED; no decimal Lychrel certificate or result about the orbit of 196.