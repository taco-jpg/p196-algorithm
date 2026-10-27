# Agent 107 — no universal period-4 linear quotient modulo 101

**Status: PAPER PROOF + COMPUTED.** Actual repository gate: PASS.
Coordination: [T2.period4-mod101-quotient claim](https://github.com/taco-jpg/p196-algorithm/issues/289#issuecomment-6433557513).

For decimal neutral exteriors, no nonzero fixed period-4 linear charge
modulo 101 has a deterministic next-charge law on all legal states satisfying
the necessary alternating residue modulo 11. This remains true when the
law retains width, both exterior carry flags, and the trim count, and even
when it receives all four source aggregates instead of one scalar charge.
The obstruction already occurs in four pairs of width-16 nonoverflow edges.
It is not a cycle exclusion or a decimal Lychrel existence result.

## 1. Prior work and the mathematical distinction

- [Agent51ReciprocalMoment](../lean/P196/Agent51ReciprocalMoment/ReciprocalMoment.lean)
  proves the exact reciprocal first-moment identity for symmetric words,
  including `reciprocal_first_moment` and derivative redundancy modulo 9.
  Those statements concern symmetry and weighted sums; they do not assert
  closure of the present nonsymmetric exterior aggregate under a transition.
- [REPORT_204](REPORT_204.md), Theorem 1, and
  [REPORT_214](REPORT_214.md), Section 2, give exact directional-carry bulk
  maps. In particular, REPORT_214 equation (2.5) already contains the local
  no-9 defect `-20` at a high column and `+1` at either neighbor.
  Their spatially periodic bulk words differ from the arbitrary finite
  exterior words aggregated by position modulo 4 here.
- [Agent112's numeric-step scope](https://github.com/taco-jpg/p196-algorithm/issues/289#issuecomment-6433452510),
  subsequently published as [PR414](https://github.com/taco-jpg/p196-algorithm/pull/414),
  derives the actual carry flags and both positional values of raw `nextB`
  from width and the forward/reversed source values. It is not a dependency here.
  Such full numeric information
  differs from the reduced modular aggregates studied in this report.
- [Agent107 alternating-charge report](agent-107-T2-alternating-charge.md),
  published in [PR363](https://github.com/taco-jpg/p196-algorithm/pull/363),
  gives the strong necessary residue used below. This report does not
  re-prove or claim invention of the alternating-moment method.

The contribution is a finite collision obstruction within that strong
residue class, with a full-rank four-row matrix over the field with 101
elements. The hypothetical transition function need not be linear or affine.

## 2. Exact domain and the proposed quotient

Coefficients are least significant first. A legal nonempty decimal exterior
`B` has coefficients in `0..18` and `B[0] > 0`. Write

\[
A(B)=\sum_{i=0}^{|B|-1}(-1)^iB_i,\qquad
R_{11}(B)=A(B)-(-1)^{|B|}\pmod {11}.
\]

Let `norm(W,c)` be ordinary base-10 carry normalization with entry bit `c`.
Set `(D,e)=norm(B,0)` and `(H,g)=norm(reverse(B),1-e)`.
For `g=0`, the unchanged A120 exterior map is

\[
F(B)=D+H^{\mathrm{rev}},
\]

with coordinatewise addition. A legal edge removes a suffix of `u` neutral
coefficients, so `F(B)=B' ++ 9^u`. Only the `g=0` restriction is needed
for the obstruction; the witnesses below also all have `u=0`.

Define the exact centered aggregates and their scalar projection by

\[
M_r(B)=\sum_{i\equiv r\ (4)}(B_i-9),\quad r=0,1,2,3,
\qquad S_w(B)=\sum_{r=0}^3w_rM_r(B)\pmod {101},
\]

where `w` is a fixed vector in `F_101^4`.
Appending or deleting neutral coefficients does not change these aggregates.
Since `10^2 = -1 (mod 101)`, the familiar centered positional evaluation
modulo 101 uses `w=(1,10,100,91)`; the theorem covers every fixed `w`.

**Theorem.** Suppose a function `Phi`, with no algebraic restrictions,
satisfies

\[
S_w(B')=\Phi(S_w(B),|B|,e,g,u)
\]

for every legal exterior edge with `R11(B)=R11(B')=0`.
Then `w=0`. The same conclusion holds if `Phi` is given the whole vector
`(M_0(B),...,M_3(B)) mod 101`, and also if it retains the common center
source, center target, and center trim of the witnesses below.

## 3. Four exact pairs of legal edges

Let `E_i` denote the coordinate unit vector of length 16. For each
`j in {2,3,4,5}`, start with the word having head 2 and all other entries 1,
and define

\[
X^{(j)}_j=X^{(j)}_{j+4}=5,\qquad X^{(j)}_{j+8}=4,
\qquad Y^{(j)}=X^{(j)}+5E_j-5E_{j+4}.
\]

Thus the corresponding entries of `Y` are `10,0,4`.
All modified positions lie between 2 and 13. Both heads are 2, both tails
are 1, and every coefficient lies in `0..10`. In particular, these are
legal nonempty words with no removable neutral suffix.

The source aggregates agree as integers: the two changed positions have
the same residue modulo 4 and their changes sum to zero.
The default word has alternating sum 1. If `s=(-1)^j`, the modifications
defining `X` add `(4+4+3)s=11s`; the change from `X` to `Y` adds zero.
Consequently

\[
A(X)=A(Y)=1+11s,\qquad R_{11}(X)=R_{11}(Y)=0.
\]

For `X`, forward normalization has no carry, and reverse normalization
with entry 1 adds one only at position 15. Hence `e=g=0` and

\[
F(X)=2X+E_{15}.
\]

For `Y`, the single coefficient 10 at position `j` generates a carry in
each direction. Its unmodified neighbors both equal 1, so those carries
stop immediately. The entry carry at position 15 also stops immediately.
The two normalized words, written in the original coordinate order, are

\[
D(Y)=Y-10E_j+E_{j+1},\qquad
H(Y)^{\mathrm{rev}}=Y+E_{15}-10E_j+E_{j-1}.
\]

Neither carry reaches an exit, giving `e=g=0`, and

\[
F(Y)-F(X)=-10E_j-10E_{j+4}+E_{j-1}+E_{j+1}. \tag{1}
\]

Both targets have head 4, tail 3, width 16, and coefficients in `0..10`.
Thus `u=0` is also the maximal legal suffix trim. Moreover,

\[
A(F(X))=1+22s,\qquad A(F(Y))=1,
\]

so both targets retain `R11=0`.

These are full A120 legal edges, not merely autonomous exterior examples.
Use the same one-cell center `C=[18]` for every source. Its normalization
with entry `e=0` is digit 8 and exit `e2=1`, so `Hyp` holds and
`nextC=[16]`. Choose `v=0`. Every target exterior has exit carry 0
(its final coefficient 3 clears any incoming bit); normalizing `[16]`
with entry 0 again exits with 1. Thus target `Hyp` holds too. Both centers
are bounded, symmetric, and nonempty. The common retained edge data are
`width=16, e=0, e2=1, g=0, u=v=0, C=[18], C'=[16]`.

## 4. The collision matrix forces every weight to vanish

Aggregating (1) modulo 4 gives the exact vector

\[
d_j=\mathbf e_{j-1}-20\mathbf e_j+\mathbf e_{j+1},
\]

where subscripts on the four-dimensional unit vectors are read modulo 4.
In the script's order `j=2,3,4,5`, the rows are

\[
D=\begin{pmatrix}
0&1&-20&1\\
1&0&1&-20\\
-20&1&0&1\\
1&-20&1&0
\end{pmatrix},\qquad
\det D=158400\equiv32\pmod {101}. \tag{2}
\]

For an independent determinant derivation, reorder the rows to residues
`0,1,2,3`. This even permutation gives the circulant matrix with diagonal
`-20` and cyclic-neighbor entries 1. Its eigenvalues over the reals are
`-18,-20,-22,-20`, whose product is 158400. The same integer determinant
is nonzero modulo 101.

For each pair, every argument to the proposed function agrees, so its
outputs must agree. Therefore `d_j dot w=0` for all four rows. Equation (2)
forces `w=0` over `F_101`, proving the theorem. This argument also proves
the stronger input-vector version because the full source aggregates agree.

The natural positional weights give output differences `20,99,81,2`
modulo 101 in the stated row order, all nonzero. As a separate consistency
control, the old alternating weights `(1,-1,1,-1)` give differences
`-22(-1)^j`, which vanish modulo 11, exactly as required by the strong filter.

## 5. Reproducibility and limits

The companion `calculation/agent-107/period4_quotient.py` generates these
eight full edges, replays the unchanged `neutral_band_search.py` checker,
checks source and target `Hyp` and `R11`, and validates the exact matrix,
determinant, and both products with a supplied inverse modulo 101.
The `witnesses` command prints the complete finite certificate.

```sh
python3 calculation/agent-107/period4_quotient.py check
python3 -O calculation/agent-107/period4_quotient.py check
python3 calculation/agent-107/period4_quotient.py witnesses
python3 -O calculation/agent-107/test_period4_quotient.py
python3 tools/verify.py --changed
```

Normal and optimized `check` both return `status: PASS`, with:

```text
pairs=4 mirror_edges=8 source_target_hyp=16 strong_R11=16
equal_input_moments=4 target_difference_rows=4 inverse_product_entries=32
determinant=158400 determinant_mod=32 rank=4
natural_output_differences=[20,99,81,2]
alternating_mod11_output_differences=[0,0,0,0]
inverse_mod=[[24,38,29,38],[38,24,38,29],
             [29,38,24,38],[38,29,38,24]]
```

The independent optimized-Python suite passes six tests in 0.335 seconds.
It reconstructs all eight transitions by whole-integer normalization,
checks the exact determinant by rational elimination and the inverse by
cofactors, and verifies both inverse products. Ten corrupted evidence
objects are rejected. It also checks the natural positional weights,
the retained alternating control (matrix rank3 modulo11), and both CLI modes.
No validation depends on Python assertions. The source checker validates
submitted evidence rather than replacing corrupted outputs with regenerated ones.

Actual `python3 tools/verify.py --changed`: **PASS**, checking 5,217 Lean
files / 301 projects with zero changed Lean modules / audited endpoints.
No new Lean module or Lean verification of this theorem is claimed.

The theorem concerns fixed period-4 linear charges modulo 101 and a law
valid on the entire stated domain. It does not exclude richer carry or
memory data, nonlinear word representations, other periods or moduli,
or a law restricted to recurrent states. The witnesses are legal edges;
they are not proved to belong to exterior cycles or to have infinite
compatible center orbits. This result neither excludes decimal exterior
cycles nor proves that the neutral-band route cannot work.
