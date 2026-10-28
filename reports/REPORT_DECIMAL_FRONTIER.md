# Decimal frontier for neutral-band, absorbing-band and lattice certificates (2026-10-27)

**Not a Lean result, and no decimal certificate.** This report collects one research session's base-10
computations and paper arguments: what is excluded, with exact scope, and what is open. Code and full write-ups are
in [`calculation/decimal_frontier/`](../calculation/decimal_frontier/README.md).

Labels:
- COMPUTED = exact finite computation, not Lean-checked.
- PAPER PROOF = a written proof, numerically tested.
- UNDECIDED = outside every bound that was searched.
The only Lean result of the session is [REPORT_ABSORBING_BAND.md](REPORT_ABSORBING_BAND.md) (base 13).

## 1. Neutral one-band format (`Agent120.Neutral.cycleOK 10`)

**Exterior B-cycles, full census for periods p ≤ 32** (COMPUTED; `exterior_census/`).
- Engine: `bx`, an exact position automaton with no state-key truncation. Validation:
  - identical to the repository's `bauto` on every word with p ≤ 14, on 15 bases with p ≤ 8, and on all necklaces
    with p = 17 and p = 19;
  - identical to an independent BDD encoding on control words.
- Candidate words: every word passing the first-coordinate NFA filter (PAPER PROOF, 36 edges checked), 187,967
  words in all.
- Accepted streams: only the known p = 11 stream (`g = 11100010000`, `e = 10100110011`), the p = 12 stream
  (`g = (1000)^3`), and p = 22, which is the p = 11 stream repeated twice. **No new exterior stream exists.**
- Coverage:
  - completely decided: p ≤ 15, 17–20, 22, 23;
  - 54 words hit the state cap and are UNDECIDED: (01)^8 at p = 16, one word at p = 21, (0001)^6 and (01)^12 at
    p = 24, and 2/3/2/9/12/22 words at p = 27/28/29/30/31/32.
- Note: the earlier p = 16–24 Studio run of `bauto` silently skipped 560 streams whose key exceeded 127 bits. `bx`
  has no such limit.

**Theorems** (PAPER PROOF + tests; `theory/THEORY.md`).
- *Density* (§2.2): every exterior cycle with overflow count G satisfies 2G ≤ p ≤ bitlen(b)·G. In base 10 this
  gives 2G ≤ p ≤ 4G, and the zero-runs of the overflow word have length ≤ 4.
- *Charge law mod (b−1)* (§4.1b, 146,268 random tests): every exterior step satisfies
  s(B′) ≡ 2 s(B) + 1 − 2 e1 (mod b−1). Hence gcd(2^P − 1, b − 1) divides the binary value of the e-word. This
  rules out the stream `10` whenever b ≡ 1 (mod 3), and in particular the one-overflow-per-cycle exteriors that carry
  the known certificates of bases 2^j, 11 and 26 cannot exist in base 10.
- The ratio-product identity over a cycle is a tautology, so "log₂10 is not an integer" gives no obstruction.

**Centres for p = 11 and p = 12** (COMPUTED). The claims of PRs #411, #404 and #399 (no centre for any number
of laps) were reproduced with their own code. An independent brute force written from the mirror (all palindromic
centres of phase-0 width ≤ 12, 71.8M states each) agrees. The transducer model itself was not re-derived. CP-SAT
finds no p = 11 centre for k = 3 laps at any width ≤ 121.

**Conditional reduction.** If the PR claims hold, any decimal neutral one-band certificate needs one of the 54
capped words or an exterior of period ≥ 33.

## 2. Absorbing-band and lattice formats

- The absorbing band loops of base 10 are {0}, {18}, {6,12} and {2,4,8,16,14,10}. A decimal exterior search in
  this format (`lattice_formats/`) covered periods ≤ 24 and, with a symbolic backward-cone engine, some denser
  words. The only closing structures it found are lattices that cannot merge at the centre.
- **Decimal p = 8 lattice exterior** (COMPUTED): overflow word `10101010`, |B| = 39, followed by a periodic
  absorbing lattice of spatial period 20 (two shifted copies) or 48.
  - Real orbits of 196 and of random seeds lock into this exterior for 75–155 steps (`orbits/ORBITS.md`).
  - The lattices are not palindromic necklaces, so a certificate would need a time-periodic centre ("kink", period
    80 or 192).
  - No kink exists with lower-half window width ≤ 7 (`lattice_kinks/KINK.md`; DFS and SAT agree). Width 8–9 is
    excluded for half of the phase classes. Wider windows are UNDECIDED.
- **Hybrid centres** (neutral exterior with an absorbing core band; `hybrid_centres/HYBRID.md`):
  - for p = 11 and p = 12, a stationary wall is impossible at any width or period;
  - moving walls are exhausted for T = 11, 12 and 22;
  - SAT finds none (for example p = 11, k = 1, register width ≤ 250);
  - positive control: a base-4 hybrid certificate replays for 30,000 steps.

## 3. Observations (`orbits/ORBITS.md`)

Natural orbits become regular (enter a certificate template) only in bases 2^k, and never in 11, 17, 20 or 26,
whose Lychrel numbers are proven. So the absence of visible regularity in the orbit of 196 is not evidence against a
decimal Lychrel number.

## 4. Open, in order of cost

1. The 54 capped words and periods 33–40 (`exterior_census/STUDIO_JOBS.md`; about 55 core-hours for a first
   pass).
2. Wider kinks for the p = 8 lattice (`lattice_kinks/STUDIO_JOBS.md`). An all-width answer needs a
   transfer-operator or wall-speed argument.
3. The absorbing-band format for decimal exteriors with period > 24.
