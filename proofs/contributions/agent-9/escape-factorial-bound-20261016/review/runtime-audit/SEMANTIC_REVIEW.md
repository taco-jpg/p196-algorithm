# Independent factorial-bound semantic review

Reviewer: Agent #9/runtime-audit. Mathematical sources were read unchanged. Agent #9/horizon-safety additionally provided a parallel read-only algebra check; that contribution is attributed in `ALGEBRA_REVIEW_ATTRIBUTION.json` 和 is 不 counted as a separate full compiler replay.

**Final independent gate: PASS.** All eleven mathematical modules compiled from a fresh source/object tree with `--trust=0`, followed by a separately generated exhaustive audit. That audit checked 1,456 theorem constants 和 182 safe definitions across all eleven expected originating modules. The two new modules contributed 19 theorem constants 和 five safe definitions, including generated auxiliaries; all eleven explicitly named authored exports also have literal axiom reports. Every collected dependency is within `Classical.choice`, `Quot.sound`, 和 `propext`. The selected mathematical sources, registry, 和 recorded compiler files stayed unchanged. Raw evidence is in `runs/full-001/`.

## Exact source 和 acceptance target

The reviewed contract specifies `strengthening_notes.txt`, section 5, equation (9), at original commit `2eb05ef47671d6b1883e54fec9f6a4f8de9ed8f5`. Independent Git reads resolved the original path `proofs/research/continuation/strengthening_notes.txt` to blob `7103ee939d82740b970dd23fb91e9db50db4ea54`; its exact bytes have SHA256 `15e07772d87cc4ee469541f4fb39ce1d0dce28ac5f630b16980c8abb02db258f` 和 match the retained source-tree copy. Commands 和 hashes are in `provenance.json`.

The source states the recurrence for positive mass indices, with `E(1)=1`, 和 the bound

\[
E(M)\le (4\kappa)^{M-1}M! \qquad(M\ge1).
\]

The formal generic theorem uses natural `κ` with `0 < κ`, natural-valued `E`, `E 1 = 1`, 和 exactly

```lean
∀ i, E (i + 2) =
  κ * ((i + 2) + (i + 1) * (2 * E (i + 1) + 1))
```

Putting `M=i+2` gives the source expression `κ * (2*(M-1)*E(M-1)+2*M-1)`. The shift covers exactly indices `M≥2`; there is no recurrence premise at zero. The generic result's mass-index premise is exactly `1 ≤ M`. No monotonicity, lower bound on `E`, initial-mass bound, or general-base dynamical theorem is assumed.

## Generic theorem: semantic PASS

`factorial` is ordinary natural factorial: its definition gives `factorial 0 = 1` 和 `factorial (m+1) = (m+1)*factorial m`. It is independent of `E` 和 `κ`. This fixes the exact mathematical quantity in the conclusion; it is 不 a surrogate sequence tailored to the bound.

The shifted induction proves `E(i+1) ≤ (4*κ)^i * factorial(i+1)`. At `i=0`, `E 1 = 1`, the zero power, 和 `factorial 1 = 1` give the exact base case. The value `E 0` is neither assumed nor read by the induction or its final wrapper.

For the induction step, set `C=(4*κ)^i * factorial(i+1)`. Positivity of `κ` 和 ordinary factorial proves `1 ≤ C`. The previous bound is substituted monotonically into the exact recurrence, after which the proved elementary inequality is

\[
(i+2)+(i+1)(2C+1)\le 4(i+2)C.
\]

Its direct arithmetic margin is

\[
4(i+2)C-\bigl((i+2)+(i+1)(2C+1)\bigr)
=(2i+6)C-(2i+3)\ge3.
\]

The submitted proof obtains the same inequality using `i+2 ≤ (i+2)*C`, `2*C+1 ≤ 3*C`, 和 multiplication/addition monotonicity. Multiplying by `κ` 和 unfolding the factorial successor equation turns the right side into `(4*κ)^(i+1)*factorial(i+2)`. All factors 和 indices therefore match equation (9).

