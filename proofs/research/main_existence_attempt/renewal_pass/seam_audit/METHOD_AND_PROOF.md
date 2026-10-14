# Active seams certify safety; raw isolated-digit symmetry detects palindromes

## Result and scope

Let Q be a canonical whole decimal pair word, partitioned in **any** way
into nonempty consecutive coefficient blocks. Normalize each block in
isolation from incoming carry zero, retain its original width, include its
terminal carry, and place the results at their original starts. Write E
for this raw polynomial sum, D for the actual whole normalized digits,
gamma for the whole final carry, and K for the seam mask in

`D = E + (x-10)K`.

Then the following three conditions are equivalent:

1. E is symmetric in the actual output width L+gamma.
2. D is symmetric in that width, so the first ordinary reverse-add output
   is a palindrome.
3. If gamma=0, every coefficient of Q is at most 9. If gamma=1, every
   coefficient of Q is 0 or 11 and the outer coefficient is 11.

Whenever these conditions hold, **K=0**. The useful positive contrapositive is

**If K is nonzero, the next ordinary reverse-add output is nonpalindromic.**

This is a realizable one-step collision safety certificate. It requires no
symmetry hypothesis on E. In seam terms, any block entered with carry one
and having a nonempty initial run of 9s certifies safety of the whole update.

The previously considered
conditional safety antecedent, “E is symmetric in actual width and K is
nonzero,” is impossible for every canonical whole pair word. This includes
all reflection-symmetric lists of symmetric blocks and every BHB partition.
No assumption on symmetry or canonical status of the individual blocks is
needed for the impossibility proof.

The universal seam identity and its mass-iff criterion remain correct. The
extra E-symmetry hypothesis had hidden the usable active-seam criterion.
This result supplies a one-update safety test, but no recurrent collision
reset or Lychrel existence proof.

## Definitions and the identities being audited

Write the full pair word low-to-high as `q_0,...,q_(L-1)`. Canonical means
L>=1, `0<=q_i<=18`, `q_0>0`, `q_i=q_(L-1-i)`, and an even middle
coefficient when L is odd. These are precisely the conditions needed for a
positive decimal realization. Its reverse-add output is the integer Q(10),
independent of the chosen realization.

For each column i, let C_i be its outgoing carry when its own block is
normalized in isolation. Let tau_i be its incoming isolated carry: zero
at a block start, and the preceding C inside that block. Then

`C_i,tau_i in {0,1}`, and `0 <= q_i+tau_i-10C_i <= 9`.

The isolated normalization of each block includes its final carry digit.
Consequently the placed raw sum has the exact polynomial form

`E = Q + (x-10)C`, where `C(x)=sum_i C_i*x^i`.

In coefficient notation, with C_-1=0,

`E_i=q_i+C_(i-1)-10C_i` for 0<=i<L, and `E_L=C_(L-1)`.

This formula uses the globally preceding isolated carry in the overlap
term, even when i is a new block start. The difference between that
overlap and tau_i is precisely why E can have coefficient 10.

Let A be the actual whole outgoing carry polynomial. On the initial run
of 9s in a block entered with carry one, actual and isolated carries differ
by one; at the first other coefficient the difference vanishes. This includes
an all-9 block, where the difference reaches the end. Therefore `A-C=K`,
where K is exactly the nonnegative mask in the original seam theorem.
Subtracting the two normalization identities proves `D=E+(x-10)K`.

Reflection in the actual width preserves coefficient mass. Thus the pair
correction has mass `-18*K(1)`. Since K has nonnegative coefficients, the
uncorrected common-clock pair expression `E+rev(E)` equals the actual next
pair word if and only if K=0. The audit confirms this theorem, including
all-9 blocks, terminal carry creation, and unequal isolated clocks.

## No-overflow rigidity

Suppose gamma=0 and E is symmetric in width L. Q is also symmetric in
width L. Their difference `H=E-Q=(x-10)C` is therefore symmetric in that
width. In particular, `H(10)=0` implies

`H(1/10)=10^(-(L-1))*H(10)=0`.

But `H(1/10)=(1/10-10)*C(1/10)`, and all C_i are nonnegative. Hence C=0.
The isolated remainder condition then gives `q_i<=9` at every column.
Starting with carry zero, no coefficient of Q can generate an actual carry,
so A=C=0, K=0, and D=E=Q. All are symmetric.

Conversely, when every coefficient of Q is at most 9, all whole and isolated
carries are zero for every partition. Thus gamma=0 and E=D=Q is symmetric.

