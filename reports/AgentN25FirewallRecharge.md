# N25: exact reflection-matched firewall replenishment and observed rate

Label: COMPUTED (specific integer orbit and limits). Not a decimal Lychrel proof, not a Lean theorem.

The previous N25 result proves that mirror-paired zero intervals survive for at least `g-2t+G_t` positions after `t` reverse-and-add steps. That is a worst-case erosion bound, not a measurement of the actual paired zero domain. We now track the **maximal reflection-matched** zero sectors, which are stricter than merely finding a long zero run on one side.

## Exact boundary-credit identity and conditional infinite criterion (paper derivation)

Let `d_t` be the canonical digit word of length `n_t`, and let `gamma_t=n_{t+1}-n_t` in `{0,1}`. For a central vacuum, take `W_t` to be the largest contiguous *self-mirror* interval of zeros containing the guaranteed central interval. For the two exterior sectors, extend the nominated left interval `[a,b]` to `[a-x,b+y]` only when both that enlarged interval and its reflection about `n_t-1` are all-zero. Let `w_t` denote either maximal matched width, and `G_t=sum_{j<t}gamma_j`.

The local zero-sector lemma applies to **the entire enlarged paired sector**, so `w_{t+1} >= w_t-2+gamma_t`, provided that the protected sectors have not merged/collided. Define the *effective replenishment credit*

`r_t := w_{t+1} - w_t + 2 - gamma_t >= 0`.

Then `E_t=sum_{j<t}r_j` is monotone and the **exact accounting identity** is

`w_t = w_0 - 2t + G_t + E_t`.

This is not equivalent to counting digits newly set to zero: a credit also occurs when a boundary digit survives a worst-case erosion. For an infinite-time sector automaton, a sufficient *width condition* across every `q`-step period would be `sum_{period}(r_t+gamma_t)>=2q`, with individual substeps maintaining enough positive width; combined with an exact arithmetic recurrence, reflection pairing, canonical leading digit and a permanently nonpalindromic boundary witness, it would give a sound nonshrinking-sector Lychrel certificate. **We do not have such a decimal recurrence.** The criterion redirects search toward carry-carrying joints that supply additional paired credits instead of dead fixed-width centre censuses.

## Computation

Seed: `1789 0^40001 3141 0^40001 5926 0^40001 5358`, 120019 digits. For each `t=0,...,20000`, `safe_scan.cpp` independently computes exact ordinary digit-list reverse-add, counts overflows and finds the matched sectors by checking zeros at *both* reflected positions. At each step it enforces `E_{t+1}>=E_t`; all 20000 transitions pass. The independent base-10^9 bigint engine from the preceding result agrees with the complete ordinary decimal orbit at every step (20,001 trace rows), and `regen_check.py` separately computes an early boundary event using Python's built-in arbitrary-precision integers.

| t | G_t | passive width | outer matched width | central matched width | outer E_t | central E_t |
|---:|---:|---:|---:|---:|---:|---:|
| 0 | 0 | 40001 | 40001 | 40001 | 0 | 0 |
| 1000 | 421 | 38422 | 39402 | 39402 | 980 | 980 |
| 5000 | 2066 | 32067 | 36993 | 36999 | 4926 | 4932 |
| 10000 | 4104 | 24105 | 33992 | 33995 | 9887 | 9890 |
| 15000 | 6165 | 16166 | 30974 | 31002 | 14808 | 14836 |
| 20000 | 8227 | 8228 | 27981 | 28032 | 19753 | 19804 |

Net matched width loss: 12020 (outer) and 11969 (central) over 20000 steps. This is approximately 0.601 and 0.598 digits per step. Gross worst-case loss is `2*20000-8227=31773`; effective replenishment credits are 19753 and 19804, corresponding to ~0.988 and ~0.990 per step. A stable wall would require an average `2-8227/20000=1.58865` credits per step. The missing rate is ~0.600 and ~0.598. No matched-width *growth* event occurs in the 20,000-step sample, although the maximal unmatched central zero run has an independently confirmed two-cell growth at t=1848; that unmatched event must **not** be mistaken for a mirror-paired wall regeneration.

## Reproduce

From the repository root:

`python3 calculation/new_structures/agent-N25/run_recharge.py`

This compiles and executes `safe_scan.cpp` for 20,000 transitions, verifies every published checkpoint in `recharge.json`, calls `regen_check.py` for a positive ordinary Python big-integer local control, and reruns the two independent full-orbit engines in `run.py`. No external Python packages or Lean are required. Data are compact checkpoints, not a 20,000-line log.

## Next construction

Search temporally clocked *paired* joint rules that attain `r_t=2-gamma_t` on average or exceed it on growth cycles. Track matched sectors, not independent longest-zero runs: the latter can temporarily grow asymmetrically without replenishing a valid reflection-coupled firewall. A plausible certificate needs a verified finite joint transducer whose bulk vacuum width is a nondecreasing counter, plus a separately checked nonpalindromicity witness.
