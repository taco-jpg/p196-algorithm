# Conditional final scalar-period composition

`ScalarPeriods.lean` prepares the final arithmetic application of the finite
scalar hierarchy. **Every accepted numerical bound in `ScalarPeriods.lean` has
an explicit `RootVertexCertificate` premise.** The accepted results do not
prove that premise or establish an unconditional 94- or 98-period bound.

The exact agreed certificate interface is: for every admissible actual pair
word of initial width at least 14, every finite actual path in the exact
seven-vertex scalar root graph has at most 659 vertices, at every start time
and phase. The concrete finite-table package will supply this proposition
only after its row checks and hierarchy instance have been completed.

`RootBridge.lean` also checks the exact field and edge correspondence between
the semantic root and finite job zero, using `Fin.val` as the encoding. Its
five development-compiled theorems reduce the required certificate to the
same vertex bound on job zero's natural-number IDs. They await the final
combined finite-instance audit; the present `verification.json` covers
`ScalarPeriods.lean` and its prerequisites only.

`ScalarBound.lean` is an **uncompiled, unaccepted endpoint draft**. Its seven
declarations show the intended unconditional application after
`ScalarHierarchy.finite_root_bound` is accepted. They are excluded from the
66-declaration report and must not be cited as proved numerical bounds. The
production finite-certificate build was stopped for publication before any
`JobChecks` module or final endpoint was compiled. The exact partial checkpoint
and continuation instructions are preserved in the finite-certificate package.

Eight theorems establish the rest of the composition:

- `iterPairs_restart` and `clock_restart` identify a later actual state with a
  restarted orbit. This permits application of the certificate after warmup.
- `wide_periods_le_94_of_root_certificate` maps a clock interval of `7R` steps
  to `7R+1` root vertices, including both endpoints. Thus `7R+1 ≤ 659` implies
  `R ≤ 94`. The physical-width assumption is at the chosen starting time.
- The width-dependent bound is `R ≤ 94 + warmup L`, using the already proved
  gain of three columns per full period.
- For width at least two, `warmup L ≤ 4` gives `R ≤ 98`. Width one completes
  no period, so the uniform result covers every admissible positive width.
- The shifted and canonical-digit forms cover every actual starting time and
  every rotation of the scalar clock `[4,8,16,7,15,6,13]`.

No statement introduces an independent carry choice, assumes persistence of
the clock, or concludes an eventual palindrome. Each bound applies to a
specified finite clock segment. All accepted numerical bounds retain the
numerical certificate premise; the uncompiled endpoint draft is not acceptance
evidence.

Run the fresh Lean 4.19.0 rebuild and axiom audit with:

```sh
python check.py --lean /path/to/lean
```

The checker recompiles the pinned base and every project dependency in a new
temporary directory, imports no old project objects, and records source,
object, log, and direct-import hashes. It audits all public declarations,
including the eight new wrappers. Only the standard `Classical.choice`,
`Quot.sound`, and `propext` axioms are accepted. The local environment uses
`-j1 -DElab.async=false` and the documented executable-path compatibility shim;
neither changes the Lean kernel.
