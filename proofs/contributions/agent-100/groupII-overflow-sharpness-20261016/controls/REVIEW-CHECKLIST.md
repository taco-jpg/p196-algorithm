# Review plan for the claimed Group II overflow-sharpness package

Status: preparation only. No new frozen theorem source has been accepted or independently compiled by this reviewer yet.

## Exact statement and finite-word scope

- Retain all `r>=1`, `5<=p<=9` and exactly the seven Group II cores: `5<=u<=8`, `v in {5,6}`, `u+v<=13`.
- Use original `component`, `initial`, ordinary `step/orbit`, and actual `iterPairs` semantics. Do not substitute a new algebraic dynamics.
- Establish first-step widths `2r+6` and `2r+7` and second-step widths `2r+7` and `2r+8` from actual terminal carries.
- Compare `Q2` with `shiftOne` of a zero extension of the represented `A2` prefix. Include the newly created endpoint and never read arbitrary raw `iterPairs` tails.
- Check the signed difference on every valid whole column: support at `r+1,r+3,r+4,r+6`, values `1,-1,-1,1`. In particular the nonzero witness `r+1` is inside both represented widths.
- An overlap iff `p<=4` must quantify only the claimed seven-core family and `1<=p<=9`, preserving the earlier positive theorem's provenance. No conclusion about `p>=10`, Groups I/III, later return times or other shifts is justified.

## Carry and shortest-boundary checks

- The first component coefficients are at most 9, including `p=9`; verify its carry-zero proof actually uses that bound.
- For `p=9,r=1`, the whole carry generated in the central region is reset by the adjacent coefficient `u<=8` before reaching the two outer 9 coefficients. A naive outer-small lemma requiring `q0<=8` does not cover this case; the exact carry certificate must do so.
- At second input, `2p` lies in `10..18`, so terminal carry is 1 for the actual admissible component and whole states. Do not infer this for an arbitrary nonadmissible comparison without its own carry certificate.
- The `r=1` external carry and central-adjacent 1 can be adjacent. Check actual normalized digit sums, including `p=9`; no-extra-carry overlap must retain the exact boundary addition.
- Do not import the old no-overflow second-step Group II carry/no-overflow theorem outside its `p<=4` domain. Reuse definitions and generic lemmas only with their actual assumptions.

## Raw redundant comparison and transport

- The redundant coefficient word `Phi1(A1)` has center `4v>=20` and is not `Admissible`. It may have internal carries equal to 2. Do not apply `carry_bounded` under a nonexistent all-coefficient-at-most-18 premise, or use ordinary realization for this raw comparison.
- Prove its actual terminal carry 1 explicitly. Check old-width normalized digit difference `(1,1,0,-1,-1)` at `r+1..r+5`, using `Int` subtraction rather than truncated `Nat` subtraction.
- Import Agent #8's precise existing common-overflow transport source. Check equal old width, equal terminal carry 1, antisymmetry and zero extension, including new column `i=L`. Preserve the theorem's original identifier and provenance; no substitute generic transport proof is needed.
- The separate bridge must establish `G(Phi1(A1))=Phi1(G(A1))` on its enlarged finite width. Its no-extra-adjacent-carry premise must be proved from the concrete normalized component digits, not assumed or inferred from a few representatives.

## Ordinary realizations and nonvacuity

- Any numeric lift must keep arbitrary original `n,d` satisfying canonical initial representation. Check the orbit of that same `n` is propagated by `representation_next` or `iterPairs_representation`.
- Obtain full finite output pair identity and exact width before transferring the signed discrepancy. An existential output digit function does not authorize total-function equality outside its canonical width.
- Positive existence should be supplied from actual initial admissibility, not left as a hypothetical representation premise. The redundant raw word is excluded from this existence claim.
- If two positive-time nonpalindrome outputs are included, audit the output-time convention of `palindrome_iff_bad`; do not confuse the input word's symmetry with a palindrome of the represented integer.

## Independent execution gates after source freeze

- Pin every new source and transitive imported source by byte hash; resolve module naming collisions against exact source bytes.
- Preserve the upstream verifier unchanged. Generate only the scoped registry and audit harness, with separate executor attribution.
- Use pinned official Lean 4.19.0 and a fresh empty source/output directory; do not import author-generated `.olean` files.
- Preserve each compiler command, actual exit code and full stdout/stderr, including any failed attempt before correction.
- Enumerate every new explicit theorem and audit all module-origin theorem constants in the complete closure. Allowed logical axioms are only `propext`, `Classical.choice`, `Quot.sound`; separately classify compiler-generated unsafe implementation symbols without confusing them with theorem dependencies.
- Recheck frozen source hashes after execution. Report source semantics and actual execution independently, and do not upgrade a source-only or finite control to a Lean PASS.
- Do not rerun the already successful 420-case experiment without a concrete changed-risk reason; archive provenance is sufficient for that unchanged payload.
