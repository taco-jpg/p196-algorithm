# One-step ordinary digit-sum collapse

This packet formalizes the scalar consequence stated in strengthening-notes
section 8. The original framed-nine family, its canonical realization, its
exact first numerical output, and its two-step palindrome behavior are reused
unchanged. Original source attribution and the correction to the pre-claim
coverage census are recorded in `CENSUS_AND_REUSE.md` and `PROVENANCE.json`.

The new mathematical module is `Agent9OneStepDigitSumCollapse.lean`, in namespace
`P196.Agent9.OneStepDigitSumCollapse`. Author: Agent #9/horizon-safety. Independent
semantic review and rebuild: Agent #9/runtime-audit. Root owns publication and
the rolling coverage record.

## Exact result

Let `digitSum` mean the original `DecimalMass.digitSum` and let `step` mean the
original ordinary-decimal reverse-and-add map `Lychrel196.step`. If `n` has a
canonical digit representation `d` of width `2*r+2` whose pair sums are
`SeamAnnihilation.framedNine (2*r)`, then

\[
\operatorname{digitSum}(n)=9r+10,
\qquad
\operatorname{digitSum}(\operatorname{step}(n))=2.
\]

The statement is universal over **every canonical realization**. The universal
equalities hold for all natural r, including r=0. For the existential family,
`framedNine_digitSums_realized` assumes r>0 and directly reuses the original
`even_family_realized`, matching the manuscript's even k>=2 through k=2*r.

The joint consequence is:

```lean
theorem arbitrarily_large_digitSum_and_width (B : Nat) :
    ∃ n d L, 0 < n ∧ Canonical n d L ∧
      B < digitSum n ∧ B < L ∧ digitSum (Lychrel196.step n) = 2
```

Both strict bounds concern the same positive finite integer and its canonical
representation. Canonical width is the actual width of that integer, not an
extra padded word. The proof takes r=B+1: input digit sum is 9*B+19, canonical
width is 2*B+4, and the next digit sum is two. This includes threshold B=0.

The projected theorem `arbitrarily_large_digitSum` retains just the positive
integer, the initial digit-sum bound, and the exact next digit sum.

## Proof structure and reuse

The new finite-sum calculation gives

\[
\operatorname{wordSum}(\operatorname{framedNine}(k),k+2)=9k+20.
\]

The original `DecimalMass.wordSum_columns` identifies this as twice the input
digit sum, after `digitSum_value` transports through the canonical digit
representation. This proves the stronger intermediate equation
`2 * digitSum n = 9*k+20` for any canonical realization of `framedNine k`, and
then the required formula for k=2*r.

For the next digit sum, the module reuses the original
`framedNine_realization_step_value`, `framedNine_value`, `framedNine_output`,
`framedNine_extended`, and `framedNine_carry`. The carried prefix has unweighted
sum zero before its first one; its ordinary output has sum one, and the final
carry contributes one more. The original `value_extended`, `value_output`,
`digitSum_value`, and `wordSum_extended` lemmas transport this finite calculation
to the actual numerical update.

No new realization construction or generic carry-budget result is introduced.
The packet formalizes a written source consequence; it does not claim discovery
of the family. The family varies with the threshold and gives a one-step
collapse statement, with no new conclusion about one fixed infinite orbit.

## Export map

| Export | Role |
| --- | --- |
| `framedNine_prefix_wordSum` | Finite initial endpoint/interior sum. |
| `framedNine_wordSum` | Exact complete pair-word sum `9*k+20`. |
| `framedNine_realization_digitSum_double` | Universal scalar bridge `2*digitSum n = 9*k+20`. |
| `framedNine_realization_digitSum` | Exact input digit sum `9*r+10`. |
| `framedNine_output_prefix_wordSum` | Zero sum of the finite carried prefix. |
| `framedNine_realization_step_digitSum` | Exact next ordinary digit sum two. |
| `framedNine_realization_digitSums` | Both universal scalar equalities. |
| `framedNine_digitSums_realized` | Positive canonical witnesses with both equalities for r>0. |
| `arbitrarily_large_digitSum_and_width` | Both unbounded thresholds on one canonical witness. |
| `arbitrarily_large_digitSum` | Projected unbounded input digit-sum consequence. |

## Verification evidence

The author gate passed on the second attempt: all six project modules were
freshly compiled with `--trust=0`, then the generated audit checked 1,320 theorem
constants and 183 safe definitions. The new module contributes 21 theorem
constants including generated declarations, representing its ten public
exports, and no safe definitions. Every public export's literal axiom report
contains only the three permitted standard axioms. The first failed source and
both reported proof-script errors are retained in full.

`AUTHOR_STATUS.json` records the actual author result and attempt history;
`development/` preserves attempted sources, exact commands, logs, and manifests.
`BUILD_NOTES.md` gives the replay command and the precise runtime/audit boundary.
The exact import and source registry is `verification/source-registry.json`.
The author verifier rebuilds the five original project modules and the new
module with `--trust=0`, prints every new export's type and literal transitive
axiom report, and audits every project-origin theorem and safe definition.

Only the standard axioms `propext`, `Classical.choice`, and `Quot.sound` are
permitted. Standard runtime modules come from the pinned official Lean 4.19.0
release. This selected-source verification does not claim a repository-wide
build or replacement of the original dependencies.

`AUTHOR_FILES.json` and `SHA256SUMS` cover the stable author packet. Root-owned
`CONTRACT.json`, `ROLLING_COVERAGE.json`, and the independently produced
`review/` subtree are explicitly outside that author manifest. Root maintains
the final combined publication record.
