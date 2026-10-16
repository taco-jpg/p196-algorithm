# A neutral exterior cannot overflow back into the high region

This is a written all-base lemma about the actual normalization map. It
removes one branch from the high-region return analysis; it supplies no
infinite invariant.

Let b >= 2 and let P=(p_0,...,p_(M-1)) be a nonempty symmetric word with
0 <= p_i <= 2b-2 and exterior p_0=p_(M-1)=b-1. Normalize by ordinary
base-b carries c_0=0, c_(i+1)=floor((p_i+c_i)/b), and digits
d_i=p_i+c_i-b*c_(i+1). All carries are bits. Suppose the final carry is
one. The canonical output then has M+1 digits, including d_M=1.

**Claim.** Its pair-coefficient word R contains a coefficient at most b-2.
In particular, R cannot have every coefficient at least b-1.

If every p_i were b-1, zero incoming carry would persist to the end,
contrary to the hypothesis. Let j be the least index with p_j != b-1.
Since the exterior is neutral, j >= 1. Symmetry gives
j <= floor((M-1)/2), p_(M-1-j)=p_j, and neutral coefficients at every
index strictly greater than M-1-j.

The coefficient p_j must be at least b. Otherwise p_j <= b-2, so the
reflected coefficient at M-1-j resets its outgoing carry to zero even
if its incoming carry is one. The remaining neutral suffix preserves
zero, contradicting the final carry one.

The initial neutral prefix preserves the initial zero carry. Hence
c_j=0 and d_j=p_j-b <= b-2. At the reflected high coefficient M-1-j,
the outgoing carry is one regardless of the incoming carry. The next
coefficient, at M-j, is neutral, so its output digit is zero. Since
1 <= j <= floor((M-1)/2), this partner index is a genuine source column,
not the extra terminal digit. Reflection in the actual output width M+1
therefore gives

    R_j = d_j + d_(M-j) = p_j-b <= b-2.

This proves the claim. No center-parity hypothesis is needed. In
particular it applies to every canonical ordinary pair word satisfying
the stated hypotheses, and even to symmetric words not realizable as a
pair word because of an odd center.

## Consequence for two-step high-region returns

Suppose Q is a canonical pair word in base b >= 3, all its coefficients
lie in [b-1,2b-2], and q_0 >= b. The established first-update formula
gives exterior p_0=q_0-b+1 in [1,b-1] for P=Q_1.

If p_0 <= b-2, the last exterior column cannot overflow. If p_0=b-1,
the lemma shows that overflow would force a coefficient of Q_2 below
b-1. Consequently every two-step return to the high region must use a
nonoverflowing second addition. This includes the exceptional initial
exterior q_0=2b-2; it does not exclude returns with that exterior and
no second overflow.

The reference first-update formula and actual-width convention are in
`../2026-10-15-seam-persistence-obstruction/SEAM_PERSISTENCE_OBSTRUCTION.md`.
The restricted decimal return theorem is in
`../2026-10-15-high-carry-renewal/HIGH_CARRY_RENEWAL.md`.

## Controls and limits

`check.py` exhausts bases 2 through 10 and symmetric even words of
lengths 2, 4, 6, and 8 with neutral exterior. It also tests symmetric
odd words of lengths 1, 3, and 5, including odd centers to exercise the
stronger statement. The checker computes ordinary carries directly and
independently checks the actual numeric output and its reversal pair
word. It retains every input, output, overflow status, and witness in
`controls.json.gz`, with hashes and counts in `verification.json`.

Finite controls corroborate the formulas; the all-width proof is the
argument above. No Lean verification, invariant, or claim about the
infinite orbit of 196 is made here.
