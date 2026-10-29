# W28: modulo-clocked non-gauge packet erasure in the rooted decimal period-eight lattice

**Labels:** PAPER PROOF for the local exact rule and its arbitrary finite-packet composition; COMPUTED for Python, digit-list and GMP controls. **Not** a base-10 Lychrel certificate, not an all-time decimal orbit, and no Lean verification.

## Template and the new positive rule

Use least-significant-first decimal pair coefficients \`P_i=d_i+d_{n-1-i}\` (in 0..18). Let \`B\` be the 39-column rooted p8/rec0 block and \`W=(17,3,1,13,17,11,14,3,18,1,2,0,7,3,14,12,15,9,7,13)\` its 20-column bulk. The complete \`B\` is in \`certificate.py\`. For integer K>=8 form \`H=B ++ W^K ++ [8]\` and the odd-length symmetric \`P=H ++ reverse(dropLast(H))\`; the unique middle decimal digit is 4. The initial integer is obtained by splitting pair x into low digit max(0,x-9) and opposite high digit x-low. The highmost digit is 9, so the integer is canonical.

For any subset A of j in {3,...,K-4}, independently replace the three coefficients \`(11,14,3)\` starting at halfword position \`s_j=39+20*j+5\` by \`(6,6,7)\`, and reflect the replacements. These coefficients do **not** differ by multiples of 9: the residues are (2,5,3) versus (6,6,7) modulo 9. The choice of A can depend on any finite modulo counter, e.g. \`j mod 200 in {0,1,3,7,21,34,55,89,144,199}\`, or be completely arbitrary.

**Local erasure theorem (PAPER PROOF).** For every such K and A, the complete pairword of the modified initial integer at time 3 is identical to the complete pairword of the unmodified integer at time 3. Consequently their **actual ordinary integers** agree at time 4 and at all later times. Arbitrarily many independently programmable packet bits disappear together, without requiring a short fixed-width centre. The clock is the genuine rooted decimal overflow itinerary \`1,0,1\` during the three steps.

## Exact three-step carry table and why it is universal

For an internal coefficient x other than 9, the outgoing schoolbook carry is \`z(x)=1[x>=10]\` regardless of incoming carry (which is 0 or 1). At non-neutral internal columns the next pairword is therefore the exact radius-one map

\`F_0(P)_i=((P_i+z(P_(i-1))) mod 10)+((P_i+z(P_(i+1))) mod 10)\`

for overflow 0, while for overflow 1 it is

\`F_1(P)_i=((P_i+z(P_(i-1))) mod 10)+((P_(i-1)+z(P_i)) mod 10)\`.

The overflow-one formula includes the one-position reflected alignment shift. Both formulas are exact schoolbook arithmetic, not statistical assumptions, provided the indicated cells avoid coefficient 9. At the affected relative positions \`s,s+1,...\` the full differing coefficient rows are:

| time | background | packet | differing columns |
|---|---|---|---|
| 0 | 11,14,3 | 6,6,7 | s..s+2 |
| 1 | 10,7,8,12 | 14,12,13,16 | s..s+3 |
| 2 | 1,15,17,5 | 10,6,8,14 | s..s+3 |
| 3 | identical | identical | none |

At every intermediate step the radius-one dependencies in \`s-1,...,s+4\` are non-neutral, checked directly by the independent local arithmetic in \`certificate.py\`. Outside each width-six causal cone, the words agree by finite propagation speed. The nearest packet starts 20 columns away, so their cones remain disjoint. The root and high cap are untouched and contain carry-absorbing coefficients; they fix the same overflow itinerary \`101\` for both words. The table plus these finite guards proves the all-K, arbitrary-A statement. There is no renewal: after three steps the programmed information is irretrievably erased.

## Finite controls and exact 20,000-step decimal replay

\`certificate.py\` verifies the independent local formula, whole pairword equality for 440 deterministic randomized subsets at K=8,9,10,12,15,20,25,50,100,260,420, and 21 short independent Python big-integer controls through actual-number coalescence at t=4. The long C++ source generates **three** distinct K=260 programs (empty, modulo-200, modulo-7), checks all initial pairwords and exact coalescence at t=3/t=4, then performs 20,000 ordinary reverse-add steps for the modulo-200 program.

The two arithmetic engines are independent: (a) a least-significant-first decimal string addition routine, and (b) GMP integers whose decimal strings are reversed and reparsed before arbitrary-precision addition. A third coefficient-normalization route checks the entire pairword at **every** step, also verifying that the fixed 39-column rooted p8 exterior and at least one full 20-column band remain present, in the correct phase, at every one of 20,001 states. Measured minimum band copies: **3** (at the first programmed slot); at step 20,000: **32** copies. The ordinary digits and GMP integers agree exactly at every step; every state is nonpalindromic; the total number of length overflows is 10,000. Length starts at 10,479 and ends at 20,479; final FNV-1a 64-bit checksum on the most-significant-first ordinary decimal string is \`11093401814211976744\`. Compact checkpoint hashes are in \`observations.json\`.

This shows a **non-gauge, modulo-programmable exact one-time memory reset in the specific reachable p8/m20 exterior** and a completely verified finite survival family. The root safety margin is ultimately a finite reservoir, not a proof of infinite protection. The constructive next target is an emitter that regenerates these non-gauge packets each 8- or 16-phase cycle while the packet erasure occurs before the incoming front reaches the root. The missing positive condition is a replenishment/return of the finite carry boundary state, not another fixed-centre width census.

## Reproduce

\`\`\`sh
python3 calculation/new_structures/agent-W28/certificate.py
g++ -O3 -std=c++17 calculation/new_structures/agent-W28/modular_eraser.cpp -lgmpxx -lgmp -o /tmp/w28
/tmp/w28 260 20000
\`\`\`

No Lean files were modified. This container had no repository checkout and could not run \`python3 tools/verify.py --changed\`; the two self-contained source programs were compiled/run and passed independently in the working container.
