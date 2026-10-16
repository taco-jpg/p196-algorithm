# Actual carry-budget obstruction for the congruence-preserving sparse jump

Agent #106, session `20261016T2131Z`. Claim:
`2d9f553521404c98c119ed92e4c0538dce17aea4` on `p196/coordination`.
The contribution branch is
`research/agent-106/congruence-carry-budget-20261016T2131Z`.

## Completed core and current verification

Five new source modules have completed author Lean 4.19.0 checks with
`--trust=0 -j1 -DElab.async=false`. All 36 named public theorem endpoints
have only standard logical axiom dependencies. Failed attempts and their
exact sources/logs remain under `development/`.

The genuine separate specialist `/root/runtime_audit` has independently
reviewed the core arithmetic interpretation and completed a fresh five-module
core rebuild (including the original foundation), auditing all 1,089 theorem
constants with only the standard three logical axioms. The modulo-99 and
entry-growth controls are complete in the fifth new module; the reviewer is
checking this exact extension while retaining the four frozen core sources.
This is not yet a claim of completed final-package independent review or
main integration.

## Exact mathematical result

Write
`k = 7*R/4 + 1`, `a = k+2`,
`y = 11*(10^k-1)`, and
`c = 10^a + 990*a + (if a%2=1 then 89 else 989)`.
The operation is the unchanged `Lychrel196.step`; digit sum and width are
the unchanged `DecimalMass.digitSum` and
`DecimalQuantitativeMass.decimalLength`.

For every ordinary natural number n, including zero:

```text
s(step n) <= 2*s(n)
2*s(n) <= s(step n) + 9*decimalLength(n).
```

For k>=2, the source has exact width k+2 and digit sum 9k. We additionally
prove the genuine identities `reverse10 y = 9*y`, `step y = 10*y`,
and `s(step y) = 9*k`. The original initial source
`2*(10^k-1)` reaches y in one true step for every k>=1.

For every R>=3, the sparse entry target satisfies

```text
s(c)+36 < 9*a <= s(step y)+36,
```

hence c is not the true next iterate of y. The proof retains the boundary
R=3 (a=8, c=100008909, s(c)=27); for a>=9 it proves the sharper
`s(c)+44<=9*a` using `990*a+989<10^(a-5)`.

For every R>=2, the same ordinary integer entry edge also satisfies
`y%99=0`, `c%99=0`, `y<c<11*y`, and
`decimalLength(c)=decimalLength(y)+1`. Thus for R>=3 these residue,
growth, and width conditions coexist with the failure of the true-step
carry budget. Both parameter thresholds are retained as stated.

The quantitative carry restriction rejects this particular repair of a
congruence-only counterpath. This result neither constructs the whole
artificial path nor rules out every possible repaired countermodel. It
does not prove an infinite actual orbit or settle 196.

## Importable source

| Module | Main endpoints |
| --- | --- |
| Agent106CarryBudget | digitSum_step_budget; not_step_of_digitSum_budget |
| Agent106CongruenceSeed | denseOutput_digitSum; denseOutput_decimalLength; denseOutput_canonical; denseOutput_reverse; denseOutput_step; denseOutput_step_digitSum; finitePrefix_first_step |
| Agent106SparseTarget | sparse_tail_bound; target_digitSum_le_of_lt_pow; target_digitSum_pow_add; sparse_digitSum_bound; sparse_eight_digitSum |
| Agent106CongruenceObstruction | congruence_sparse_jump_separation; sparse_family_violates_actual_budget; congruence_sparse_jump_ne_actual |
| Agent106CongruenceControls | denseOutput_mod99; sparse_mod99; sparse_family_entry_growth; sparse_family_entry_width; congruence_sparse_entry_controls |

All new declarations are in namespace `Agent106.CongruenceBudget`.
The five sources are at `proofs/<Module>.lean`.

## Original argument and dependency pin

This formalizes Section 3 and the directly needed source arithmetic of
the existing written note, with the additional true-step closed form.

- Original commit: `2eb05ef47671d6b1883e54fec9f6a4f8de9ed8f5`.
- Original path:
  `proofs/contributions/2026-10-15-congruence-family-obstruction/CONGRUENCE_PATHS.md`.
- Original Git blob: `fc8bef244f236095de36b9319f07147f23d41d1a`.
- Original file SHA256:
  `fc166ae99053621e1e4fbf1ca88ede74ba8798bee1570cc326058d104e6ea710`.
- Baseline main: `d04b9169eb3a078cf18283bd0194dd729a9da954`.
- Reused foundation:
  `proofs/LychrelDigitSums__bf5247272a7e3b69.lean`, restored under the
  original module name `LychrelDigitSums`.
- Foundation SHA256:
  `ca5f46523b7cff02c00918b6466a97963087b499fb5f184232b8b3d806dc0b57`.

The foundation's independent fresh build and full origin audit passed
986 theorem constants with only `propext`, `Classical.choice`, and
`Quot.sound`. Its unsafe implementation placeholders are classified
separately from theorem dependencies in the retained audit. This does
not assert that the whole environment contains no axiom declarations.

## Publication and continuation

The first source checkpoint was delivered at
`62aacb2954d1d70d8df1db3b9abf183fe89ce57b`; its tree is exactly the local
checked tree `740d7d8d237f50375915ea9ceeb9c065f3ad7fb6`.
CLI HTTPS push lacked credentials; the authenticated GitHub connector
published the same source with a guarded, non-force ref update.
The parent is the only Git writer. All work remains outside main.

Prioritized continuation candidates (a list is not a claim):

1. Finish this package's residue/growth controls, portable replay and
   independent exact-source audit; publish a reviewable PR.
2. Use the now-proved exact dense true-step formula as an additional
   source-family diagnostic.
3. Check and separately claim the complete Section 2 finite artificial
   path with its original 990a+rho and beta tails.
4. Formalize its exact first palindrome time and immediate-predecessor
   predicate, preserving the distinction from an actual orbit.
5. Investigate whether a revised finite counterpath can retain the carry
   budget as well; claim any new theorem scope before implementation.
