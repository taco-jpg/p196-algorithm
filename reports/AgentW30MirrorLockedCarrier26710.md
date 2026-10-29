# Agent W30 follow-on: mirror-axis-locked five-site odd wave, asymmetric causal cone

Labels: **PAPER PROOF** for the conditional interval-propagation argument, **COMPUTED** for the finite phase tables, exact 26,710 ordinary integer updates, and first violation of the required overflow clock. No infinite base-10 Lychrel certificate is claimed.

## Input and exact bulk rule

This uses the explicit seed, coefficient normalization and exact 9-free piecewise-affine local formulas in `results/AgentW30OddFiveCarrier.md` and `reports/AgentW30OddFiveCarrier.md`. In particular, for pairword coefficients `P_i!=9` and their immediate neighbours also not 9, the next low-half coefficient is:

```
gamma 0: 2*P_i + h(P_(i-1)) + h(P_(i+1)) - 20*h(P_i)
gamma 1: P_i + P_(i-1) - 9*(h(P_i)+h(P_(i-1)))
h(x)=1 if x>=10, else 0.
```

For `gamma 0` there is one-cell dependence on both sides; for `gamma 1` there is one-cell dependence on the low-index side only. The latter asymmetry was not used in the previously published symmetric 20,000-step corridor. The local equations hold up to the midpoint when necessary mirror indices coincide; this follows directly from the same carry substitution with palindrome symmetry of `P`, not from treating two mirrored digits as independent.

## Exact reflection clock

Let `V_0=(17,3,14,3,17)` and `V_t` be the 5-site cyclic evolution with alternating overflows `gamma_(even)=1` and `gamma_(odd)=0`. Every `V_t` is 9-free and contains an odd coefficient. The 40-row table closes, and `V_(t+8)[i]=V_t[(i-2) mod 5]`. Define `n_0=54078` and `n_t=n_0+ceil(t/2)` when the overflow clock holds through the first `t` edges. Our seeded island begins at `idx=39+20*300=6039`. The reflection-axis residue of a low-index offset `r=(i-idx) mod 5` is:

```
delta_t=(n_t-1-2*idx) mod 5=(ceil(t/2)-1) mod 5.
```

The checker verifies all 40 exact equalities `V_t[r]=V_t[(delta_t-r) mod 5]` for `r=0..4`, and all 40 local updates. Because after 40 steps the vector is identical and the midpoint shifts 20 sites (zero modulo 5), those finite checks imply these reflection equalities for **all** `t>=0` under the assumed overflow clock. This is a comoving, unbounded-centre compatibility condition, not a stationary finite kink.

## Sound conditional corridor induction

For a palindromic decimal pairword with the initial island `V_0^(8400)`, set `a_t=6039+t+2` and:

```
I_t = [a_t, n_t-a_t) = [6039+t+2, 48039-floor(t/2)-2).
width(I_t) = 42000 - t - floor(t/2) - 4.
```

**Conditional lemma.** Suppose every overflow bit through `t-1` follows the alternating schedule and the indicated intervals stay at least a few coefficients wider than the one-cell local stencil. Then for every `j in I_t`, the true pairword coefficient equals `V_(t mod40)[(j-6039) mod5]`.

Proof by induction: `t=0` holds because the full central island consists of 8,400 copies of `V_0`; the two-site initial margin is conservative. Assume it at time `t`. For every target index `i` from `a_t+1` to the next word's midpoint, its source neighbourhood under the appropriate gamma formula lies in `I_t`, provided the guard remains sufficiently wide. The 9-free hypothesis holds there automatically because `V_t` contains no 9. Substitution into the finite local transition table gives `V_(t+1)[(i-idx) mod5]`. The resulting **true** pairword is palindromic, and the finite reflection-axis equality above extends the same predicted vector from the lower half to the upper half. Therefore the new protected interval begins at `a_t+1` and ends at `n_(t+1)-(a_t+1)`. Since `n_(t+1)-n_t` is the checked gamma bit, this upper boundary moves inwards by only floor(t/2) after t steps, not by t steps. An interval of at least 5 consecutive cells contains an odd coefficient because each vector is 5-periodic with an odd entry, proving nonpalindromicity on each protected state. The induction depends on the *global overflow clock* and makes no claim that the clock remains valid infinitely.

## Full decimal replay and first break

`replay.cpp`, compiled with `-DW30_ASYM_GUARD`, replays from exactly the same canonical initial integer as the earlier W30 result. Each step is verified independently by three complete implementations: (1) ordinary base-ten digit-array addition, (2) pairword carry-normalization followed by reversal pairing, and (3) a separately implemented arbitrary-precision base-10^9 limb integer that reverses its own decimal numeral and adds its own independent limbs. The code compares the **entire** canonical integer decimal representation and the **entire** pairword at every step, tests the complete interval `I_t` at every step, checks every overflow against the alternating clock, and refuses any palindrome. It does not merely sample a few positions or extrapolate from checkpoints.

Result: 26,710 consecutive additions pass, all 26,711 integer states are nonpalindromic and match the phase-clocked odd wave on every coefficient of the protected interval. The final length is 67,433 digits, 13,355 length overflows have occurred, the guarded interval has 1,931 coefficients, and 1,544 of those coefficients are odd. A one-more-edge run reports the exact **first failed overflow edge** at `t=26710`: expected gamma 1, observed gamma 0. The previous state is still nonpalindromic and has a healthy protected odd region. The failure is specifically of the *external alternating overflow schedule*, not of the pairword arithmetic or the physical existence of the seed.

Run `sh calculation/new_structures/agent-W30/run_asym.sh` for the positive replay. Set `W30_TEST_BREAK=1` for an additional independently caught bad-clock edge; the script requires the predicted failure. `mirror_26710.json` contains a compact checkpoint trace, the exact formula and break descriptor. The independent local-wave/reflection controls in `test_mirror_lock.py` check the exact 40 rows, eight-step translation and reflection classes for 4,040 integer times (periodicity makes this a regression check, not the mathematical reason they hold for all times).

## Next constructive direction

The wave's reflection centre is already phase-locked without any bounded kink. The missing ingredient is a **finite exterior clock-switching transducer** that can replace the alternating clock with a new legal overflow phase at the first switch without destroying an odd interior wave, perhaps through a finite set of 40-row carrier modes and a nondepleting interface. No nonexistence theorem is inferred from this first break. No Lean file was created (Lean 4.19 and the full repository verifier are unavailable locally); the local proof is a paper argument with separately checked finite identities.