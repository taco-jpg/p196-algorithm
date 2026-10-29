# X25: mixed-clock packet collision and candidate sheared certificate format

## Scope and construction
**COMPUTED**, finite base-10 statement only. The standalone p8/m20 exterior has temporal overflow clock 10101010 (mean 1/2), but the p12/m9 lattice has mean 1/4. A single ordinary decimal orbit has only one global overflow sequence, so treating both lattice interiors as autonomous at once would be unsound. The new experiment instead transplants only p12's finite *packet symbols* into a rooted p8/m20 carrier and drives them under the actual p8 clock.

Work with least-significant-first symmetric pair coefficients 0..18. Initial P=B ++ W^q ++ (8,0,0,16,0,0,8) ++ reverse(B ++ W^q), using N01's corrected B (39 coefficients) and W (20 coefficients), and N18's seven-cell core. Let species A=(6,1,0,1,11,14,10,6,11,16,1) and D=(16,0,9,11,1,10,8,5,14,18,0), formerly N21's p12 symbols A/B. Modify both mirrored eleven-coefficient positions at x=960 and y=x+180k. Track the reference, four single placements, and both orders AD and DA (seven actual coefficient orbits). P is realized by an actual positive canonical integer via digit-pair splitting.

## Measured scattering law and its limit
The nonlinear correction is J=P_AD-P_A-P_D+P_0 (with matching lengths); a daughter is a position where the double perturbation differs from the reference but both corresponding single perturbations are unchanged. C++ full-word decimal normalization/re-pairing found, for every tested k=1,...,8 with q=220, exactly two lower-half first nonlinear coefficients, located at:
- AD (t,j)=(198k-4,135k+962);
- DA (t,j)=(198k-1,135k+964).
The first daughter sites are not so simply time-affine: at k=2, AD=(407,1231), DA=(398,1232); at k=4, AD=(803,1501), DA=(794,1502). Across the eight k, DA's daughter first appears 3 steps after nonlinear contact. AD's latency is 29 for k=1, 32 for k=3,5,7, and 15 for k=2,4,6,8. This is an exact finite *observation*, not proof for k>8 or an infinite packet cycle.

An independently written ordinary Python big-integer oracle uses N+int(str(N)[::-1]) on all seven q=140,k=2 seeds for every t=0..1000, verifies nonpalindromicity of all seven at every time, the global p8 alternating overflow (initial 5685, final 6185 digits), common 39-column exterior, and 8-phase recurrence in three separate undisturbed windows. It recovers both interaction onsets and both daughter onsets from the integer's entire actual decimal pairword. The C++ eight-gap table is not an eight-gap bigint replay, and the nonlinear wake grows afterward.

## Candidate format: exact sheared carry-port tiles (conditional PAPER argument)
A tile is a *finite spacetime array* of pair coefficients P(t,i), low/right carry ports, and next-row partner digit pairs. Each cell enforces d(t,i)=(P(t,i)+c(t,i)) mod b, c(t,i+1)=floor((P(t,i)+c(t,i))/b), and next P(t+1,i)=d(t,i)+d(t,n+gamma-1-i) including the reflected partner and actual terminal overflow gamma. Ports for both reflected halves are included. Tiles can be glued only when spatial boundary coefficients and *both* carry ports agree, their reflected partner offsets agree, their temporal phases (environment clock mod 8; packet register mod 12) agree, and the actual global overflow is unchanged. Allow a fixed spatial shear s and temporal shear tau in a repeatable tile. Packet species may change in nonlinear collision tiles; *no additive superposition* is assumed at a collision.

**Soundness statement:** Suppose a finite set of tile types covers all active coefficients and their reflected partners in each row, the low-to-high carry chain begins at c=0, the outermost tile verifies the actual overflow, every shared port agrees, all tile concatenations cover the whole genuine digit word, and the final row of every edge is the stated next pairword. Then any compatible finite spacetime tiling equals ordinary base-b reverse-and-add at each covered step. Proof: the deterministic carry recurrence forces the normalized digit word, tile by tile, from the outer low endpoint; reflected partner equations then force the complete next pairword. If repeated space-time tiles have a finite carry-port semigroup whose *entire* power orbit is checked (not just a few repetitions), they can certify infinitely many gap parameters. If those certified tiles close a regenerative finite macrocycle with a nonpalindrome witness on every intermediate row, and nondecreasing or invariant nonnegative gap parameters, induction on macrocycles yields a genuine infinite certificate. A Lean path is digit normalization uniqueness, a two-ended seam-gluing lemma, semigroup pumping, then cyclic invariant induction. None has been Lean-checked here.

The empirical candidate shear is (spatial gap, temporal collision)=(180,198), with first-contact coordinate increment 135. What is MISSING is an exact 198-row tile whose boundary port relation repeats when an extra 180-column gap is inserted, plus a *wake-erasing* nonlinear output and a regenerative return. Therefore this format is a precise conditional construction mechanism, not a decimal instance of an infinite cycle. It extends N21's disjoint carry firewalls by allowing mixed environmental/internal clocks and nonlinear species-changing collision tiles.

## Reproduce
g++ -O3 -std=c++17 calculation/new_structures/agent-X25/collision.cpp -o /tmp/x25
/tmp/x25 220 2200 > /tmp/x25.jsonl
diff -u calculation/new_structures/agent-X25/collision_table.jsonl /tmp/x25.jsonl
python3 calculation/new_structures/agent-X25/independent_bigint.py --q 140 --gap 360 --steps 1000

No Lean files were changed. Shell GitHub DNS prevented a local checkout and the repository-wide verify.py --changed could not be run. No Lean verification is claimed; the two standalone arithmetic engines were run locally.
