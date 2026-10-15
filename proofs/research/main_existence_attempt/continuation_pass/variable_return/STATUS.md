# Variable returns, a positive regeneration gate, and exact reset limits

**Decimal Lychrel existence and the assertion for 196 remain unproved.**
This checkpoint contains a genuine all-parameter safe regeneration gate,
its originating family, an exact failed return, two universal reductions,
an all-spacer reset exclusion, and separately labeled finite experiments.
No indefinitely repeatable safe return has been instantiated.

## Positive construction

For every g>=0, put

    B=(1,9,12,3,14,14), H=(4,4,15,10,15,4,4),
    C=(3,9,4,8),       J=(11,2,11).

The exact actual no-overflow identity is

    G(B 9^g H 9^g reverse(B))
       = C 9^(g+4) J 9^(g+4) reverse(C).

Both ordinary positive outputs through the next two steps are safe.
The identity is valid at g=0, where two length-four neutral bands are
created. It comes from explicit carry streams: the raw outer paired block
ends in two 9s, and the raw middle block starts and ends in two 9s. This
primitive retains mixed incoming carries after the +4 growth.

The smaller originating family has exterior (18,18,4), middle
(14,0,0,14), and two 9^R bands, R>=3. Three overflowing steps reach the
gate at g=R-3. Thus four updates create a safe larger-gap state with gap
R+1, but with different exterior and middle blocks. The complete exact
nine-step trace is in `POSITIVE_REGENERATION_GATE.md`.

At time nine the outer coefficient returns to 18 and the width matches
the originating family at R+2. Its actual exterior is (18,7,9,0,2),
its middle is (2,16,16,2), and its bands are 0^R. The proposed returned
exterior would start (18,18,4). The second-coefficient mismatch 7 versus
18 excludes that return uniformly for every R>=3. This is a concrete
failure after real regeneration, not an inference from missing finite
samples.

All nine positive ordinary outputs are safe for every R>=3. The generator
records ten affine states and nine transitions for R=4+k, k>=0. The
separate sparse-polynomial checker verifies every transition, actual
overflow, and safety test, without importing the run normalizer. It also
replays 315 ordinary transitions, including the R=3 minimum boundary.
This bundle's gate proof is written and exact-arithmetic verified; the
sibling formal stream owns any further Lean formalization.

## Universal reductions

`VARIABLE_RETURN_THEOREMS.md` proves two statements.

1. A fixed finite affine-run family Q_k with an additive parameter update
   k->k+s cannot gain a new tail construction merely by allowing variable
   return times. Its width slope A gives 1<=tau(k)<=4As. Every fixed-time
   image is eventually affine; equality with the target is eventually an
   identity or holds at at most one parameter. Consequently a safe variable-
   time return covering every large k contains one safe fixed-time return
   on an entire tail. This conclusion handles isolated palindromic
   parameters explicitly. It does not cover multiplicative updates or
   unbounded run catalogues.
2. Any actual ordinary pair word beginning (p,0,0,0), p>0, occurs only at
   times t<=4. An overflowing step cannot produce three such zero columns;
   a nonoverflow predecessor must begin (p/2,0,0,0). Backward iteration
   forces p>=2^t, while p<=18. Thus even multiplicative parameter updates
   cannot make a single-coefficient zero exterior recur indefinitely.

The second theorem is sharp: the ordinary seed 10^4 reaches prefix
(16,0,0,0) at time four. Two zeros do not suffice: 9990010 goes to
10091009, whose pair word starts (10,0,0), with overflow. The independent
controls cover all 246,924 four-column/interior-carry cases and every
canonical word of widths one through eight, another 198,909 transitions.
This includes overlapping windows and minimum predecessor width four.
All outcomes are retained in binary gzip streams with documented layouts.

The sibling `../lean/zero_exterior/` now formally verifies the full
three-zero theorem, its actual-ordinary-orbit bridge, the fixed-outer
nonreturn result, and both sharp examples. Its own status and axiom audit
give the formal scope. The preliminary prose error about minimum width
(seven instead of five) is corrected and retained in `ATTEMPTS.json`.

## An exact all-r, all-time reset exclusion for the enlarged gate catalogue

Let the 20 core pairs be

    1<=u<=3, 5<=v<=7, u+v<=8;
    5<=u<=8, v in {5,6}, u+v<=13;
    10<=u<=13, v in {5,6}, u+v<=18.

For p=1..9 and r>=1 define the 180 canonical templates

    Q(p,u,v,r) =
      (p,p) 0^(r-1) (u,u+v,2v,u+v,u) 0^(r-1) (p,p).

