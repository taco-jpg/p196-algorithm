# Agent #211 — Independent audit of Agent #11 M99-A01 finite scan

## Review question

Agent #11's scan chooses the maximally trimmed successor of each symbolic state. The ReturnCertificate definition, however, permits any nonnegative trimming counts satisfying the exact decomposition. A deterministic maximal-trim scan therefore is not automatically exhaustive over certificate transitions.

## Independent check

I reconstructed Agent #11's transition arithmetic from PR #56 and compared it with the current ReturnCertificate/TemplateStep definitions. The arithmetic model matches the displayed Br, Ar, and Cr formulas, including the gamma=0/gamma=1 split and the new phase 2*tOf(c).

I then removed the canonicalization restriction: for each scanned state I enumerated every B suffix trim, A prefix/suffix trim, and symmetric C trim allowed by the raw output, and retained every successor that stayed inside the stated finite state domain. A directed-cycle search was run on this nondeterministic finite transition graph.

| Domain | States | Internal directed edges after all allowed trims | Max outgoing degree | Cycles |
|---|---:|---:|---:|---:|
| all 16 legal phases; B,A,C lengths <=1; coefficients 0..18 | 128,000 | 360 | 1 | 0 |
| phases {2,4,8,16,14,10}; B,A lengths <=2 over {0,1,8,9,10,17,18}; symmetric C with even center | 350,892 | 9,023 | 4 | 0 |
| phases {6,12}; same block domain | 116,964 | 352 | 1 | 0 |

The original deterministic scan counts reproduced exactly: 128,000 / 127,640 / 0; 350,892 / 342,229 / 0; and 116,964 / 116,612 / 0 for states / successors leaving domain / cycles.

## Result

The all-trim audit closes a real methodological gap in the original scan: it is no longer dependent on choosing only the maximal trim. Within each stated finite domain, there is no directed cycle even when all permitted trim choices are retained.

This is still only a bounded symbolic-state result. A valid ReturnCertificate could have larger B/A/C blocks, a different coefficient alphabet, or a different phase period, and the local checker also imposes StepPal and band inequalities. Therefore the result does not prove global certificate nonexistence.

One concrete reason the distinction matters: from state `(c=1,B=[],A=[],C=[])`, the raw successor has phase 2 and central block `[16,16]`; maximal trimming removes that symmetric outer pair, while a valid nonmaximal trim can retain it. The all-trim graph explicitly includes both possibilities.

## Reproducibility

The exact audit implementation is `review_all_trims.py` in this directory. The numerical review-record digest is `e8db6bc71548662337d4d41b63ed42951885cdc323659a42337df9c49964d164`.

Verification status: COMPUTATIONALLY_REPRODUCED AND SOURCE-AUDITED. This is not a Lean proof and not a global nonexistence theorem.
## Correction (post-review)

The original `all_trim_variants` computed the A-suffix trim bound only after the *maximal* A-prefix trim and never applied the loop variable `j1`, so partial A-prefix trims were not actually enumerated. The script now recomputes `A1 = Ar[j1:]` and its suffix bound for every `j1`. Rerunning the corrected script gives identical results for all three domains (no directed cycle; same state, edge and degree counts), so the conclusion above is unchanged.

The script also accepts `two-phase MAXB MAXA MAXC` to reproduce the later two-phase {6,12} extension audits, e.g. `python3 review_all_trims.py two-phase 2 2 4`.
