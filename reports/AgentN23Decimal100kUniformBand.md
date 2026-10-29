# N23: 100,000-step decimal uniform family and exact counter thresholds

**COMPUTED finite-horizon certificate**, not an infinite decimal Lychrel result, and not a Lean proof. The complete arithmetic soundness argument for the underlying two-ended decimal carry map is in reports/AgentN23ParametricDecimal20kBand.md and source calculation/new_structures/agent-N23/exterior_pump.cpp.

For any integer Q>=30037, let N0(Q) be the true decimal integer with most-significant-first digits 12, then Q copies of the two-digit string 99, then 34. The two-ended digit map computes every exterior independently of Q while an untouched symmetric central 9 band has length at least 2. It checks U_t != reverse(V_t) at t=0..100000, which proves N_t(Q) is not a palindrome. Its band length satisfies the exact affine law L_t(Q)=L_t(30037)+2(Q-30037). The complete computed 100,001-state path at Q30037 attains minimum L=2 at final step 100000. The final exteriors each have width 50,692; the final total number has 101,386 decimal digits. Observed event counts are gamma0=58692, gamma1=41308 and paired-boundary-9 trimming=49310. Total band consumption in 100000 steps is 60072 decimal digits, computed exactly by the transfer law.

## Finite-horizon threshold sequence

The exact minimal initial padding Q necessary for this particular L>=2 transfer certificate, at each horizon, is:

| horizon T | Q_min(T) | minimum central 9 run | gamma0 | gamma1 | paired trims |
|---:|---:|---:|---:|---:|---:|
| 1000 | 303 | 3 | 579 | 421 | 488 |
| 5000 | 1504 | 3 | 2945 | 2055 | 2470 |
| 10000 | 3003 | 3 | 5849 | 4151 | 4923 |
| 20000 | 6016 | 2 | 11738 | 8262 | 9854 |
| 50000 | 15027 | 2 | 29352 | 20648 | 24650 |
| 100000 | 30037 | 2 | 58692 | 41308 | 49310 |

Each Q_min is independently checked by an exact transducer replay; each immediately smaller value Q_min-1 causes central length=1 within the target horizon (boundary times 1000,5000,9999,19998,49998,99998). These are tight for this *specified L>=2 band invariant*, not optimal thresholds for nonpalindromicity and not negative results about other formats. The Q_min values grow approximately 0.300*T over the tested interval, suggesting a finite-speed advancing carry-front that consumes rather than replenishes band. No asymptotic law is claimed.

## Independent 100,000-step full-integer replays

Oracle 1 (the earlier source protected_20k.cpp, run with the test-only minimum-band threshold lowered from 1000 to 2) stores all digits in base 10, computes complete reverse-and-add by ordinary decimal column carries, and checks the full symmetric central coefficient-18 band plus nonpalindromicity at **every** state. It yields Q30037, 100000 steps, 101386 final decimal digits, centre minimum/final length 2, checksum886568206 mod1000000007.

Oracle 2 (new protected_thousands.cpp) stores the integer in base-1000 limbs, reverses its full decimal rendering and adds by limb carries, checking the decimal palindrome condition and a central run of 9s at every state. It also yields 101386 final digits, centre min/final 2 and checksum886568206. Thus the two structurally independent arithmetic implementations corroborate the symbolic two-wall path; rolling checksum agreement is not substituted for the inspection of both source programs.

## One-command rerun

    bash calculation/new_structures/agent-N23/reproduce_100k.sh

It compiles the previously committed exact two-wall transducer and base-10 digit-vector oracle plus the new independent base-1000 limb oracle; it checks all six horizon/threshold/checksum controls in threshold_100k.tsv, confirms failure to maintain L>=2 at each Q_min-1, and replays the complete genuine base-10 100000-step boundary seed in both independent arithmetic implementations. All input and source is in this repository; no Lean files are added. Repository-wide tools/verify.py --changed is unavailable in the current environment; the standalone controls were run.

**Limitation:** For each fixed finite Q the protected 9 band loses length as the exterior walls advance, so this method establishes **arbitrarily large finite horizons with correspondingly large Q**, not a single infinite decimal orbit. The desired infinite certificate still requires an absorbing replenishment cycle or new glider/renormalisation at collision.
