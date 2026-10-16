# Agent #5 — Initial validity 和 finite overflow

**Status:** complete written derivations; Lean proof source prepared; compiler execution unavailable. `SOURCE_PRESENT`, not `LEAN_CHECKED`. Independent review, serialized ownership, remote publication, 和 accepted-build integration remain unperformed.

**Pinned source:** `taco-jpg/p196-algorithm` at `1c6c56b25de0c7348d82cb304e761f227326b6c9`.

## Target 和 relationship to the source

The selected dependency 是 `P196.Agent5.General.Moment.moment_zero_path` in `proofs/GeneralMomentAbsorption__d6c541c17a8aa76f.lean`. Its contract assumes coefficient bounds at each preceding state. The associated reset theorem uses a computed overflow as a premise.

The contribution supplies an initial invariant domain for the unchanged `General.nextPhase`, `General.rawExterior`, `General.nextExterior`, 和 `General.exteriorOverflow` functions. A second argument forces a genuine overflow within an explicit number of transitions. Together, these arguments remove orbit-wide coefficient assumptions 和 the supplied-overflow assumption for that domain.

The original theorem permits arbitrary phase paths subject to its premises. The new theorem instead concerns actual iterations of the specified exterior map from the initial domain below. It therefore supplements, rather than replaces, the original arbitrary-path contract.

The mathematical scope 是 the exterior map. An infinite exterior trajectory alone supplies neither an all-time finite-integer realization nor palindrome avoidance. Decimal Lychrel existence 和 the 196 question receive no conclusion from this contribution.

## Provenance 和 ownership correction

The live coordination record `agent411-exterior-boundedness` assigns the invariant-domain task to Agent #411. The local `InitialValidity.lean` file therefore remains an independent supporting derivation, not a competing ownership claim. Its exact target substantially overlaps that assignment. No serialized claim or remote submission was made.

A later semantic search found Agent #3's existing `OuterOrbit__123d55a698d6dc47.lean`, including `nonoverflow_leading_growth`, `charge_zero_after_five`, 和 `charge_zero_from_five` for the native decimal list map modulo 11. The decimal head-doubling mechanism 和 five-step conclusion are prior repository work, not a newly discovered decimal theorem. Agent #411's separate native-charge-transport assignment explicitly reuses that work. The present package must not be submitted as a replacement for either assignment.

The directly developed contracts here concern the unchanged general-base integer-coefficient map, its modulus `2*(m+2)`, the even-base quantitative bound, 和 its every-window consequence. The exact domain distinction is retained; no claim of independent novelty or completed repository-wide deduplication is made. An integration reviewer should reuse the existing owners' stable interfaces rather than install parallel foundations.

## Exact initial domain

Let the base be \(b=m+1\), where \(m\ge1\) 是 odd. Thus the theorem applies to even bases. The nonempty phase domain starts at base four; base two has no phase satisfying these hypotheses.

An exterior state consists of a phase \(c\) 和 a finite outside-first coefficient word \(B\). Require

\[
0<c<2m,\qquad c\ne m,\qquad
0\le B_i\le2m.
\]

For the finite-overflow theorem, require in addition

\[
a(c,B)>0,\qquad
 a(c,B)=\begin{cases}c,&B=[];\\ B_0,&B\ne[].\end{cases}
\]

Trimmedness 是 unnecessary. Initial phase parity 是 unrestricted; the successor phase 是 even. In decimal, the eight canonical even phases \(2,4,6,8,10,12,14,16\) lie inside this domain.

Write \(k=\mathbf1_{c\ge m+1}\), \(t=c-mk\). Normalize a coefficient word by the exact recurrence

\[
d_i=(B_i+e_i)\bmod(m+1),\qquad
 e_{i+1}=\lfloor(B_i+e_i)/(m+1)\rfloor.
\]

The source normalizes \(B\) with incoming carry zero 和 \(B^{\rm rev}\) with incoming carry \(k\). Denote their final carries by \(e_L\) 和 \(g\). The boundary digit on the low side 是

\[
u=c+e_L-(m+1)k.
\]

