# Absorbing interiors, shrinking run ancestry, and new births

This note follows the frozen two-neutral-band quotient in
`../METHOD_AND_PROOF.md`. It gives exact boundary propagation for homogeneous
coefficient 0 and 18 runs under arbitrary actual overflow clocks. It does not
prove that such coefficients eventually disappear from a whole orbit: new
runs can be born elsewhere, and a safety witness may switch ancestry.

All words are low-to-high canonical decimal pair words. Let `G` be their
ordinary reverse-add pair update. For an input word of width `L`, let `a_i`
be the forward incoming carry at position `i`, and let `beta_(i+1)` be its
backward incoming carry. Put `gamma=a_L`, the actual overflow bit.
As before, normalized directional digits are

`r_i=q_i+a_i-10a_(i+1)`,

`u_i=q_i+beta_(i+1)-10beta_i`.

When `gamma=0`, `G(q)_i=r_i+u_i`. When `gamma=1`, interior output positions
have `G(q)_i=r_i+u_(i-1)`. The output endpoints use the actual terminal
digit 1. These are full canonical-word identities, not fixed-width padding.

## 1. A same-symbol interior survives a controlled trimming

Fix `c` in `{0,18}` and put `h=c/18`, so `h` is its reset carry.
Suppose `q[a:b]` is a run of `c` of length `ell=b-a`.

On a no-overflow update, every output position in `[a+1,b-1)` is `c`.
This assertion is useful for `ell>=3`; it gives an empty interior for
`ell=1` or 2. On an overflow update, every output position in `[a+1,b)`
is `c`; it is nonempty for `ell>=2`.

Indeed, a 0 resets both directional carries to 0, while an 18 resets both
to 1. A column with both neighbors inside the run therefore has two digits
equal to 0 or 9, respectively. During overflow, two adjacent old run columns
already suffice: both shared carries are fixed, and their paired digits
again sum to `c`.

It follows by induction that after any finite sequence containing `N`
no-overflows and `O` overflows, a known constant run of initial length `ell`
retains a same-symbol interior of length at least

`max(ell-2N-O,0)`.

The statement is a guaranteed interior, not a claim that the surrounding
maximal run has exactly that length. Whenever the lower bound is positive,
the inductive trimming intervals are valid and stay within the actual output
word. Both kinds of update move the low endpoint of this conservative core
right by one; the high endpoint moves left by one only at no-overflow steps.

Consequently a fixed finite return, with interface widths bounded independently
of an unbounded parameter `ell`, cannot change a macroscopic homogeneous
0 or 18 region completely into a 9 region. For sufficiently large `ell`, a
constant interior survives that return. This does not exclude regeneration
after a time proportional to the gap, moving fronts that traverse the gap,
or a new large 9 band at a different location.

## 2. Sharp maximal-run ancestry: no expansion or merging

Now require `[a,b)` to be a **maximal** run of `c`. Its natural descendant is
the same-symbol core obtained from these positions under the update.
Let `alpha=a_a` and `beta=beta_b` be the two exterior incoming carry bits.

**No overflow, `ell>=2`.** The left endpoint survives exactly when
`alpha=h`, and the right endpoint survives exactly when `beta=h`. All
interior columns survive. Thus the descendant interval is

`[a+[alpha!=h], b-[beta!=h])`,

unless this interval is empty. Its length is

`ell-[alpha!=h]-[beta!=h]`.

A lost endpoint is 1 when `c=0`, and 17 when `c=18`, so it separates the
surviving core from any newly born equal coefficient outside it.

**No overflow, `ell=1`.** The one output value is `alpha+beta` for `c=0`,
and `16+alpha+beta` for `c=18`. The singleton survives exactly when both
bits equal `h`. Otherwise it disappears; the lost value can be 1 or 2,
or 16 or 17, respectively. Applying the two-endpoint length formula to a
singleton would double-count the same column and is therefore invalid.

**Overflow.** The descendant interval is exactly `[a+1,b)`, of length
`ell-1`. For a singleton it is empty. When nonempty, its immediate output
neighbors are not `c`; hence it is a maximal output run and cannot merge
with a newly born run beyond its old boundary.

These statements include a run of 18 touching either whole-word endpoint
or occupying the entire word. A canonical 0 run is always internal.
No-overflow 18 runs are internal because outside coefficient 18 would
itself force overflow. At an overflowing 18 endpoint, the new endpoint
coefficient is `8+1=9`, providing the required non-18 boundary.

**Proof of the no-merging assertion.** At no overflow, a lost endpoint is
already a non-`c` barrier. Suppose instead that the left endpoint survives.
The immediately preceding old coefficient `z` is not `c` and sends carry
`h` into the run. If `c=0`, then `z` is in `1,...,8`, or is 9 carrying 0;
its output is positive. If `c=18`, then `z` is in `10,...,17`, or is 9
carrying 1; its output is at most 16. So that neighboring output is not
`c`. Reflection gives the right side. The same argument applies to a
surviving singleton.

