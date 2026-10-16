# Independent review of high-carry renewal

**Verdict: PASS.** The full written proof and producer were read independently. A separate sequential-column normalizer also verifies all 177 saved controls, all 708 recorded transitions, all claim labels, the ten boundary recurrences, the sharp example, and the rejected stronger conjecture. The replay imports no producer code and uses no integer-reversal routine. Exact input hashes are retained in `independent_review.json`.

## Exterior-only safety

For a canonical pair word, the outside coefficient is positive and at most `2b-2`. An outside coefficient at least `b` forces final carry one, irrespective of the interior, so the next outside coefficient is `a=q_0-b+1`. The following addition has no low carry because `a<=b-1`. With actual high incoming bit `v`, its outside pair coefficient is `2a+v` unless the addition overflows. Overflow requires exactly `a=b-1,v=1`, and then the outside coefficient is `b` at the increased physical width. Under `2a>=b+2`, either output excludes both palindrome classes. The original outside coefficient also excludes them. This remains valid at length one; no independent choice of `v` is assumed. The range is empty at base three.

## Local regeneration and short widths

In the high region, the original carry profile is all one after the initial column. Writing `r_i=q_i-b+1` gives exactly the stated pair update with outside `r_0` and adjacent interior sums. At maximum outside coefficient, the high neighbor forces the second addition to overflow; the next pair coefficients are `b` and `q_1-b`. In the other range, the outside coefficient is at most `b-2`, so the final carry is zero despite high incoming carry one. The resulting coefficients are `2a+1` and `2(z-b)+v`.

At original length two the neighboring observations coincide in one middle column. Its incoming carry is zero, so the nonoverflowing formula holds with `v=0`; there is no doubling of an independent observation. The maximum case also uses the actual increased width correctly. The ceiling and floor endpoints yield the advertised positive small coefficient in both cases. The decimal hypotheses exclude the uniform `11` first-hit exception, while the all-base maximum case correctly retains the uniform `4` exception in base three. Claims concern positive output times; the seed may already be palindromic.

## Exact restricted return and its bound

Section 3 continues the high-region assumptions from Section 2. For `L>=3`, outside at most seventeen, and adjacent sums at least twenty-eight, the second addition has incoming carries `0,0,1,...,1` and outgoing final carry zero. Its first interior digit loses ten, the remaining interior digits lose nine, and the outside digits are `a,a+1`. Reflection at width `L+1` gives the stated outside, near-outside, and interior formulas. The index ranges handle `L=3`; the separate `L=2` formula is correctly excluded from this return theorem.

For a near-outside sum `s`, `2s-55>=9` is equivalent to `s>=32`. For an interior sum, `2s-54>=9` has the same integer threshold. These cover every adjacent sum. That threshold also forces `q_0>=14` because `q_1<=18`, hence the new outside is at least ten. All upper bounds follow from the canonical bounds, with the near-outside sum at most thirty-five. Thus the return condition is an equivalence, not merely sufficient.

Every qualifying return has boundary update `A'=2A-17`, `B'=2A+2B-55`. For `A<=16`, the new first sum is at most twenty-eight, so no immediately following qualifying return is possible. For `A=17`, the new neighbor is at most fifteen; a second return requires it to be exactly fifteen and hence the original neighbor eighteen. That second return produces neighbor nine, precluding a third. The word `(17,18,18,17)` realizes exactly the two advertised qualifying returns. The last word remains high but fails the hypothesis needed for another return.

The result concerns consecutive applications of this particular two-step return map. It neither prevents a different later return nor proves eventual palindrome formation. The counterexample to automatic mixed-certificate regeneration is retained correctly. No additional search or independent Lean build was performed.

Reproduce the independent finite replay with:

```sh
python proofs/contributions/2026-10-15-high-carry-renewal/independent_review.py
```
