# W18: a shorter decimal 20,000-step protected-band family
**Label: COMPUTED** (finite-horizon, base 10, independent ordinary-integer replay). Neither an infinite-time Lychrel certificate nor Lean verification.

## Construction and exact scope
Let `N_0(Q)` be the genuine decimal numeral `5 (99)^Q 4` for integer `Q>=4138`. Its least-significant-first digit template is `U_0 ++ 9^(2Q) ++ V_0`, where `U_0=[4]`, `V_0=[5]`. Its symmetric pairword is `[9] ++ [18]^(2Q) ++ [9]`. This belongs to a different pair-sum class than the previously published `12 (99)^Q 34` family, whose initial end coefficients are 5.

The exact two-wall carry rule from `reports/AgentN23ParametricDecimal20kBand.md` applies: normalize `U + reverse(V)` with incoming 0 to get low word and carry `c`; the first 9+9 produces `8+c` and carry 1; normalize `V + reverse(U)` with incoming 1 to obtain high and overflow `gamma`. Form equal-width exterior words, remove paired boundary 9s, and adjust the band length by `-2+gamma+2*trims`. The complete decimal integer identity holds whenever the incoming central 9-run has length at least 2. No base-100 reversal-conjugacy assumption is made.

The source's exterior sequence is **independent of Q**, and its middle length at time t is exactly `L_t(Q)=L_t(4138)+2(Q-4138)`. C++ checks `L_t(4138)>=2` and `U_t != reverse(V_t)` at **every** `t=0..20000`. Induction from the exact carry rule therefore certifies every Q>=4138 for exactly 20,000 steps. Because the middle digits are all 9, the symmetric pairword has the central coefficient-18 run. This is a full claimed pairword shape, not merely a numerical no-palindrome test.

## Exact data and independent controls
| t | decimal digits | central 9-band | full-number checksum |
|--:|--:|--:|--:|
| 1 | 8279 | 8275 | 678940962 |
| 100 | 8323 | 8231 | 259195213 |
| 1000 | 8703 | 7851 | 224600994 |
| 5000 | 10376 | 6178 | 754174213 |
| 10000 | 12438 | 4116 | 381862759 |
| 20000 | 16552 | 2 | 425518744 |

The 20,000 steps contain **11,726 paired nine-boundary trims** and **8,274 overflows**. Thus the band change is `-40000+8274+2*11726=-8274`; `L_0(4138)=8276` and `L_20000=2`. Independent oracle `bigint.cpp` uses radix-1,000,000,000 limbs, converts to an ordinary decimal numeral, reverses its entire decimal string, parses and adds the limbs, and verifies nonpalindromicity and the central 9-run at every step. It agrees with the source's final length and checksum; every listed checkpoint agrees as well. The two engines share no reverse-add or carry code.

The immediately smaller Q=4137 first reaches band length 1 at t=19998, invalidating this **specific** two-wall transfer condition. Q=4138 reaches length 1 at t=20002, two steps beyond the certified horizon. Neither loss implies a palindrome. This is a transient decaying resource, not a replenishing macro-cycle. The constructive next direction is to find a wall-recharge or a moving-splice mechanism when the length drops to 1.

## Reproduction and provenance
Run `bash calculation/new_structures/agent-W18/reproduce.sh` at repository root (C++17 compiler, standard shell only). The result and threshold ledger are in `calculation/new_structures/agent-W18/`. The 20,000-step independent arithmetic and full-state pairword-form controls passed locally. The local environment cannot resolve GitHub HTTPS, so the full repository checkout and `python3 tools/verify.py --changed` could not be run; no Lean files are added. Prior N23 work is explicitly credited for the existing two-wall soundness theorem. The new contribution is the seed class and quantitatively shorter constructive finite-horizon uniform witness.