At overflow, a non-9 adjacent pair has output
`f(x)+f(y)`, where `f(z)=z-9*[z>=10]`. For a pair with one entry `c` and
the other entry neither `c` nor 9, this sum differs from `c`: for `c=0`
it is positive; for `c=18` it is at most 17. If the neighboring coefficient
is 9, the new boundary value is `9+epsilon` when `c=0`, or `8+epsilon`
when `c=18`, with `epsilon` a carry bit. Neither equals `c`. Whole-word
endpoints were checked above. This proves exact maximality. ∎

In particular, while an old run has a nonempty descendant, its length obeys

`ell_next <= ell-gamma`.

No choice of partition and no changing interface can make this ancestry
expand. A run of original length `ell` is extinct by the `ell`-th overflow.
Every five consecutive ordinary updates contain an overflow: otherwise the
positive outside pair coefficient would double at least five times, although
each non-overflow input requires it to be at most 9. Therefore this ancestry
is extinct within `5*ell` updates. This is a bound on one ancestry, not on
palindrome attainment or on the presence of all 0/18 runs in an orbit.

## 3. An exact central-18 quotient is always eroding

The central-18 erosion result in this section recovers the prior result in
the project-root `novel_projective_notes.md`, under “Why a permanently
protected 18-core does not work.” It is included here as a corollary and
is not claimed as a new obstruction. The extension in the present note
is the sharp ancestry law for arbitrary maximal 0/18 runs, including
singletons, endpoint cases, and the proof that a surviving old run cannot
merge with new births.

As a special case, let

`Q=B,18^g,reverse(B)`,

where `B` is empty or ends in a coefficient different from 18, and the whole
word is canonical. The run `18^g` is its maximal central 18 run. Let `e`
be the outgoing carry from `B` normalized with incoming 0.
Symmetry makes both exterior bits at the central run equal to `e`.

For `g>=2`, its exact next central-run length is

| Actual clock | Boundary bit | New central-run length |
|---|---:|---:|
| No overflow | `e=1` | `g` |
| No overflow | `e=0` | `g-2` |
| Overflow | Either | `g-1` |

The raw exterior can be computed independently of `g`, so this is an exact
interface quotient. However, trimming the new exterior cannot add any 18
back into the central run: the preceding no-merging proof excludes that
possibility for arbitrary exterior width and content. For `g=1`, only a
no-overflow step with `e=1` preserves the singleton; every other case removes
the central 18 run. Thus there is no expanding return that follows one
maximal central 18 band, under any overflow schedule or exterior blocks.

The corresponding statement for a maximal central 0 run interchanges the
roles of `e=0` and `e=1` on no-overflow steps. Its exterior is necessarily
nonempty, because the whole canonical word has positive endpoints.

## 4. Births permit a safety witness to change ancestry

The preceding obstruction does not justify tracking only one old run forever.
At a no-overflow update, let `s=a_i+beta_(i+1)`. Direct carry arithmetic gives

`G(q)_i=18`

if and only if either `q_i` is 8 or 18 and `s=2`, or `q_i=9` and `s=0`.
Likewise,

`G(q)_i=0`

if and only if either `q_i` is 0 or 10 and `s=0`, or `q_i=9` and `s=2`.

These are unrestricted one-column equivalences. In particular, an old 8
between two incoming carry-1 regions can create a new 18, while a mixed
9 region remains 9 and a low-low 9 region becomes 18.

For every `g>=2`, the exact no-overflow identity

`(1,10,8),18^g,(8,10,1)`

`   -> (3,0,18,17),18^(g-2),(17,18,0,3)`

exhibits this distinction. The old central 18 run loses two columns, but
two new singleton 18 runs appear outside the 17 barriers. The total number
of 18 coefficients is unchanged on that step. Thus a future safety induction
could in principle switch from an old 18 witness to a newly created one.
No rule guaranteeing such a switch indefinitely is proved here.

This complements the mixed-symbol safety and active-seam certificates without
requiring every state to contain a 9. A coefficient 18 itself rules out both
immediate-palindrome-predecessor classes. What remains missing is a closed
mechanism that regenerates some valid witness after each erosion phase.

## Verification

`check_absorbing_core.py` independently evaluates each input coefficient word
as an integer, obtains its normalized decimal digits, and constructs the next
pair word from those digits. It checks all canonical whole words of widths
1 through 7, every maximal 0/18 run in them, the exact descendant positions
and no-merging conditions, both no-overflow birth equivalences, and the
parametric birth example at several lengths. Full run records and hashes
are retained in `absorbing_core_controls.json.gz` and `absorbing_core_results.json`.
The unrestricted result is the proof above, not the finite census.

The provisional birth example had outside coefficient 2 instead of 3.
The first complete integer audit rejected it, and the root review supplied
the same correction independently: the outside input coefficient 1 receives
backward carry 1 from the adjacent 10, so its pair output is `2*1+1=3`.
The corrected family above is the one checked and retained in the archive.
