# X24 exact target

Decide the neighboring phase-1 rooted p12/m9 cell for the 120-step epoch seam map:

- source halfword: `B_1 ++ W_1^q ++ J ++ U^k`, with mirrored palindromic coefficient centre `C`;
- `q >= 14`, `k >= 100`, `|J| in {3,4}` and every coefficient of `J` in `0..18`;
- `U` ranges over all 30 charge-zero rotations of `(9,a,18-a)`, `a in {0,2,...,18}`;
- `C` ranges over every canonical palindromic coefficient word of length 2..13, including both even and odd lengths (odd midpoint even).
- use the phase-1 clock `gamma[(1+t) mod 12]`, exactly 120 ordinary decimal reverse-and-add steps.

Necessary condition for any fixed point or finite cycle of the epoch seam map in this cell: the entire rooted `B_1 ++ W_1^q` prefix is restored at step 120. T12's phase-rotated cut/insertion and U3 reset-cone lemmas remove dependence on `q`, `k`, and `C`; therefore the finite reference-width decision is `(q,k)=(14,100)` and the endpoint test is on all 30 `U` words times all `19^3+19^4` junctions.

This target is a cell-local obstruction search, not a claim that a decimal Lychrel number exists.
