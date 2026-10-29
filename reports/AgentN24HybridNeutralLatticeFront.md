# Agent N24: Decimal neutral/lattice conversion and a 20,000-step rooted hybrid orbit

**COMPUTED, finite scope only.** This is *not* a base-10 Lychrel proof or an indefinitely repeatable certificate. All coefficients below are low-digit-first pair coefficients `P_i = d_i + d_{n-1-i}` in `0..18`. The p12/m9 lattice rows and width-34 rooted exterior come from `calculation/decimal_frontier/lattice_kinks/data/lat_p12m9.txt` (repo data, not discovered here).

## New splice / conversion mechanism

For base ten, in a homogeneous coefficient-9 zone, carry normalization sends `9` to digit `9` if the incoming carry is `0`, or to digit `0` if it is `1`. If the carries entering its two mirrored zones are `a,c in {0,1}`, the next pair coefficient *away from the shifted endpoints* is exactly `18 - 9(a+c)`, hence `18, 9, 0` for carry pairs `(0,0)`, `(0,1)/(1,0)`, `(1,1)`. This is a local PAPER PROOF of the splice rule. On overflow steps the mirror pairing shifts by one, but any homogeneous interior still obeys the rule. A zero-coefficient band immediately absorbs an incoming carry after one cell (`0+1=1`, carry out `0`). This creates a carry-selected neutral-to-absorbing band conversion, instead of a fixed short centre.

An explicit rooted hybrid pairword is

`P0 = B0 ++ W0^450 ++ 9^80 ++ [18] ++ 9^80 ++ reverse(W0^450) ++ reverse(B0)`.

`B0` has 34 coefficients; `W0` is the spatial 9-word of the period-12 lattice. The middle `[18]` makes the total length odd, and has a valid centre digit `9`. To form a concrete decimal seed `N0`, split each mirrored coefficient `p` as digits `(min(9,p), p-min(9,p))`, and split the central `18` as `(9)`. `N0` has 8,329 digits and nonzero leading and trailing digits. The reverse-and-add iterates are computed as ordinary integers, not by relying on the coefficient template.

## Main replay

With `g = 100010001000` (3 overflows per 12 steps), **both independent implementations** match exactly through step 20,000:

- `replay_bigint.py`: ordinary Python integers `N <- N + int(str(N)[::-1])`.
- `replay_digitlist.py`: independent base-10 schoolbook digit-list addition.
- At **each** step `t = 0..20000` the number is nonpalindromic, has the predicted length, and its symmetric pairword begins with the entire period-12 root `B[t mod 12]` plus at least the next **256** coefficients of the `W[t mod 12]` spatial lattice (and their mirror at the opposite end).
- Initial length 8,329, final length 13,329; max first mirrored-digit mismatch index (from the least significant side) = 4. Both replays give identical full-number seed SHA-256 `bb33d2a8f75b601d058ee1c8821c74bfc58fd242d7cd8c324de4d3d59d4992b7` and final SHA-256 `ddce08ab35fbc178c93ab775e2e0c10123a19afe524544c161ef63d7a33df9dd`.
- Rooted lattice matching length measured from position 34: step 0: 4050; 1000: 3862; 5000: 3112; 10000: 2175; 15000: 1238; 20000: 299. The interface invades the rooted lattice at about 0.18755 coefficients/step, numerically close to 3/16. The rate is an observation, not a proven velocity.

## The conversion has a measurable failure mode

`small_probe.py` constructs the smaller `B0 ++ W0^20 ++ 9^80 ++ [C] ++ mirror`, then exactly normalizes the symmetric pairword. With `C=18`, the neutral-9 half-run has lengths `80,79,79,0` over steps `0..3`, while a zero-run of length 79 appears at step 3; with `C=0`, the centre-side 9-run converts to an 18-run of length 79 at step 1. The neutral component **does not remain 9-periodic**. In the large orbit, the defect front moves inward through the lattice and the rooted prefix loses ~187-189 matched coefficients per 1000 steps. Thus the presented seed is not a certificate and cannot be extrapolated to infinite time without a regenerative interface.

## Proposed clocked carry-splice certificate format (conditional PAPER PROOF)

A proposed state consists of temporal phase `t mod p`, a finite root `B_t`, a left/spatial lattice `W_t`, a finite alphabet of *interface carry contracts* `(incoming low carry, incoming upper carry, overflow)`, and a regular (or finitely transduced) language `L_t` of symmetric centre words. A state denotes all pairwords `B_t ++ W_t^k ++ D ++ reverse(W_t^k) ++ reverse(B_t)`, with `k >= k_min`, `D in L_t` and valid pairword-leading/central parity constraints. To certify a finite cycle, an independently sound digit-normalization transfer relation must establish, for **every** admissible `k,D`, that one step maps to the next state with `k' = k + delta_e`, `D' in L_{t+1}`, a legal leading digit, and a forced nonpalindromic normalized digit word. If the cycle's prefix sums of deltas keep `k>=k_min`, its net delta is nonnegative, and all states are nonpalindromic by their forced local witness, induction gives an infinite decimal nonpalindromic orbit. This is a precise soundness condition; **no such finite complete decimal interface cycle was found or checked here**. The unrestricted growing core in this computation is not an `L_t` proved closed by a finite transducer.

## Reproduction and controls

From the repository root:

```
cd calculation/new_structures/agent-N24
python3 replay_bigint.py hybrid_data.json 20000 > bigint.json
python3 replay_digitlist.py hybrid_data.json 20000 > digitlist.json
python3 small_probe.py hybrid_data.json
```

Compare the samples and SHA-256 fields of both JSON outputs; all 21 sampled rooted-lattice front lengths agree. Negative controls: changing the phase of `W` at t=0 fails the pairword check immediately; `56 + reverse(56) = 121` is a positive palindrome detector control. No Lean files are changed. In this tool environment repository git clone / `tools/verify.py --changed` cannot run because DNS for github.com is unavailable; no `LEAN-VERIFIED` claim is made.