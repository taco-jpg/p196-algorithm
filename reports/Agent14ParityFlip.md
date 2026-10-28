# Agent14ParityFlip: parity-changing centre-frame complement classification

**PAPER PROOF.** Scope: the four already stored reachable decimal absorbing-lattice SCCs, p8/10101010 rec0/rec1 (m=20), rec2 (m=48), p12/100010001000 (m=9). No centre or Lychrel certificate is claimed.

Set h(n)=ceil(n/2). Let G(t,d) be the total overflow in d steps starting from overflow phase t. If G is odd, the central coordinate h advances by delta=(G+1)/2 for even starting n and delta=(G-1)/2 for odd starting n. An exact coefficient-complemented finite centred interface with periodic bulk must satisfy W[(t+d)%p][(j+delta)%m] = 18-W[t][j] for every j, with the corresponding steady ascending carries summing to 1. Far from a finite centre the periodic bulk forces this relation. It is necessary, not sufficient for a centre transition.

Let S=sum(g) in one period p, and L=p*(2m/gcd(2m,S)). At time L the spatial phase and time phase reset, and the total overflow is divisible by 2m. Every positive parity-changing alignment therefore has a representative 1<=d<L and repeats modulo L. Exhaustion needs only finite pairs (t,d) and both starting parities; no state caps.

The complete coefficient-and-carry complement glides (dt,dx) are rec0/rec1: (2,5),(6,15); rec2: (4,24); p12/m9: none. For rec0/rec1, d=8k+2 has G=4k+1, so even-start delta=2k+1 equals 5 mod20 precisely for k=2 mod10, or d=18 mod80; odd-start delta=2k is incompatible. Similarly d=8k+6 has G=4k+3: odd-start delta=2k+1 equals 15 mod20 precisely for k=7 mod10, or d=62 mod80; even-start delta=2k+2 is incompatible. For rec2, the complement glide requires d=8k+4 but G=4k+2 is even, so no parity flip. P12 has no complement glide.

| Lattice | L | Odd-G (t,d) cases per starting parity | Compatible parity-changing return |
|---|---:|---:|---|
| rec0 and rec1 (m20) | 80 | 320 | even n: d=18 mod80; odd n: d=62 mod80, every t |
| rec2 (m48) | 192 | 768 | none |
| p12 (m9) | 72 | 432 | none |

Two complementary phase-changing returns must alternate even and odd lengths; their first possible two-stage cycle is 18+62=80 steps. Thus a hypothesized 18-step complemented half-return does **not** by itself reduce the ordinary 80-step certificate to 18 steps: a distinct, exact 62-step centre transition remains necessary. A centre satisfying both is not supplied.

Reproduce from repository root:

```sh
python3 calculation/decimal_frontier/lattice_kinks/code/agent14_parity_flip.py
g++ -O2 -std=c++17 calculation/decimal_frontier/lattice_kinks/code/agent14_parity_flip_independent.cpp -o /tmp/p196_agent14_independent
/tmp/p196_agent14_independent
```

Both programs independently recover the published (coefficient) complement glides and the 80/192/72 centre-frame periods as positive controls, as well as the precise 18/62 parity-changing cases. The Python checker additionally checks complementary steady carries and period-preserving overflow. Inputs are existing `calculation/decimal_frontier/lattice_formats/p8_scc.txt` and `calculation/decimal_frontier/lattice_kinks/data/lat_p12m9.txt`. No new exterior census, other bases, complete finite centre, 196-orbit claim, or Lean verification is asserted.
