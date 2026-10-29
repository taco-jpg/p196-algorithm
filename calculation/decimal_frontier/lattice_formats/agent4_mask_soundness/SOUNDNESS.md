# K1 conservative bitmask DFS: soundness proof

**PAPER PROOF** (finite-horizon exclusion, not existence). For every valid
lattice and a fixed word length/starting phase, each bitmask in
kinkdfs_mask.cpp is a superset of values attained by all concrete
coefficient/carry trajectories with the specified free-digit prefix.

**Initial-state invariant.** Frozen left coefficients are lattice
singletons; every unfixed free coefficient is assigned the entire legal
integer interval 0 through 2b-2; each fixed coefficient is a singleton.
If the word length is odd, the central pairword coefficient is even.
Intersecting its mask with even values removes no legal concrete word.

**Directional carry steps.** For each coefficient x and incoming carry c,
the normalization digit is (x+c) mod b and the outgoing carry is
floor((x+c)/b). The norm routine explicitly unions both outputs over
all elements of its coefficient/carry masks. Thus a concrete digit and
carry are always retained, regardless of spurious independent combinations.
Applying this fact inductively across the ascending then descending
normalization passes proves preservation for both orientations, including
the odd central meeting convention.

**Sum and shift.** The pairSum routine unions x+y for every possible
normalized digit x in the upward domain and digit y in the downward
domain. Every concrete pair is included even if the two masks are
correlated. Orientation and length-overflow phase use exactly the
same source indices as the integer map in check.py. In the frozen
lattice region, rejection occurs only when the required next lattice
coefficient is absent from the superset of possible sums. Therefore
no legal concrete continuation is rejected. Introducing leftmost
lattice cells without testing their reachability only enlarges the
abstract set, never shrinks it. Odd-centre parity is a necessary
condition, so the second intersection also preserves all legal words.

**Induction and conclusion.** Repeat the argument H times. Every exact
length-H continuation respecting the lattice remains represented by
feasible(prefix). DFS exhausts all full free-digit vectors by disjoint
prefix enumeration. If every full vector is rejected, there is no
exact length-H continuation. A periodic centre with *any* positive
time period would provide H steps, hence is also excluded.
A positive DFS leaf is only an abstract survivor, not necessarily
a concrete continuation. This is not a proof about unsearched widths,
unverified lattice models, or the base-10 Lychrel problem.

**Finite representation.** The supplied b=10/b=26 input formats have
binary carries, binary growth indicators and pairword coefficients
in 0..2b-2. Normalized digit sums are <=2b-2<=50, safely inside
the 64-bit mask; K=w+10 is checked below the compiled bound.
Malformed inputs and source modifications are outside this theorem.

**Reproduction.** From the repository root execute:
python3 calculation/decimal_frontier/lattice_formats/agent4_mask_soundness/check.py
This independent Python checker uses only scalar integer carries,
cross-checks 720 concrete complete-digit assignments, 24 fully
enumerated small input spaces, six prefix-splitting identities,
and the known base-26 positive centre control (4,2).
The concrete finite checks are regression tests, not the proof itself.
