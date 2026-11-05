# r11e: chain 1, branch 3 | r — the missing lemma "only N12" (status: UNDECIDED, gap sharpened)

Directory `~/p196_run/r11e/` on the Studio; copy in `~/Desktop/p196_studio/r11e/`. Repo read-only, nothing pushed.
Labels: PAPER PROOF / COMPUTED / UNDECIDED only. This continues an earlier agent of the same run (it was cut off by a
network drop). Its files are kept, and section 1 records its state.

**Target lemma L(k).** Take k ≥ 3. Every exterior with clock (0001)^{3k} is an N12 repetition. Equivalently, Φ^12 restricted
to clock (0001)^3 has no period-k orbit other than the three rotations of N12.
**Status: UNDECIDED for every k ≥ 3.** I found no counterexample, so there is nothing to replay with big integers.
Below are three new PAPER PROOF reductions, one k-uniform partial result (inherited and re-run), and an exact
statement of what is still missing.

---------------------------------------------------------------------------------------------------------------
## 1. Inherited state (previous agent, files in this directory)

- `src/bxd.cpp` is repo `bx.cpp` with three added flags:
  - `-from P L H Y` starts from the cut u^k, where u is a P-periodic cut;
  - `-desync` keeps only first steps whose cut word is not invariant under the 12-shift;
  - `-first0` applies the root rule at depth 0.
  
  `src/bxs.cpp` adds `-stack`, which starts at an accepting 9-sea cut and counts non-trivial accepts.
- `py/n12cuts.py` → `py/n12cuts.txt` lists the 56 N12 cut states u_h (h = 0..55), after verifying the N12 witness under
  the exact mirror.
- `bx_p36.out`: the full search for P = 36 (k = 3) is **CAPPED** at 2·10^8 states, depth 10, 15.4 GB RSS. A direct P(9)
  run is out of budget.
- `desync_all.out` runs a desync search from u_h^k for every h ≤ 54 (cap 1.5·10^8). COMPUTED:
  - k = 2: 52/55 EXHAUSTED; h = 3, 42, 47 CAPPED;
  - k = 3: 52/55 EXHAUSTED; h = 19, 20, 42 CAPPED;
  - k = 4: 34/55 EXHAUSTED; 21 CAPPED.
  
  No accept appears anywhere. **Scope caveat (new):** these runs start only from N12's own cuts. By §2 the first
  desynchronisation may happen from *any* P = 12-reachable cut, so these runs are a sub-case and not a reduction of L(k).

## 2. New PAPER PROOF lemmas

Notation follows r11g/PROOF.md. The interface (cut) at height x is I_x = (c, δ, ρ), and the clock has an overflow.

**Lemma D1 (column is determined by its two cuts).** In an accepting history, the cell series v_x is a function of
(I_x, I_{x+1}), and that function commutes with time shifts.

