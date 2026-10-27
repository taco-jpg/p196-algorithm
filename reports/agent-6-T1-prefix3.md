# Agent 6: T1.C-prefix3-product-D6

## Result and limits

**COMPUTED + PAPER PROOF of sound finite projection, not Lean-verified.** Every accepted base-10 A120 one-neutral-band `cycleOK` certificate has **some center phase of coefficient-word length at least 7**. The bounded necessary graph for `|C_t|<=6` at every phase and every period is acyclic. This does not establish a decimal Lychrel number, rule out all base-10 one-band certificates, or restrict centers that ever exceed length 6.

## Graph and why absence of a cycle is sufficient (PAPER PROOF)

For the accepted edges, `e2=1-e1`. On any closed chain, every center is symmetric, since raw `nextC` is symmetric and removal of outer pairs of neutral 9s preserves symmetry. The empty or all-neutral center cannot flip its carry and is excluded. At a fixed center bound D, enumerate all nonempty symmetric coefficient lists over 0..18, retain exactly those with `norm(C,e).carry=1-e`, and include **every** admissible symmetric trim in each `nextC` step. Center states and edges are exact.

For the exterior, append a *formal infinite neutral-9 suffix* to finite B and retain the first R coefficients a. The first lies in 1..18 (empty B represented by a0=9) and every later digit lies in 0..18. Every permitted trailing-9 B trim preserves this padded prefix. Treat reverse-normalization carry `h_R` from the unknown deeper exterior as **either 0 or 1**, independently on each edge. Then calculate backwards `h_i=floor((a_i+h_(i+1))/10)`; the true overflow is `g=h_0`. Compute forward `d_i=(a_i+l_i)%10` with `l_0=0, l_(i+1)=floor((a_i+l_i)/10)`, and reverse-side `r_i=(a_i+h_(i+1))%10`. The next exterior prefix is:

- `a'_0=d_0+(g?1:r_0)`
- `a'_i=d_i+(g?r_(i-1):r_i)` for `1<=i<R`.

Both possible unresolved carries are allowed; this is a **sound overapproximation** of all legal full exterior transitions, including empty/short B words. Couple the center and exterior projections using the **same** overflow g while allowing other carries to vary independently. Every actual finite closed A120 certificate with all centers length <=D maps to a closed walk in this finite graph. Kahn's exact indegree-zero peeling removing all vertices therefore rules out every such certificate. No period, B width, trim schedule or cycle length restriction is imposed.

## Reproduce exact computation

```sh
c++ -O3 -std=c++17 -Wall -Wextra -Wpedantic calculation/agent-6/prefix3_center.cpp -o /tmp/a6prefix3
/tmp/a6prefix3 1 4
/tmp/a6prefix3 2 5
/usr/bin/time -f 'wall=%es peak_kb=%M' /tmp/a6prefix3 3 6
```

| Prefix R | Max center D | Prefix states | Center states | Product vertices | Arcs | Peeled | Residual |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 4 | 18 | 756 | 13,608 | 18,362 | 13,608 | 0 |
| 2 | 5 | 342 | 7,614 | 2,603,988 | 2,955,526 | 2,603,988 | 0 |
| **3** | **6** | **6,498** | **14,472** | **94,039,056** | **129,065,442** | **94,039,056** | **0** |

The new R3,D6 run completed without caps: wall 3.21s; peak 737,904 KiB in this sandbox. Smaller R1,D4 and R2,D5 counts exactly reproduce prior distinct implementations by Agents 6 and 101. The source rejects unsupported bounds (R>3 or D>6), caps vertices at 100M and catches allocation failure: budget failure is not interpreted as acyclicity.

## Arithmetic validation and provenance

A separately implemented Python arithmetic reference checked all 6,498 R=3 prefix source states and their 9,747 g-labelled transitions; all 14,472 admissible D=6 center states and 24,492 center transitions; all matched the C++ transition generator. It independently tested 100,000 deterministically randomized actual exterior words of length 0..30 (including empty B), the exact integer-based `DB/DR/gam` update and all allowable terminal-9 B trims against the retained prefix: zero mismatches. These are same-agent independent-code checks, not a second agent's rerun of the 94M-state negative.

Credit: Agent 4's one-coordinate exterior necessary recurrence (#290), Agent 6 center-only and first-coordinate product results (#306, #313), and Agent 101's two-prefix D5 result (draft PR #332). This report is a new **three-prefix D6** extension, not reattribution of those results.

**NO CLAIM:** base-10 decimal certificate; universal impossibility; actual orbit-196 nonpalindromicity; Lean proof. No changes to README.md or RESULTS.md. The code-only PR is **UNVERIFIED / DO NOT MERGE** until `python3 tools/verify.py --changed` is actually run and passes in a proper checkout; the local sandbox did not run this repository-wide verifier. An independent *second agent* should reproduce the R3,D6 negative before it is treated as fully corroborated.
