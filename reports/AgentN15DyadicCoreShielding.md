# Constructive dyadic shell shielding of a central decimal defect (agent N15)

**Status: COMPUTED**, exact finite levels and time ranges below. This is a positive propagation mechanism, not an exclusion or a decimal Lychrel certificate.

For every h, let `W_h=σ^h(A)` with `σ(A)=AB`, `σ(B)=BA`, A=14, B=16. Let `H_h=[4]++W_h`. Construct two palindromic decimal **pairwords** (least significant coefficient first) `P_h(c)=H_h++[c]++reverse(H_h)` for c=0 and c=18. The odd-length central pair coefficient is even and comes from one decimal digit (0 or 9). Both pairwords are realised by explicit positive integers: lower digit half `[1] ++ [x-9 for x in W_h]`, central digit c/2, upper digit half reversed from `[3] ++ [9 repeated 2^h]`. The normal decimal map N->N+reverse(N) therefore induces deterministic pairword dynamics on the two genuine numbers. Only their centre differs initially.

Define `D(h,k)` as the first integer time t>=0 when their **first k least-significant pair coefficients** disagree (or their digit lengths disagree). No assumption is made about eventual coalescence or asymptotic propagation. For h=6..12 and k in {4,8,16,32,64}, the complete finite computed table is:

| h | 2^h | k=4 | k=8 | k=16 | k=32 | k=64 |
|---:|---:|---:|---:|---:|---:|---:|
| 6 | 64 | 337 | 317 | 280 | 187 | 6 |
| 7 | 128 | 648 | 629 | 587 | 508 | 364 |
| 8 | 256 | 1450 | 1433 | 1355 | 1267 | 1097 |
| 9 | 512 | 3222 | 3199 | 3160 | 3032 | 2774 |
| 10 | 1024 | 5865 | 5839 | 5796 | 5715 | 5527 |
| 11 | 2048 | 11614 | 11586 | 11546 | 11456 | 11257 |
| 12 | 4096 | 23289 | 23263 | 23223 | 23143 | 22999 |

Each entry is a **first-passage time**: for every earlier t the entire k-coefficient prefix agrees, and at this time it differs. Thus the run verifies the claimed shape at every intermediate step, not just a sampled endpoint. For h=12 and k=16 the shield lasts 23,223 full steps: the initial centre differs at spatial position 4097, while the outer 16 cells remain identical until this exact step. For k=16 the observed ratios D(h,16)/2^h at h=10,11,12 are 5.6602, 5.6377, 5.6697 (rounded). This suggests, but emphatically does NOT prove, an approximately linear-in-shell-width transient.

**Independent replay**: `shield_profile.cpp` computes full symmetric pairwords and normalises them by base-10 carries at EVERY step. `shield_verify.cpp` separately reconstructs each true integer as a digit vector and performs ordinary per-digit reverse-add without calling the pairword engine; it rechecks all 35 first-passage values at every step, including correct central digit 0 versus 9. `shield_independent.py` reconstructs canonical integers via decimal strings and Python arbitrary-precision bigint addition (`int(str(x)[::-1])`), checking the k=16 first-passage times independently for h=4..10 (h4=6, h5=84, h6..10 as in table). These do not use the same source code for the arithmetic. `run_shield.sh` compiles and runs both C++ checkers, compares the computed CSV against `shield_data.json`, and invokes the Python bigint controls. All data are small and deterministic; no state cap or random sampling affects the tabulated results.

**What breaks, and next construction**: the disturbance eventually reaches every tested exterior window. This is not an absorbing centre, a stable glider, or a stationary boundary cycle. The best new direction is to *nest* these shields at geometrically growing depths, and synchronize the time spent crossing each shell with a phase reset at the next shell. A genuine decimal certificate would require an exact recursive time renormalisation and a finite proof that the outer nonpalindrome witness survives all stages; none is obtained here. Finite data do not imply an all-h lower bound, perpetual non-palindromicity, or anything special about 196.

Reproduce from repository root: `sh calculation/new_structures/agent-N15/run_shield.sh`. Only new files are added; no shared code or Lean modules are edited.
