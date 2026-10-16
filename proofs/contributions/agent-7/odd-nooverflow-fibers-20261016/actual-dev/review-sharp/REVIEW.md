# Independent review: canonical odd-fiber sharpness

Reviewer: Agent #7, `/root/runtime`. Result: **PASS** for the frozen `OddSharp.lean` and its stated scope. No author source was changed.

`OddSharp.lean` is pinned at SHA256 `bc4d4fe2d7655a5bb81ecda5475f3b0abd9dbc91e41cc766dec92b35c5741d57`. The independent fresh execution is `attempt-001/verification.json`, SHA256 `87baea0f90792feed49eec39f084d3e833dcb4768f40a0ec843e6c32059f1f87`. It rebuilt all 13 project modules in the Sharp import closure and 11 independent reviewer fixtures with Lean 4.19.0 and `--trust=0 -j1 -DElab.async=false`. All 188 explicit public theorem audits and all 431 module-origin theorem audits passed, with axiom dependencies confined to `propext`, `Classical.choice`, and `Quot.sound`.

## What is counted

The upper bound applies to the length of `fullOddPreimages`, already proved duplicate-free and exactly equivalent to the full literal canonical source-word predicate. It therefore counts distinct coefficient words. The canonical-positive filter can only decrease the complete path-enumerator count. The proven bound on that path count then gives `(fib (m+1)+1)/2` for every target half of length `m` and every normalized middle digit.

## Fixed-center formula and attainment

The prescribed center is the middle digit of the normalized output before pairing; its paired output coefficient is twice that digit. It is not identified with the source's middle coefficient. The phase proof rotates the four state-count differences through six cases and gives the exact parity-dependent floor/ceiling formula. When the relevant Fibonacci number is even, the floor and ceiling coincide.

For positive half-width `m=n+1`, the target half `11 :: replicate n 9` has the same count as the all-nine half. The leading-eleven local equation forces source outer coefficient five, so the positivity filter removes no word. This gives exact prescribed-center maxima, including empty fibers when the maximum for that center is zero.

The positive-half-width quantifier is essential. At `m=0`, center digit zero has an empty canonical fiber even though its unfiltered bound is one. The source correctly treats width one separately. Its explicit global sharp family is `[[6]]` at `m=0`; at larger half-widths it uses the leading-eleven target and center six in residues 0, 1, 2 modulo six, or center seven in residues 3, 4, 5. This supplies an actual positive attaining fiber at every odd width.

## Independent boundary controls

Direct reduction of the enumerator, independently of the claimed formulas, gives sharp-family counts `1, 1, 1, 2, 3, 4, 7` for `m=0..6`. Checks over all ten prescribed center digits give counts one/zero for even/odd centers at `m=1`, one/two at `m=3`, and seven/six at `m=6`. Further checks establish the width-one zero-center gap and the exact original transition `[6]` to `[12]`.

No blocking issue was found. `OddSharp` itself presents targets by encoded parameters `ss,v`; the arbitrary-output extension is reviewed separately in `FINAL_REVIEW.md`. The source does not claim all-time orbit nontermination.
