# Agent14ChargeSaturation: mod-3/9/11 filters cannot exclude a width-three complementary centre

**PAPER PROOF.** Scope: necessary modular conditions on an even-length base-10 rec0/rec1 (p8/m20, overflow 10101010) centre whose pair coefficients are complemented after 18 steps and return after 80 steps. This is modular *feasibility*, not a centre transition or a certificate. It holds for all sufficiently long exterior bands and all half-widths w>=3.

For a decimal integer with digits d and palindromic pairword P[i]=d[i]+d[n-1-i], sum(P)=2 digitSum(N). Begin at even length n0=2h with lower half X0 followed by w free centre coefficients C. An imagined 18-step complemented state has odd length n18=n0+9 and lower half X18 followed by 18-C; X0 and X18 are the fixed rec0/rec1 exterior prefixes at time phases t and t+18. Write A0=sum(X0), A18=sum(X18), and choose C=[0,...,0,u,v,2r], 0<=u,v<=18 and 0<=r<=9. The centre coefficient 18-2r is even and legal at the odd length.

An ordinary 80-step return adds one 20-cell spatial period to each lower half, and every rec0/rec1 W row has digit-pair sum divisible by 9 (171, 180 or 189). Hence s80=s0 (mod9) for the hypothesized return. Reverse-and-add gives s80=2^80*s0=4*s0 (mod9), so s0=0 (mod3). It yields

    u+v+2r = -A0                (mod3).

Likewise 2^18=1 (mod9), and the central coefficient of an odd pairword is counted only once. Therefore s18=s0 (mod9) requires

    -2u-2v-3r = A0-A18         (mod9).

An even-length integer's first reverse-and-add result is divisible by 11, because reversal changes sign modulo 11; divisibility is then preserved by all subsequent steps. At time 18, length is odd, so alternatingSum(P18)=2*N18=0 (mod11). Let Q18 be the alternating sum when C is all zero (so the complemented centre consists of 18s); set epsilon=(-1)^(h18-1). Replacing its final three coefficients changes the alternating sum by -epsilon*(2u-2v+2r). Thus

    2u-2v+2r = epsilon*Q18     (mod11).

**Constructive surjectivity theorem.** For any prescribed (a mod3, b mod9, c mod11), there are legal u,v in 0..18 and r in 0..2 such that (u+v+2r,-2u-2v-3r,2u-2v+2r) = (a,b,c) in these moduli. Pick r=(b-a) mod3 in {0,1,2}; choose the unique s in [18,26] satisfying s=4*(b+3r) (mod9). Then s=u+v satisfies the first two congruences. Take u in [s-18,18], v=s-u. This interval has 37-s>=11 consecutive integers, and the third expression 4u-2s+2r runs through every residue modulo 11 because 4 is invertible there. Thus some u meets the desired c, with all three coefficients legal.

The constructive Python checker exhausts all 297 right-hand sides. It also directly builds 1,280 mirrored pairword pairs using the real rec0/rec1 exterior source (8 time phases, four even lengths 400..406 and all 20 widths 3..22) and checks all three congruences, central parity and reflection. The independent C++ checker enumerates all 19*19*10=3,610 coefficient triples and recovers 297/297 residues. These control words are NOT 18-step trajectories.

Reproduce from repository root:

```sh
python3 calculation/decimal_frontier/lattice_kinks/code/agent14_charge_saturation.py
g++ -O2 -std=c++17 calculation/decimal_frontier/lattice_kinks/code/agent14_charge_saturation_independent.cpp -o /tmp/p196_agent14_charge
/tmp/p196_agent14_charge
```

Expected control lines: `SURJECTIVE MODULAR MAP: 297/297 residues (constructive proof)`; `DIRECT REAL-LATTICE PAIRWORD CONTROLS: 1280 successful phase/length/width cases`; `INDEPENDENT 3610-ASSIGNMENT RESIDUE COVERAGE: 297/297 PASSED`.

This does not prove a valid periodic centre, a full orbit, independence of all other modular/nonlinear constraints or existence of any decimal Lychrel number. Widths 1 and 2 are outside the saturation theorem.
