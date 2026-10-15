# Agent #113: the uniform five-layer obstruction, kernel-checked

Task `agent113-five-layer-obstruction-lean` (claim `d5d014f` on `p196/coordination`).
Branch `research/agent-113/s20261015`.

**This does not prove that 196 is a Lychrel number.** It formalizes a
restricted whole-word obstruction and its all-time exclusion from the orbit
of 196.

## What is proved

Source: [p196_uniform_five_layer_obstruction.md](../../../chat-6acee928/originals/p196_uniform_five_layer_obstruction.md),
section 1, statements (1)–(2) (written proof only until now).

Namespace `Agent113.FiveLayer`; `width`, `pairAt` are the canonical decimal
width and pair sums of `Agent113.TwoDigit` (independently reviewed).

```lean
-- strengthened: only the outer four pair sums are constrained
def OuterPattern (X : Nat) : Prop :=
  5 ≤ width X ∧ pairAt X 0 ∈ [10, 12, 14, 16] ∧ pairAt X 1 = 0 ∧
    pairAt X 2 ∈ [0, 10, 12, 14, 16] ∧ pairAt X 3 = 0
theorem five_layer_strong : ∀ A t X, 0 < A → orbit A t = X → OuterPattern X → t < 5

-- the written statement (every position constrained)
def FullPattern (X : Nat) : Prop :=
  5 ≤ width X ∧ ∀ j, j < width X →
    (j % 2 = 1 → pairAt X j = 0) ∧ (j % 2 = 0 → pairAt X j ∈ [0, 10, 12, 14, 16])
theorem five_layer (A X : Nat) (hA : 0 < A) (hX : FullPattern X) :
  ∀ t, 5 ≤ t → orbit A t ≠ X

theorem no_196_full_pattern : ∀ t, ¬ FullPattern (orbit 196 t)
theorem sharp_four : orbit 10000 4 = 80008 ∧ FullPattern 80008   -- five cannot become four
```

`X` need not be a palindrome; intermediate palindromes are allowed; `A` need
not be divisible by 11. The strengthened form shows the obstruction only uses
the outer four pair sums.

Not formalized here: the same file's mixed-digit theorem `H₁₁(D(V)) ≤ 6` and its
corollary (5).

## Proof architecture

| module | content |
|---|---|
| `FourColumnProjection` | `nextQuad`; `quad_no_overflow`, `quad_overflow`: for every width `L ≥ 4` (overlapping widths included) the outer four pair sums of the canonical next word are `nextQuad` of the outer four pair sums and the actual carry into column `L-4` |
| `FourColumnChain` | number-level `quad`, `quad_step`, `quad_box`, width bounds; generic certificate `Cert4` with per-row checks; `Cert4.depth_bound`: no positive orbit reaches, at a time `t ≥ h`, a state of width ≥ 4 whose quadruple is in layer 0 |
| `FiveLayerData` (generated) | the five layers (20, 20, 18, 17, 5 quadruples; layer 5 empty) and the exhaustive check of all numbers below 1000 |
| `FiveLayerR{r}A{a}` (90, generated) | kernel checks (`decide +kernel`) of the closure rows `s0 = a`, `s1 = 0..18` of layer `r` |
| `FiveLayerRows{r}` | assembly of each layer's 342 rows |
| `FiveLayer` | endpoints above |
| `Audit5.lean` | enumerates every `Agent113` theorem and fails on any axiom outside `propext`, `Classical.choice`, `Quot.sound` |

Unlike the two-digit package, no last-step lemma is needed: the target set is
layer 0 itself. The generator (`generator/gen_five_layer.py`) is untrusted; it
was cross-checked against an independent model of the projection (200,000
random inputs, 0 mismatches), and the kernel re-checks every row.

## Status and verification

**LEAN-CHECKED** (official Lean 4.19.0, `6caaee842e94`, core + Std only; no
`sorry`, no `native_decide`, no new axioms). Fresh from-source build of source
`7f5736f` in an empty directory: all 104 modules exit 0 (14 structural, 90
generated row modules). Exhaustive audit of every `Agent113` theorem constant in
the final environment (3,806, including the imported two-digit modules): axiom
union exactly `propext`, `Classical.choice`, `Quot.sound`. The five endpoints
use only `propext` and `Quot.sound`. Evidence: `verification/`,
`verification.json`. Not yet independently reviewed. Reproduce:

```sh
cd proofs/contributions/agent-113/five-layer
./build.sh <repo-root> <new-empty-dir> 2     # official lean 4.19.0 on PATH; ~45 min on 2 cores
```

Numerical cross-check (not proof): for every `A < 3·10^7`, `T⁵(A)` never has
the outer pattern (C program, 0 violations).
