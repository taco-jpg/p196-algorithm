# Exact one-step carry-excursion delay bound for the decimal p12/m9 lattice

**PAPER PROOF with a complete finite-state decision.** This theorem supplies a precise conditional all-bulk-width upper bound on how long one *connected carry excursion* can be invisible under the pairword successor map. It complements, rather than contradicts, `Agent5P12NonErasingFrontJump`: that counterexample uses two separated source components, the first of which resets to baseline before the second is encountered. A bound for actual periodic centres is NOT claimed.

## Full statement

Fix any of the twelve temporal rows of the published base-10 period-12, spatial-period-9 lattice (`calculation/decimal_frontier/lattice_kinks/data/lat_p12m9.txt`). Consider two realizable palindromic coefficient words of the same length, both with the common exterior B_t, the same final overflow bit g_t and identical coefficients from the exterior up to their first lower-half mismatch j. Assume j and the next twelve lower positions lie safely inside the periodic bulk, away from the centre and the exterior. Compare their exact full next pairwords.

**Either** a successor coefficient differs at a lower index no later than `j+L_t`, **or** while matching the output pair coefficients an exact two-sided normalization cut state returns to the baseline cut state within the first `L_t` matched columns after j. Here

```
t :    0  1  2  3  4  5  6  7  8  9 10 11
L_t:   9 11  7  0  9 11  7  0  9 11  7  0
```

The bound is width-independent. Returning to the baseline cut ends the current local carry excursion and permits a **different, disconnected** defect later; therefore the theorem does not assert a global first-successor-defect speed bound if the input is permitted multiple components. `L_t` is the exact maximum matching-excursion length in the finite abstract transfer graph; no physical witness attaining the maximum is claimed. In phase 3,7,11 the first differing coefficient forces an immediate output difference if the earlier outputs match.

## Exact finite-state proof

Let O be the decimal carry normalization of the first symmetric coefficient word P. Its next palindromic coefficient at index i is `O_i+O_(n+g_t-1-i)` (with the optional terminal overflow digit). At the first lower-half input mismatch j, all lower incoming carries still match. If all successor pair coefficients before j also agree, the corresponding upper output digits agree (because their lower partners are unchanged), and the last exterior upper outgoing carry at j is likewise the baseline carry. Thus the two-sided transfer starts from the exact unmodified cut state and its **first** chosen replacement coefficient must differ from P_j. If an output pair mismatch occurred earlier, the theorem is already satisfied.

If g_t=0, the transfer state is `(r,a,b)` with r the lower position modulo the nine-site lattice, a the incoming lower carry, and b the outgoing upper carry at the reflected cell. The exact edge choices for replacement coefficient x∈{0,...,18} and guessed upper incoming u∈{0,1} are

```
b = floor((x+u)/10),
(x+a)%10+(x+u)%10 = S_r,
(r,a,b) -> (r+1 mod 9, floor((x+a)/10),u).
```

If g_t=1, reflection pairs lower coefficient position i with normalized upper position n-i, the mirror of the *previous* lower coefficient, so the state needs its last chosen lower coefficient v: `(r,a,b,v)`. Every edge is similarly determined by

```
b = floor((v+u)/10),
(x+a)%10+(v+u)%10 = S_r,
(r,a,b,v) -> (r+1 mod 9, floor((x+a)/10),u,x).
```

The zero-overflow graph has at most 9*2*2=36 states, the overflow graph at most 9*2*2*19=684. All cell/carry target data `S_r` are exactly nine-periodic when safely in the bulk: each row has frequent carry-reset coefficients outside the neutral value 9. The previous two committed transfer proofs establish this finite reduction and independently checked its arithmetic against actual one-step decimal digits. Here we use those same formulas and the exact repository lattice input, but ask a **different question**: how long can output equality continue before a nonbaseline carry state either (a) returns to baseline, or (b) has no pair-equality edge and must generate a successor mismatch?

For every temporal phase t and every first-defect residue r (108 rooted graphs), enumerate every allowed first replacement x != q and **all** later edges with x∈0..18, u∈{0,1}. Stop each path upon returning to the unchanged baseline two-sided state; exclude baseline states when testing for directed cycles. The complete reachable nonbaseline subgraph is a **DAG** in every one of these 108 cases. Its longest directed path is computed by dynamic programming in reverse DFS postorder, with a matching edge count of one for the first changed site and one for each later pair-equality edge. The largest graph delay per t is precisely the L_t table above, globally 11. Since a DAG has no arbitrarily long path, no first carry excursion can remain both nonbaseline and pair-output-invisible for more than L_t columns, no matter the physical bulk width.

In particular, when an excursion survives 11 matching columns in phase 1/5/9 without returning to baseline, the next column cannot preserve pair agreement. The theorem does **not** claim that the source defect has been erased if the normalized pair coefficients match for several columns: complete erasure requires a baseline state return, checked explicitly by the graph.

## Reproduce

```
python3 calculation/decimal_frontier/lattice_kinks/code/k2_component_dag.py
```

The standalone script imports the two sibling exact transfer encodings (already committed and tested), reads the checked-in p12/m9 lattice, generates **all** first-defect edges and all reachable continuation edges, checks the absence of nonbaseline directed cycles by three-color DFS, and computes the exact graph matching-delay upper bounds. No solver, memory/time/state cap or approximation is used. It prints the 108 finite graph decisions and asserts the complete twelve-phase maxima `(9,11,7,0)*3` and the global maximum 11. Reproduction needs only standard Python 3, no Lean or optional SAT packages.

This is a first-step result with a fixed pure-lattice baseline, not a theorem about a globally persistent front across a 12/72-step period, nor a proof of a decimal Lychrel number.