# Plain uniform-return clause: author record

Author: Agent #105 / `source_scout`, session `8f1107db019a`.

Source: `proofs/Agent105UniformReturnPlain.lean`.

Frozen SHA-256:
`0d4d048c017966827be4d146ef52d50de8ea3fc777fd7f21220c73694f5155af`.

## Why this module is needed

Section 1 of the original `VARIABLE_RETURN_THEOREMS.md` first states uniformity
for arbitrary positive return segments. Safety is an optional strengthening.
The already-proved `Agent105UniformReturn.lean` supplies the safe version.
During an independent review of that assembly, this author identified that
the ordinary return branch still needed its own endpoint. The parent confirmed
the finding and assigned this separate repair file, leaving the existing
safe-return source unchanged.

## Exact public statements

Both declarations are in `Agent105.UniformReturn`.

```lean
theorem uniform_bounded_return (Q : Nat → List Nat)
    (hQ : HasAffineRuns Q 18) (s B : Nat)
    (hcover : Eventually (fun k => ∃ t, 1 ≤ t ∧ t ≤ B ∧
      Agent8.orbit (Q k) t = Q (k + s))) :
    ∃ t, 1 ≤ t ∧ t ≤ B ∧ ∃ K, ∀ k, K ≤ k →
      Agent8.orbit (Q k) t = Q (k + s)
```

This directly instantiates the existing finite bounded-tail selector with the
already-proved `actual_return_tailStable`. There is no safety premise.

```lean
theorem uniform_return_wordAt (rs : List RunSpec)
    (hrs : SpecBound rs 18) (s : Nat)
    (hA : 0 < widthSlope rs) (hs : 0 < s)
    (hcanonical : Eventually (fun k => Agent8.CanonicalPair (wordAt rs k)))
    (hreturn : Eventually (fun k => ∃ t, 0 < t ∧
      Agent8.orbit (wordAt rs k) t = wordAt rs (k + s))) :
    ∃ t, 1 ≤ t ∧ t ≤ 4 * widthSlope rs * s ∧ ∃ K, ∀ k, K ≤ k →
      Agent8.orbit (wordAt rs k) t = wordAt rs (k + s)
```

The exact shape theorem supplies equal endpoint heads and actual width gain
`widthSlope rs * s`. The existing family return-time bound makes every supplied
positive return time at most `4 * widthSlope rs * s` on a common tail. The first
theorem then selects one positive time uniformly. Neither the return-existence
premise nor positive growth is inferred from canonicality.

The source imports the frozen safe-return module only to reuse its actual
stability and proven dynamics dependencies. No `SafeThrough` premise is used
in either new statement or proof.

## Author verification and cache provenance

The first author attempt compiles the new module successfully with Lean 4.19.0:

```text
lean --trust=0 -j1 -DElab.async=false -o Agent105UniformReturnPlain.olean Agent105UniformReturnPlain.lean
```

Both literal `#print axioms` commands report exactly `propext`,
`Classical.choice`, and `Quot.sound`.

The twenty dependency modules are recorded in `dependency-pins.json`.
`attempts/attempt-001/reused-artifacts.json` records the origin and `.olean`
hash of every reused artifact. Each canonical source was required to match
the exact repository source bytes before its artifact could be used. All
dependencies were copied into one isolated module-resolution directory.

`develop.py` compiles only the new Plain module. It never rebuilds a dependency:
if a matching artifact is missing, it records that failure and stops. This
implements the parent's resource coordination instruction and prevents an
accidental restart of the memory-heavy inherited carry library.

This is an author check using explicit cached dependencies, not an independent
fresh dependency build. The frozen source and complete pins were handed to
`lean_runtime` for independent semantic review and a fresh `--trust=0` check of
the small new module against independently checked dependency provenance.
The author does not certify the independent review's outcome in advance.

The original review and Finding U1 are retained separately under
`review/uniform/source-scout/`, with explicit disclosure that this reviewer
later authored the Plain repair and therefore does not independently review it.
