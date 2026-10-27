# Agent 115 — Central 3/4-window universal-safety obstruction

Task: `T1.central-window3-4-safety`, coordination issue #289.
Baseline: `eafbbbfd6b5b857597f95f68268c56dbd96b6bcb`.

## Result 和 exact scope

**PAPER PROOF + COMPUTED:** a predicate depending only on the central 3 folded
coefficients at odd digit width, or the central 4 at even width, cannot be both
nonempty, universally sufficient for next-step nonpalindromicity, 和 preserved
under every compatible ordinary-decimal reverse-add transition. The exact
realizable abstraction has 551 states 和 3,662 labelled edges. Its universally
safe subsets prune as

\[
397\longrightarrow201\longrightarrow50\longrightarrow5\longrightarrow0.
\]

The quantifier over exterior completions is essential. This result does **not**
exclude an individual infinite orbit whose central window stays safe. It does
not exclude a neutral-band certificate, a fixed p11/p12 center, or a decimal
Lychrel number. Interfaces, remembered carries, phase correlations, 和 larger
windows remain available. In particular, REPORT_206 section12's question about
one actual infinite orbit remains open.

The separate Lean result, described below, certifies the finite local model;
the ordinary-integer realization bridge is a paper proof with integer checks.

## 1. Prior work 和 definitions

[REPORT_216 sections3–4](REPORT_216.md) proves the corresponding 29-state,
single-central-coefficient abstraction has 188 edges 和 empty universal safe
invariant. [REPORT_206 section12](REPORT_206.md) explicitly proposes a moving
safety witness inside the wider central 3/4 window. This report analyzes that
wider window, retaining exact edge realizability.

For a positive canonical decimal integer with units-first digits \(d_i\), put
\(q_i=d_i+d_{L-1-i}\). Thus \(q\) is symmetric, \(0\le q_i\le18\),
\(q_0>0\), 和 an odd middle coefficient is even. Conversely these conditions
suffice: assign the high digit of each reflected pair \(\min(q_i,9)\), the low
digit \(q_i-\min(q_i,9)\), 和 the odd middle digit half its coefficient.

The state space is

\[
O(a,r)=(a,r,a),\quad 0\le a\le18,\quad r\in\{0,2,\ldots,18\},
\]
\[
E(a,s)=(a,s,s,a),\quad 0\le a,s\le18.
\]

There are 190 odd states 和 361 even states. The domain is ordinary input width
at least 3, with the indicated parity; even width consequently starts at 4.
There is no upper bound on the full input width. Width never decreases under
positive reverse-add, so this domain is forward invariant. An edge means that
some compatible integer realizes the source, overflow bit, 和 target.

## 2. PAPER PROOF — exact local transitions

Write
\[
f(x,c)=\lfloor(x+c)/10\rfloor,\qquad d(x,c)=(x+c)\bmod10.
\]
Normalization of a short word uses the displayed incoming bit, then propagates
\(f\) from left to right. These are ordinary column carries.

For \(O(a,r)\), choose an outside mirrored coefficient \(z\in[0,18]\)
和 an incoming carry \(c\in\{0,1\}\). Normalize \((z,a,r,a,z)\) to
\((D_0,D_1,D_2,D_3,D_4)\). The target is

\[
g=0:\ O(D_1+D_3,2D_2),\qquad
g=1:\ E(D_1+D_4,D_2+D_3).
\tag{1}
\]

For \(E(a,s)\), normalize \((a,s,s,a)\) with incoming carry \(c\)
to \((D_0,D_1,D_2,D_3)\). The target is

\[
g=0:\ E(D_0+D_3,D_1+D_2),\qquad
g=1:\ O(D_1+D_3,2D_2).
\tag{2}
\]

**Necessity.** Without overflow, reflected output indices sum to \(L-1\);
with overflow, they sum to \(L\), because the appended leading digit shifts
reflection by one. Taking the central indices gives (1)–(2). An actual wider
word supplies its actual \(z,c\). For the minimum odd width 3, use virtual
\(z=c=0\): its right virtual zero emits the actual final carry, so an overflow
emits the required appended 1. Minimum even width 4 uses \(c=0\).

**Sufficiency 和 realizability.** Let \(v=1+9g\), \(u=10c\). The folded
fixtures

\[
[v,u,z,a,r,a,z,u,v],\qquad [v,u,a,s,s,a,u,v]
\tag{3}
\]

realize the odd 和 even cases respectively. The first/last coefficient
\(v=1\) forces \(g=0\); \(v=10\) forces \(g=1\). The lower coefficient
\(u\in\{0,10\}\) forces the chosen carry into the local word. These fixtures
satisfy the coefficient-realization conditions above. Thus every enumerated
edge is an actual ordinary-integer edge, with no independent-carry fiction.

After deduplication, the exact counts are:

| Source | Overflow | Target | Edges |
|---|---:|---|---:|
| Odd | 0 | Odd | 380 |
| Odd | 1 | Even | 2,180 |
| Even | 0 | Even | 722 |
| Even | 1 | Odd | 380 |
| Total | | | 3,662 |

## 3. PAPER PROOF — universal safety is exact

The existing complete next-palindrome criterion is

\[
\operatorname{Pal}(T(n))\iff
(\forall i,\ q_i\le9)\ \lor\
(q_0=11\ \land\ \forall i,\ q_i\in\{0,11\}).
\tag{4}
\]

Source: `DecimalDigits.step_palindrome_iff` in
[`Foundations/LychrelDigitSums.lean`](../lean/P196/Foundations/LychrelDigitSums.lean),
with the complete carry proof restated in REPORT_216 section2.

