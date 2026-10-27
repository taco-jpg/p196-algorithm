# Agent 114 — neutral exterior padding in the unchanged A120 checker

## Result and attribution

**LEAN-VERIFIED:** arbitrary neutral exterior suffix padding preserves `Hyp`,
both interface carries, overflow, and the center successor; the exterior
successor gains the same suffix. The original Boolean `edgeOK` is equivalent
before and after a balanced redistribution of source padding, target padding,
and exterior trim. This holds in every base at least two, with arbitrary finite
interfaces, including an empty exterior. Center symmetry is not assumed.

This formalizes the exterior part of Agent 7's prior PAPER padding argument;
the mathematical mechanism is credited to
[issue 301](https://github.com/taco-jpg/p196-algorithm/issues/301) and
[PR 315](https://github.com/taco-jpg/p196-algorithm/pull/315).
Agent 7's canonical-cycle theorem in
[PR 326](https://github.com/taco-jpg/p196-algorithm/pull/326) is a separate result.
Agent 119 owns the concurrent center-padding formalization; this contribution
changes no center representation and imports no unpublished center lemma.

Checked repository base: `eafbbbfd6b5b857597f95f68268c56dbd96b6bcb`.
The A120 definitions and certificate checker are unchanged.

## Exact statements

Put `h = b - 1` and `S_a(B) = B ++ h^a`, where coefficients are least
significant first. Under `Hyp b B C`, for every natural padding length `a`:

```text
Hyp b (S_a B) C <-> Hyp b B C
e1 b (S_a B) = e1 b B
e2 b (S_a B) C = e2 b B C
gam b (S_a B) C = gam b B C
nextB b (S_a B) C = S_a (nextB b B C)
nextC b (S_a B) C = nextC b B C
```

The `Hyp` equivalence is unconditional; either side supplies the base and
coefficient bounds needed in its implication. Additional registered endpoints
give the exact normalized digit words `DB`, `DC`, `DR` and `xd`, `yd`.

For an original edge `E`, define `padEdge b a a' w E` by replacing
`B` with `S_a(B)`, `B2` with `S_a'(B2)`, and `u` with `w`, leaving `C`,
`C2`, and `v` unchanged. The principal checked-edge theorem is:

```text
a + E.u = w + a' ->
  (edgeOK b (padEdge b a a' w E) = true <-> edgeOK b E = true)
```

All offsets and trim counts are natural numbers. Thus no truncated subtraction
or unproved nonnegativity condition is hidden in this formulation. It includes
zero padding, zero trim, empty source exterior, and empty target exterior.
The theorem preserves the original checker's source-only `Hyp` semantics;
target validity is supplied by the next checked edge when there is a chain.

## Proof structure

`ExteriorPadding.lean` imports the existing A120 template module. The existing
`norm_append` and `norm_replicate_neutral` identify normalization of a neutral
suffix. Forward normalization appends `a` copies of `h*(1-e1)`; reverse
normalization prepends `a` copies of `h*(1-e2)`. Their sum is `h` because
`Hyp` forces the two carries to be complementary.

The proof handles both overflow branches of `nextB`, including the extra
coefficient in the overflow branch. The source head condition is proved
equivalent separately, treating an empty exterior explicitly. Removing an
added suffix recovers the original coefficient bound and carry flip, giving
the reverse `Hyp` implication.

`EdgeTransport.lean` first proves a propositional equivalence for the exact
original Boolean `edgeOK`. For exterior transport the count equation gives

```text
S_a'(E.B2) ++ h^w = (E.B2 ++ h^E.u) ++ h^a.
```

The forward direction uses covariance. The reverse direction cancels the
common suffix `h^a`; ordinary list cancellation needs no nonempty assumption.
The center equation is unchanged by `nextC_suffixPad`.

## Lean validation

Project `Agent114NeutralExteriorPadding` registers two modules and 14
endpoints in `lean/registry.json`:

```text
P196.Agent114NeutralExteriorPadding.ExteriorPadding
P196.Agent114NeutralExteriorPadding.EdgeTransport
```

Commands from the repository root, with Lean 4.19.0 on `PATH`:

```bash
export LEAN_NUM_THREADS=1
ulimit -v 8388608
cd lean
timeout 1200 lake build P196.Agent114NeutralExteriorPadding.EdgeTransport
cd ..
timeout 1200 python3 tools/verify.py --changed
```

Actual repository-gate result:

```text
[rules] 5219 Lean files, 302 projects, OK
[changed] against origin/main: 2 new/changed Lean file(s); building 2 module(s); auditing 1 project(s)
[build] OK
[kernel replay] 2 module(s) re-checked by lean4checker
[axioms] 14 endpoints checked
ALL CHECKS PASSED (changed files only, against origin/main)
```

All registered endpoints use only allowed axioms. The six printed core
endpoints depend exactly on `[propext, Quot.sound]`.
No forbidden proof mechanism or additional axiom is used.

Each file was also compiled separately with `lake env lean`, one Lean thread,
the same 8 GiB address-space limit, and a 1,200-second timeout:

| File | Exit | Wall seconds | Peak RSS KiB |
| --- | ---: | ---: | ---: |
| `ExteriorPadding.lean` | 0 | 1.406 | 454580 |
| `EdgeTransport.lean` | 0 | 0.540 | 427484 |

`/usr/bin/time` is absent in this environment, so these measurements use
Python `time.monotonic()` and `os.wait4(pid, 0).ru_maxrss` for each child.
Both files are far below the repository's per-file resource limits.

## Independent arithmetic controls — COMPUTED

The standalone standard-library script normalizes a whole positional integer
using repeated `divmod`; it does not use the mirror's normalization to decide
its own assertions. The repository mirror is a differential control and its
Lean-source reader supplies the eight pre-existing certificate fixtures.

Exact commands from the repository root:

```bash
python3 calculation/agent-114/exterior_padding_controls.py
python3 -O calculation/agent-114/exterior_padding_controls.py
python3 calculation/neutral_band_search.py selftest
```

Both control runs produce the same counts and end with
`ALL EXTERIOR PADDING CONTROLS PASSED`; the third command ends with
`SELFTEST PASSED`.

| Control | Exact count |
| --- | ---: |
| Exhaustive sources, bases 2–5, both widths <=2 | 5282 |
| Exhaustive padding identities | 21128 |
| Seeded sources, bases 2–32 | 3968 |
| Seeded padding identities | 15872 |
| Dedicated large-padding identities, lengths 64 and 257 | 62 |
| All padding identities | 37062 |
| Identities with empty exterior | 3878 |
| Whole-integer state comparisons against the mirror | 46343 |
| Accepted-edge transport equivalences | 4096 |
| Rejected-edge transport equivalences | 4960 |
| Existing source bases / original edges | 8 / 56 |
| Complete transported cycles / their edges | 224 / 1792 |
| Rejected malformed edges / transport parameters | 14 / 5 |

Seed `114` is fixed. Seeded exterior widths are at most 8 and center widths
at most 10; symmetric and nonsymmetric centers are included. The complete
cycle controls redistribute exterior trim totals among phases, choosing
natural offsets from prefix differences. They verify every transported edge,
adjacent interface, closure, overflow, and gain with both independent
integer arithmetic and the original Python `cycleOK` mirror.
Every guard and acceptance assertion is an explicit branch, so optimized
Python does not disable a check.

## Scope limits

The universal Lean result concerns local exterior padding and checked-edge
transport. The complete transported-cycle examples are finite COMPUTED
controls; this PR does not yet formalize arbitrary chain/cycle transport,
maximal-suffix decomposition, or full canonicalization.

No new base-10 cycle, finite-search exclusion, all-period obstruction,
ordinary-decimal Lychrel existence theorem, or statement about the orbit of
196 is claimed. The result supplies a verified local tool for later
certificate-preserving normalization and search reductions.
