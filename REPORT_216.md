# REPORT_216 — Palindrome conditions, center obstructions, 和 exact run renewal

Agent: **216**. Direction: **6**. Date: **2026-10-22**. Repository baseline: `c6902ac6c366ce018e68a810f58b400dda07145a`.

## Answer in 1 paragraph

No decimal Lychrel witness or returning template is established in 这 report. **THEOREM:** the abstraction retaining only digit-length parity 和 the single central column sum 有 exactly 29 states 和 188 realizable transitions; its 13 universally safe states reduce to 3, then to none after 2 closure rounds, excluding every nonempty universal invariant based only on 那 information. **THEOREM:** a maximal centered constant run cannot grow without overflow; on overflow its exact successor length 是 the length of the maximal centered block over the companion alphabet \(\{a,a+9\}\), minus 1. 这 gives an exact renewal balance 和 excludes persistent centered-band constructions with no companion absorption. **THEOREM:** whole-word companion blocks in residue classes \(a=1,2,3,4\), with high outer coefficient, reach a palindrome within 2 steps; the explicit growth example \(2119\to11231\to24442\) refutes the inference that a growing center alone supplies safety. The complete proofs below distinguish 这 conclusions from existing **LEAN-VERIFIED** palindrome, center, 和 extreme-run results. Bounded checks cover all 10,467 realizable profiles of lengths 1–6, all 188 abstract transitions through 836 constructed fixtures, 1000 additional transitions, 和 1000 consecutive ordinary steps from each of 2 seeds. The remaining question is whether a bounded interface can replenish the required companion material through a full bulk-symbol cycle while preserving an actual global return.

## 1. Scope, conventions, 和 existing results

All words are indexed from the units end. For a positive canonical decimal input of length \(L\), write

\[
q_i=d_i+d_{L-1-i},\qquad
c_0=0,\qquad
c_{i+1}=\left\lfloor\frac{q_i+c_i}{10}\right\rfloor,
\qquad e_i=q_i+c_i-10c_{i+1}.
\]

Append \(e_L=1\) exactly when \(c_L=1\). The output width is \(L'=L+c_L\), 和 its folded word is

\[
q'_i=e_i+e_{L'-1-i}.
\]

Every carry 是 a bit: induction from \(c_0=0\) gives \(0\le q_i+c_i\le19\), hence \(c_{i+1}\in\{0,1\}\). The carry update is explicitly

\[
f(s,x)=\left\lfloor\frac{s+x}{10}\right\rfloor
=\begin{cases}
0,&0\le s\le8,\\
x,&s=9,\\
1,&10\le s\le18,
\end{cases}\qquad x\in\{0,1\}.
\]

A realizable positive folded word is symmetric, 有 coefficients in \([0,18]\), 有 positive outer coefficient, 和 有 an even central coefficient at odd length. 这 conditions are sufficient: for every reflected pair choose its high digit as \(\min(q_i,9)\), its low digit as \(q_i-\min(q_i,9)\), 和 at an odd center choose \(q_i/2\). The high outer digit is positive. 这 realization is used below to ensure that abstract transitions come from actual integers.

**LEAN-VERIFIED — existing repository groundwork.** The following source declarations were inspected at the baseline above. Their status 是 the repository's existing source/registry status; no new Lean compilation is claimed in 这 report.

