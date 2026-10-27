# Agent 114 — fixed center windows retain false projected loops

Task: **T3.center-core-projection**, coordination [#289](https://github.com/taco-jpg/p196-algorithm/issues/289).

**PAPER PROOF.** Every finite centered-window radius admits a closed projected
path for the documented p11 stream, at every repetition, 和 for p12 at every
even repetition. This persists with exact center lengths, maximal trim labels,
all retained normalization digits/carries, the mod-9 coefficient sum, 和 the
established odd-center mod-11/middle-parity conditions. Each projected edge has
a genuine normalized full-center witness. Different edges use different
unrecorded outer coefficients; their full centers do **不** close.

**Scope:** a limitation of this precisely defined abstraction, independent of
its finite radius. Actual center existence, an all-width center obstruction,
和 decimal Lychrel existence remain unresolved. This result is **不
LEAN-VERIFIED**. No candidate certificate is asserted.

## 1. Prior results 和 exact abstraction

The definitions are the center part of
`calculation/neutral_band_search.py`, mirroring
`Agent120NeutralBandCalibration/A120Template.lean`:

\[
D=\operatorname{norm}_{10}(C,e).\mathrm{digits},\qquad
\operatorname{carryOut}(C,e)=1-e,
\]
\[
F_g(C,e)=\begin{cases}
\operatorname{pairs}(D),&g=0,\\
\operatorname{pairs}(D\mathbin{+\!+}[9e]),&g=1.
\end{cases}
\]

Here `pairs` adds a word to its reversal, coefficientwise. All words are
least-significant-first; coefficients belong to `0..18`. The center is
symmetric. A normalized center has first coefficient different from 9.
Remove the maximal outer neutral-9 pairs from `F_g`, obtaining `C'` 和 trim `v`.
Also require the target flip `carryOut(C',e')=1-e'`.

The prior mathematical ingredients retain their original attribution:

- Agent 7: normalized maximal trimming, [#315](https://github.com/taco-jpg/p196-algorithm/pull/315)
  和 [#326](https://github.com/taco-jpg/p196-algorithm/pull/326).
- Agent 2: `s'=2s+4e-2 (mod 9)`,
  [#312](https://github.com/taco-jpg/p196-algorithm/pull/312).
- Agent 3: odd-center alternating sum `A(C)=9 (mod 11)` 和 even midpoint,
  [#303](https://github.com/taco-jpg/p196-algorithm/issues/303).

Fix `r>=1`. The projection records `e`, exact length `N`, the centered
`2r+(N mod 2)` coefficients, their normalization digits 和 every carry touching
that window, `sum(C) mod 9`, 和 `A(C) mod 11` at odd lengths. Each edge also
records `g` 和 actual maximal `v`. The projected relation contains an edge
exactly when **some** full-center edge realizes its source 和 target records.
Short centers may be retained exactly; the constructed paths remain longer
than the window throughout, so short-state handling does 不 affect the result.

## 2. Ten exact shell witnesses

For a finite shell `S`, take

\[
C=S\mathbin{+\!+}0^M\mathbin{+\!+}\operatorname{reverse}(S),
\qquad M\ge4.
\]

The following table gives every mode required below. `R` is the displayed
outer shell of the **trimmed** target; the target has form `R 0^m reverse(R)`.

| e | g | e' | v | Source shell S | Target shell R | m |
|---:|---:|---:|---:|---|---|---:|
| 0 | 0 | 0 | 0 | 15,5 | 10,11 | M |
| 0 | 0 | 1 | 0 | 10,0 | 0,1 | M |
| 1 | 0 | 0 | 0 | 5,6 | 11,12 | M |
| 1 | 0 | 1 | 0 | 0,1 | 1,2 | M |
| 0 | 0 | 0 | 1 | 14,15,0 | 11,1 | M |
| 0 | 0 | 1 | 1 | 14,10,6 | 1,13 | M |
| 1 | 0 | 0 | 1 | 4,5,0 | 10,0 | M |
| 1 | 0 | 1 | 1 | 4,0,6 | 0,12 | M |
| 0 | 1 | 1 | 0 | 10,0 | 0,1,0 | M-1 |
| 1 | 1 | 0 | 0 | 0,1 | 10,1,1 | M-1 |

**Proof of the table.** Normalize each listed coefficient with its entering
carry, using `(x+c) mod 10` 和 `floor((x+c)/10)`. After at most one zero,
the carry through the central zero block is 0. Pair the normalized word,
appending `9e` first precisely when `g=1`.
For the four `v=1` rows the raw outer pair is 9; its next coefficient is,
respectively, `11,1,10,0`. Thus the maximal trim is exactly 1. The other raw
outer coefficients are different from 9, giving maximal trim 0.
The source outer coefficient is below 9 precisely when `e=1`; the target
outer coefficient is below 9 precisely when `e'=1`. These strict inequalities
force the respective exit carries to `1-e` 和 `1-e'`, independent of the
incoming carry into the last coefficient. Every source 和 target is normalized.

At odd source lengths the alternating sum is twice the alternating shell sum.
Those shell sums are congruent to `10 (mod 11)`, so `A(C)=9 (mod 11)`.
The table gives the same congruence at every odd target. The middle coefficient
is 0. For sufficiently large `M`, all coefficients, digits 和 carries in either
retained central window are zero.

## 3. Independent adjustment of the mod-9 sum

Insert the guarded filler `H_d=[0,d,d,0]`, for `d=0..8`, just inside the shell:

\[
C=S\mathbin{+\!+}H_d\mathbin{+\!+}0^M
  \mathbin{+\!+}\operatorname{reverse}(H_d)
  \mathbin{+\!+}\operatorname{reverse}(S).
\]

The leading zero kills any carry from `S` before either `d`; each `d<9`
passes carry 0, 和 the last zero separates the filler from the central block.
On the other side the reversed filler also exits with carry 0.
Consequently the shell's normalization, outer target coefficients, source/
target flips 和 maximal trim counts in the table remain valid. Any changes
near the filler remain outside a sufficiently deep retained window.

The symmetric filler contributes `4d` to the coefficient sum 和 zero to the
odd alternating sum. Since `4*7=1 (mod 9)`, any requested residue `s` is realized
by

\[
d=7\left(s-2\sum S\right)\pmod9,\qquad 0\le d\le8.
\]

The existing exact recurrence then gives target residue
`s'=2s+4e-2 (mod 9)`. Thus the zero-core construction also respects the global
mod-9 state; this checksum does 不 distinguish its adjacent full-word witnesses.

## 4. Closing the projected path, including lengths 和 trims

Consider any periodic bits `(e_t,g_t)` satisfying

1. `g_t=1` implies `e_(t+1)=1-e_t`;
2. a chosen binary trim schedule has `v_t=0` when `g_t=1` 和 `2 sum(v)=sum(g)`;
3. the affine mod-9 recurrence admits a periodic residue sequence `s_t`.

Define `N_(t+1)=N_t+g_t-2v_t`. Condition 2 makes the exact lengths close.
Choose the common initial length large enough that every source's
`M_t=N_t-2 len(S_t)-8` leaves the retained window inside a zero block, with
at least one zero of carry-reset margin on either side. Increasing the common
initial length preserves every edge's length equation, so any finite radius
is permitted.

At phase `t`, select the table row `(e_t,g_t,e_(t+1),v_t)`, its filler realizing
`s_t`, 和 its exact required length. Its target projection equals the next
source projection: same `e`, length, zero coefficients/digits/carries,
coefficient-sum residue, 和 odd alternating-sum residue. The projected path
therefore closes. Every edge has an actual full-word witness; compatibility
of those witnesses outside the retained state is deliberately absent.

For p11, `g=11100010000`, `e=10100110011`: there are four overflows 和 seven
nonoverflow phases per repetition. Choose any two nonoverflow trims per
repetition. The one-period sum map is `s -> 5s+6 (mod 9)`, fixing `s=3`.
All three conditions hold for every repetition count.

For p12, `g=100010001000`, `e=101010010101`: there are three overflows 和 nine
nonoverflow phases per repetition; the one-period sum map is the identity.
Every even repetition count admits `3k/2` nonoverflow trims. Odd `k` already
fails the prior exact length-parity condition. Joint phase rotations preserve
the construction, covering the three documented p12 carry rotations.

This proves the claimed projection limitation at **every finite radius**.
It does **不** produce a full center cycle: adjacent edge witnesses can have
different outer coefficients even when every recorded quantity agrees.
Indeed, canonical phase 0 in either documented stream has `(e,g)=(1,1)`;
its target starts `[10,1]`. The next p11 source starts `[10,0]`. The next
p12 source starts `[10,0]` when `v=0`, or `[14,10,6]` when `v=1`.
Thus a full-word mismatch exists for every radius, repetition 和 filler choice,
independently of the finite checks below.

## 5. Reproduction 和 verification

From the repository root:

```bash
python3 calculation/agent-114/center_core_projection.py --max-radius 32
python3 calculation/agent-114/verify_center_core.py
python3 tools/verify.py --changed
```

The main construction checks 5,760 local witnesses (radii 1..32, both parities,
ten modes, all nine residues), 和 90 full `edgeOK`/target-`Hyp` comparisons
against the existing mirror. It constructs 14 projected loops: p11 repetitions
1,2,3,4 和 p12 repetitions 2,4,6, at radii 1 和 32.

```text
LOCAL_WITNESSES=5760 MIRROR_EDGES=90 PASS
PROJECTED_LOOPS=14 FULL_CENTER_CYCLE_CLAIM=False PASS
```

At radius 32, p11 k=1 has center lengths 88..92 和 11 full-word mismatches;
p12 k=4 has lengths 88..99 和 41 mismatches. These directly expose the missing
full-center compatibility instead of presenting the projected paths as hits.

The independent verifier uses ordinary integer evaluation/division for
normalization, separate shell data 和 independently assembled transitions;
it imports neither the main program nor the repository mirror.
Its default audit covers both starting parities 和 every allowed initial
mod-9 residue at radii 1..12:

```text
shell_checks=2160 projected_loops=840 loop_edge_checks=36912
PASS: bigint center arithmetic, maximal trims, core coefficients/digits/carries, mod9, odd mod11, exact lengths, projected closure
```

Repository verification is reported separately from mathematical status:
the change contains no Lean module, so a changed-files pass supplies no new
kernel-checked theorem.
The actual gate passed against `eafbbbfd6b5b857597f95f68268c56dbd96b6bcb`:
5,217 registered Lean files, 301 projects, zero changed Lean modules,
`ALL CHECKS PASSED (changed files only, against origin/main)`.

## 6. Consequence for follow-up work

Increasing an isolated central-window radius cannot remove these projected
loops. A stronger decision procedure must retain cross-phase compatibility
of the omitted outer word, a boundary-to-core relation, or another global
invariant. This result leaves such strengthened procedures open. It also
leaves the existing full-center automata 和 bounded full-word graphs intact.
