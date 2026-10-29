# X07 nine-piston: an overflow-synchronized moving wall in decimal repdigits

**COMPUTED (finite):** The exact repdigit-frontier transducer from `AgentX07RepdigitFrontier` has a special *nine-piston* mode. For `N_n=10^n-2908 = 9R_n-2907`, its front width `m_t` and cumulative leading overflows `G_t` satisfy **`m_t=G_t+4` for every t=1..60,000** in the symbolic, length-independent frontier computation. Each 60,001 checked pairword states has an odd coefficient by index 21 (0-based). Max `m_t=24,878`, `G_60000=24,874`, max `2m_t-G_t=24,882`. Therefore **for every n>=24,884** the actual decimal orbit remains exactly in the two-front/constant-nine-centre format and is nonpalindromic through step 60,000. This is an exact finite computation together with the soundness lemma below, not an infinite-orbit theorem.

**COMPUTED (independent integer replay):** The threshold `n=8297` also passes 20,000 complete ordinary decimal steps, comparing GMP `N+reverse(N)` against a separately coded schoolbook digit engine and the full symbolic frontier at every step. Initial integer `10^8297-2908`, final length 16,584, 8,287 overflows, minimum centre width 2, no palindrome; FNV64 `a5a5b7b3e4e9b7ca`. At 20k, `m=8291`, `G=8287`, maximum odd-pair index 19. This is a new simple repdigit-like seed, distinct from the period-20 lattice family.

## Sound guarded piston identity (PAPER PROOF)

Let a least-significant-first decimal digit string be `A ++ 9^L ++ H`, `L>=2`, `|A|=|H|=m`. Let `alpha` be the carry leaving the low-end `A` sum-normalization, and `gamma` the carry out of the high-end `H` normalization, which becomes the leading overflow digit. The all-nine interior has coefficient 18; after its first cell its carry is identically 1, so its output digit remains 9. Write `r` for the number of equal-nine pairs stripped from the inward-facing ends of the new low/high frontiers by canonical trimming. The exact identity is

`m' = m + 1 - r`, `L' = L + gamma - 2 + 2r`.

Suppose the *complementary carry guard* `alpha+gamma=1` and *single-trim guard* `r=1-gamma` hold. Then **`m'=m+gamma` and `L'=L-gamma`**, hence `m'-G'=m-G` for that step. This is an exact all-length identity, not a statistical statement. These two guards are checked for all 59,999 post-initial steps (`t=1..59,999`) in `piston_probe.cpp`; the first exceptional step (`t=0`) changes `m` from 6 to 5 and has `gamma=1`. The guard does not imply infinite continuation: `L` decreases whenever `gamma=1` and must eventually exhaust for every fixed starting length if overflows occur indefinitely.

## Bounded exhaustive seed scan (COMPUTED)

For all 9,999 negative perturbations `k=-9999..-1` of `9R_n+k` (six-digit low cap), check the first pairword for an odd coefficient, then demand at each `t=1..20000` both an odd coefficient and `m_t-G_t=m_1-G_1`. Exactly **51** satisfy this *finite-horizon* criterion: 45 with offset 4, 4 with offset 3, 2 with offset 2. Every one is divisible by 9; divisibility is an observed filter here, **not** a proven sufficient condition. The complete 51-element list is in `piston_data.json`; the counted seeds are exact, not sampled. The run has no artificial cap besides the stated time horizon.

**Mechanism and next structural direction:** The potentially useful new invariant is the *carry-complementary pair of active walls* with signed flux `m-G`, not a stationary kink. One can seek a renewal gadget that periodically increases `L` despite the individual-piston drain `L'=L-gamma`, e.g. by coupling two nine-domains with a carry-converting relay. This is a proposal, not a discovered infinite certificate.

Reproduce: `bash calculation/new_structures/agent-X07/piston_run.sh`. Sources `piston_scan.cpp`, `piston_probe.cpp` depend on the original `repdigit_front.cpp` in the same directory; data `piston_data.json`. No Lean or repository-wide `verify.py --changed` build was claimed; local git checkout cannot resolve GitHub DNS, but all individual standalone programs were compiled and run.
