# Reciprocal first moments and derivative residue redundancy

This contribution formalizes the identity `2 Q'(1) = (L-1) Q(1)` and its modulo-nine consequence from the original `astra_spectral_carry_quotient.md`, lines103–118, source blob `eac5b8f61385a615d9cc3e7796a4d698c66b716b`.

## Exact statement

For every `q : Nat → Int` and every natural fixed width `L`, assume only `q i = q (L-1-i)` for `i<L`. Then:

```text
2 * sum(i<L, i*q(i)) = ((L:Int)-1) * sum(i<L, q(i))
```

Both sums have literal `List.range` interpretations. `formalDerivativeValue q L x` is explicitly the finite sum of `(i:Int)*q(i)*x^(i-1)`; the zero-index term vanishes. Its value at one equals the independently defined weighted coefficient sum `derivativeAtOne`.

The checked modulo-nine formula is:

```text
derivativeAtOne q L %9 =
  (5 * (((L:Int)-1) * finiteSum q L)) %9
```

Consequently two separately symmetric words of the same width, with equal coefficient masses modulo9, have equal derivatives at one modulo9. The natural-coefficient specialization has the unchanged imported `polynomialValue q L 1` on the right.

All natural widths are included. At `L=0`, the sums vanish and the integer factor is `-1`. Negative coefficients and zero boundary coefficients are permitted; width means the fixed reflection window and need not equal the actual polynomial degree plus one. Nothing is assumed outside that window.

## Public source endpoints

All names are in `P196.Agent51`:

- `reciprocal_first_moment`
- `reciprocal_first_moment_literal`
- `reciprocal_derivative_at_one`
- `reciprocal_derivative_mod_nine`
- `reciprocal_derivative_mod_nine_determined`
- `natural_reciprocal_derivative`

The module exports14 public declarations, including reusable integer finite-sum additivity and reflection helpers. The reflection helper acknowledges the related original natural-valued `DecimalMass.wordSum_reflected` argument. This contribution formalizes existing source mathematics; it does not claim its discovery.

## Dependencies and build coverage

The exact local import closure is `OverflowDigits → ResidueSums → ReciprocalMoment`. The first two modules are reused byte-for-byte from PR148, mathematical source commit `7360b12a0a5889761c845a56a4b8d8a1df5f39b5`; they are not reauthored here. The registry `proofs/Agent51ReciprocalMoment.registry.json` selects this entire three-module closure and all50 explicitly public declarations across it.

From a checkout containing this contribution:

```sh
python proofs/verify_project__214bf7673efe116b.py \
  --lean /absolute/path/to/lean-4.19.0-linux/bin/lean \
  --output /absolute/path/to/a-new-output-directory \
  --registry proofs/Agent51ReciprocalMoment.registry.json \
  --project agent51-reciprocal-moment
```

This is the unchanged existing verifier implementation, called directly to use the repository's current flattened source paths. Its actual flags are `-j1 -DElab.async=false`. This checkpoint records no completed canonical replay of the new registry yet.

## Verification at the source checkpoint

The genuine author specialist `/root/claim_census` compiled the frozen source with official Lean4.19.0, `--trust=0 -j1 -DElab.async=false`. Author attempt002 passed; all14 explicit public declarations printed only `propext` and `Quot.sound`. The initial elaboration/rewrite failure remains unabridged under `author/attempts/001`, outside the accepted source closure.

The author development reused recorded previously built dependency objects. A genuine nonauthor source-semantic review and a separate clean three-module source build plus exhaustive module-origin audit are in progress. Author compilation is not being presented as those independent acceptance steps. No accepted proof uses an admitted proof, a new mathematical axiom or compiler-trusted evaluation.

The complete Laurent-polynomial quotient classification, carry dynamics and decimal saturation remain separate claims. This theorem proves the stated coefficient identity and coordinate redundancy.

Task `agent51-spectral-reciprocal-moment-20261016` was published and read back at coordination `61ed23a9e1dc36f0ad3d0b49e46eaa5c104433f8`, blob `2b26e99231b0e5731345af0de22b5cea9677af72`. The branch is stacked on PR148 and must be retargeted only after that prerequisite is actually integrated. No main-write role is claimed.
