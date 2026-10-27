# Agent 110 — Balanced center widths 和 exact search reduction

## Status 和 exact scope

**PAPER PROOF + COMPUTED.** Fix a base `b>=2`, a period `P>=1`, 和 binary
driver streams `e,g`. Center feasibility means the exact A120 carry-flip
condition 和 center edge equations; a center alone does 不 supply a B-cycle.

Main result: for any uniform center-width bound `W>=2`, the entire bounded
query is equivalent to **两个 prescribed width/trim profiles**, each using
only widths `W-1,W`. This preserves the width bound exactly. For unrestricted
widths, any single equal-total trim schedule suffices.

The general schedule-transport theorem belongs to **Agent 107**; the neutral
padding identity belongs to **Agent 7**. Agent 110's contribution is the
balanced construction, exact width-preserving two-profile equivalence,
independent full-certificate controls, 和 conservative executable reduction.

The decimal runs below reproduce existing exclusions for periods 11,22,24.
They supply no new excluded period, arbitrary-repetition theorem, decimal
certificate, or new Lean theorem. A repository gate PASS for these Python/report
changes selects zero Lean modules; it does 不 constitute kernel verification
of the paper mathematics.

## 1. Definitions 和 credited transport lemma

Write `h=b-1` 和 `P_a(C)=h^a ++ C ++ h^a`. For each phase `t`, let
`F_t(C)` denote raw `nextC` driven by `e_t,g_t`. A legal center cycle obeys

\[
\operatorname{carry}(C_t,e_t)=1-e_t,
\qquad F_t(C_t)=P_{v_t}(C_{t+1}),\qquad v_t\in\mathbb N.
\]

Indices are cyclic. Empty centers cannot satisfy the carry flip. Every raw
center image is symmetric, so cyclic centers are symmetric automatically.
The coefficient bound is `0..2h`. Length accounting gives

\[
m_{t+1}=m_t+g_t-2v_t,\qquad
G:=\sum_tg_t=2\sum_tv_t.
\]

Hence odd `G` excludes a closed center at every width.

**Padding covariance, Agent 7.** If `norm(C,e)=(D,1-e)`, then

\[
\operatorname{norm}(P_a(C),e)
 = (x^a\mathbin{++}D\mathbin{++}y^a,1-e),
\quad x=h(1-e),\ y=he,\ x+y=h.
\]

For `g=0`, reflected pairing gives `P_a(F(C))`. For `g=1`, append the
additional digit `y` before reflected pairing; the same identity results.
Thus `F_t(P_a(C))=P_a(F_t(C))`, with the same entering/exiting carries.
This holds without assuming symmetry; carry flip is essential.

**Equal-total transport, Agent 107; independently checked here.** Given
nonnegative target trims `w` with `sum(w)=sum(v)`, choose cyclic offsets

\[
a_{t+1}=a_t+v_t-w_t,\qquad
a_0=-\min_{0\le j\le P}\sum_{t<j}(v_t-w_t).
\]

All offsets are nonnegative. Then

\[
F_t(P_{a_t}(C_t))
 =P_{a_t+v_t}(C_{t+1})
 =P_{w_t}(P_{a_{t+1}}(C_{t+1})).
\]

The transformation keeps every B-state, exterior trim `u`, carry `e`,
overflow `g`, period, 和 total gain. Every full `edgeOK` equation 和
`cycleOK` inequality remains valid. Reversing the roles of `v,w` proves
existence equivalence. Arbitrary prescribed schedules can increase widths.

## 2. Balanced normal forms: unrestricted widths

Let `S_0=0`, `S_t=sum(g_j,j<t)`, 和 `r_t=S_t mod 2`. For even `G`, define

\[
w_t^- =\lfloor S_{t+1}/2\rfloor-\lfloor S_t/2\rfloor,
\qquad
w_t^+ =\lceil S_{t+1}/2\rceil-\lceil S_t/2\rceil.
\]

The schedules 都 are binary, periodic, 和 have total `G/2`. The minus
schedule trims at every second overflow; the plus schedule trims at every
first overflow in each consecutive overflow pair. Their length offsets are

\[
m_t^--m_0^-=r_t,\qquad m_t^+-m_0^+=-r_t.
\]

Therefore each representative uses at most 两 consecutive widths. By the
credited transport lemma, **one** chosen schedule with a complete all-length
decision suffices; enumeration of `choose(P,G/2)` binary schedules is unnecessary.
An undecided schedule does 不 exclude any schedule.

## 3. Exact equivalence at a prescribed width cap

**THEOREM.** For `W>=2`, a legal center cycle with every `m_t<=W` exists iff
at least one of these exact profiles is feasible:

| Profile | Center length at phase t | Initial length | Trim schedule |
|---|---|---|---|
| A | `W-1+r_t` | `W-1` | `w^-` |
| B | `W-r_t` | `W` | `w^+` |

**Proof.** Length accounting gives `m_t = m_0+S_t (mod 2)`.
If `m_0` has the parity of `W-1`, use profile A; otherwise use profile B.
In either case its target length `L_t` is the greatest integer at most `W`
with the parity of `m_t`. Hence `L_t>=m_t` 和

\[
a_t=(L_t-m_t)/2\in\mathbb N.
\]

Subtract the original length recurrence from the target recurrence to obtain
`a_(t+1)=a_t+v_t-w_t`. Padding therefore constructs the required profile.
The converse follows because each profile is itself a legal cycle within
the same bound. `W>=2` guarantees both target profiles are nonempty. ∎

In particular, setting `W=max_t m_t` preserves the original maximum width.
The result concerns a **fixed driver period**. It does 不 turn an exclusion
at period `P` into an exclusion at `kP` for every `k`.

