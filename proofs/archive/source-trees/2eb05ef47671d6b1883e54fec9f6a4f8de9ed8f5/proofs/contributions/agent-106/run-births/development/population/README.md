# Population obstruction development record

## Proven deliverable

`../../PopulationObstructions.lean` imports only the retained Std-based
`LychrelDigitSums` foundation. All lists use least-significant-column-first
order. Coefficient counts and maximal constant-symbol run counts use the
full physical word (the center is counted once).

The three exact certificates are:

| Input | Next integer | q before | q after | (count0,count18,run0,run18) before → after |
|---|---|---|---|---|
| 10499 | 109900 | [10,9,8,9,10] | [1,0,18,18,0,1] | (0,0,0,0) → (2,2,2,1) |
| 10518 | 92019 | [9,1,10,1,9] | [18,3,0,3,18] | (0,0,0,0) → (1,2,1,2) |
| orbit(196,5)=52514 | orbit(196,6)=94039 | [9,3,10,3,9] | [18,7,0,7,18] | (0,0,0,0) → (1,2,1,2) |

The certificate checks actual `Lychrel196.step`, canonical input digits,
actual overflow and width, `FoldedDecimal.nextColumns`, and independently
the repository's list implementation `AstraLanguages.qstep`. Inputs and
outputs are certified nonpalindromic. The actual-integer, actual-q, and
population certificates use kernel `decide` and print an empty axiom set.

All positive **integer** fixed weight combinations of counts, run counts,
and the four jointly are formally ruled out. These proofs depend only on
`propext` and `Quot.sound`. No new axiom, placeholder proof, or untrusted
native evaluation is used.

The vector certificate is independent of the scalar domain. For ordinary
positive real or rational weights the population/run change is
`w0 + 2*w18 > 0`, and the joint change is `a + 2*b + c + 2*d > 0`.
This elementary real/rational conclusion is stated as a mathematical
corollary, not mislabeled as a Lean real-number instance: the imported
Std-only foundation has no `Real`. `any_strict_score_obstruction` is a
kernel-proved generic score formulation with its comparison hypothesis
explicit; it adds no scalar or order axioms.

## Finite exact discovery (not a universal theorem)

Command from repository root:

```sh
python proofs/contributions/agent-106/run-births/population_search.py --max-width 8 --orbit-seed 196 --orbit-steps 100
```

The JSON retains all parameters, per-width counts, complete transition
delta histograms, least found integer witnesses in each branch/criterion,
and every actual integer and q transition in the 100-step orbit scan.
There are 198909 admissible symmetric q words at widths 1 through 8.
Enumeration uses q in [0,18], a positive outer coefficient, and an even
center coefficient at odd width. Each discovered witness is independently
realized by decimal digits, added as an integer, and checked against qstep.
The search is not invoked by Lean.

The finite search suggests the least input for simultaneous increases is
10499 (overflow), and 10518 without overflow. Minimality is **not Lean
proved** and is not used anywhere.

In the 100 tested steps of the 196 orbit all four counts increase at times
5,23,33,59,75,79,84,88,91,99. Time 23 is an overflow example:

```text
900544455998 → 1800098901007
[17,9,9,10,9,8,8,9,10,9,9,17]
  → [8,8,0,1,0,18,16,18,0,1,0,8,8]
(0,0,0,0) → (4,2,4,2)
```

Only time 5 → 6 is formalized in the main file. The later times and any
claim about recurring or infinitely many births are **not Lean proved**;
no infinite behavior is inferred from this scan.

## Development and verification history

- `ApiProbe.lean` and `ApiProbe.log` retain the failed scalar API probe:
  `Rat`, `Rat.add_pos`, `Rat.mul_pos`, `Rat.zero_lt_one`,
  `Std.LawfulOrderLT`, `Std.IsLinearOrder`, and the guessed list theorem
  are not present in this foundation. This motivated the accurately
  scoped integer theorem and scalar-independent vector certificate.
- `PopulationAttempt01.log`: first complete file compiled successfully.
- `PopulationFinal.log`: final source recompiled after comment cleanup.
- `population_search.log`: complete deterministic discovery summary.

The Lean command uses Lean 4.19.0, the shared build106 foundation, and the
runtime shim specified by the parent agent. No Git operation was performed
by this subagent.
