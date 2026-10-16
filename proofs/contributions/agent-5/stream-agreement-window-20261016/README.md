# Agent 5: finite ordinary stream agreement window

## Result and current status

The seven-export general window source is author-checked with Lean 4.19.0 `--trust=0 -j1 -DElab.async=false`. The two canonical all-gap sharpness proofs and independent execution are in progress. This checkpoint is WIP for the complete package; no full published-source replay is yet claimed.

Let `D, B, W : List Nat`, let `c` be one of `[2,4,6,8,10,12,14,16]`, and assume every coefficient of `B` and `W` is at most 18. Use the original exact shape

```text
paired D = B ++ replicate (gap + 2) c ++ W
             ++ replicate (gap + 2) c ++ B.reverse.
```

Write `n = B.length` and

```text
gamma = if 9 * 10^n <= rhoNum c B then 1 else 0.
```

For every `q <= gap + gamma`, the first `n + 1 + q` entries of `paired(reverseAddDigits D)` equal the coordinatewise sum of the literal streams:

```text
adicNumeratorDigits (n + 1 + q) (zValue c B - c)
fractionDigits (n + 1 + q) (rhoNum c B) (9 * 10^n * 10^gamma).
```

The subtraction in the low numerator is in `Int`. Actual normalization-carry and coordinate-quotient variants have the same bound and denominator. The entries on the left are paired coefficients; they can exceed 9. Empty exterior and middle words, zero gap, and untrimmed coefficient words remain in scope.

The ordinary numeral wrapper additionally assumes the original `DecimalDigits D` and `PositiveLast D`. It reuses `reverseAddDigits_correct` for decimal output, positive last digit, and the exact ordinary reverse-and-add value equation.

## Why the carry changes the window

The original `surrounded_normalization` formula exposes `gap + 1` stable digits on both sides of the normalized word. After the first `n + 1` high-end digits have been consumed, `gap` stable digits remain when the final carry is zero; `gap + 1` remain when it is one. The low end always has `gap + 1` available. Their common protected extension is therefore `gap + gamma`.

The outgoing carry is the exact coordinate threshold. It can differ from the initial phase carry `[10 <= c]`.

## Uniform sharpness targets

For every natural gap `g`, define the following little-endian digit words. Write `R(m,d)` for `List.replicate m d`.

| Carry | Canonical input | Exterior data | First excluded cutoff | Actual paired prefix | Stream prediction |
|---|---|---|---|---|---|
| 0 | `R(g+2,1) ++ [9] ++ R(g+2,1)` | `B=[]; c=2; W=[18]` | `g+2` | `R(g+1,4) ++ [5]` | `R(g+2,4)` |
| 1 | `R(g+2,5) ++ [0] ++ R(g+2,5)` | `B=[]; c=10; W=[0]` | `g+3` | `[1] ++ R(g+1,2) ++ [1]` | `[1] ++ R(g+2,2)` |

The gap-zero ordinary inputs are 11911 and 55055. These families establish uniform sharpness by witnesses. Other middles can continue agreeing at the next column; no universal first-failure statement is intended.

## Source, provenance, and scope

`StreamAgreementWindow.lean` imports the unchanged `OrdinaryStreamStep` package. The sharpness source is authored independently from the same prerequisite. All original authorship, normalizer definitions, carry semantics, and coordinate definitions are retained.

The accepted task claim is `034572d95e15a884e30a2ed8e94816bceadb55be`, task blob `a99d084a5c2ea1957b9e2b775abfecccf20cee39`. The complete prerequisite is [PR #121](https://github.com/taco-jpg/p196-algorithm/pull/121), frozen mathematical source `5b4238ebe95f5fb80512d1b1ad3dbe3b062279a3` and evidence descendant `5c4d394f20b70547aa7cb8dd14091bcd391e424c`. Public coordination is [issue #61](https://github.com/taco-jpg/p196-algorithm/issues/61).

This is a finite one-step theorem under an explicit input shape. It establishes neither later shape persistence nor an all-time ordinary orbit result or a conclusion about 196. Agent #5 holds no main integration slot.

