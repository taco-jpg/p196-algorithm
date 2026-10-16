# Source review of the external intrinsic-seam checkpoint

**PASS, source and mathematical review only.** This review covers the exact
`IntrinsicSeam.lean` and `SeamAnnihilation.lean` sources at external commit
`e52125515490b668d14e95b0cf8d31767bcde7c4`. Their 31 theorems and five
definitions were read in full, together with the external status note.
The exact source bytes, status, and upstream verification report are retained
in `sources/`; their Git blob identities were checked against the retrieved
commit tree, and SHA-256 digests are in `source_manifest.json`.

No new independent Lean compilation or axiom audit is claimed here. The
upstream report states a successful fresh build and audit of the 31 theorems
and five definitions. Its three dependency hashes match the sources already
freshly checked in the separate 42-theorem external raw-symmetry audit.
That earlier audit does not automatically audit these new declarations.

The intrinsic criterion is exact under its stated decimal coefficient bound
`0..18`, without symmetry or canonicality. Singleton isolated outgoing carry
is `q_i/10`, the smallest outgoing carry possible at the column. Subtracting
from the actual carry shows every partition defect is nonnegative and bounded
coefficientwise by the singleton defect. Binary actual carry then makes a
nonzero singleton defect equivalent to coefficient 9 with actual incoming
carry 1. Backward induction through a run of nines reaches a coefficient at
least 10 immediately followed by a nine; the impossible base case is actual
incoming carry 1 at column zero. The converse follows directly from division
at the high column. Every index in this argument is bounded by the finite
word length.

Thus the source already proves both the partition-free local criterion and
simultaneous coefficientwise maximality of the singleton partition. Neither
is an additional decimal discovery of this review stream. Canonicality enters
only in the ordinary numeric bridges. The input-nonpalindrome bridge uses
the odd pair coefficient 9; it is distinct from the next-output safety
bridge, which uses nonzero carry defect.

For the framed family `(10,9^k,10)`, the carry and digit formulas correctly
retain the actual terminal carry. The exact next word
`(1,1,0^(k-1),1,1)` is stated only when `k>0`; the weaker bound by two also
covers `k=0`, where the middle coefficient is two. The initial total defect
mass is exactly `k`, and every partition defect after one update vanishes.

The coefficient function continues with nines beyond the finite word. Its
all-index defect formula consequently equals one outside the two designated
endpoints, rather than having finite support. The finite mass theorem and
orbit statements restrict to the actual word. The source/status explicitly
record the earlier failed finite-support formulation and its correction.
There is no out-of-range zero-extension assumption in the reviewed theorem.

Even `k` supplies admissible pair words; positive even `k` gives actual
positive finite seeds using the existing constructive realization theorem.
Every canonical realization is nonpalindromic at times zero and one and
palindromic at time two. The exact first output is proved, whereas the
explicit closed seed formula is correctly identified as a separate written
construction, not a theorem of these modules. No persistent invariant or
all-time claim is made.

For later generalization, the intrinsic carry argument and singleton
maximality extend naturally to base `b>=2`, with neutral coefficient `b-1`
and coefficient bound `2b-2`. The all-base next-output safety theorem needs
`b>=3`. The input-nonpalindrome parity argument extends only to even bases:
in base three, the palindromic seed `(121)_3` has pair word `(2,4,2)`, which
contains a high coefficient followed by the neutral coefficient two. This
domain distinction must remain explicit in any extension.
