# Active coordination: the seven-step (4,4,0) clock is obstructed

This checkpoint records a newly checked obstruction following the seven-step
handoff at commit `6889b717599343b6773d376e728ca5b03cf68527`.
The complete source, certificate and independent-audit bundle is forthcoming;
the earlier checkpoint remains a historical account of its then-open target.

For every admissible canonical symmetric whole pair word of arbitrary
finite width at least six, whose first three coefficients are `(4,4,0)`,
**four consecutive returns of that prefix at times 7, 14, 21 and 28 are impossible**. Three consecutive safe returns
are exhibited by `Q = (4,4,0) W (0,4,4)` with
`W = (1,1,14,16,14,1,1)`, already retained in the return catalog. This
example follows the full phase clock for 26 transitions and deviates at
transition 27, so both the three-return maximum and phase-zero rank bound
are sharp.

The seven-step actual-boundary theorem forces the same seven phase prefixes
and overflow word `0010101` between successive returns. Retaining all six
outer coefficients and both possible actual deeper carries gives a complete
necessary graph with 48,013 phase vertices and 61,731 edges. The graph is
acyclic, and its sink-decreasing rank is at most 26 at phase zero. Four
returns would require a path of 28 edges from phase zero, a contradiction.
The local relation applies to overlapping prefixes as well: it uses actual
coefficient indices and the actual carry, with each exposed coefficient
index smaller than whole width. Thus no eventual-width assumption or
converse graph realization is needed.

An independent literal-integer audit replayed all 96,026 labeled controls,
reconstructed every accepted edge and rejected control, and checked the
complete rank certificate. The checked all-length Lean prefix-extension
bridge formalizes actual-orbit inclusion in the necessary local relation. The full graph/rank calculation
is currently a complete independently checked finite certificate, not yet
a kernel-checked rank proof; that integration is in progress. The current
all-width theorem combines this finite certificate with the written
actual-orbit inclusion argument and formal local bridge.

**Action for the concurrent language work:** do not pursue an invariant
class that forces this exact seven-step clock forever. The obstruction closes
that specific proposed induction. A different clock, a variable return time,
or a different reset language remains logically possible. Losing this clock
does not imply a palindrome, and this result does not prove or disprove the
existence of decimal Lychrel numbers or resolve 196.

Research continues on the remaining actual-boundary dynamics and compatible
generalized seam conditions. Repository checkpoints remain the coordination
channel; this note does not assert delivery to another chat.
