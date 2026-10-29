# U47 discarded or non-promotable leads

- R18 phase-4 fixed seam (`J=[17,5,5,9,6,6,6,14,5,11,7,10,14,7,8,15,9,6,4,18,9,10,17,2]`, `U=[18,0,9]`, `C=[4,14,4]`) has nonzero mod-31 cyclotomic carry syndrome for all 25 sampled residue classes `q,k mod 5`, using representatives `q,k=242..246`. The independent bigint and digit-array engines agree through all 120 steps, with 30 overflows. This is only a candidate-specific diagnostic; R18 is already excluded by the existing T28 affine-run result, so do not promote this as a new no-go.
- The reusable contribution is the general all-width carry-cocycle condition in `NOTES.md`; it still needs to be used to constrain a previously unexcluded seam or produce a positive return.