## Overflow rigidity at arbitrary width

Now suppose gamma=1 and E is symmetric in actual width L+1, so
`E_i=E_(L-i)`. Define the reversed isolated carries and their prefix imbalance:

`R_i=C_(L-1-i)`,

`S_i=sum_(0<=j<i)(C_j-R_j)` for 0<=i<=L.

Both endpoints of this integer sequence are zero: S_0=0, and S_L=0 because
reversal preserves the sum of the C_i.

**Coefficient identity.** For every 0<=i<L,

`q_i=10C_i+R_i+9S_i`.  (1)

At i=0, symmetry gives `E_0=E_L`, which is
`q_0-10C_0=C_(L-1)=R_0`. For i>=1, symmetry of E and Q gives

`q_i-q_(i-1)=10C_i-C_(i-1)+R_i-10R_(i-1)`.

Substituting the preceding instance of (1) and
`S_i=S_(i-1)+C_(i-1)-R_(i-1)` proves (1) by induction. This derivation does
not assume that the partition itself is reflection symmetric.

Substitute (1) into the ordinary isolated remainder condition:

`0 <= R_i+9S_i+tau_i <= 9`.  (2)

As R_i and tau_i are bits and S_i is an integer, (2) forces `S_i in {0,1}`.
If S_i=1, then (2) forces R_i=tau_i=0. Equation (1) becomes
`q_i=10C_i+9`; the bound q_i<=18 forces C_i=0. Consequently
`S_(i+1)=S_i+C_i-R_i=1`. Once the value 1 is reached it persists through
the remaining columns, contradicting S_L=0. Therefore all S_i are zero.

The recurrence for S now gives C_i=R_i, and (1) reduces to `q_i=11C_i`.
All coefficients of Q are 0 or 11. Since Q is canonical, its endpoints
are positive, hence equal to 11. If L is odd, canonical center parity
additionally forces the center coefficient to be zero. The L=1 canonical
case therefore cannot satisfy the overflowing symmetry hypothesis.

Every coefficient 0 resets the carry to zero; every coefficient 11 sets it
to one, independently of its incoming bit. Thus actual and isolated carries
agree for every partition: A=C, so K=0. Moreover C is symmetric and

`D=E=11C+(x-10)C=(1+x)C`,

which is symmetric in width L+1. This also proves the converse for every
canonical symmetric word over {0,11} with outer coefficient 11.

## Equivalence with actual palindromicity

The preceding two cases prove that E symmetry forces the stated coefficient
classification and K=0, hence D symmetry. Conversely, apply the same result
to the partition consisting of the single whole block. In that partition
E=D by definition. If D is symmetric, the classification follows, and the
two converse arguments above show E=D is symmetric for **every** partition.

Thus raw E symmetry is independent of the chosen partition on this domain:
it identifies exactly the ordinary palindrome-predecessor class. It cannot
be combined with K!=0 to prove safety at a canonical collision.

## Positive one-step safety from any active seam

For a canonical whole word Q and any chosen partition, K!=0 implies that
D is nonpalindromic. Otherwise the equivalence just proved would force K=0.
This applies to every ordinary realization of Q, since all have the same
first output Q(10).

There is also a direct structural proof. A difference between actual and
isolated outgoing carries can occur only at a coefficient 9: coefficients
at most 8 reset both carries to zero, and coefficients at least 10 reset
both to one. At an active seam column, the actual incoming carry is one.
Since the whole word starts with incoming carry zero, some earlier
coefficient must be at least 10 to have generated that carry. Thus Q
contains both a 9 and a coefficient at least 10. This excludes both exact
palindrome-predecessor classes: all coefficients at most 9, and coefficients
only in {0,11} with outer coefficient 11. Hence its output is nonpalindromic.

For the concrete canonical collision B=(9,9), H=(18), the whole word is
`Q=(9,9,18,9,9)`. The right B block receives carry one, so

`K=x^3+x^4`, `E=(9,9,8,10,9,0)`, `D=(9,9,8,0,0,1)`.

The E list here includes a zero at the actual terminal column. A canonical
ordinary realization is 99900, and its next output is **100899**, visibly
nonpalindromic. The actual next pair word is `(10,9,8,8,9,10)`. No hypothesis
of raw E symmetry is used.

The criterion is sufficient, not necessary. For example,
`Q=(2,2,18,2,2)` has no coefficient 9 and hence K=0 under every partition,
but its canonical realization gives `22900 -> 23822`, also nonpalindromic.
Failure to find an active seam therefore does not establish a palindrome
or exclude another safety proof.

