# Incremental non-author review: numerical decoder

Reviewer: Agent #105 / scope105 / session 9df76b. This review covers Target and Local at the source hashes recorded in the accompanying JSON. The scanner is still under development; no complete-scanner verification or new kernel control pass is asserted here.

## Target interface

`PayloadSpec e L h q` uses original `Admissible L q`, actual output digits on precisely `i < L`, and the actual terminal carry. `WidthChoice` retains either equal width and carry zero or an additional target digit equal to one and carry one. The truncated overflow payload is not required to be canonical. That distinction is necessary for the valid input 5, whose output 10 leaves the one-digit payload `[0]` after removal of the overflow digit.

`realize_payload` invokes the original canonical realization theorem and then the original numerical step/value bridge; its conclusion is an actual positive natural-number predecessor. `canonical_predecessor_payload` uses actual canonical output width and digits in the reverse direction. The finite-list equivalence preserves exactly L coefficients and puts no conditions on irrelevant tails. Width zero is excluded by Admissible even when the syntactic width-choice expression itself permits L=0. No mismatch was found in these four theorem statements or their proof dependencies.

## Local interface

The local pair equations are `q+a=u+10*low` and `q+high=v+10*b`, where low and high are the next inner carry states. Both states lie in `{0,1}` and q lies in `0..18`. The second equation forces two candidate coefficients to differ by at most one; the first forces any difference to be a multiple of ten, yielding uniqueness even for arbitrary natural-number inputs u,v,a,b. No extra input range hypothesis is required for this equation-level specification.

Candidate subtraction is truncated natural subtraction, but every candidate must subsequently satisfy both complete equations. Thus `u<a` cannot create a spurious accepted q=0 solely through truncation. The center candidate similarly checks the complete equation, coefficient bound, and even coefficient condition. The finite candidate list covers both possible low states and both possible high states. The success/none equivalences match these exact equations. No semantic defect was found in the Local endpoints.

## Output digit range is a global contract

For e(0)=10, L=1 and h=0, the current raw scanner returns `[10]` because its center equation is 10+0=10+0. However, the actual decimal output digit of q=10 is 0 and its carry is 1. This is an intentional out-of-domain explanatory control: equation-level soundness alone does not imply normalized decimal output/carry without an output-digit bound.

Parent and scanner author have confirmed the final physical `decodeAtWidth` iff will require `he : ∀ i, i < L → e i ≤ 9`. A canonical target supplies this bound. The raw function need not reject arbitrary out-of-domain e. The example is not a defect in that planned bounded-input contract.

## Controls queued for the completed scanner

Lists below are least-significant first. These are expected results to be checked later by the actual Lean kernel, not assertions of a completed kernel run.

| Ordinary step | Target digits | Expected candidate profiles | Boundary exercised |
| --- | --- | --- | --- |
| 5 → 10 | `[0,1]` | L=1,h=1 gives `[10]`; L=2,h=0 gives none | Zero truncated payload; even source center above nine |
| 1 → 2 | `[2]` | L=1,h=0 gives `[2]`; zero-width candidate rejects | Minimal positive source; single source column |
| 29/110 → 121 | `[1,2,1]` | L=2,h=1 gives `[11,11]`; L=3,h=0 gives `[1,2,1]` | Empty interior may join carries one and one |
| 200799/1098900 → 1197801 | `[1,0,8,7,9,1,1]` | L=6,h=1 gives `[11,9,7,7,9,11]`; L=7,h=0 gives `[1,0,18,16,18,0,1]` | Nonpalindromic cross-width target; changing inner carry states; coefficients 16 and 18 |

The last two coefficient profiles and their common output are retained prior research. The concrete integer realizations and actual reverse/step facts are already available in the previously verified witness module. No counterexample discovery is claimed.
