# Full semantic acceptance, finite repair, and exact inverse scope

## Definitions

A canonical folded word is a finite list p of outer-to-inner mirrored digit
sums, each in {0,...,18}, together with an absent center or an even center
c in {0,2,...,18}. If p is nonempty then its first entry is positive. The
one-digit case is an empty p and positive c. Its width is `2|p|` without a
center and `2|p|+1` with one. Write C for these words.

Every word has an ordinary positive-integer realization: use high-side
digits `min(p_i,9)`, low-side digits `max(p_i-9,0)`, and center c/2 when
present. Let T(n)=n+reverse(n). Every realization of the same folded word
has the same T(n), because evaluating its full symmetric coefficient word
at 10 gives exactly that sum. Thus the folded image G:C->C is deterministic,
and positive palindrome first-hit times are independent of realization.

Let B consist of words whose first positive ordinary output is a palindrome.
A word is safe when it is outside B. Set S0=C and
`S_(j+1)=G(S_j minus B)`. In particular, a two-edge ancestry with both
predecessors safe proves membership in S2. Our candidate is

`F10 = S2 intersect {w : T^j(n) is nonpalindromic for j=1,...,11}`,

where n is any realization of w. Equivalently, the eleven bits recording
`B(w),B(Gw),...,B(G^10w)` are all zero. The index 10 refers to observation
depth, not to ten additions.

## A sound adaptive acceptance interface

Let M be any mode set. For each m in M specify a language L_m contained in
C. A valid certificate needs the following three properties.

1. **Nonemptiness:** there exist m0 and a concrete canonical word w0 in L_m0.
2. **Universal safety:** for every m and every w in L_m, w is outside B.
3. **Universal successor coverage:** for every m and every w in L_m, there
   exists m' in M such that G(w) belongs to L_m'.

The next mode may depend arbitrarily on m and the complete word w. A
certificate may use a relation of allowed mode transitions or a symbolic
partition to supply this existential witness, but its coverage obligation
is universal over **all** accepted words and modes. Providing one selected
trajectory, or one word per accepted class, does not discharge it.

Put `L = union_m L_m`. Properties 2 and 3 imply `L subset C minus B` and
`G(L) subset L`; property 1 makes L nonempty. Induction gives a word in L
at every future iterate, and property 2 makes every positive ordinary output
nonpalindromic. This is the desired implication to a decimal Lychrel witness.
It is a conditional interface; this pass supplies no satisfying instance.
If the definition of a Lychrel witness includes time zero, use the first
ordinary output as the witness: it is nonpalindromic by property 2, and
all of its later iterates are covered by the same argument.

### Projection theorem for common configuration classes

Fix an equivalence relation ~ on C. Assume each L_m is saturated under ~:
if w~v and w belongs to L_m, then v belongs to L_m. Then the projected L
is also saturated, since a witnessing mode for w is also a witnessing mode
for every equivalent v. Hence any universally safe, universally covered
adaptive controller of this form yields an ordinary safe forward-closed
union of the same equivalence classes. Finiteness of M is unnecessary.

In the configuration models studied here, a complete class includes the
entire reachable subset of the exact 6,680-state S2 NFA, the exact observer
residual, center, canonical status, and current acceptance mask. The mask
is determined by the subset and center but must not be silently dropped
when specifying the class. Boolean conjunctions, disjunctions, or switching
among acceptance predicates of this fixed tuple remain saturated.

If one such class contains a representative v whose first positive
palindrome occurs at time h, no safe closed saturated L can contain it.
Indeed v would be in L, closure would put G^(h-1)(v) in L, and that word is
in B, contradicting safety. Therefore the earlier 146 independently checked
complete-class collisions remain exclusions even for arbitrary adaptive
mode switching over their respective fixed partitions. This does not merge
different depth partitions into one theorem, exclude all classes, prove that
196 terminates, or forbid an invariant entered at a later 196 iterate.

An acceptance rule using an actually finer equivalence, an unsaturated
subclass, or a verified constraint on complete histories lies outside this
projection argument. Such a rule still has to satisfy all three universal
interface obligations. Relabeling modes alone supplies no new word semantics.