A window \(w\) guarantees a nonpalindromic next output for every exterior
completion exactly when

\[
\operatorname{Safe}(w)\iff
\max(w)\ge10\ \land\ \exists x\in w,\ x\notin\{0,11\}.
\tag{5}
\]

Sufficiency follows by contradicting both branches of (4). For necessity,
if \(\max(w)\le9\), the completion \([1]\mathbin{+\!+}w\mathbin{+\!+}[1]\)
produces a palindrome. Otherwise failure of (5) means every window coefficient
belongs to \(\{0,11\}\); use exterior coefficient 11 instead. Both completions
are symmetric, positive, 和 realizable, including the odd-middle parity guard.
There are exactly 397 safe states 和 154 unsafe states.

## 4. COMPUTED closure 和 the universal no-go

Let \(S_0=\operatorname{Safe}\) 和 define
\[
S_{j+1}=\{x\in S_j:\operatorname{Succ}(x)\subseteq S_j\}.
\]

| Round | Odd states | Even states | Total |
|---:|---:|---:|---:|
| 0 | 139 | 258 | 397 |
| 1 | 53 | 148 | 201 |
| 2 | 10 | 40 | 50 |
| 3 | 0 | 5 | 5 |
| 4 | 0 | 0 | 0 |

The last five states are \(E(a,18)\),
\(a\in\{7,8,16,17,18\}\). Assign rank zero to unsafe states 和 rank \(j\)
to states removed in round \(j\). The rank histogram is
\(\{0:154,1:196,2:151,3:45,4:5\}\). Each positive-rank state has an explicit
realizable successor of rank exactly one less.

If a universally safe predicate \(P\) is preserved by every compatible
integer transition, edge realizability gives \(P\subseteq S_j\) inductively.
Hence \(P\subseteq S_4=\varnothing\). Equivalently, follow a selected decreasing
rank edge from a hypothetical member of \(P\) until safety contradicts rank zero.

Different edges may require different exterior completions. The rank argument
is therefore **not a four-step termination bound for an individual orbit**.
Indeed the safe state \(E(18,18)\) has an existential abstract self-loop; universal
closure fails because it also has edges leaving the surviving safe subsets.

## 5. Reproduction 和 independent checks

From repository root:

```bash
python3 calculation/agent-115/central_window.py
python3 calculation/agent-115/central_window_independent.py
python3 -O calculation/agent-115/central_window.py
```

Both independent implementations return the exact state/edge/round counts above.
The primary checks 3,662 integer edge fixtures, 154 unsafe palindrome completions,
522 minimum-width profiles, 和 397 decreasing-rank witnesses. Its explicit guards
remain active under optimized Python. The second implementation derives local
formulas separately, imports no primary code, 和 checks 9,044 integer fixtures,
10,440 exhaustive profiles of widths 3–6, 154 unsafe completions, 和 the same rank
partition. Every fixture is checked using ordinary integer addition plus decimal
string reversal, separately from local carry propagation. Both programs finish
in under one second in this environment.

`central_window.py --states --edges` emits the complete rank/witness relation on
demand; `--lean-data` emits the finite rank/control certificate used by the Lean
model. These outputs are reproducible; no output dumps or logs are committed.

## 6. Lean endpoint 和 repository gate

**LEAN-VERIFIED:** registered project `Agent115CentralWindowSafety` checks the
local arithmetic model, its finite escape certificate, 和 the abstract conclusion
`Agent115.CentralWindow.no_nonempty_universally_safe`. The companion theorem
`universally_safe_empty` proves every universally closed safe predicate empty.
The other six registered endpoints check the certificate size, selected-successor
bound/edge, strict rank decrease, safety iff positive rank, 和 rank at most four.
Successors are recomputed from arithmetic controls; the table cannot invent edges.
The kernel checks 29 blocks of 19 rows using ordinary `decide`.

The complete edge census 和 exact pruning cardinalities in sections2–4 remain
COMPUTED: the Lean certificate checks selected legal escape edges 和 ranks,
not the deduplicated edge census or the cardinalities of the pruning sets.

With Lean 4.19.0 和 matching official `lean4checker` v4.19.0 on `PATH`:

```bash
LEAN_NUM_THREADS=1 lake --dir lean build P196.Agent115CentralWindowSafety.Certificate
LEAN_NUM_THREADS=1 python3 tools/verify.py --changed
```

The actual repository gate returned exit 0: 5,219 Lean files / 302 projects
passed rules; 2 changed modules built; both modules kernel-replayed; all 8
registered endpoints passed the allowed-axiom audit; `ALL CHECKS PASSED
(changed files only, against origin/main)`. `LEAN4CHECKER` named the official
checker executable. The baseline is recorded at the top of this report.

The successful two-module build took 46.317 seconds with peak RSS 2,120,392 KiB;
this combined time is a conservative upper bound for either file. The actual
changed-file gate took 79.205 seconds with peak RSS 783,616 KiB. Runs used one
Lean thread, an 8 GiB address-space limit, 和 a 20-minute per-file budget.
An initial monolithic finite check exhausted its memory budget; it was replaced
by the checked blocks before these successful runs. No failed check is counted.

The Lean conclusion concerns the defined finite model. Sections1–3 supply the
ordinary-integer bridge as PAPER PROOF, with the independent checks in section5.
A finite-model kernel proof is not a kernel proof of decimal Lychrel existence
or impossibility.