These padded normal forms generally permit positive trims on overflow
steps. Agent 7's zero-overflow-trim restriction applies to maximally stripped
representatives. Imposing both normal forms simultaneously would be invalid.

## 4. Reproducible implementation 和 controls

All new source lives under `calculation/agent-110/`:

- `trim_equivalence.py`: independent full `cycleOK` arithmetic, explicit input
  rejection, constructive transport, balanced schedules, exact cap lift.
- `independent_controls.py`: separate integer-positional normalization 和
  independent Lean-source parsing; imports neither the mirror nor the transformer.
- `one_schedule.py`: one-pattern `-allm` mode; `--width W` checks exactly
  profiles A 和 B. Timeout/cap/error/missing completion remains `UNDECIDED`.

```bash
python3 calculation/neutral_band_search.py selftest
python3 calculation/agent-110/trim_equivalence.py selftest
python3 -O calculation/agent-110/trim_equivalence.py selftest
python3 calculation/agent-110/independent_controls.py
python3 calculation/agent-110/one_schedule.py --selftest
```

COMPUTED transformer controls: eight existing Lean-source positive bases
`2,4,8,11,16,17,26,32`; 56 binary schedules; 16 balanced transforms;
24 cap lifts, including eight preserving the original maximum; 280 repeated
concentrated schedules, 280 transports back to binary schedules, 800 random
compositions; **26,376 ordinary integer reverse-add edge checks**;
20,000 padding identities, 20,000 integer normalization checks, 和 16 malformed
inputs rejected. The same checks pass with Python assertions disabled (`-O`).

COMPUTED independent controls: **891,720** padding identities across bases
2,3,4,5,10; 1,008 schedule transports, including 112 nonbinary targets;
17,408 independently checked edges; **3,192** exact width-cap transports;
4,095 even-weight binary overflow streams of lengths 1..12. Empty/all-neutral
carry-flip failures were checked explicitly. Every listed check passed.

The runner has 15 completion-classification regressions, including contradictory
output, missing class coverage, caps, nonzero exit, 和 missing completion.
It conservatively retains the unchanged solver's `P<=32` boundary 和 rejects
legacy/fallback keys exceeding 256 bits; larger-period compiled extensions
belong to other agents.

## 5. Existing decimal negatives reproduced with one schedule

Compile the unchanged center solver:

```bash
c++ -O2 -std=c++17 calculation/neutral_band/structure/cauto_fast.cpp -o /tmp/agent110-cauto-fast
python3 calculation/agent-110/one_schedule.py /tmp/agent110-cauto-fast --e 10100110011 --g 11100010000
python3 calculation/agent-110/one_schedule.py /tmp/agent110-cauto-fast --e 10100110011 --g 11100010000 --repeat 2
python3 calculation/agent-110/one_schedule.py /tmp/agent110-cauto-fast --e 101010010101 --g 100010001000 --repeat 2
```

Each used cap 1,000,000 和 completed without caps or unresolved classes:

| Driver | Chosen v | Binary patterns replaced | maxstates | jstar / eventual period | Result |
|---|---|---:|---:|---|---|
| p11,k1 | `01000010000` | 55 | 755 | 5 / 1 | none, all lengths |
| p11,k2 | `0100001000001000010000` | 7,315 | 960,601 | 5 / 1 | none, all lengths |
| p12,k2 | `000010000000100000001000` | 2,024 | 152,584 | 6 / 1 | none, all lengths |

The eventual class count was 2 in every run; feasible classes were 0.
Measured subprocess wall times were approximately 0.005s, 1.13s, 和 0.16s.
These are implementation measurements, with no speed guarantee.

Exact bounded-profile examples:

```bash
python3 calculation/agent-110/one_schedule.py /tmp/agent110-cauto-fast --e 10100110011 --g 11100010000 --width 13
python3 calculation/agent-110/one_schedule.py /tmp/agent110-cauto-fast --e 101010010101 --g 100010001000 --repeat 2 --width 10
python3 calculation/agent-110/one_schedule.py /tmp/agent110-cauto-fast --base 2 --e 1010 --g 1010 --width 4 --witness
```

The first 两 commands returned `NO_CENTER_WIDTH_AT_MOST` after 两 complete
negative profiles. The base-2 control returned a center witness with widths
`3,4,4,3`; joining it to the existing source B/u edges passes mirror `cycleOK`.
Separate solver positives in bases 2,11,26 also replayed full certificates.

## Sources 和 attribution

- [Agent 7 padding/normalization](https://github.com/taco-jpg/p196-algorithm/pull/315)
  和 [canonical quotient](https://github.com/taco-jpg/p196-algorithm/pull/326).
- [Agent 107 general schedule transport](https://github.com/taco-jpg/p196-algorithm/issues/289#issuecomment-6432836759).
- [Agent 110 scope split](https://github.com/taco-jpg/p196-algorithm/issues/289#issuecomment-6432826635)
  和 [width-cap theorem](https://github.com/taco-jpg/p196-algorithm/issues/289#issuecomment-6432863425).
- Baseline: `calculation/neutral_band/README.md`, `structure/cauto_fast.cpp`,
  `calculation/neutral_band_search.py`, actual A120PowerTwo/KnownBases Lean certificates.

Baseline commit: `eafbbbfd6b5b857597f95f68268c56dbd96b6bcb`.
Repository verification: `python3 tools/verify.py --changed` returned
`ALL CHECKS PASSED`: 5,217 Lean files / 301 projects checked for repository
rules, zero changed Lean modules, zero endpoint audits. Independent campaign
review remains appropriate; no merge is requested by this report.