## An infinite family defeating every finite repair of F10

For r>=5 define

```
A_r = (2,12,4,4,9^(r-5),14,16,16,15), no center
B_r = (5,4,9^(r-2),14,14,12), no center
C_r = (10,9^r,10,6), no center
Q_r = (1,1,0^(r-1),1,7), center 12.
```

All are canonical. The checked identities are
`G(A_r)=B_r`, `G(B_r)=C_r`, and `G(C_r)=Q_r`.
The separate all-r tail theorem proves that every realization of Q_r first
reaches a palindrome at addition 11. An actual palindrome has even mirrored
digit sums at every position. B_r has odd outer pair 5, C_r contains an
odd pair 9, and Q_r has odd outer pair 1. Thus the first output at each of
the three preceding edges is nonpalindromic. Their first-hit times are
exactly 14,13,12, respectively. This reasoning concerns every realization,
not only the displayed canonical representative.

In particular A_r and B_r are safe, whence C_r is in S2. Its first eleven
positive outputs are nonpalindromes, so C_r is in F10. Its image Q_r has its
eleventh output palindromic, so Q_r is not in F10. Both C_r and Q_r are in
S2: the latter follows from the safe two-edge path B_r->C_r->Q_r.

**Finite symmetric-difference theorem.** Let H be any language such that
the symmetric difference E between H and F10 is finite. Choose W as the
maximum width of a word in E, or zero when E is empty, and let
`r >= max(5,W+1)`. The widths of C_r and Q_r are 2r+6 and 2r+7, respectively,
so neither is in E. Thus C_r is in H but G(C_r)=Q_r is outside H. Therefore
H is not forward closed. This proof allows arbitrary finite additions as
well as deletions, and gives a constructive new witness after every finite
repair. Any safe closed sublanguage of F10 must in particular delete all
infinitely many C_r.

This does not forbid an infinite semantic refinement of F10 or establish
that its maximal safe closed sublanguage is empty.

### The unrestricted polynomial certificate

For a full symmetric coefficient polynomial Q(x), normalize with low-to-high
outgoing carry polynomial C(x). Each carry is 0 or 1. The actual digit
polynomial is `D=Q+(x-10)C`; if input width is L and final carry is h, output
width is W=L+h and `G(Q)=D+rev_W(D)`.

The certificate uses constant-valued runs of lengths `a*k+b`, with a>=0,
b>=1, for k>=0. Multiplication by x-1 replaces each run by two sparse affine
endpoints. The independent checker verifies the polynomial identities as
formal affine-exponent identities. A coefficient <=8 kills carry, 9 passes
it, and >=10 sets it. The outgoing carry after the first column of a run
therefore persists throughout that run. All digit remainders and widths
are checked. These facts prove every parameter instance without extrapolation.

The ladder uses r=6+k and verifies r=5 separately. Its checker also replays
the complete first-hit-eleven tail certificate, including every nonzero
preterminal digit-reflection difference and the terminal zero difference.
The tail certificate's SHA256 is pinned. Integer controls audit the formulas;
the unrestricted assertion follows from the polynomial identities and
positive run lengths.

## A reusable prefix obstruction at every finite width

Use an outside-in carry state `(h,a,b,t)`: overflow h, low incoming carry a,
high outgoing carry b, and (when h=1) the delayed high digit t. Initially
`(0,0,0,-1)` or `(1,0,1,1)`. For source pair q choose an inner high carry
`b' in {0,1}` satisfying `0 <= q+b'-10b <= 9`. The low and high output
digits are

`ell=q+a-10a'`, with `a'=floor((q+a)/10)`, and `u=q+b'-10b`.

Without overflow the emitted folded pair is ell+u. With overflow it is
ell+t and the next delayed high digit is u. These are ordinary decimal
column equations, with both high-carry alternatives retained until the
center resolves them.

### No image begins with (1,6,2)

First output pair 1 is impossible without overflow: the only candidate
source pair zero is noncanonical. In the overflowing branch it forces the
source outer pair to be 10. To emit the second pair 6, there are precisely
four surviving local states:

| Source first two pairs | Low carry | High carry | Delayed high digit |
|---|---:|---:|---:|
| (10,5) | 0 | 0 | 5 |
| (10,5) | 0 | 1 | 6 |
| (10,14) | 1 | 0 | 4 |
| (10,14) | 1 | 1 | 5 |

The next ordinary emitted pair is a nonnegative decimal digit plus the
delayed digit, hence at least 4. It cannot equal 2.

There is one width case to cover. An output with three folded pairs has
width at least six, so its input has width at least five and at least two
folded pairs. The first two emitted pairs are therefore ordinary pair
edges. If there is no third input pair, the input has five digits, is odd,
and overflows to six digits. The output's third pair is the center digit
remainder plus t, again at least 4. The finite certificate lists all 20
valid center cases. Even-input termination emits a center rather than a
third pair and cannot supply an exception. This proves the claim for
arbitrary tails and all widths admitting that prefix.

### Prefix (2,12,4) has no two-step ancestor

If the first emitted pair is 2 in the overflowing branch, the source outer
pair is 11 and its retained high digit is 1 or 2. Therefore the second
emitted pair is at most 9+2=11 and cannot be 12.

In the no-overflow branch, first pair 2 forces source pair 1 and inward
high carry zero. Second pair 12 then forces source pair 6 and again inward
carry zero. No-overflow termination emits no extra pair; an output with
three pairs therefore has at least three input pairs. Third pair 4 forces
source pair 2. Thus every predecessor of the entire `(2,12,4)` cylinder
belongs to the `(1,6,2)` cylinder, which has no predecessor. In symbols,

`G^(-2)({w in C : p(w) starts (2,12,4)}) = empty`.

The certificate checker exhausts the complete local frontiers and center
cases. The separately audited Lean theorem proves a stronger full-column
statement, including a center at width five, and transfers it to ordinary
integer orbits. The two presentations agree on the folded cylinders used
here.

### Consequence and its exact limit

For r>=6 put
`D_r=(1,6,2,2,4,9^(r-6),17,7,18,7)`, no center. A separate symbolic identity
proves `G(D_r)=A_r` for r>=7, and the r=6 boundary is checked directly.
A_r contains an odd pair 15, so this output is nonpalindromic; every
realization of D_r has first positive palindrome time 15. Since every A_r
begins `(2,12,4)`, none has a two-step predecessor. D_r proves that its
maximum backward depth is exactly one for r>=6. A_5 has no predecessor by
complete finite inverse enumeration. In particular this chosen construction
cannot be repeated to produce arbitrarily long safe delays.

The theorem concerns all inverse branches **above the A cylinder**, not all
branches above Q_r. Complete finite inverse exploration explicitly refutes
the stronger forcing claim: `994999060500005`, whose prefix is `(14,9,4)`,
maps in three steps to a realization of Q_5 and first reaches a palindrome
at step 14. Its intermediate folded words and full integer orbit are saved
in `outside_A_cylinder_witness.json`. Other branches persist at depth six
in every tested r=5,...,8. No general backward-depth bound or parameter-
consuming recurrence for those branches was obtained.

## Exact finite archives and remaining obligation

`exploration_archive.json.gz` retains every extended gate orbit, every
single-symbol insertion probe, all selected A predecessors and their empty
second predecessor sets for r=5,...,12, the Q/C predecessor probes, and all
safe Q inverse trees at r=5,...,8 through depth six. Its checker imports no
discovery or transducer module. It reconstructs full NFA subsets, raw
observer signatures, local inverse graphs including terminal cases, and
ordinary arithmetic independently. The same checker exhausts the saved
342-entry unary-prefix pump catalog from `pump_search_result.json.gz`.

These finite catalog failures are scoped to their explicit grammar and
bounds. In particular a missing terminating representative is not a proof
of universal safety or closure. The preserved finite UNKNOWN trajectories
are not candidate certificates. To finish the existence goal one still
needs an actual nonempty semantic language satisfying universal safety and
successor coverage, possibly after an infinite refinement not excluded by
the theorems above. The machine-readable interface is marked
`NOT_INSTANTIATED`; no positive proof is claimed.
