# Agent N04: folded-regular invariant format and moving phase-front controls

**PAPER PROOF (format soundness); COMPUTED (finite controls).** Neither a decimal certificate nor a claim about 196.

## 1. New certificate format: a regular invariant of folded pairwords

For base `b>=2`, define the symmetric pairword of a canonical number `N` with `n` digits by `P_i=d_i+d_{n-1-i}` (least-significant first). Encode the halfword `u=P_0...P_{h-1}` plus an explicit even/odd length marker; for odd `n=2h+1`, append the central coefficient `P_h=2d_h`. Every noncentral coefficient is in `[0,2b-2]`, and `P_0>0`. Its entire reverse-and-add successor depends **only on P**, not on the chosen digit decomposition of `N`.

A **folded-regular invariant certificate** is a DFA `A` recognizing a nonempty language `L` of these marked halfwords such that (i) all its words encode valid pairwords and have some **odd-valued** coefficient; (ii) the following exact, nondeterministic finite-state two-carry transducer `R_b` maps every word of `L` to a word of `L`. The transducer reads outer-to-inner, outputs the successor folded coefficients, and is allowed one additional terminal output symbol because the digit length can increase by one. There is no stationary centre, bound on its width, fixed period, or individual band-length constraint. In particular, `L` may contain regular languages of words `U^a I V^c`, where phase-interface location and two domains can change asynchronously; DFA closure holds for the entire language, not for a fixed template cycle.

### Exact transducer equations

Write `p_i=P_i` for `0<=i<h`, `ell_i=c_i` for the ascending carry, and `r_i=c_{n-1-i}` for the carry into the mirrored high digit. Both carry bits are in `{0,1}`. Initially `ell_0=0`; guess `r_0`, and set the overflow `g=floor((p_0+r_0)/b)`. For each `i<h`, define

    L_i = (p_i+ell_i) mod b,  U_i=(p_i+r_i) mod b,
    ell_{i+1}=floor((p_i+ell_i)/b),
    r_{i-1}=floor((p_i+r_i)/b)  for i>=1.

Then the successor folded coefficient is `P'_0=L_0+U_0` if `g=0`, but `P'_0=L_0+1` if `g=1`; for `1<=i<h` it is `P'_i=L_i+U_i` if `g=0`, and `P'_i=L_i+U_{i-1}` if `g=1`. The transducer stores `(g,ell_i,r_{i-1},U_{i-1})`; guessing `r_i` and checking the descending equation uses constant memory, with `U_{i-1}` only needed if `g=1`.

At the centre, for **even** input length `n=2h`, require `r_{h-1}=ell_h`. If `g=0`, the target halfword has no extra coefficient; if `g=1`, append target centre `2U_{h-1}` (new odd length). For **odd** input length `n=2h+1`, with centre `z=P_h` (even), require `r_{h-1}=floor((z+ell_h)/b)` and set `Z=(z+ell_h) mod b`. If `g=0`, append target centre `2Z` (new odd length); if `g=1`, append `Z+U_{h-1}` (new even length). These are the entire acceptance conditions. `P_0>0` prevents leading-zero ambiguity. The case `n>=2` suffices for certification, and the checker restricts to it.

### Soundness theorem (PAPER PROOF)

If `L` is a nonempty regular language of valid folded pairwords, every member has at least one odd coefficient, and `R_b(L) subseteq L`, then every canonical starting integer `N` with folded pairword in `L` has a reverse-and-add orbit that never reaches a palindrome. Choose a valid digit decomposition for one accepted word. Inductively, the successor's pairword is the unique output of `R_b`; DFA closure keeps each folded pairword in `L`. A palindromic `N` would have `P_i=2d_i` for every `i`, contradicting the odd-coefficient condition. The two-carry equations follow directly from grade-school addition at corresponding outer and inner digit positions, including the unique possible length overflow. No assumption about 196, distribution of digits, or empirical recurrence enters this proof.

Because `R_b` has finite states and bounded input/output lag (zero or one final symbol), `R_b(L) subseteq L` is **decidable** by finite automata: intersect `R_b` with the product of the DFA for `L` and the complemented DFA for `L`, and check emptiness of the resulting reachable graph. Nonemptiness, valid-word restriction and odd-coefficient restriction are separate regular-language emptiness tests. This gives a finite, inspectable certificate once a suitable DFA is found. A Lean implementation can define the transition table with `Fin (2*b-1)` coefficient symbols and two carry bits, prove each transition matches normalization using quotient/remainder lemmas, prove final-centre soundness by the two cases, and apply finite-graph reachability with a Boolean checker verified by `decide +kernel`; no unbounded arithmetic replay is required in the final certificate.

## 2. Constructive use: moving phase front

Start from the published decimal `p=8, m=20` SCC `rec0` (source file `calculation/decimal_frontier/lattice_formats/p8_scc.txt`). Let `B` be its first-time 39-symbol transient prefix and `W_t` the time-dependent 20-symbol bulk. Form a symmetric length-2000 pairword whose lower half is `B`, then unshifted `W_0` until position `300+offset`, then the same bulk shifted by `shift` modulo 20 until the centre; mirror around the centre. For `offset=0..19`, `shift=1..19`, test 380 separate initial *domain walls*. The natural language for search is `B U^a I V^c mirror(...)`, with a DFA tracking the active interface and its carry state. If an invariant DFA of this kind exists and excludes all-even words, the theorem proves a decimal Lychrel integer without solving a fixed-width periodic centre.

The literal uncorrected splices, however, emit an expanding defect interval rather than a stable travelling glider. For each time `t`, inspect indices `[seam-45,seam+160)` and record the first site not equal to the unshifted lattice `W_t` and the last not equal to the shifted lattice. Their inclusive span width at `t=8,16,32,64` has minimum `3,8,17,39`, median `7,13,26,55`, maximum `10,17,31,60` over the 380 cases; exact alternating overflow `10101010...` holds for every one of the 380 seeds through step 64. These are *finite observations*, not an exclusion of corrected moving fronts or longer-time dynamics. Independent ordinary decimal big-integer replay for three representative splices (2000 to 2032 digits, all 64 steps) reproduces the complete coefficient pairword at every step.

**Search redirection:** replace a passive single cut with a *carry-regenerating, finite-state active interface*, potentially allowing several admissible local words at each seam and a nontrivial two-sided glider language; search for a closed DFA rather than enumerating longer dead centre widths.

## 3. Reproduction

From repository root:

    python3 calculation/new_structures/agent-N04/folded_transducer.py
    python3 calculation/new_structures/agent-N04/phasefront_scan.py --output /tmp/n04_scan.json
    python3 calculation/new_structures/agent-N04/independent_replay.py --output /tmp/n04_bigint.json

Exhaustive transducer control: b9 has 2,880 checked folded words with even n=2,4 and odd n=3,5; b10 has 3,960; each with all possible valid coefficients for n<=5. Separately 3,000 random words per base (lengths up to 201 digits), all checked against ordinary big-integer addition: zero disagreement in both suites. Both expected outputs and exact command summaries are in `calculation/new_structures/agent-N04/*.json`. Python standard library only.

**Claim scope:** exact formal arithmetic and decidable finite-state invariant criterion for arbitrary `b>=2`; a computed 380-seed uncorrected phase-splice diagnostic to 64 decimal steps; three 64-step independent big-integer controls. **NOT CLAIMED:** existence of a nonempty decimal closed language/DFA, proof that any candidate orbit is Lychrel, exhaustive glider search, or a universal phase-wall-speed theorem.