The final wrapper excludes `M=0` explicitly. This is required: when `E 0` is unconstrained, the generic assumptions cannot imply `E 0 ≤ 1`. The implementation correctly leaves this case outside the generic theorem instead of adding a hidden base-value assumption.

## Decimal instantiation: semantic PASS

The unchanged `DecimalProfile.sharpEscapeBound` has existing clauses `E 0 = 0`, `E 1 = 1`, 和 the exact recurrence with multiplier five. The new positive-index specialization discharges its recurrence by definitional equality. Consequently, `4*κ` is exactly `20`; no larger constant or different recurrence is substituted.

`sharpEscapeBound_factorial` additionally covers `M=0` by a separate case using the existing zero value. Natural subtraction makes `0-1=0`, so its upper bound in that case is `20^0*0!=1`. This extra case is true for this concrete sequence 和 is 不 claimed for arbitrary `E`.

The unchanged `DecimalUniformEscape.sharpDigitSumEscapeBound B` is exactly `sharpEscapeBound (2*B)`. Applying the mass-index result at `2*B` therefore gives the advertised closed decimal horizon

\[
D(B)=20^{\,2B-1}(2B)!,
\]

where the formal exponent uses natural subtraction. For `B=0`, `D(0)=1` while the exact inherited horizon is zero; the documentation states this loss of sharpness correctly.

## Actual orbit window: semantic PASS

The numeric theorem invokes the original `DecimalUniformEscape.digitSum_uniform_window_sharp` with the original ordinary-decimal digit sum 和 `Lychrel196.orbit`. It preserves the returned time `t`, its lower bound `s ≤ t`, 和 its strict digit-sum inequality. Only the upper endpoint is enlarged by the proved horizon comparison:

\[
s\le t\le s+D(B),\qquad
B<\operatorname{digitSum}(\operatorname{orbit}(n,t)).
\]

This is an inclusive time interval. If counting its number of integer positions, the count is `D(B)+1`; the theorem itself correctly uses `s+D(B)` as its upper endpoint. There is no missing endpoint shift.

Its only seed hypothesis is `0 < n`, inherited unchanged from the original escape theorem. It adds no requirement that the initial digit sum be at most `B`, no bound on decimal width or initial zero gaps, 和 no assumption about future palindromes. The theorem holds for every natural threshold `B` 和 start `s`, including zero. The 196 specialization simply proves that its seed is positive.

The orbit is the original total reverse-and-add sequence, which continues after a palindrome. These finite escape windows do 不 assert palindrome avoidance, pointwise digit-sum divergence, optimal escape times, or a new general-base arithmetic construction. The generic recurrence result is conditional algebra; the concrete decimal instantiation 和 its positive-seed window are unconditional apart from their stated parameters.

## Frozen mathematical snapshot

| File | SHA256 |
| --- | --- |
| `Agent9FactorialRecurrence.lean` | `62ac425c0522fed1ea4cef602779018a7833ad8a12e65b34fe11c13503e471ef` |
| `Agent9DecimalFactorialEscape.lean` | `e8bfbb937aab16552e253b6c8db3581b6408de4d6a70ef64f6b046b0d1a77d28` |
| Authored audit support file | `1e225f85fa917248953967ab09a2b1d7c96c2e3bb43e4131d9003a757386f914` |

All nine historical mathematical dependencies are registered with exact source commit, original path, Git blob, SHA256, 和 import list. Independent preliminary provenance checks additionally matched their current flattened paths against `CONTRACT.source_main`, commit `ae8bbdfd2a18e8910eebc25fd2a81661c01abc16`. The completed fresh replay rebuilt all eleven mathematical modules, then executed its own generated exhaustive theorem/safe-definition audit with `--trust=0`. Compiler results are retained separately from this semantic review.
