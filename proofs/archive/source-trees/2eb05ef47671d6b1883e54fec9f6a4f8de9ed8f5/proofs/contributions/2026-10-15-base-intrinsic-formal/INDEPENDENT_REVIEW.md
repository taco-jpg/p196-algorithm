# Independent review of the all-base intrinsic criterion

**PASS** for all 27 new theorem statements and proofs in `IntrinsicCarry`,
`IntrinsicPattern`, and `IntrinsicReverseAdd`, together with the final README.
The producer's fresh build audits 109 theorems, comprising these 27 and their
82 prerequisites. Exact source/report/document hashes are pinned in
`independent_review.json`. This review reads the mathematics and source;
it does not claim a second independent compilation of that final chain.

At every base `b>=2`, the local carry trichotomy is correct under
`0<=q<=2b-2` and binary incoming carry. A coefficient below `b-1` gives
outgoing zero, the neutral coefficient `b-1` transmits the incoming bit,
and a coefficient at least `b` gives outgoing one. The local singleton
defect iff follows, with no symmetry or parity assumption.

The two pointwise bounds are proved against the actual reset recurrence.
Singleton cuts set each active incoming carry to zero and minimize outgoing
carry. An arbitrary reset cannot increase outgoing carry above continuous
normalization; monotonicity of integer division and carry bounds make the
induction valid. Subtracting these inequalities yields nonnegative defects
and simultaneous singleton maximality, including the common zero default
beyond the finite word.

The intrinsic-pattern induction retains the arbitrary initial bit rather
than discarding an initial active neutral run. Its exact auxiliary statement
says a defect occurs either when the initial carry is one and the word
starts neutral, or when a high/neutral adjacency occurs inside the word.
The initial-zero specialization therefore has precisely the claimed
partition-free meaning. `defect_iff_out_witness` connects this recurrence to
an actual index at which continuous and singleton carries disagree; it is
not merely an abstract predicate introduced without a carry interpretation.

`HighNeutral` is explicitly proved equivalent to a decomposition
`front ++ high :: (b-1) :: tail` with `high>=b`, so the relation is genuinely
adjacent in least-significant-first order. The existential partition theorem
ranges over all Boolean-tagged lists with the fixed coefficient projection.
That equality fixes the whole word and its length, while arbitrary reset
flags cover every consecutive partition. The singleton witness gives the
converse, and coefficientwise maximality gives the forward implication.
Empty words have no witness; equal zero defaults prevent out-of-range
indices from creating one. No canonicality, positive terminal coefficient,
or input symmetry is smuggled into this combinatorial iff.

Output safety is a separate consequence at `b>=3`, where the all-base seam
theorem applies. It requires symmetry of the coefficient word. The ordinary
reverse-and-add wrapper obtains this symmetry, coefficient bounds, and
positive leading normalization from actual canonical input digits. It
therefore supplies a nonpalindromic canonical expansion of the exact integer
`n+reverse_b(n)`, rather than only nonsymmetry of a padded coefficient list.

The two boundary distinctions are preserved correctly. The combinatorial
iff includes binary, while binary output safety is false: the checked
`110_2+11_2=1001_2` control has a high/neutral pair and unequal carries but
a palindromic output. Input nonpalindromicity is not asserted for all bases;
the earlier odd-base `212_3` example remains a counterexample to that
extension of the decimal parity argument. The local criterion is also not
a complete test for nonpalindromic output: words without neutral coefficients
can normalize nonpalindromically.

The source and README explicitly attribute decimal singleton maximality and
the high/nine iff to the other stream's `IntrinsicSeam.lean` at commit
`e52125515490b668d14e95b0cf8d31767bcde7c4`, whose exact bytes were separately
source-reviewed. The contribution here is the formal variable-base extension
and canonical ordinary-output interface. Neither temporal persistence nor
an infinite safe orbit follows from the current theorem, and neither is
claimed.
