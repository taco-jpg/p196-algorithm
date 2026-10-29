# AgentX12TwoClock20000
**COMPUTED**: TWO explicit positive base-ten integer orbits, both nonpalindromic at every t=0..20000, with independent decimal digit-array and base-1000-limb *integer* reverse-and-add equality at each state (40,002 full-number comparisons).
Initial paired coefficients: P_(q,r)=B ++ W^q ++ C_r ++ rev(W)^q ++ rev(B), with q=300, r=20000 or 20001, B (39 digits) and W (20) the rooted decimal p8/m20 exterior, C_r=[8,0,0]++U++1^r++[16]++1^r++rev(U)++[0,0,8], U=1^40 except U[13]=7,U[20]=7,U[30]=6.
Full pairwords preserve a symmetric ONE-coefficient insertion relation on EVERY one of 20,001 states, with inserted symbol cycling 2,4,8,16,14,10 after t0. The splice moves exactly -44 *absolute* coefficient positions per 264 steps on each of 19,737 checked windows.
Both orbits keep the **entire phase-8 rooted B exterior** at all 20,001 states; 20,000 overflow bits are exactly (10)^10000. Palindrome tests are performed on actual integers (zero hits).
For r=20000, digits 52165 -> 62165, final splice cut 22749, FNV64 digit hashes (LSD first) 769a482b8c36ccfa and 402e99c32c98dd80 for r and r+1.
Source: `calculation/new_structures/agent-X12/beat20k.cpp`; data `calculation/new_structures/agent-X12/observations20k.json`; details `reports/AgentX12TwoClock20000.md`.
Reproduce: `g++ -O3 -std=c++17 calculation/new_structures/agent-X12/beat20k.cpp -o /tmp/agent_x12_20k && /tmp/agent_x12_20k 300 20000 20000`.
**Not claimed:** a certificate for infinite time, a finite return of the entire centre, a theorem for all q/r, or a base-10 result about 196.