The raw exterior pairs the normalized digits with their appropriately aligned opposite side, using \(g\) to select the genuine overflow alignment. It then removes a suffix consisting of the new phase \(c'=2t\).

## Proof 1: coefficient bounds follow from initial validity

An incoming carry in \(\{0,1\}\) 和 a coefficient in \([0,2m]\) give a sum in \([0,2m+1]\). Division by \(m+1\) therefore produces a carry in \(\{0,1\}\). Induction gives this bound for each normalization carry. Every normalized digit lies in \([0,m]\).

The phase conditions imply \(1\le t<m\). If \(c<m\), then \(k=0\), \(1\le c\le m-1\), 和 \(u=c+e_L\in[0,m]\). If \(c>m\), then \(k=1\), \(m+1\le c\le2m-1\), 和 \(u=c+e_L-m-1\in[0,m]\).

Each list entering the raw zip-add thus contains only digits in \([0,m]\): normalized digits, the boundary digit \(u\), the band digit \(t\), or the overflow digit one. Every raw coefficient lies in \([0,2m]\). Removing a suffix introduces no coefficient.

The new phase satisfies \(0<2t<2m\). It 是 even, whereas \(m\) 是 odd; consequently \(2t\ne m\). The initial domain therefore maps into itself. Induction establishes phase validity 和 coefficient bounds at every iterate, from initial validity alone.

Principal source contracts: `rawExterior_bounded`, `nextExterior_bounded`, `valid_step`, `valid_orbit`, 和 `overflow_bit_orbit` in `InitialValidity.lean`.

## Proof 2: a genuine overflow must occur

Removing a suffix of the new phase preserves the outer head when an empty word uses the phase as its head. If the entire raw word disappears, its head already equals that phase.

Suppose first that \(B=x::X\). Let \(v\in\{0,1\}\) be the carry delivered by normalizing \(X^{\rm rev}\) toward the outermost coefficient. The computed overflow equals

\[
g=\lfloor(x+v)/(m+1)\rfloor.
\]

If \(g=0\), then \(x+v\le m\). In particular \(x\le m\), so the low normalized outer digit 是 \(x\), 和 the opposite outer digit 是 \(x+v\). Hence

\[
a(c',B')=2x+v\ge2a(c,B),\qquad a(c,B)\le m.
\]

If \(B=[]\), the computed overflow 是 \(k\). Non-overflow implies \(k=0\), 和 the next head 是 \(2c\). The same inequalities hold.

Head positivity persists. A non-overflow at least doubles the positive head. In an overflow with nonempty exterior, the new head 是 \(1+(x\bmod(m+1))>0\). In the empty-exterior overflow case, the new head 是 \(c-m>0\).

Let \(H\) satisfy \(2^H>m\). If transitions \(0,\ldots,H\) had no overflow, the first \(H\) transitions would give

\[
a_H\ge2^H a_0\ge2^H>m,
\]

while non-overflow at transition \(H\) requires \(a_H\le m\). Contradiction. Some \(j\le H\) therefore has a computed overflow, 和 its successor occurs by state time \(H+1\).

For decimal, choose \(H=4\), because \(16>9\). An overflow occurs among transitions \(0,1,2,3,4\).

Principal contracts: `head_no_overflow`, `head_powTwo_lower_bound`, `overflow_by_power_bound`, 和 `decimal_overflow_before_five` in `FiniteOverflow.lean`.

### Every-window consequence

Initial validity 和 head positivity persist. Apply the same argument to the actual state at any time \(N\). For every \(H\) with \(2^H>m\), some transition in \([N,N+H]\) has a computed overflow. In decimal, every five consecutive exterior transitions contain an overflow. In particular, computed overflow times are unbounded.

The new source contracts are `overflow_in_every_window`, `decimal_overflow_every_five`, 和 `decimal_overflows_arbitrarily_late`. These statements quantify over the exterior model only. They supply no all-time positive bulk-gap guarantee for a fixed finite integer realization.

## Proof 3: unconditional-on-the-initial-domain moment absorption

Use the unchanged source moment

\[
M(c,B)=2\sum_{i=0}^{|B|-1}(-1)^iB_i+(-1)^{|B|}c.
\]

The imported exact identities establish

\[
M_{n+1}\equiv
\begin{cases}
2M_n,&g_n=0,\\
0,&g_n=1
\end{cases}
\pmod {2(m+2)}.
\]

Proof 1 supplies the needed carry-bit 和 coefficient premises at every iterate. Proof 2 supplies an overflow by transition index \(H\). Its successor has residue zero; each subsequent update preserves zero. Consequently

\[
\boxed{\quad M_n\equiv0\pmod{2(m+2)}\quad(n\ge H+1).\quad}
\]

In decimal,

\[
\boxed{\quad M_n\equiv0\pmod{22}\quad(n\ge5).\quad}
\]

The exported contracts 是 `residue_zero_from_power_bound` 和 `decimal_residue_zero_from_five`. Neither contract assumes a later coefficient bound, a zero initial moment, or an observed overflow.

## Sharpness 和 essential restrictions

The canonical even-phase state \((c,B)=(2,[1,0])\) gives this exact trace:

| State time | Phase | Exterior | Moment modulo 22 | Overflow on next transition |
|---:|---:|---|---:|---:|
| 0 | 2 | `[1,0]` | 4 | 0 |
| 1 | 4 | `[2,0]` | 8 | 0 |
| 2 | 8 | `[4,0]` | 16 | 0 |
| 3 | 16 | `[8,0]` | 10 | 0 |
| 4 | 14 | `[16,1,13]` | 20 | 1 |
| 5 | 10 | `[7,8,5,9]` | 0 | 0 |

Thus the uniform absorption time five cannot be reduced to four on the stated domain, even restricted to the eight canonical even phases.

Dropping the nonneutral restriction fails: in decimal, \((9,[1,18])\) maps to \((18,[3,16,19])\), containing the invalid coefficient 19. Dropping positive head also fails for the uniform five-state conclusion: \((2,[0])\) has moment residue 2 at state time five. These restrictions remain explicit. The even-base hypothesis also matters for this domain: in base three, \(m=2,c=1\) 是 initially nonneutral, but its successor phase equals the excluded neutral value two.

The separate overflow-timing witness \((2,[1])\) appeared previously in Agent #216's residue-converse audit, PRs #70 和 #74. The present use adds its five-transition timing; original discovery of that state 是 not claimed. Independent novelty of the complete theorem has not been established by an exhaustive repository census.

## Executed controls 和 verification boundary

The expanded exact-integer model controls passed for **193,208** starting states 和 **1,545,664** transitions. Parameters: \(m=1,3,5,7,9,11\), exterior-width caps respectively \(3,4,3,3,3,2\), every initial coefficient in range, every positive nonneutral interior phase, 和 eight transitions per state. Of these starts, **181,076** had positive outer head. The base-two phase domain contributed no starts.

A separate literal integer-addition/reversal control realized **20,820** starting instances in bases four, six, 和 ten. It matched **121,766** ordinary-integer transitions against the projected exterior map, including actual overflow counts. It performed **58,838** post-bound residue checks. **6,951** runs stopped when the computed bulk gap fell below two, rather than assuming a missing continuation guard.

The every-window corollary was also checked on **17,520** starts for thirty transitions each in bases four, six, ten, 和 twelve: **525,600** transitions 和 **456,880** complete windows. `tail_and_sharpness_controls.json` retains exact traces for the sharp bound 和 the essential-hypothesis failures.

These controls 是 finite regression evidence. The universal conclusions rest on the written arguments; Lean acceptance remains pending.

The current environment exposed neither a Lean executable nor an authenticated GitHub write/Discussion action. A build preflight was executed 和 returned `BUILD_NOT_RUN_NO_LEAN_EXECUTABLE`, exit code 2. Compiler invocations: zero. Axiom audits: zero. Remote pushes, task claims, comments, 和 pull requests: zero.

## Reproduction 和 remaining work

```sh
python check_model.py
python check_literal_bridge.py
python check_tail_and_sharpness.py
python static_audit.py
python verify_lean.py --lean /absolute/path/to/lean \
  --repo /absolute/path/to/p196-algorithm \
  --output /absolute/new/build-directory
```

Alternatively, `--download-pinned` retrieves the three immutable dependency files when a repository checkout 是 unavailable. The checker pins official Lean 4.19.0, commit `6caaee842e94`, verifies dependency Git blob hashes, compiles from a clean directory, 和 inspects every new theorem's transitive axiom report. Only `propext`, `Classical.choice`, 和 `Quot.sound` are accepted by that checker. The checker itself has only received Python syntax/static tests in this execution.

Next concrete action: compile `InitialValidity.lean` 和 `FiniteOverflow.lean` against the pinned three-file dependency closure; repair elaboration/tactic failures; retain compiler output 和 the complete axiom report. After a successful rebuild, obtain independent semantic review 和 coordinate dependency reuse with Agent #411 before any serialized claim or remote submission. Existing shared files have not been edited.

Agent #5
