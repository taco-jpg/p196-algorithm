# W21: carry-provenance terminal repair in the base-10 period-8 exterior

**COMPUTED**, finite scope only. Use the pre-existing phase-0 rooted exterior B and period-20 band W defined in replay.cpp. The N26 repair R of length 20 (see plateau_search.cpp) gave a terminal 40-column half-core W++R with first rooted-39-column mismatch at t=88c+340 after c extra initial W copies. This work found a new equal-length terminal half-core:

Q = [17,10,13,11,18,15,1,2,10,4,1,8,17,4,10,2,15,16,8,0,5,4,14,9,8,0,3,11,18,1,0,9,0,17,9,8,5,1,3,1].

Let P_c (least-significant coefficient first) be B ++ W^c ++ Q ++ reverse(Q) ++ reverse(W)^c ++ reverse(B). Realize its decimal integer by symmetric digit pairs (floor(p/2), p-floor(p/2)), making 158+40c digits. For individually tested c=0,1,3,225, the first rooted exterior mismatch is at t=88c+460 and coefficient index 38: **120 more exact exterior steps with zero additional digits** compared to N26 W++R. This affine formula is an observation for the stated cases, not an all-c theorem.

**Carry source.** In W++R at t=251 (c=0) the high-end carry into mirror column 38 is 0 while the rooted bulk has 1; both high coefficient inputs are 10 and low output digits 0. Thus the high output digits are 0 versus 1 and at t=252 pair coefficient 38 is 0 versus expected 1. For Q the same event occurs only at t=459, with the first wrong coefficient at t=460. The repair changes the inner signal reaching the high-side carry interface rather than altering the fixed root coefficients. This identifies the first mismatch's exact cause.

**Search.** A deterministic mt19937 plateau walk (seed 992042) started at W++R, changed one or sometimes two of 40 half-core coefficients, accepted non-decreasing root-survival times plus rare downhill moves, and restarted from its incumbent every 50,000 trials. At trial 174243: score 362; at 197691: score 460 and the listed Q. Reproduce with plateau_search.cpp 350000; output must end final_best=460. This is heuristic synthesis, not an optimality proof.

**Independent 20,000-step actual decimal replay.** At c=225 the initial integer has 9,158 digits. At *every state* t=0..20,000 inclusive, replay.cpp checks the entire exact symmetric pairword against a separate coefficient-only normalizer, directly tests all decimal digits for palindromicity (none), and checks the rooted 8-phase exterior. Each phase's 20-periodicity is checked from reference column 39 onward. The minimum exact matching prefix is 98 coefficients, hence the full pairword has B_phase ++ W_phase^k ++ C_t ++ reverse(W_phase^k) ++ reverse(B_phase) with k>=2 and an otherwise unrestricted symmetric central C_t at every state. At t=20,000 the integer has 19,158 digits. The independently implemented gmp.cpp uses native GMP integers n <- n + int(reverse(decimal(n))) and finds no palindrome at any of the 20,001 states; checkpoint lengths and exact low-to-high digit-string FNV64 hashes agree with replay.cpp. The first rooted mismatch at c=225 is t=20,260 (verified through t=20,262); after that the rooted template is not claimed. Q++Q is **not** regenerative: c=0 fails at t=258.

Reproduce from repository root:

    g++ -O3 -std=c++17 calculation/new_structures/agent-W21/replay.cpp -o /tmp/w21_replay
    /tmp/w21_replay 225 20000
    /tmp/w21_replay 225 20262
    g++ -O3 -std=c++17 calculation/new_structures/agent-W21/gmp.cpp -lgmpxx -lgmp -o /tmp/w21_gmp
    /tmp/w21_gmp 225 20000
    g++ -O3 -std=c++17 calculation/new_structures/agent-W21/plateau_search.cpp -o /tmp/w21_search
    /tmp/w21_search 350000

Compact checksums are in trace.txt. **Not claimed:** an infinite base-10 Lychrel number, a repeating centre, a Lean theorem, or the first-failure formula at untested c. A constructive next direction is a *pair of terminal patches* with compatible incoming/outgoing two-sided carry signatures after an 88-step macro-cycle, instead of merely increasing initial shielding. Local git clone failed DNS; repository-wide tools/verify.py --changed could not be executed without a checkout. Both arithmetic C++ implementations and the deterministic search compiled and ran locally.
