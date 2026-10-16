# Independent source review of the scalar-clock formal bridge

**Result: PASS.** This review read all four proof modules and their README,
then inspected the supplied fresh-build checker and verification report.
It independently checks the mathematical statements and proof wiring;
it does not claim a second compiler run. The report's source and checker
hashes were recomputed from the reviewed files and agree.

The reviewed package is `../2026-10-15-scalar-clock-formal/`.

## Findings

- `ScalarClock` computes the prescribed phase sequence
  ((4,8,16,7,15,6,13)), its exact allowed input bits, and the overflow
  sequence ((0,0,1,0,1,0,1)). Every seven-step rotation has exactly three
  overflows. The finite control cases are kernel decision proofs.
- `ActualScalar` identifies the input bit with the actual whole-word
  carry into column (L-1). Its transition and overflow identities use
  actual finite symmetry and actual carry bounds. They include width one;
  they do not assume that boundary controls are independently selectable.
- `ScalarOrbit` composes those identities along `iterPairs`. Clock windows
  include both endpoints and allow arbitrary initial phase and time.
  Complete periods increase the actual width by exactly three per period.
  The canonical bridge identifies this width with the decimal length of
  the actual ordinary integer iterate.
- The warmup quantity is exactly
  (k=\lceil\max(14-L,0)/3\rceil). The proof handles (R<k), (R=k),
  and (R>k), and restricts the inclusive orbit window at time (7k)
  with phase shifted by (7k). For (L\ge2), it correctly gives (k\le4).
- `WidthOne` uses evenness of the center coefficient and actual carry zero.
  Odd clock phases cannot be initial width-one coefficients. The even
  phase 6 immediately fails its required successor 13. The even phases
  4, 8, and 16 reach outside coefficient 7 at width two, where the actual
  carry is zero and the next coefficient is 14 rather than the required
  15. Thus no rotation completes a period from an admissible width-one
  word.

## Explicit trust boundary

`period_bound_after_warmup` and
`uniform_period_bound_of_wide_bound` retain the premise `hwide`: every
relevant actual orbit window starting at width at least fourteen, for
every time offset and phase, has at most (B) complete periods. The
conclusion is respectively (R\le B+k) and (R\le B+4).

The package does **not** instantiate this premise with a numerical graph
certificate or claim that the reported 94/98 hierarchy is kernel checked.
It does not prove palindrome occurrence, palindrome avoidance, or the
196 conjecture. The README states this scope accurately.

## Pinned evidence

The observed report records Lean 4.19.0, successful fresh compilation of
the original prerequisite and all four new modules, and the transitive
axiom audit of all 35 public theorems. Its only permitted and observed
axioms are `propext`, `Classical.choice`, and `Quot.sound`. The checker
uses a new temporary build directory, supplies all project dependencies
as source, checks dependency fingerprints during the build, and verifies
source stability before writing the successful report.

| Reviewed file | SHA-256 |
| --- | --- |
| `ScalarClock.lean` | `e9e89c4245247dad196d8af0279c85adbbfe3f53a32db8746173397aef688c83` |
| `ActualScalar.lean` | `a5ee385aa1bc8d4e71ca5c42ef99f738663d0d7c7f77ded1b68e5295aeabe31b` |
| `ScalarOrbit.lean` | `26e4277439ad146192772ab401aba8c0add1835301a1267034f40c869fec1d80` |
| `WidthOne.lean` | `ad42f91053829b96b89f10b99a9d66e3dd8817278439a9abc4ce5de822ad097d` |
| `check.py` | `1101da8eb077e7b6d470e0c8f9b0e63344bde5f7163eacc0d3a05364dd1c1bfa` |
| `verification.json` | `df1ee6e58af23b3946e5681014ab586000b1d91a80cdf539c41197db9e71c368` |

No proof-source correction was requested by this review.
