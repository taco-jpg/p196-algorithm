# Raw symmetry obstruction and positive seam-defect safety

`RawSymmetryObstruction.lean` proves the complete finite-word obstruction
with an actual decimal bridge, and a useful positive safety corollary.
It imports the unchanged incoming-carry module and its unchanged decimal
dependency. All earlier gate, prefix, and incoming-carry sources remain
unchanged.

## Main checked statements

For every finite symmetric coefficient word q with entries in 0 through
18, and every partition into consecutive nonempty blocks:

1. If the raw sum E of the separately normalized blocks is symmetric at
   the actual full output width, every actual outgoing carry agrees with
   the corresponding separately normalized outgoing carry. Hence the
   actual seam-defect polynomial K has every coefficient zero.
2. More specifically, in the no-overflow branch every coefficient of q
   is at most 9. In the overflow branch every coefficient is 0 or 11.
   For a canonical pair word, raw symmetry therefore makes the next
   ordinary reverse-and-add output a palindrome.
3. Independently of raw symmetry, any nonzero actual seam carry defect
   certifies that the next ordinary reverse-and-add output is
   nonpalindromic.

Thus imposing both symmetric E and nonzero K is impossible. The positive
one-step safety criterion needs only nonzero K, with K computed from the
actual and isolated carry recurrences. No symmetric-E assumption occurs
in `numeric_nonzero_defect_safe`.

The concrete canonical partition

    (9,9) | (18) | (9,9)

is instantiated by the ordinary seed 99900. The source proves a nonzero
carry defect at column 3, then applies the general safety theorem. It
also proves the exact ordinary step value 99900 -> 100899. These finite
numeric facts use kernel-checked `decide`, never `native_decide`.

## Actual partition representation

An arbitrary Boolean function `cut` marks starts of blocks. The first
column's incoming carry is zero regardless of its boundary bit; every
other marked position resets the isolated incoming carry to zero.
`resetOut` computes the resulting outgoing carry at every column.

`resetOut_on_block` proves that any interval starting at zero or a marked
boundary, with no further interior boundary, has exactly the ordinary
normalization carry stream started from zero. Thus the reset definition
represents the isolated normalization of every block of any finite
partition. Boundary bits outside the finite word are immaterial.

`rawCoeff_is_placed_sum` proves that the raw coefficient is its isolated
output digit plus the preceding block's terminal carry at a cut.
`resetRaw_lt` and `resetRaw_terminal` identify the zero-extended integer
formula

    E = q + (x-10) C

with those actual raw placed coefficients, including the final terminal
carry. The raw coefficients are nonnegative and at most 10. `raw_value`
proves exact finite numerical value conservation.

`seamDefect q cut i` is the actual outgoing carry at column i minus the
isolated reset outgoing carry there. Its i-th coefficient is the K used
by the constructive seam argument. The theorem rules out any nonzero
coefficient within the whole word, including the last outgoing carry.
No polynomial-library representation or unproved coefficient identity
is assumed.

## Arithmetic proof and its boundary

The separately named `finite_state_rigidity` is an auxiliary arithmetic
theorem. It explicitly assumes S_L=0, the recurrence S_(i+1)=S_i+C_i-R_i,
and q_i=10C_i+R_i+9S_i, with nonnegative C and binary R and tau. The local
normalized remainder lies in 0 through 9. Backward induction proves
S=0, C=R, and q=11C. This core does not itself claim to instantiate a
decimal partition.

The stronger `raw_overflow_rigidity` does instantiate the boundary from
the raw palindrome equations. Extend q and C by zero, set

    R_i = C_(L-1-i) for i<L, and 0 otherwise,
    P_i = q_i - 10C_i - R_i.

The full raw symmetry equations imply
P_(i+1)=P_i+9(C_i-R_i), including the last column; P_L=0 follows from the
zero extensions. A backward local arithmetic lemma forces every P_i=0.
No terminal S hypothesis, finite reverse-sum identity, or bounded search
is assumed in the full theorem.

In the no-overflow branch, actual carry domination forces the last
isolated carry to vanish. Raw symmetry, exact value conservation, and
the existing injectivity theorem for bounded symmetric coefficient
words give E=q. The local raw column equation then forces every isolated
carry to vanish and every q_i<=9.

`actual_width_raw_symmetry_rigidity` combines both branches at the actual
`nextWidth`. `admissible_raw_symmetry_bad` and
`numeric_raw_symmetry_palindrome` supply the canonical pair-word and
ordinary decimal bridges.

For the positive result, `badWord_reset_agrees` directly proves agreement
of actual and isolated carries in both exact immediate-palindrome
classes. Its contrapositive supplies `numeric_nonzero_defect_safe`.
This positive theorem does not depend on an assumption that E is symmetric.

## Scope and reproduction

This is one-step safety and a structural obstruction. It gives no rule
regenerating a nonzero defect forever, no invariant infinite safe family,
and no proof of decimal Lychrel existence.

From the project root run:

    python main_existence_attempt/renewal_pass/lean/raw_symmetry/check.py /workspace/scratch/fe6abe1df721/lean-runtime/lean

The checker freshly rebuilds the decimal source, incoming-carry source,
and new module; audits every new theorem transitively; and compares all
source hashes before and after compilation. Only `propext`,
`Classical.choice`, and `Quot.sound` are permitted. Source placeholders,
custom axioms, and `native_decide` are rejected. The complete compiler
output and final audit are retained beside this report.

Every development source and failure log is retained in
`development_checks/`. The first arithmetic attempt omitted nonnegativity
of C in the auxiliary scaled lemma. That omission is false: C=-1, R=0,
tau=0, P=9 has zero next state and a valid remainder. The repaired lemma
states C>=0 explicitly, as the actual binary-carry model already ensures.
Other failed attempts concerned beta reduction before arithmetic tactics
and simplification of boundary definitions. No theorem was rescued by
an unproved numerical assumption or by discarding a valid counterexample.

Fresh Lean 4.19.0 compilation and all 42 new theorem audits completed
with PASS. The decimal dependency compiled in 53.99 seconds, incoming
carry in 0.94 seconds, this module in 2.21 seconds, and the generated
audit in 0.97 seconds. Only the three standard axioms listed above occur.
The checked source SHA-256 is
`922b660e5b3ac42389cd6ea00885075327d4b44fb315b9cc496e1323890e9c87`.
