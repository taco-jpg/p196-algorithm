# Complete finite numerical decoder scan

Agent 105, session `9df76b`; source author `/root/structure105`.
Claim coordination commit: `2873e4a2fa49854d8c6b4b77d972f15ff1253527`.
Integration branch: `research/agent-105/numeric-decoder-9df76b-20261016`.

The frozen source is `proofs/Agent105DecoderScan9df76b.lean`, namespace
`Agent105DecoderScan9df76b`. Its SHA-256 is
`4e7f3a29e41c3e40adc08326947fe28b5505015f3c68cba67a1cb648318cad1d`.

## Public function and exact specification

```lean
def decodeAtWidth (e : Nat → Nat) (L h : Nat) : Option (List Nat)
```

The target payload consists of the first `L` values of `e`, in
least-significant-first order. `h` is the candidate final carry. A
successful result is the full finite source column-sum word, also
least-significant first. The function rejects zero width, `h > 1`, and
a zero exterior coefficient. Interior zero coefficients remain allowed.

The exact public theorem is:

```lean
theorem decodeAtWidth_eq_some_iff
    (e : Nat → Nat) (L h : Nat) (qs : List Nat)
    (he : ∀ i, i < L → e i ≤ 9) :
    decodeAtWidth e L h = some qs ↔
      qs.length = L ∧
      FoldedDecimal.Admissible L (Agent101.digitFn qs) ∧
      (∀ i, i < L →
        DecimalDigits.output (Agent101.digitFn qs) i = e i) ∧
      DecimalDigits.carry (Agent101.digitFn qs) L = h
```

`decodeAtWidth_isSome_iff` gives the same condition existentially over
`qs` for `(decodeAtWidth e L h).isSome = true`. This is the interface
used by the integration agent's actual numeric-target wrapper.

The semantics are the original definitions: `Admissible` asserts positive
finite width, positive exterior coefficient, coefficients at most 18,
reflection symmetry, and even self-reflected center coefficients.
`output` and `carry` are the original physical decimal normalization.
`digitFn` is Agent101's existing finite-list extension by zero.

## Complete scan and proof

The executable `scan L e a b` has exactly three recursive cases:

- At width zero it accepts the empty interior precisely when `a = b`.
- At width one it delegates to the exact local center solver, enforcing
  `q + a = e 0 + 10*b`, `q ≤ 18`, and even `q`.
- At width `L + 2` it reads `e 0` and `e (L + 1)`, asks the exact local
  pair solver for the shared outer coefficient and the next two carries,
  recursively scans the shifted inner payload, and returns the shared
  coefficient around the returned inner list.

`scan_sound` proves that every success, from two boundary carry bits,
returns a word of precisely the requested length with the original
bounds, symmetry, and center parity. It also constructs a complete
bit-valued trace `c` satisfying

```text
c 0 = a,  c L = b,
digitFn qs i + c i = e i + 10*c (i+1)  for every i < L.
```

`scan_complete` proves the converse for any finite word and any complete
trace satisfying those same original column equations and bounds. The
proof strips equal outer coefficients using symmetry and list length,
obtains exactly the local pair edge, applies the induction hypothesis to
the inner word and shifted trace, and reconstructs the finite list.

At the public root, the target digit bound implies that every trace
equation determines the standard division-by-10 recurrence. The original
`FoldedDecimal.forward_trace_unique` then identifies the whole trace with
`DecimalDigits.carry`. The original `column_equation` identifies the
emitted digits with `output`. The positive exterior and width guards add
exactly the remaining `Admissible` requirements. Conversely, an actual
admissible output/carry specification supplies a complete trace directly,
so `scan_complete` recovers the word and the root guards pass.

## Boundary semantics

The assumption `he` is essential to the public physical specification.
The local solver accepts natural-number equations; without `he`, a value
such as target payload `[10]`, width 1, and carry 0 could satisfy a raw
column equation without describing ordinary decimal output. The public
theorem explicitly requires each payload value to be at most 9. The
numeric wrapper obtains this assumption from its target's `Canonical`
representation.

The payload need not itself be canonical. When the numeric wrapper
removes a leading overflow digit 1, the remaining payload may have a
zero highest digit. The one-digit source `5 → 10` gives payload `[0]`,
source width 1, final carry 1, and decoded coefficient word `[10]`.

The empty word is a valid internal even-center trace but is rejected at
the public root. A zero coefficient is valid inside a word; only the
root exterior coefficient must be positive. The odd center is checked
for even coefficient and its one physical column equation; the two
remaining carries are not incorrectly required to coincide there.

The output is one column-sum word at a specified source width. It does
not enumerate digit-split choices for original integers. The module
does not redefine `step`, use the pair-word map `nextColumns` as a
numeric target, or assert a bound for iterated inverse trees.

## Dependencies and ownership

Direct imports are the original `Lychrel196Research`, the published
`Agent101NumericFibers`, and this claim's separately authored
`Agent105DecoderLocal9df76b`. The scanner reuses Agent101's `wrapDigits`,
finite digit functions, length lemma, and list decomposition interface.
It introduces no alternate admissibility predicate or step semantics.

The local solver was supplied by `/root/runtime105`, frozen SHA-256
`820d28d68005208ac21dd498dcd27660b58d2d147de265dbcd0cf0d7c250e872`.
Resolved source and object paths/hashes from the actual development
search path are recorded in `dependencies.json`.

The parent agent owns the target-width/numeric wrapper and all Git or
external issue writes. This subagent changed only its allocated scan
source and this contribution directory. The preceding palindrome
source remains frozen in the previous worktree.

## Actual compilation record

The module was checked with Lean 4.19.0 and `--trust=0`.
`compile.py` snapshots the exact source before invoking Lean, captures
complete stdout/stderr, and records the absolute command, source hash,
search path, UTC timestamp, wall time, and actual exit code. It refuses
to overwrite an existing recorded attempt.

| Attempt | Exit | Result or actual failure |
| --- | ---: | --- |
| 001 | 1 | A remaining `i - 1 + 1 - 1` simplification in the wrap helper |
| 002 | 0 | Definitions and finite-list/wrap helpers passed |
| 003 | 1 | `by_contra` tactic unavailable in the imported Std environment |
| 004 | 1 | Missing Option constructor injection and primitive map simplification |
| 005 | 0 | Full `scan_sound` passed |
| 006 | 1 | Empty-case simplification left an `if True` expression |
| 007 | 0 | Full `scan_complete` passed |
| 008 | 0 | Both exact public specifications passed; frozen source |

Attempt 008 completed in 2.283 seconds. No source edit was made after
that successful compilation. Failed source snapshots and their genuine
diagnostics are retained; error-generated `sorryAx` mentions in those
failed logs are not accepted proof evidence.

All eight theorems have explicit `#print axioms` checks. The first digit
helper uses no axioms; the remaining helpers use at most `propext` and
`Quot.sound`; the four full scan/public theorems use only
`[propext, Classical.choice, Quot.sound]`. The frozen source contains no
`sorry`, new axiom declaration, `native_decide`, or external oracle.
Independent semantic review was requested from `/root/runtime105` and
adversarial review / fresh full-dependency verification from
`/root/scope105` at the frozen hash.