The remaining recurrence obligation is precise: for every future canonical
iterate, regenerate some partition with nonzero K, or provide another valid
safety certificate. The partition may change with the iterate. One active
seam certifies one update only; a recurrent mechanism must establish this
coverage at every update of its claimed invariant domain. No such mechanism
is proved here.

## Finite core certificate and independent controls

`overflow_local_certificate.json` gives the complete arithmetic relation
induced by (1) and the local remainder bound. Since
`9S=q-10C-R`, the bounds q in [0,18], C,R in {0,1} imply
`S in {-1,0,1,2}` before the remainder condition is applied. Enumerating the
608 possible tuples `(S,C,R,tau,q)` leaves exactly nine valid local rows.
Only S=0 and S=1 have outgoing rows. The sole S=1 row is
`C=R=tau=0,q=9`, and it returns to S=1.

The independent checker calculates the states from which a finite path can
end at zero. Only zero qualifies. Exactly four local rows lie on zero-to-zero
paths: C=R=0 or C=R=1, with either tau bit. Their q values are 0 and 11.
This proves the finite arithmetic implication for paths of **arbitrary
length**, not just for enumerated word lengths. The polynomial coefficient
bridge above explains why every overflowing symmetry instance gives such
a zero-to-zero path.

`audit_seam.py` independently replays all 2,737 saved original seam cases,
including 1,767 ordinary canonical controls and 645 nonzero-K cases.
It computes outgoing carries from integer prefix quotients and imports no
original normalization or transducer code. It confirms the universal digit
identity, pair identity, mass law and iff criterion on every recorded case.

The additional complete finite controls include every canonical whole word
of widths one through five and every nonempty consecutive partition of
each word: 3,969 words and 58,221 partitions. All input and response records
are preserved in `short_controls.json.gz`. There are 2,100 nonzero-K cases,
8,122 raw-symmetric cases with gamma=0, and 54 with gamma=1. None has both
raw symmetry and nonzero K.

`check_short_controls.py` independently reconstructs isolated digits using
ordinary decimal conversion and recovers K by exact polynomial division
of D-E by x-10. It checks every archived case, complete coverage, and the
closed-form counts of the two symmetry classes. The unrestricted conclusion
comes from the proof, not from the small-width absence of counterexamples.

`check_positive_safety.py` separately reconstructs the masks from actual
incoming prefix carries and verifies ordinary integer output nonpalindromicity
for every saved canonical nonzero-K case: 395 in the original archive
(91 without overflow and 304 with overflow), and all 2,100 in the exhaustive
short archive. Every one of these 2,495 positive controls is retained in
`positive_safety_controls.json.gz`, together with the explicit BHB example
and the safe K=0 example. These are checks of a sufficient certificate;
the proof itself is unrestricted in word length and block count.

## Why whole-word symmetry matters

The conditional algebraic implication is not vacuous on arbitrary
nonsymmetric coefficient words. Two explicit singleton partitions are
retained in `noncanonical_examples.json`:

| Whole input Q, low-to-high | gamma | Raw E | K support | Actual D |
|---|---:|---|---|---|
| `(11,9,1)` | 0 | `(1,10,1)` | `{1}` | `(1,0,2)` |
| `(11,11,9,0,10,9,12)` | 1 | `(1,2,10,0,0,10,2,1)` | `{2,5}` | `(1,2,0,1,0,0,3,1)` |

In both examples E is symmetric and K is nonzero, while D is nonsymmetric.
Neither Q is a whole mirrored digit-pair word. They demonstrate the precise
scope: the algebraic implication is valid for general block words, but its
antecedent cannot occur on the canonical whole-word domain needed for the
Lychrel collision construction.

## Research history and remaining gap

`source_SEAM_RESPONSE_snapshot.md` preserves the exact audited report before
this result, including the explicitly uninstantiated conditional paragraph.
`source_manifest.json` pins all four source artifact hashes. The live source
report can link this result while retaining that earlier attempt as research
history. No finalized `renewal_pass/language/` report was changed.

The all-block seam correction exactly describes a collision, and nonzero K
is a realizable safety certificate for that update. What is missing is a
proof that the subsequent coupled dynamics regenerate an active seam or
another safety certificate indefinitely. This audit removes an unnecessary
symmetry hypothesis but makes no all-time claim about the remaining `(1,7)`
family or about decimal Lychrel existence.
