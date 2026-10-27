# Agent 117 — Exact center-head trim language 和 its limit

Task: T3.center-boundary-language, coordination [#289](https://github.com/taco-jpg/p196-algorithm/issues/289#issuecomment-6432820476).
Source baseline: `eafbbbfd6b5b857597f95f68268c56dbd96b6bcb`.

**PAPER PROOF:** the complete one-edge existential relation for a normalized
decimal center's head, incoming carry, overflow, exact trim size, 和 target
head is given below. An arbitrary positive trim follows a four-state,
six-transition carry language. The relation admits balanced p11/k1 和
p12/k2 projected loops; repetition therefore covers every p11 k 和 every
even p12 k. Thus this exact local boundary abstraction, even with center
length accounting, cannot exclude those drivers at every width.

**COMPUTED:** independent full-word arithmetic audits, constructive local
witnesses, 和 the explicit projected loops reproduce the formulas.
**Scope:** these are local witnesses 和 a limitation of this abstraction.
They are neither consistent full-center cycles nor decimal certificates.
No new Lean theorem is claimed.

## 1. Sources 和 prerequisites

Definitions are the unchanged `norm`, `nextC`, `Hyp`, `edgeOK`, 和 `cycleOK`
in [A120Template.lean](../lean/P196/Drafts/Agent120NeutralBandCalibration/A120Template.lean)
和 [A120Certificate.lean](../lean/P196/Drafts/Agent120NeutralBandCalibration/A120Certificate.lean),
with the [Python mirror](../calculation/neutral_band_search.py).
Agent7's [normalization proof](https://github.com/taco-jpg/p196-algorithm/pull/315)
和 [canonical quotient](https://github.com/taco-jpg/p196-algorithm/pull/326)
justify maximal neutral stripping throughout an accepted cycle; these
prior results are credited, 不 claimed anew. The prior center length
identity gives `2*sum(v)=sum(g)` on a closed cycle.
Agent3's [odd-center invariant](https://github.com/taco-jpg/p196-algorithm/pull/318)
is addressed in Section 4. The fixed-driver all-length k1/k2 negatives
in the neutral-band README are prior computations, 不 new results here.

Every `nextC` is symmetric, so every center in a closed cycle is symmetric.
A center consisting only of neutral 9s transmits its incoming carry,
contradicting the required flip. Its normalized core is therefore nonempty
with head x different from 9. Put H={0,...,8,10,...,18}.

Symmetry makes the last coefficient equal x. A nonneutral last coefficient
resets the exit carry independently of the interior. Consequently

    e=1 when x<9; e=0 when x>9; z=x−10(1−e) lies in {0,...,8}.

This is an equivalence for every nonempty normalized symmetric center.

## 2. The complete local neutral-output language

Let a_j be the carry entering C[j]. At an outer paired layer j, write

    (L,R)=(a_j,a_(m−j)), (L',R')=(a_(j+1),a_(m−j−1)), c=C[j].

R is the outgoing carry of the reflected coefficient. For g=0 the raw
output coefficient q at this layer satisfies

    L'=floor((c+L)/10), R=floor((c+R')/10),
    q=(c+L) mod10 + (c+R') mod10.

If q=9, parity forces R'=1−L, then `2c=8+10(L'+R)`.
The carry inequalities leave exactly the following transitions:

| Outer carries (L,R) | c | Inner carries (L',R') |
|---|---:|---|
| (1,0) | 4 | (0,0) |
| (0,0) | 4 | (0,1) |
| (0,1) | 14 | (1,1) |
| (1,1) | 14 | (1,0) |
| (1,0) | 9 | (1,0) |
| (0,1) | 9 | (0,1) |

The table is necessary 和 sufficient for the paired local equations.
Normalization forbids an initial c=9. For e=1, a trimmed input prefix is
therefore a finite prefix of

    4,4, 9*, 14,14, 9*, 4,4, 9*, 14,14, ...

Each `9*` is an arbitrary finite run; the prefix can end inside a pair.
For e=0 use coefficientwise complements `18−c`.
This extends the previously known first-two-coefficient constraint to
arbitrary trim depth.

At an even midpoint the remaining carries must coincide. At an odd
midpoint the raw output coefficient is twice a digit, hence never 9.
A completely neutral even raw output can strip to empty, but an empty
target cannot belong to a legal closed cycle. The audits count such
inputs separately.

## 3. Exact one-edge existential head relation

For g=1, the raw head equals `(x+e) mod10 +9e`, which is never 9:

    v=0, e'=1−e, z'=z; equivalently y=x+10 if e=1, y=x−10 if e=0.

For g=0,v=0, with inward carry h in {0,1},

    y=2z+e+h, y!=9; e'=1[y<9].

Each choice is realizable by a sufficiently long symmetric center.
For positive trims, the exact relation is:

| Source (e,x) | Exact v | Possible target heads y |
|---|---:|---|
| (1,4) | 1 | H |
| (0,14) | 1 | H |
| (1,4) | 2 | H except 18 |
| (0,14) | 2 | H except 0 |
| (1,4) or (0,14) | every v>=3 | H |

No other normalized source head permits a positive trim.

**Proof of necessity.** The exit sets of nonneutral q values at a paired
carry state, obtained directly from the equations in Section 2, are

    E(0,0)=E(1,1)=H, E(0,1)=H\{18}, E(1,0)=H\{0}.

For example, at (0,0), c<=8 gives q=2c or 2c+1, while c=9 only permits
inward carry 0 和 gives q=18. Removing q=9 yields H. Complementation
gives (1,1); the other 两个 cases omit the indicated endpoint.
After one trimmed pair the state is 00/11 for e=1/0; after 两个 it is
01/10. This proves the v=1/2 entries.

**Constructive sufficiency, every v>=3.** With e=1 choose the trimmed
prefix `[4,4] ++ 9^(v−3) ++ [14]`, ending at state 11. With e=0 choose
its complement, ending at 00. Choose one further coefficient c 和 its
inward carry to realize any desired y in the corresponding exit set.
Place an inner symmetric reset core after c, then reflect the outside
prefix. A final core coefficient 0 or 10 supplies inward carry 0 or 1.
The raw image begins with exactly v neutral coefficients, then y!=9;
its canonical trim is exactly v. The same construction from states
00/11 or 01/10 proves the v=1/2 sufficiency statements. The target
remains nonempty 和 its head determines its next legal incoming carry.

Thus the positive-event abstraction allowing an arbitrary new head is
exact after existentially forgetting v: v=1 already realizes every head.
Retaining exact v removes only the 两个 displayed v=2 combinations.

## 4. Length, parity, 和 existing odd-center invariants

The constructions can use either source-length parity. They are available
at every sufficiently large prescribed source width: insert a symmetric
reset core of the required length after the exit coefficient.
For odd widths, the middle coefficient can remain even while arranging
`A(C)=sum_j (-1)^j C[j] == 9 (mod 11)`.

Indeed, with outside prefix P including the exit coefficient, choose an
inner core `[a,t,a]`. Choose a in 0..8 for required outward carry 0, or
10..18 for outward carry 1, 和 even t in 0..18. Then

    A(C)=2*sum_j (-1)^j P[j] + (-1)^|P|*(2a−t).

The possible `2a−t` values cover every residue modulo 11 in either carry
class, so the required congruence is always possible. Longer odd cores
use additional symmetric filler while retaining reset endpoints 和 a
tunable even middle. Even cores need only the reset endpoints.
The target also satisfies its appropriate odd-center invariant: the
nonoverflow relation preserves `A−9=0 (mod11)` under doubling 和 neutral
pair stripping; even-to-odd overflow supplies the invariant directly.
Consequently these already known odd-center conditions do 不 eliminate
any entry in the one-edge existential table.

## 5. Explicit balanced projected loops

For the documented p11 driver, use one period:

```text
e=10100110011
g=11100010000
heads=4,14,4,14,11,2,5,15,10,0,1
trims=0,0,0,2,0,0,0,0,0,0,0
```

Every local edge satisfies the exact table, including the v=2 edge
`(e,x,y)=(0,14,11)`. Closure gives G=4, V=2. Repeating this loop k times
gives a balanced projected loop for every k>=1.

For the documented p12 driver, use 两个 periods:

```text
e=101010010101101010010101
g=100010001000100010001000
heads=2,12,5,12,4,14,13,6,14,4,10,1,3,13,6,13,6,16,13,6,14,4,10,0
trims=0,0,0,0,0,3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
```

This gives G=6,V=3; repeat it for every even k. Odd k is impossible even
in this projection because the length equation would require `2V=3k`.
Joint rotations give the corresponding statements for the three p12
starting phases.

Assign `m_(t+1)=m_t+g_t−2v_t`. Both schedules close. Choose m0 sufficiently
large that every edge admits a local witness at its prescribed source
width; this can also respect odd-middle parity 和 the mod11 invariant.
**The quantifier gap remains:** each edge has some suitable finite center,
but its full output need not equal the finite source chosen for the next
edge. Only the heads, carries, trims, 和 widths are shared. No full center
cycle is reconstructed. Therefore the exact one-edge head abstraction
cannot establish the desired all-width p11 or even-p12 exclusions.

## 6. Reproduction 和 verification

Run from the repository root; every program uses the Python standard library:

```bash
python3 calculation/agent-117/center_boundary.py --selftest --drivers
python3 calculation/agent-117/trim_language_audit.py
python3 calculation/agent-117/independent_boundary_check.py
python3 tools/verify.py --changed
```

`center_boundary.py`: 15,224 exhaustive full-word edges, 19,965 sampled
wider edges, driver checks k=1..6, 和 the exact traces printed above.
Its dynamic program retains head, positive-event count, 和 whether a
trim event permits size 2. For surplus trim budget >=2, one event can
absorb the surplus with size >=3; surplus 1 needs a permitted v=2 site.

`trim_language_audit.py`: 260,640 normalized symmetric words through
width 8; 521,280 images; 897,768 paired-column tests; six empty images
separately excluded; 14,480 nonempty positive trims. Constructive checks
through v=128 give 9,212 accepted parity/head cases 和 four excluded
cases (the 两个 v=2 exceptions, tested at both parities). All 56 center
edges in the eight existing source certificates pass independent integer
normalization, padding, 和 normalized-overflow controls.

`independent_boundary_check.py` uses a separately written whole-integer
implementation, without importing the mirror or the other new programs.
It checks 137,178 canonical sources through width 7, 274,352 legal edges,
four empty targets, 770 local classes through v=20, 2,310 basic witnesses,
和 3,850 invariant-compatible witnesses at prescribed widths. Every edge
of the p11 loop lifts locally at m0=12 (widths 11..15); every edge of the
p12 loop lifts at m0=20 (widths 16..22). The chosen full-word witnesses
fail to chain at 10/11 和 23/24 boundaries respectively, as explicitly
reported by the program. These failures illustrate the quantifier gap;
they do 不 assert that no different full-word witnesses could chain.

The repository gate returned `ALL CHECKS PASSED`: 5,217 Lean files,
301 registered projects, zero changed Lean modules, zero audited
endpoints. No Lean file or registry entry changes; this PASS checks
repository rules, not kernel verification of this paper theorem.

## 7. Limit 和 next useful step

Any stronger obstruction must retain compatibility of interior coefficients
across multiple times, use additional center information that genuinely
restricts this relation, or solve the full center system. Merely refining
the exact head/trim transition table, keeping the same state information,
cannot remove the displayed locally realizable balanced loops.