*Proof.* At an overflow time t, the output letter contains δ'_t and ρ'_t = (v+δ'_t) mod 10, and the constraint is
⌊(v+δ'_t)/10⌋ = δ_t. Hence v_x[t] = 10δ_t + ρ'_t − δ'_t. From that time on, v[t+1] = (v[t]+c_t) mod 10 +
(g_t ? ρ_t : (v[t]+δ'_t) mod 10) determines the whole cycle. ∎

**Corollary D2 (desync characterisation).** An exterior with clock (0001)^{3k} is an N12 repetition if and only if
every cut I_x of its (unique, by Theorem B) history is 12-periodic.

*Proof.* (⇐) By D1 every column is 12-periodic, so the exterior has period 12, and P(3) gives N12. (⇒) is clear,
because the cuts are the carry streams (forward c, backward d, R), and these are 12-periodic when B_t is. ∎

**Corollary D3 (first-desync reduction).** Let a counterexample be given, and let j ≥ 1 be the least height with I_j
not 12-periodic. Then I_{j−1} = u^k, where u is a cut reached by a 12-periodic path, i.e. u ∈ R12 (the P = 12 BFS set,
136,653 states without quotient). The step I_{j−1} → I_j is a desync step. Two kinds of desync step exist:
- (i) the column v_{j−1} is not 12-periodic;
- (ii) the column is 12-periodic, and only the free bit δ' at overflow times differs. This bit is free whenever
  v ≠ 9, and it does not change the column.

Kind (ii) shows that desync steps exist from almost every u, so the one-step filter is empty. All the content lies in
the continuation.

**Lemma C (mod-9 charge, exact).** Let C(B) = ΣB_i mod 9. This does not depend on the 9-padding. Then
C(Φ B) ≡ 2C(B) + 1 − 2e1(B) (mod 9).
- The gam = 0 case: ΣF ≡ ΣB − e1 and ΣR ≡ ΣB + (1−e1) − gam.
- The gam = 1 case adds the +1 and the top entry 9(1−e1), which gives the same formula.

COMPUTED check (`py/chk_charge.py`): 199,592 random B against the mirror, 0 mismatches. On N12 the sum is Σ e_t 5^t ≡ 0.

Consequence for a period T = 12k: since 2^6 ≡ 1, the only condition is Σ_t e_t 5^t ≡ 0 (mod 9). This is one linear
congruence on the e-word alone. **It cannot separate anything from N12^k:** it is a function of e, and it is
automatically satisfied by every e that is a 12-periodic repetition of a valid e. The charge route of REPORT_205 §5–6
(bulk letter invertible mod 9) does not apply here, because the bulk letter is 9 ≡ 0.

## 3. k-uniform partial result (top rigidity) — PAPER PROOF + COMPUTED

`py/stack_uniform.py` (previous agent) was re-run by me, with output in `py/stack_uniform.out`. Let u = (e, 1−e, 9e)
be the accepted 9-sea cut of N12, and let A and AT be the one-column and two-column transducers above u. The run gives:
- (b) CL(AT) ⊆ CL(A) (5,138 product states, exhaustive);
- (c) and (c'): every cycle of accepting-label edges has column value 9.

I checked the argument.
- By induction on height, (b) shows that every cut above u^k lies in CL_k(A), for every k.
- (c') shows that the last column into acceptance is all 9.
- A 9-column with accepting output forces an accepting input: a 9-column with input (c, δ, ρ) is consistent iff
  δ = 1−c and ρ = 9c.
- Going down one column at a time, all columns above u are therefore 9.

**Lemma T.** For all k, a history that passes through u_acc^k is N12^k. So a counterexample never contains N12's
accepted cut.

**Limit of the method (COMPUTED, `py/stack_h.py` → `py/stack_h.out`).** The same closure test from every N12 cut u_h
gives:
- h ≤ 52: (b) **fails at once**, with a closed walk of length 12 and at most 10^4 states;
- h = 53, 54, 55 (already the 9-sea): (b) holds.

So the k-uniform automaton certificate exists only once N12 is complete. Any middle cut leaves a cyclic-word language
that is not closed after one column.

## 4. The gap, stated exactly (UNDECIDED)

By D2, D3 and T, L(k) is equivalent to the following.

**(G_k)** There is no u ∈ R12 and no WIRE-accepting path of period 12k from u^k whose first step is a desync step.

Facts and limits for G_k:
- It is proved for k = 2 (ReachDisk, now unconditional through r11g).
- For k ≥ 3 it is open. The previous agent's runs cover only 55 of the 136,653 states u, and even those are capped
  in places.
- The K-head method fails at the bottom, because N12 is a 12-walk in every G_K.
- The stack method fails at every middle cut (§3).
- The charge invariant is blind (Lemma C).
- i481's S/L result shows that cell 2 at phases ≡ 0 (mod 4) is pure S for r < 57. That fixes one cell row and does not
  bound j.

What would close G_k uniformly is a ranking that strictly decreases along every desync continuation and is bounded at
acceptance. It could be built from the cyclic-language automaton of the cuts above u (as in §3), but that automaton is
not finite-closing below the 9-sea. I have no candidate. Feasible next steps:
- (a) run bxd from all u ∈ R12 with k = 3, sharded on 4 threads, with a cap per u. This is still not a proof when caps
  are hit.
- (b) a two-column closure (AT ⊆ ATT) at middle cuts, to see whether the closure depth stays bounded.

## 5. Files (all small; nothing large left, no background processes of mine)

| file | content |
|---|---|
| `py/chk_charge.py` | Lemma C check (199,592 cases, 0 mismatches) and the N12 charge |
| `py/stack_uniform.py`, `.out` | Lemma T certificate (inherited script, my run) |
| `py/stack_h.py`, `.out` | closure test from every N12 cut: fails for h ≤ 52 |
| `desync_all.sh`, `.out`, `src/bxd*` | inherited desync runs (sub-case only) |
| `bx_p36.out/.err` | inherited direct P = 36 run, CAPPED |