| Existing result | Exact source |
|---|---|
| Complete next-palindrome criterion | [`DecimalDigits.step_palindrome_iff`](https://github.com/taco-jpg/p196-algorithm/blob/c6902ac6c366ce018e68a810f58b400dda07145a/lean/P196/Foundations/LychrelDigitSums.lean), with `no_overflow_palindrome_iff` 和 `overflow_palindrome_iff` |
| Exact folded center equations | `FoldedDecimal.odd_center_no_overflow`, `even_center_overflow`, `odd_center_overflow`, in the same file |
| Complementary-band safety independent of the center | [`Agent109.NoPal.not_stepPal`](https://github.com/taco-jpg/p196-algorithm/blob/c6902ac6c366ce018e68a810f58b400dda07145a/lean/P196/Drafts/Agent109TemplateStepSafety/NoPalStep.lean); registered under `Drafts.Agent109TemplateStepSafety` |
| Exact maximal 0/18-run ancestry | [`RunAncestry.descendant_step`](https://github.com/taco-jpg/p196-algorithm/blob/c6902ac6c366ce018e68a810f58b400dda07145a/lean/P196/Agent1PeriodicEighteenReturn/RunAncestry.lean) |
| Central extreme-run formula 和 finite ancestry extinction | [`RunAncestry.central_run_step`, `extinct_uniform`](https://github.com/taco-jpg/p196-algorithm/blob/c6902ac6c366ce018e68a810f58b400dda07145a/lean/P196/Drafts/Agent7RunPopulationRenewal/AncestryExtinction.lean) |
| Isolated high-center transitions 和 short termination cases | [`LowDigitSumTermination.central_carry_exact`, `central_next_center`](https://github.com/taco-jpg/p196-algorithm/blob/c6902ac6c366ce018e68a810f58b400dda07145a/lean/P196/LowDigitSumTermination/CentralCarry.lean) |

Theorems 2–6 below are complete paper arguments, with executable checks. They 没有 new Lean endpoints. Existing identities are credited above; no claim of priority over uninspected literature is made.

## 2. THEOREM 1 — Exact palindrome condition, with complete carry proof

For every positive canonical decimal input,

\[
\boxed{\operatorname{Pal}(T(n))\iff
\bigl(\forall i<L,\ q_i\le9\bigr)
\ \lor\
\bigl(q_0=11\ \land\ \forall i<L,\ q_i\in\{0,11\}\bigr).}
\tag{1}
\]

这 是 the existing `DecimalDigits.step_palindrome_iff`, restated with its mechanism 因为 every later safety statement depends on both branches.

### No overflow

Assume \(c_L=0\), so reflection pairs \(i\) with \(j=L-1-i\). If the output is symmetric, then \(q_i=q_j\) gives

\[
c_i-c_j=10(c_{i+1}-c_{j+1}).
\]

The left side lies in \(\{-1,0,1\}\), while the right side 是 a multiple of 10. Thus

\[
c_i=c_{L-1-i},\qquad c_{i+1}=c_{L-i}.
\]

For \(0\le i\le L-2\), the first equality at \(i\) 和 the second equality at \(L-2-i\) give \(c_i=c_{i+2}\). 也 \(c_0=0\) 和 the second equality at \(i=0\) gives \(c_1=c_L=0\). Every carry is therefore zero, including the width-1 case. The column equation 现在 gives \(q_i=e_i\le9\).

Conversely, if every \(q_i\le9\), induction from \(c_0=0\) gives every carry zero. Hence \(e_i=q_i\), a symmetric word.

### Overflow

Assume \(c_L=1\), so reflection pairs \(i\) with \(L-i\). Palindromicity forces \(e_0=e_L=1\), hence \(q_0\in\{1,11\}\). The value \(q_0=1\) is impossible, 因为 symmetry gives

\[
c_L=\left\lfloor\frac{q_0+c_{L-1}}{10}\right\rfloor=0.
\]

Thus \(q_0=11\). Inductively, suppose \(q_{i-1}=11b\), where \(b\in\{0,1\}\). Both reflected copies reset their outgoing carries to \(b\), so

\[
c_i=c_{L-i+1}=b.
\]

Equality \(e_i=e_{L-i}\) then becomes

\[
q_i=10c_{i+1}+c_{L-i}.
\]

The candidates are \(0,1,10,11\). For \(q_i=1\), 这 equation requires \(c_{L-i}=1\), but the mirrored coefficient 1 forces 那 carry to 0. For \(q_i=10\), the equation requires \(c_{L-i}=0\), but the mirrored coefficient 10 forces it to 1. Thus only 0 和 11 remain. 这 induction covers every coefficient.

Conversely, write \(q_i=11x_i\), where \(x_i\) 是 a symmetric bit word with \(x_0=1\). Each column forces \(c_{i+1}=x_i\). With \(x_{-1}=x_L=0\), all output positions, including the appended carry, satisfy

\[
e_i=x_i+x_{i-1},\qquad 0\le i\le L.
\]

Symmetry of \(x\) gives \(e_i=e_{L-i}\). 这 completes both directions of (1). ∎

**THEOREM — immediate center consequence.** A central sum at least 10 和 different from 11 rules out both alternatives in (1). At odd input width the central sum is even, so a nonzero central digit already rules out the overflow-palindrome alternative; a high coefficient somewhere is still required to rule out the no-carry alternative. A zero odd center alone does 不 force a palindrome, 因为 all remaining coefficients must 也 satisfy (1).

## 3. THEOREM 2 — The complete realizable center abstraction

Define

\[
\mathcal C=\{O_r:r=0,2,\ldots,18\}\cup\{E_s:s=0,1,\ldots,18\}.
\]

State \(O_r\) records odd width 和 central folded sum \(r\). State \(E_s\) records even width 和 the common value \(s\) of the 两 central folded coefficients. An edge means that some positive canonical decimal input in the source state 有 a successor in the target state. Width 和 all exterior data are forgotten.

The exact successor relation is:

| Source | No overflow | Overflow |
|---|---|---|
| \(O_r\), \(r\in\{0,2,4,6,8\}\) | \(O_{2r},O_{2r+2}\) | Every \(E_z\) with \(r\le z\le r+10\) |
| \(O_r\), \(r\in\{10,12,14,16,18\}\) | \(O_{2r-20},O_{2r-18}\) | Every \(E_z\) with \(r-10\le z\le r\) |
| \(E_s\), \(0\le s\le8\) | \(E_{2s},E_{2s+1}\) | \(O_{2s}\) |
| \(E_9\) | \(E_0,E_{18}\) | \(O_0,O_{18}\) |
| \(E_s\), \(10\le s\le18\) | \(E_{2s-19},E_{2s-18}\) | \(O_{2s-18}\) |

有 29 states 和 exactly \(10\cdot13+18\cdot3+4=188\) edges.

### Odd input: all carry cases

Without overflow, the central folded output is \(2((r+c_h)\bmod10)\). The 两 carry values give exactly the displayed odd-to-odd entries.

For overflow at width \(L=2h+1\ge3\), put \(s=q_{h-1}=q_{h+1}\), \(a=c_{h-1}\), \(b=f(s,a)\), \(\delta=f(r,b)\), 和 \(k=f(s,\delta)\). Since \(r\) is even, \(\delta=0\) for \(r\le8\), 和 \(\delta=1\) for \(r\ge10\). The new central pair 有 sum

\[
z=(r+b-10\delta)+(s+\delta-10k)
=r+s+b-9\delta-10k.
\]

| Adjacent \(s\) | \(a\) | \(b\) | \(k\) | \(z\) |
|---|---:|---:|---:|---|
| \(0\le s\le8\) | 0 or 1 | 0 | 0 | \(r+s-9\delta\) |
| \(s=9\) | 0 | 0 | \(\delta\) | \(r+9-19\delta\) |
| \(s=9\) | 1 | 1 | \(\delta\) | \(r+10-19\delta\) |
| \(10\le s\le18\) | 0 or 1 | 1 | 1 | \(r+s-9-9\delta\) |

For \(\delta=0\), the union is

\[
[r,r+8]\cup\{r+9,r+10\}\cup[r+1,r+9]=[r,r+10].
\]

For \(\delta=1\), the union is

\[
[r-9,r-1]\cup\{r-10,r-9\}\cup[r-8,r]=[r-10,r].
\]

At width 1 没有 adjacent coefficient. Overflow requires \(r\ge10\); its output digits are \(r-10,1\), giving center sum \(r-9\), which is already in the displayed interval. Without overflow, the actual entering carry is zero, 也 covered by the table.

### Even input: all carry cases

For \(L=2h\), set \(a=c_{h-1}\), \(b=f(s,a)\), 和 \(k=f(s,b)\). The central output digits are

\[
e_{h-1}=s+a-10b,\qquad e_h=s+b-10k.
\]

No overflow takes their sum. Overflow changes the center to the single digit \(e_h\), so its folded sum is \(2e_h\).

| \(s\) | \(a\) | \(b,k\) | No-overflow center | Overflow center |
|---|---:|---|---|---|
| \(0\le s\le8\) | 0 or 1 | \(0,0\) | \(2s+a\) | \(2s\) |
| 9 | 0 | \(0,0\) | 18 | 18 |
| 9 | 1 | \(1,1\) | 0 | 0 |
| \(10\le s\le18\) | 0 or 1 | \(1,1\) | \(2s+a-19\) | \(2s-18\) |

At width 2, \(a=c_0=0\); its transitions remain in the table.

### Every edge is realized; carries are constrained by actual columns

Use the following symmetric folded words:

\[
[v,u,s,r,s,u,v]\quad\text{for odd states},\qquad
[v,u,s,s,u,v]\quad\text{for even states},
\]

with \(v\in\{1,10\}\), \(u\in\{0,10\}\), 和 \(0\le s\le18\). The coefficient \(v=1\) forces final carry 0, while \(v=10\) forces final carry 1. The coefficient \(u=0\) forces \(c_2=0\), while \(u=10\) forces \(c_2=1\). For odd no-overflow transitions, choose \(s=9\) to transmit either entering carry; for odd overflow transitions, the preceding case table covers every interval value as \(s,u\) vary. In even fixtures, \(u\) directly sets the carry entering the central pair.

All fixtures satisfy the realizability conditions in Section 1. Thus every listed edge is an actual decimal transition, 和 the carry derivation excludes all other edges. ∎

## 4. THEOREM 3 — No universal invariant based only on parity 和 the central sum

A state is *universally safe* when every positive input with 那 state 有 a nonpalindromic next output. The complete safe set is

\[
S_0=\{O_{10},O_{12},O_{14},O_{16},O_{18}\}
\cup\{E_{10},E_{12},E_{13},E_{14},E_{15},E_{16},E_{17},E_{18}\}.
\]

Each displayed state contains a coefficient at least 10 和 different from 11, contradicting both palindrome branches. Every omitted state 有 a palindrome-producing completion: \([1,r,1]\) for odd \(r\le8\); \([1,s,s,1]\) for even \(s\le9\); 和 \([11,11]\) for \(E_{11}\), realized by \(29+92=121\). 这 establishes universal safety exactly.

Define the closure pruning

\[
S_{j+1}=\{X\in S_j:\operatorname{Succ}(X)\subseteq S_j\}.
\]

Then

\[
\boxed{|S_0|=13,\qquad S_1=\{E_{16},E_{17},E_{18}\},\qquad S_2=\varnothing.}
\tag{2}
\]

### First round

Every safe odd state 有 an overflow edge \(O_r\to E_{r-10}\), whose target is unsafe. The explicit word

\[
q=[10,0,9,r,9,0,10]
\]

有 the complete carry trace

\[
(c_0,\ldots,c_7)=(0,1,0,0,1,1,0,1)
\]

和 output

\[
e=[0,1,9,r-10,0,1,0,1].
\]

Its new central sum is exactly \(r-10\le8\).

For safe even states, no-overflow entry carry 0 gives

\[
E_{10}\to E_1,\quad E_{12}\to E_5,\quad E_{13}\to E_7,
\quad E_{14}\to E_9,\quad E_{15}\to E_{11}.
\]

Each is realized by \([1,s,s,1]\), 和 each target is unsafe. The remaining successor sets are

\[
\begin{aligned}
\operatorname{Succ}(E_{16})&=\{E_{13},E_{14},O_{14}\},\\
\operatorname{Succ}(E_{17})&=\{E_{15},E_{16},O_{16}\},\\
\operatorname{Succ}(E_{18})&=\{E_{17},E_{18},O_{18}\}.
\end{aligned}
\]

All 这 successors belong to \(S_0\), establishing the exact first round.

### Second round 和 the quantified obstruction

The overflow edges \(E_{16}\to O_{14}\), \(E_{17}\to O_{16}\), 和 \(E_{18}\to O_{18}\), realized by \([10,s,s,10]\), leave \(S_1\). Therefore \(S_2\) is empty.

Suppose a set \(P\subseteq\mathcal C\) guarantees a nonpalindromic next output for every input in its states, 和 every such input 有 successor state in \(P\). Safety gives \(P\subseteq S_0\). Exact edge realizability 和 closure then give \(P\subseteq S_1\) 和 \(P\subseteq S_2\). Hence \(P=\varnothing\). ∎

**Scope.** 这 excludes only predicates universally quantified over all exterior completions of a parity/center state. Different abstract edges may use different exteriors. It gives no 2-step palindrome bound for individual orbits. Larger center blocks, remembered carries, restrictions on interfaces, 和 correlations between phases remain available.

## 5. THEOREM 4 — Exact maximal centered-run renewal

For a symbol \(s\), its maximal centered-run length is 0 if the central position, or central pair, does 不 consist of \(s\). Otherwise it 是 the length of the largest centered constant \(s\)-block.

Suppose the input 有 such a nonempty maximal run on \([p,b]\), where \(p+b=L-1\), with length \(r=b-p+1\), 和 \(s\ne9\). Define

\[
\kappa=\mathbf1_{s\ge10},\qquad F(s)=2s-18\kappa,\qquad v=c_p.
\]

The reset rule gives \(c_{p+1}=\cdots=c_{b+1}=\kappa\).

### A. No overflow: no growth

If \(c_L=0\), the maximal centered \(F(s)\)-run in the output 有 exactly

\[
\boxed{r'=\begin{cases}r,&v=\kappa,\\\max(r-2,0),&v\ne\kappa.\end{cases}}
\tag{3}
\]

For \(p+1\le i\le b\), the output digit is \(e_i=s-9\kappa\). At every strictly interior folded position, both digits therefore sum to \(F(s)\). If \(r\ge2\), the 两 folded boundary values are

\[
q'_p=q'_b=F(s)+(v-\kappa).
\]

A mismatched entering carry removes exactly 2 positions; if \(r=2\), the new center contains no \(F(s)\). If \(r=1\), the central digit is counted twice, giving \(q'_p=F(s)+2(v-\kappa)\); mismatch then gives length 0.

For a matched carry, expansion must 也 be excluded. If \(p=0\), the run fills the word. Otherwise put \(t=q_{p-1}=q_{b+1}\ne s\), \(u=c_{p-1}\), 和 \(\eta=f(t,\kappa)\). Since \(c_p=\kappa\), the first outside folded value is

\[
q'_{p-1}=(t+u-10\kappa)+(t+\kappa-10\eta).
\]

Equality with \(F(s)\) would imply

\[
2(t-s)+u+9\kappa-10\eta=0.
\]

For \(\kappa=0\), parity forces \(u=0\). The equation \(f(t,u)=\kappa=0\) then gives \(\eta=f(t,0)=0\), forcing \(t=s\). For \(\kappa=1\), parity forces \(u=1\). The equation \(f(t,u)=1\) gives \(\eta=f(t,1)=1\), again forcing \(t=s\). Both contradict maximality. 这 proves (3), including the singleton cases.

### B. Overflow: exact companion coalescence

现在 assume \(c_L=1\) 和 \(s\in\{1,\ldots,17\}\setminus\{9\}\). Set

\[
a=s-9\kappa\in\{1,\ldots,8\},\qquad A_a=\{a,a+9\}.
\]

Let \(B\) be the length of the maximal centered block over \(A_a\). Then

\[
\boxed{r'=B-1}
\tag{4}
\]

is the exact maximal centered \(2a=F(s)\)-run length after the step. 这 includes \(B=1\), giving length 0.

Write the maximal companion block as \([u,w]\), with \(u+w=L-1\). Inside it write \(q_i=a+9x_i\), where \(x_i\in\{0,1\}\). 因为 \(1\le a\le8\), each coefficient forces \(c_{i+1}=x_i\), independently of its entering carry. For \(u+1\le i\le w\),

\[
e_i=a+x_{i-1}-x_i.
\]

The overflow reflection pairs \(i\) with \(L-i\). Symmetry gives \(x_{L-i-1}=x_i\) 和 \(x_{L-i}=x_{i-1}\), hence

\[
e_{L-i}=a+x_i-x_{i-1},\qquad q'_i=2a.
\]

The centered interval \([u+1,w]\) 有 length \(B-1\).

For maximality with \(u>0\), put \(t=q_{u-1}=q_{w+1}\notin A_a\), \(v=c_u\), 和 \(\eta=f(t,x_u)\). The first outside folded value is

\[
q'_u=(a+v-x_u)+(t+x_u-10\eta)=a+t+v-10\eta.
\]

The entering carry is constrained by \(v=\lfloor(t+c_{u-1})/10\rfloor\). Equality with \(2a\) would require \(t+v-10\eta=a\). Every carry case fails:

| \(v\) | \(\eta\) | Required \(t\) | Exclusion |
|---:|---:|---|---|
| 0 | 0 | \(a\) | Already inside \(A_a\) |
| 0 | 1 | \(a+10\) | \(t\ge11\) forces \(c_u=1\) |
| 1 | 0 | \(a-1\) | \(t\le7\) forces \(c_u=0\) |
| 1 | 1 | \(a+9\) | Already inside \(A_a\) |

If \(u=0\), the companion block fills the word. Overflow forces \(q_0=a+9\), giving \(e_0=a-1\), \(e_L=1\), 和 \(q'_0=a\ne2a\). Thus expansion is impossible in the whole-word case as well. For \(B=1\), 这 first outside positions are exactly the new central pair; they fail the target equality, confirming length 0. ∎

**LEAN-VERIFIED — existing extreme-symbol specialization.** At \(s=0\) or \(18\), equation (3) holds, while overflow gives \(r'=r-1\). 这 is already covered by the inspected `RunAncestry.central_run_step` 和 maximality theorem. The new companion formula (4) concerns the nonextreme symbols. The symbol 9 is excluded 因为 its carry map transmits its input instead of resetting it.

## 6. THEOREM 5 — Exact growth balance 和 an obstruction class

Consider an actual finite orbit segment whose maximal centered constant runs 有 lengths \(r_t\ge3\) 和 symbols \(s_{t+1}=F(s_t)\), with \(1\le s_t\le17\), \(s_t\ne9\). At no-overflow steps let

\[
\varepsilon_t=\mathbf1_{c_{p_t}\ne\kappa(s_t)}.
\]

At overflow steps let \(B_t\) be the companion-block length 和

\[
h_t=(B_t-r_t)/2.
\]

Both blocks are centered in the same word, so \(h_t\) 是 a nonnegative integer. Equations (3)–(4) give

\[
r_{t+1}=\begin{cases}
r_t-2\varepsilon_t,&c_{L_t}=0,\\
r_t+2h_t-1,&c_{L_t}=1.
\end{cases}
\]

Telescoping yields the exact identity

\[
\boxed{r_m-r_0=2\sum_{\mathrm{overflow}}h_t
-N_{\mathrm{overflow}}-2\sum_{\mathrm{no\ overflow}}\varepsilon_t.}
\tag{5}
\]

Consequently positive central-run growth is equivalent, for such an actual segment, to

\[
\boxed{2\sum_{\mathrm{overflow}}h_t>
N_{\mathrm{overflow}}+2\sum_{\mathrm{no\ overflow}}\varepsilon_t.}
\tag{6}
\]

The bulk-symbol map 有 the cycles

\[
2\to4\to8\to16\to14\to10\to2,
\qquad 6\to12\to6.
\]

Every nonextreme starting symbol enters one of 这 cycles after at most 1 step. At their even phases, the companion differing by 9 is odd. 因为 the constant run is maximal, any strict enlargement to its companion block begins with 那 other, odd coefficient on each side. Thus every growing overflow step requires actual adjacent odd companion material.

**THEOREM — no persistent centered band without absorption.** 没有 infinite positive orbit with a nonempty tracked centered run at every time, with its symbols following \(F\) in the nonextreme phases, 和 \(B_t=r_t\) at every overflow. No-overflow steps never increase its length, including the small-run cases in (3); each overflow removes exactly 1. For a positive integer, its reversed integer is at least 1, so \(n_t\ge n_0+t\). Hence digit length is unbounded. Each step increases length by at most 1, so infinitely many overflows occur. A finite initial run cannot remain nonempty through infinitely many unit losses. ∎

这 excludes an entire specified class of centered-band certificates. It does 不 exclude larger constructions that replace the center phase after its tracked run disappears, or that replenish companion blocks. Equation (5) 是 a balance along actual transitions; arbitrary assignments to \(h_t\), carries, 和 overflow bits do 不 establish that those transitions are realizable together.

## 7. THEOREM 6 — A growing center can still reach a palindrome immediately afterward

Suppose the entire input folded word lies in \(\{a,a+9\}\), where \(1\le a\le4\), 和 its outer coefficient is \(a+9\). Both outer columns force overflow. The internal cancellation from Theorem 4, together with its whole-word boundary calculation, gives exactly

\[
q'=\bigl(a,(2a)^{L-1},a\bigr).
\]

Every new coefficient is at most 8. The next addition therefore 没有 carries 和 produces a palindrome by (1). Such an input reaches a palindrome within 2 reverse-add steps. ∎

**IDEA — refuted by an explicit counterexample.** A centered run that grows after 1 step is insufficient as an infinite avoidance mechanism:

\[
2119+9112=11231,\qquad11231+13211=24442.
\]

The corresponding folded words are

\[
(11,2,2,11)\longmapsto(2,4,4,4,2).
\]

The maximal center grows from a 2-run of length 2 to a 4-run of length 3, but the next output is palindromic. The 1000-step check below reports 这 first palindrome at step 2; extending the arithmetic afterward tests identities only.

## 8. Implications for the existing return framework

**LEAN-VERIFIED — existing safety, 不 a new certificate.** `Agent109.NoPal.not_stepPal` already excludes the template palindrome test for every allowed phase 和 bounded exterior/interface blocks, with no assumption on its center block `C`. The actual-template corollary is in the same inspected source. Thus the center does 不 need to supply an additional palindrome obstruction for the already safe complementary-band family.

**THEOREM — direct coefficient explanation.** For any realized folded word containing both \(c\) 和 \(18-c\), where \(1\le c\le17\), \(c\ne9\), one coefficient exceeds 9. Both positive complementary symbols cannot belong to \(\{0,11\}\): if they did, both would equal 11, contradicting their sum 18. Equation (1) therefore excludes a palindromic next output. Each band need only be nonempty for 这 coefficient argument.

**IDEA — consequence for further work.** The useful center question is whether interfaces can maintain a compatible global return 和 satisfy (5). Re-establishing single-step safety, or imposing a predicate on just the central sum, does 不 address 那 requirement. The existing checker remains conditional: 这 report supplies no accepted return certificate.

## 9. Reproducible bounded checks

The following Python program uses only the standard library. Its fixtures validate analytically derived formulas; it performs no seed search for a Lychrel witness. It checks the actual integer operation, including trailing-zero reversal, against explicit column carries. The 361 center-9 profiles are included in the palindrome/center-transition checks 和 excluded only from the non-9 run theorem.

Save the code block as `verify_report_216.py` 和 run `python3 verify_report_216.py`. The tests continue for exactly 1000 transitions from each listed seed even after a palindrome appears. 这 continuation is strictly an identity check.

```python
#!/usr/bin/env python3
"""Agent 216: bounded checks for the exact single-center abstraction.

This is not a search for a Lychrel number. Every one-step edge is derived
analytically in REPORT_216.md. The 836 fixtures below check those formulas
against both an explicit carry trace and ordinary integer reverse-and-add.
All fixtures are genuine positive decimal inputs: their column-sum words
are symmetric, have positive outer symbols, and have an even central
symbol when the length is odd.
"""

from collections import defaultdict


def realize(q):
    """Return least-significant-first digits realizing a valid q word."""
    assert q and q == q[::-1] and q[0] > 0
    assert all(0 <= s <= 18 for s in q)
    if len(q) % 2:
        assert q[len(q) // 2] % 2 == 0
    d = [0] * len(q)
    for i in range((len(q) + 1) // 2):
        j = len(q) - 1 - i
        if i == j:
            d[i] = q[i] // 2
        else:
            d[j] = min(q[i], 9)
            d[i] = q[i] - d[j]
    assert all(0 <= x <= 9 for x in d) and d[-1] > 0
    assert [x + y for x, y in zip(d, d[::-1])] == q
    return d


def value(d):
    return sum(x * 10**i for i, x in enumerate(d))


def step(q):
    carry = [0]
    e = []
    for s in q:
        out, digit = divmod(s + carry[-1], 10)
        carry.append(out)
        e.append(digit)
    if carry[-1]:
        e.append(carry[-1])
    q_next = [x + y for x, y in zip(e, e[::-1])]

    # Independently verify the ordinary integer operation, including
    # dropping leading zeros in the reversed input.
    d = realize(q)
    n = value(d)
    assert value(e) == n + int(str(n)[::-1])
    assert e[-1] > 0
    assert q_next == q_next[::-1]
    if len(q_next) % 2:
        assert q_next[len(q_next) // 2] % 2 == 0
    return q_next, carry, e


def center(q):
    return ("O" if len(q) % 2 else "E", q[len(q) // 2])


def formula_graph():
    graph = {}
    for r in range(0, 19, 2):
        same_width = {("O", (2 * r) % 20), ("O", (2 * r + 2) % 20)}
        lo = r if r <= 8 else r - 10
        overflow = {("E", z) for z in range(lo, lo + 11)}
        graph[("O", r)] = same_width | overflow
    for s in range(19):
        if s <= 8:
            successors = {("E", 2 * s), ("E", 2 * s + 1), ("O", 2 * s)}
        elif s == 9:
            successors = {("E", 0), ("E", 18), ("O", 0), ("O", 18)}
        else:
            successors = {
                ("E", 2 * s - 19),
                ("E", 2 * s - 18),
                ("O", 2 * s - 18),
            }
        graph[("E", s)] = successors
    return graph


def center_tests():
    expected = formula_graph()
    actual = defaultdict(set)
    fixtures = 0

    # Outer v=1 forces no overflow; v=10 forces overflow. The following
    # u=0 or u=10 forces an actual carry of 0 or 1, respectively.
    for r in range(0, 19, 2):
        for v in (1, 10):
            for u in (0, 10):
                for s in range(19):
                    q = [v, u, s, r, s, u, v]
                    q_next, carry, e = step(q)
                    assert carry[-1] == (v == 10)
                    assert carry[2] == (u == 10)
                    actual[center(q)].add(center(q_next))
                    fixtures += 1
    for s in range(19):
        for v in (1, 10):
            for u in (0, 10):
                q = [v, u, s, s, u, v]
                q_next, carry, e = step(q)
                assert carry[-1] == (v == 10)
                assert carry[2] == (u == 10)
                actual[center(q)].add(center(q_next))
                fixtures += 1

    assert dict(actual) == expected
    safe = {("O", r) for r in range(10, 19, 2)} | {
        ("E", s) for s in range(10, 19) if s != 11
    }

    # Explicit palindromic-output completions for every state excluded
    # from the universal one-step-safe set.
    unsafe_witnesses = 0
    for state in set(expected) - safe:
        parity, s = state
        if parity == "O":
            q = [1, s, 1]
        elif s == 11:
            q = [11, 11]
        else:
            q = [1, s, s, 1]
        q_next, carry, e = step(q)
        assert center(q) == state and e == e[::-1]
        unsafe_witnesses += 1

    print("realizable transition fixtures", fixtures)
    print("ordinary integer cross-check mismatches", 0)
    print("center states", len(expected), "edges", sum(map(len, expected.values())))
    print("graph equality mismatches", sum(actual[k] != v for k, v in expected.items()))
    print("unsafe-state palindrome witnesses", unsafe_witnesses)
    kernels = []
    for round_number in range(3):
        kernels.append(safe)
        print("safe kernel round", round_number, sorted(safe))
        safe = {state for state in safe if expected[state] <= safe}
    assert kernels[1] == {("E", 16), ("E", 17), ("E", 18)}
    assert kernels[2] == set()


from itertools import product
import random

def centered_block(q, alphabet):
    L = len(q)
    left, right = (L - 1) // 2, L // 2
    if q[left] not in alphabet or q[right] not in alphabet:
        return 0, left
    while left > 0 and q[left - 1] in alphabet and q[right + 1] in alphabet:
        left -= 1
        right += 1
    return right - left + 1, left


def check_run(q):
    assert q == q[::-1]
    qp, c, e = step(q)
    overflow = bool(c[-1])
    s = q[(len(q) - 1) // 2]
    if s == 9:
        return 0, 0, 0
    kappa = int(s >= 10)
    target = 2 * s - 18 * kappa
    width, left = centered_block(q, {s})
    actual, _ = centered_block(qp, {target})
    if not overflow:
        expected = width if c[left] == kappa else max(width - 2, 0)
        family = (1, 0, 0)
    elif s in (0, 18):
        expected = width - 1
        family = (0, 0, 1)
    else:
        alpha = s - 9 * kappa
        union_width, _ = centered_block(q, {alpha, alpha + 9})
        expected = union_width - 1
        family = (0, 1, 0)
    assert actual == expected, (q, qp, c, s, width, actual, expected)
    return family


def symmetric_words(L):
    half = (L + 1) // 2
    for head in product(range(19), repeat=half):
        if head[0] == 0 or (L % 2 and head[-1] % 2):
            continue
        tail = head[-2::-1] if L % 2 else head[::-1]
        yield list(head + tail)


def digits_q(n):
    digits = [int(x) for x in str(n)][::-1]
    return [a + b for a, b in zip(digits, reversed(digits))]


def run_tests():
    totals = [0, 0, 0]
    words = 0
    for length in range(1, 7):
        count = 0
        for q in symmetric_words(length):
            qp, carries, e = step(q)
            predicted_palindrome = all(s <= 9 for s in q) or (
                q[0] == 11 and all(s in (0, 11) for s in q)
            )
            assert predicted_palindrome == (e == e[::-1])
            assert center(qp) in formula_graph()[center(q)]
            families = check_run(q)
            totals = [a + b for a, b in zip(totals, families)]
            count += 1
        words += count
        print(f"L={length}: {count} realizable symmetric words; PASS")
    print(f"Exhaustive totals: words={words}, no_overflow={totals[0]}, "
          f"overflow_pair={totals[1]}, overflow_extreme={totals[2]}")
    print(f"Run theorem excludes center 9: {words - sum(totals)} cases")

    rng = random.Random(216)
    for _ in range(1000):
        length = rng.randrange(1, 101)
        half = (length + 1) // 2
        head = [rng.randrange(19) for _ in range(half)]
        head[0] = rng.randrange(1, 19)
        if length % 2:
            head[-1] = 2 * rng.randrange(1 if length == 1 else 0, 10)
        tail = head[-2::-1] if length % 2 else head[::-1]
        check_run(head + tail)
    print("Random transition checks: 1000; PASS (seed=216)")

    for seed in (89, 2119):
        n = seed
        first_palindrome = None
        for t in range(1, 1001):
            q = digits_q(n)
            check_run(q)
            qp, carries, e = step(q)
            n += int(str(n)[::-1])
            assert value(e) == n and digits_q(n) == qp
            assert center(qp) in formula_graph()[center(q)]
            if first_palindrome is None and str(n) == str(n)[::-1]:
                first_palindrome = t
        print(f"1000 ordinary steps from {seed}: PASS; "
              f"first_palindrome={first_palindrome}; final_digits={len(str(n))}")
    assert 2119 + 9112 == 11231
    assert 11231 + 13211 == 24442
    print("Counterexample: 2119 -> 11231 -> 24442 (palindrome)")
    print("All checks passed. No Lychrel construction is asserted.")


if __name__ == "__main__":
    center_tests()
    run_tests()
```

### Executed output

```text
realizable transition fixtures 836
ordinary integer cross-check mismatches 0
center states 29 edges 188
graph equality mismatches 0
unsafe-state palindrome witnesses 16
safe kernel round 0 [('E', 10), ('E', 12), ('E', 13), ('E', 14), ('E', 15), ('E', 16), ('E', 17), ('E', 18), ('O', 10), ('O', 12), ('O', 14), ('O', 16), ('O', 18)]
safe kernel round 1 [('E', 16), ('E', 17), ('E', 18)]
safe kernel round 2 []
L=1: 9 realizable symmetric words; PASS
L=2: 18 realizable symmetric words; PASS
L=3: 180 realizable symmetric words; PASS
L=4: 342 realizable symmetric words; PASS
L=5: 3420 realizable symmetric words; PASS
L=6: 6498 realizable symmetric words; PASS
Exhaustive totals: words=10467, no_overflow=4772, overflow_pair=4572, overflow_extreme=762
Run theorem excludes center 9: 361 cases
Random transition checks: 1000; PASS (seed=216)
1000 ordinary steps from 89: PASS; first_palindrome=24; final_digits=399
1000 ordinary steps from 2119: PASS; first_palindrome=2; final_digits=438
Counterexample: 2119 -> 11231 -> 24442 (palindrome)
All checks passed. No Lychrel construction is asserted.
```

The printed zero mismatch counts follow successful assertions. A failed assertion terminates execution. 这 finite checks support implementation correctness; the all-length conclusions rest on the proofs above. No new theorem in 这 report is labeled Lean-verified.

## 10. IDEA — Sharpest open question

Does there exist a finite set of center/interface states, realized by actual decimal column-sum templates, whose exact return over a full 6-step or 2-step bulk-symbol cycle regenerates the odd companion blocks 和 satisfies

\[
2\sum h_t>N_{\mathrm{overflow}}+2\sum\varepsilon_t,
\]

while all remaining blocks return compatibly 和 every phase retains a global nonpalindrome guard?

An affirmative construction needs the full carry-consistent return, including both ends, the center, 和 every run-length update. A negative theorem bounding the available companion absorption below the right side would exclude 那 whole return class. The present results identify 这 replenishment requirement exactly; they do 不 resolve it.
