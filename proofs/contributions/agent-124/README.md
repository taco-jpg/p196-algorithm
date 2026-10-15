# Agent 124 contributions

**Decimal Lychrel existence and the claim for 196 remain unproved.** Both
packages below exclude restricted palindrome families from the ordinary 196
orbit, at every time; they do not resolve P196.

| Package | Task on `p196/coordination` | Content |
|---|---|---|
| [`prefix-five-six/`](prefix-five-six/README.md) | `agent124-prefix-five-six-column-kernel` | Width-generic prefix-ancestry endpoint, code-keyed certificate checker, and the 33 remaining three-digit baseline classes (24 at five columns, 9 at six) |
| [`four-digit-refinements/`](four-digit-refinements/README.md) | `agent124-four-digit-refinements` | 1,830 four-digit refinements of three-digit classes that have no certificate of their own |
| [`forward-invariant-196/`](forward-invariant-196/README.md) | `agent124-forward-prefix-invariant-196` | A forward-closed set of prefix words containing every projection of the 196 orbit after time 100, excluding all palindromes whose leading words fall outside it |

The shared Lean infrastructure lives in `prefix-five-six/` and reuses Agent
#104's accepted modules unchanged. `prefix-five-six/check.py` rebuilds every
module of both packages from an empty directory and audits the transitive
axioms of every theorem constant they define.
