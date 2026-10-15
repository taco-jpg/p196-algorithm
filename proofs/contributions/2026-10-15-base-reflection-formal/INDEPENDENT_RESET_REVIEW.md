# Independent reset-normalization review

**PASS** for the frozen 16-theorem `ResetNormalization.lean` source,
SHA-256 `821647540a8231eb1329c44d1abf3aa5318d3ee27acde36ec3f7f636b692f3cf`.
The earlier independent review of `BaseReflection.lean` remains a separate
checkpoint. This review concerns the source's mathematics and exact interface;
the package's producer freshly compiled and axiom-audited all 40 declarations
in the dependency chain.

Every consecutive partition of a nonempty word is represented: tag each
interior block-start position `true` and every other interior position
`false`. The first tag is immaterial with initial carry zero. Conversely,
the interior true tags, together with positions zero and the final word
length, delimit consecutive nonempty blocks. The empty input is also defined
algebraically, but is not a canonical positive integer word.

Within a block, `columns` propagates ordinary outgoing carry to the next
position. At the next block's start, `active` becomes zero independently of
the preceding terminal carry. Thus each delimited block is normalized from
zero. This includes adjacent cuts, one-column blocks, a single whole-word
block, and an arbitrary final block; no minimum block width or positivity
condition is assumed. The current formal source encodes these semantics by
the reset recurrence. It does not yet state a separate nested-list theorem
equating this recurrence to a sum over an explicitly supplied block list.

`placed` preserves the distinction between incoming carry and raw placement.
At a reset, the new block's first digit is computed from incoming zero, while
the preceding block's terminal carry is added at that same global column.
This sum is retained as a raw coefficient, without being normalized again.
Away from resets there is no additional terminal contribution. At the end,
the final outgoing carry is retained as the last slot, including when zero.
This is exactly the shifted sum of separately normalized blocks, padded to
their physical block widths; leading zero digits inside a block do not alter
the value or placement.

`placed_eq_raw` derives the coefficient identity from integer division and
remainder. It even holds for arbitrary integer inputs; the later conditions
`b>=2`, coefficient bounds, and an initial carry bit ensure the intended
nonnegative digits and binary outgoing carries. `columns_conditions`
therefore supplies the previous module's existential local conditions from
actual reset division, rather than assuming a chosen carry list is realized.

The two classified coefficient languages erase dependence on cuts. In the
low language every carry is zero. In the `{0,b+1}` language, for `b>=3`, an
outgoing carry depends only on whether the coefficient is zero or `b+1`,
independently of the binary incoming carry. The proved list equality of
carry columns then gives equality of raw placement and ordinary continuous
normalization. Membership transport from `columns_qs` is sufficient because
these conclusions are universal coefficient properties, not index-specific
correlations.

Both final symmetry-to-ordinary implications are consequently valid. Their
scope remains **padded lists**: `ordinary` retains the terminal slot even
when zero. The padded `L+1` symmetry hypothesis alone does not assert a
physical overflow, and the `L` branch explicitly assumes removal of a zero
terminal slot. Determining actual width for a canonical positive word,
stating palindrome equivalence at that width, proving converse symmetry,
and connecting to an ordinary integer orbit are subsequent obligations.
The new `PhysicalWidth.lean` work is not included in this review.
