# p8 fixed-centre 80-step return: rec0 control + rec1 exhaustion (C lengths 4..12)

Directory: this folder.
Repository `~/Projects/p196-algorithm` was only read (klib.py, p8_scc.txt, agent-N10, agent1_p8_ref80). No git operations, no ssh.

Family: P(q,C) = B0 W0^q C rev(W0)^q rev(B0), C a legal palindromic coefficient centre (symbols 0..18, odd length -> even midpoint), |C|>=4.
Test: T^80(P(5,C)) == P(6,C) (whole pairword), plus clock (overflow at step t equals g_t, g=10101010) and final length 2*159+|C|.

## 1. Applicability of the R03A1 iff argument to rec1 (B1 |B|=39, W20)

`lemma.py REC` (output `lemma.log`), same checks for rec0 and rec1:

1. COMPUTED: the klib rec1 rows B_t, W_t reproduce themselves under 16 genuine `pairword_step`s of B0 W0^20 mirror; clock 10101010.
2. PAPER PROOF (finite symbolic kernel, N10 lemma generalised): for all 8 phases, W_t and rev(W_t) are carry-absorbing (outgoing carry independent of incoming), B_t's outgoing carry equals the steady W carry, and with **formal centre tokens** (lengths 0..24, both centre carry-outs u=0,1, r=1..4) T(I_t P) = I_{t+1}(T P) holds in 640/640 cases, clock forced. I_t inserts one literal 20-coefficient W_t block after the 39-site cap (and mirrored). So the rec1 80-step insertion is I_0, an injective literal 20-coefficient insertion, exactly as for rec0. The block-factorisation step from the finite kernel to all r / all centres is the same as in AgentN10UniversalPumpLemma (W absorbing).
3. COMPUTED (universal two-inlet shield, Agent1P8Ref80 method, both inner carries): rec1 passes all 81 rooted states with B_t W_t kept iff q>=5 (q=4 fails at t=74; rec0: q=4 fails at t=78). Prefix 139->73 (rec0 139->77). **Threshold for rec1 is q0=5.**
4. Every rec1 B_t has odd coefficients ([20,15,15,18,25,18,18,21]) -> shielded states are never palindromes.

Hence PAPER PROOF (conditional on the N10-style block factorisation, same status as R03A1): for rec1, for each legal C with |C|>=4 and every q>=5, T^80(P(q,C))=P(q+1,C) iff T^80(P(5,C))=P(6,C). Additionally, independent of the universal shield, the enumerator checked per centre that all 80 intermediate states carry the exact B_t W_t prefix (guardfail=0 everywhere).

## 2. Results (COMPUTED, C++ exact arithmetic, q0=5)

| rec | |C| | centres | returns | clock dev | length err | guard fail | max prefix |
|---|---|---|---|---|---|---|---|
| rec0 | 4 | 361 | 0 | 0 | 0 | 0 | 134 |
| rec0 | 5 | 3,610 | 0 | 0 | 0 | 0 | 134 |
| rec0 | 6 | 6,859 | 0 | 0 | 0 | 0 | 139 |
| rec0 | 7 | 68,590 | 0 | 0 | 0 | 0 | 140 |
| rec0 | 8 | 130,321 | 0 | 0 | 0 | 0 | 140 |
| rec0 | 9 | 1,303,210 | 0 | 0 | 0 | 0 | 141 |
| rec0 | 10 | 2,476,099 | 0 | 0 | 0 | 0 | 141 |
| rec0 | 11 | 24,760,990 | 0 | 0 | 0 | 0 | 142 |
| rec0 | 12 | 47,045,881 | 0 | 0 | 0 | 0 | 141 |
| rec1 | 4 | 361 | 0 | 0 | 0 | 0 | 133 |
| rec1 | 5 | 3,610 | 0 | 0 | 0 | 0 | 136 |
| rec1 | 6 | 6,859 | 0 | 0 | 0 | 0 | 138 |
| rec1 | 7 | 68,590 | 0 | 0 | 0 | 0 | 140 |
| rec1 | 8 | 130,321 | 0 | 0 | 0 | 0 | 140 |
| rec1 | 9 | 1,303,210 | 0 | 0 | 0 | 0 | 144 |
| rec1 | 10 | 2,476,099 | 0 | 0 | 0 | 0 | 141 |
| rec1 | 11 | 24,760,990 | 0 | 0 | 0 | 0 | 142 |
| rec1 | 12 | 47,045,881 | 0 | 0 | 0 | 0 | 142 |

Totals per record, lengths 4..12: 75,795,921 centres, 0 returns. "Max prefix" = number of leading coefficients of T^80(P(5,C)) equal to P(6,C); all are < 159, i.e. every centre fails already inside the rooted B0 W0^6 prefix. Prefix histograms: `runs.log` (HIST lines). L12 takes ~205 s on 8 threads.

**Control (rec0) vs R03A1 #6567742649 / #6567763844**: counts 361/3610/6859/68590/130321/1303210/2476099 and max prefixes 134,134,139,140,140,141,141 (L4..L10) reproduced exactly; total 4..10 = 3,989,050, 0 returns, 0 clock deviations, 0 length errors. New: rec0 L11, L12 also 0 returns (max prefix 142, 141).

Combined with section 1: COMPUTED + PAPER PROOF, for rec0 and rec1 no fixed-centre exact 80-step return exists with |C| in 4..12 at any q>=5. Not covered (UNDECIDED): |C|>=13, other return periods, evolving centres, the stacked rec2-over-rec1 exterior at small q (the iff threshold there was not separately derived; only the rec1 bulk/centre problem is addressed).

## 3. Validation
- `crosscheck.sh` / `crosscheck.log`: per-centre (prefix, clock, final length, guard) of C++ vs Python reference `ref.py` (klib.pairword_step): all centres of L4, L5 and every 37th of L6, L7, both records: 0 mismatches (12,022 centres).
- `bigint.py` / `bigint.log`: literal decimal big integers (canonical seed, 80 genuine N+rev(N)) for the max-prefix centres of rec1 L10/L11/L12 and rec0 L10/L12 plus extremes: pairwords agree at every step, no palindrome, no return.
- No return was found, so no multi-period replay was needed.

## Sources
- `centre.cpp` (enumerator; `./centre recR.tbl L 5 THREADS [dump]`), `export.py` (writes rec0.tbl/rec1.tbl from klib.load_rec)
- `lemma.py` (+`lemma.log`), `ref.py`, `crosscheck.sh`, `bigint.py`, `runs.log`