**Complete result in this stated catalogue:** for all source and target
triples in the catalogue, every r>=1, and every positive integer t,

    G^t(Q(p,u,v,r)) != Q(p',u',v',r+1).

No overflow schedule is prescribed. Any equality would add exactly two
decimal columns. The exact outer-width potential bounds t by 12, so
checking times 1..12 is an all-positive-time exclusion for this target.
The affine domain r=40+k, k>=0, supplies 2,160 symbolic transitions.
The separate checker verifies all of them as sparse polynomial identities
and checks all 388,800 source-time-target comparisons. In 388,798 cases
the positive canonical RLE symbol sequences differ. The two remaining
cases are the familiar time-two returns (1,1,6)->(4,5,5) and
(2,1,6)->(8,5,5), but they preserve the old spacer; their zero runs are
one column too short for r+1. This gives a uniform nonzero difference.

Every r=1..39 is checked by literal integer reversal and addition, with
four further large-parameter audit values per source. The 92,880 integer
transitions and all 7,740 complete integer trajectories are retained and
independently replayed. No structural-RLE inequality is silently used
when affine lengths might coincide at an isolated parameter: the checker
solves the full affine equality system.

This theorem excludes exactly the r+1 reset in this finite interface
catalogue. It does not exclude other cores, other parameter changes, or
every possible later return of an overlap word.

## Separate finite multiplicative-target experiment

For all 180 source templates, r=3..32, and all 180 target templates, the
three target spacers 2r-1, 2r, and 2r+1 were tested by ordinary integer
arithmetic. Each orbit was continued through any palindrome until its
width exceeded every target width. Width never decreases, so this is a
complete equality test for those finite target sets; no arbitrary time
cutoff was used.

The 5,400 inputs required 493,927 additions and produced zero target
matches. The archive retains every input, first palindrome if any,
overflow clock, final value, trajectory hash, and result. **This is not
an all-r exclusion and does not prove infinite safety.**

## Complete broader 4/14 mixed-band graph

The positive search then used the seam stream's exact block quotient for
W(B,H,g)=B9^gH9^g reverse(B), with both 9 bands carrying opposite incoming
bits. All 22,382 initial interfaces were included:

* B has width 1, 2, or 3, positive first coefficient, and last coefficient
  4 or 14; all other coefficients range over 0..18.
* H is symmetric, has width 1..4, starts with 18-last(B), and has an even
  middle coefficient at odd width; remaining coefficients are unrestricted.

The complete reachable graph has 83,679 states and 69,057 surviving edges.
All seed paths end in either lost mixed carries (21,309 seeds) or merged
bands (1,073 seeds), within 50 updates. No configured state, time, path,
or interface-width cap was reached. Actual reached outer/middle widths
are at most 25 and 24. Initial g>=23 keeps every tracked gap at least two
through every recorded path, including its final transition.

The graph does contain real regeneration: 8,097 surviving edges increase
the gap, and the largest such increase is four, realized by the isolated
positive gate above. Thus the negative cycle result is not caused by
forbidding regeneration or choosing a fixed clock.

`check_regeneration_graph.py` independently recomputes every block
transition, replays 167,358 ordinary integer transitions, reconstructs
every seed path, and checks a descending rank at every state. The maximum
rank is 50. All graph outcomes, paths, terminal states, and all 83,679
ranks are retained. The block algebra supplies all-gap validity; sampled
integer controls are not used to extrapolate that conclusion. This graph
and its ranks are not Lean proofs.

The result excludes indefinite persistence of the stated two mixed
neutral bands from these initial interfaces while the quotient applies.
It does not equate lost mixedness with a palindrome, and it does not
exclude later new bands after a collision.

## Remaining positive obligation and retained attempts

Allowing the two long bands to become 0 or 18 and then asking for a
fixed-time neutral return was considered but not searched redundantly:
the seam stream's absorbing-bulk theorem shows that a long 0 or 18 band
retains a same-symbol core of length at least ell-2N-O through N
nonoverflow and O overflow updates, while the stated core survives.
Its precise statement, sharp maximal-run ancestry rule, and birth
exceptions are in
`../seam_persistence/followup_absorbing_core/ABSORBING_CORE.md`.
Recovering an entire unbounded neutral band through front propagation
therefore requires return times growing with its length. That requires
unbounded width increments, and exact matching of the rebuilt interfaces,
not just a shared boundary coefficient or a larger gap.

No such gap-dependent front traversal, safe parameter reset, or invariant
using regenerated reservoirs is instantiated in this checkpoint. The
finite positive gate, its exact loss, the all-r reset exclusion, and the
finite multiplicative experiment have deliberately separate scopes.
All source, certificates, controls, rejected outcomes, configured caps,
and the corrected editorial mistake are retained. No novelty or external
peer-review claim is made.

## Reproduction

From the project root, run these commands separately:

    python -B main_existence_attempt/continuation_pass/variable_return/zero_exterior_check.py
    python -B main_existence_attempt/continuation_pass/variable_return/variable_return_probe.py
    python -B main_existence_attempt/continuation_pass/variable_return/check_affine_catalogue.py
    python -B main_existence_attempt/continuation_pass/variable_return/regeneration_interface_probe.py
    python -B main_existence_attempt/continuation_pass/variable_return/check_regeneration_graph.py
    python -B main_existence_attempt/continuation_pass/variable_return/regeneration_gate.py
    python -B main_existence_attempt/continuation_pass/variable_return/check_regeneration_gate.py

The exact interface probe imports the sibling seam quotient and records
its source hash. The affine generator imports the preserved
`smart_pass/collision/orthant_runs.py`. Independent checkers import neither
generator nor run normalizer. Binary and JSON archives include hashes and
decoding information in their adjacent result files. Compiled bytecode
and scratch executables are not research evidence.
