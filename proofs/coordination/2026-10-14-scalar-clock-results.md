# Checked scalar-clock bound and formal weighted path theorem

Integration parent: `a1b8b7be16c49a1f9041045baf1adbcf1e65bfff`, branch
`main`. This result removes the prescribed second column from the preceding
44-return obstruction, while prescribing the entire outermost sequence.
All earlier proof and coordination files are preserved.

**Theorem.** For an admissible canonical finite pair word Q of width
L >= 1, suppose the actual outer coefficient follows
`(4,8,16,7,15,6,13)` at every phase for R complete periods:
`G^t(Q)[0] = a[t mod 7]` for all `0 <= t <= 7R`. Then

`R <= min(236, 232 + max(0,ceil((14-L)/3)))`.

Every inner coefficient and its temporal history is unrestricted. The
bound is conservative and has no palindrome-safety premise. It applies
to this full seven-phase sequence; outer coefficient 4 at multiples of
seven alone does not force it. The alternate trace `(4,9,18,9,10,1,2)`
also returns to 4 and is outside this exclusion.

The [full proof](../contributions/2026-10-14-scalar-clock/SCALAR_CLOCK_BOUND.md)
uses a seven-vertex, ten-edge root graph and the actual carry-labeled
spatial lift. The complete hierarchy becomes acyclic at width fourteen.
Its weighted condensation bound is 1,629 path vertices, giving at most
232 full periods once physical width is fourteen. Every period adds
three columns. The unique width-one word `(4)` deviates at time four,
so it completes zero periods; treating this case separately gives the
uniform bound 236 rather than the coarse width-preparation bound 237.

## Independent evidence and formal scope

The literal-integer audit checks all 128,644 local controls and every
raw/recurrent graph. A separate weighted-bound audit checks all 60,952
components and ranks, including the width-one exception. Every graph,
local-control outcome, SCC assignment, condensation edge and weighted
rank used in the proof is retained. The [root review](../contributions/2026-10-14-scalar-clock-root-review.json)
records exact hashes for all 108 frozen contribution files.

Fifteen freshly rebuilt Lean theorems in
[CondensationBound](../contributions/2026-10-14-scc-bound-formal/README.md)
formalize the generic weighted path argument, including component
intervals, rank descent, path-vertex bounds, cyclic interval composition,
and the earlier 1,600-vertex-to-228-return arithmetic implication.
Only ordinary logical axioms are reported. These theorems do not certify
the numeric SCC tables or instantiate this full scalar hierarchy; those
remain complete independently replayed finite certificates. The existing
actual-prefix Lean bridge continues to supply local necessity.

## Retained capped probes and exact recovery

The separate `primitive14` and `seven_1` scalar probes remain **UNKNOWN**.
They reached declared resource caps with completed graphs through widths
twelve and fifteen respectively. A cap is neither an exclusion nor
evidence of a realizable infinite orbit. All completed raw/recurrent
graphs and reports are retained, including the next-lift cap evidence.

Two stored raw files in the `seven_1` probe were discovered truncated.
The recovery procedure rebuilt them from verified parent graphs and
reproduced their originally reported SHA-256 hashes. Atomic replacement
and a later-call inventory check verified every graph hash. Both truncated
byte streams, the verified replacement evidence, recovery source and
report are preserved. The truncated artifacts are forensic byte records,
not valid complete gzip graphs, and are identified as such in the
inventory. The repaired canonical graph files retain their original
identities. No result or search cap was changed by recovery.

## Reproduction from repository root

```sh
python3 -B proofs/contributions/2026-10-14-scalar-clock/independent_scalar_audit.py
python3 -B proofs/contributions/2026-10-14-scalar-clock/independent_scalar_bound_audit.py
python3 -B proofs/contributions/2026-10-14-scalar-clock/inventory_capped_probes.py
python3 proofs/contributions/2026-10-14-scc-bound-formal/check.py /absolute/path/to/lean-4.19.0/bin/lean
python3 proofs/verify_release.py
```

All complete gzip artifacts have compressed and decoded hashes and
recovery commands in `INVENTORY.json`; both incomplete forensic streams
are preserved as exact binary files without pretending they decompress.

## Continuing shared work

An indefinitely maintained full `(4,8,16,7,15,6,13)` outer clock is now
excluded without restrictions on deeper temporal behavior. The
concurrent seam/language work should keep the different outer traces
and variable return patterns distinct. Neither this exclusion nor the
capped probes settle 196, imply eventual palindromes, or establish
decimal Lychrel existence. Full kernel integration and further clock
analysis remain separate active contributions.
