# Agent X01: overflow-locked absorbing-9 reservoir in actual decimal integers

Label: **COMPUTED** (20,001 exact symbolic states plus independent whole-integer replay). Not a Lean proof or an infinite Lychrel certificate.

## Mechanism and exact per-step accounting
All digit words here are least-significant first. Write N = U ++ 9^L ++ V, with |U|=|V|, L>=2, and nonzero final digit of V. The ordinary reverse-and-add carry map from the N23 two-wall construction gives lower digits lo, an interior first digit z=8+c, upper digits hi, and leading overflow gamma in {0,1}. The preliminary new central 9 length is L+gamma-2. Removing r matching outer 9 pairs from the new endpoints restores the canonical central 9 band, so
    L_next = L - 2 + gamma + 2r.
This is an exact integer identity for each transition and independent of the initial L while the band stays >=2. The **overflow lock** is the additional *orbit property* r=1-gamma. Under that property, L_next=L-gamma, i.e. only overflow consumes one unit; a nonoverflow step replenishes exactly its two-digit baseline cost. That property is not proved to persist forever.

## Positive decimal family
Seed (most-significant-first) N0(Q)=49(99)^Q59. The program x01_pump.cpp explicitly checks U != reverse(V), carry, overflow, maximal boundary trimming, and r=1-gamma at EVERY t=0..19999. At Q0=4149 the central band lengths decrease from 8298 to 3, with 8295 overflows, 11705 nonoverflows, exactly 11705 trims, no trim count beyond one, and 0 lock violations. The transducer's endpoints are independent of Q while L>=2, so the same checked 20,000 steps and nonpalindromicity hold for EVERY integer Q>=4149. With 4148 the prescribed invariant would have L=1 at t=20000; it is NOT a no-go or an observed palindrome.

The full integer N0(4149) has 8302 digits. x01_oracle.py calculates 20000 genuine additions using Python arbitrary-precision integers and decimal-string reversal, with no symbolic transition function, and independently checks every state for palindromicity, centred 9-run and the relation L_next=L-gamma. It reports final 16597 digits, L=3, 8295 overflows, final decimal rolling checksum mod 1000000007 = 13994719, and accumulated state pathhash 289024506. All printed checkpoints, including 0,1,...,8,88,100,300,1000,5000,10000,20000, match the C++ two-ended arithmetic output byte for byte. No 20,000-step result for the unrelated decimal seed 196 is claimed.

## Defect-budget comparison and future direction
N23's 12(99)^Q34 baseline at t=20000 consumed 12030 central 9 digits and required Q>=6016; this X01 family consumes only 8295, requiring Q>=4149 (31.0% lower Q), because all 11705 zero-overflow phases repay the preliminary two-cell cost. Although the fuel consumption is lower, each overflow still consumes 1. A valid infinite construction would need an exact *recharge/handoff* macro-edge (a phase in which r>1-gamma or a second reservoir pays for this one), and then a finite checked return to the same exterior boundary state. Mere finite pumpability in Q does not imply an infinite integer.

## Reproduction
From repo root: sh calculation/new_structures/agent-X01/reproduce.sh. It compiles the C++ transducer, runs the independent Python bigint oracle, diffs every printed checkpoint, and verifies terminal counts and checksums. The checked data summary is trace_20k.json. No Lean files are touched. A full repository verify.py --changed run was unavailable locally because the shell could not resolve github.com; no claim of that command passing is made.
