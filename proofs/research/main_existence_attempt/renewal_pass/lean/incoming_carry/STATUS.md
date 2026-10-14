# Incoming-carry sensitivity, with an actual-block bridge

`IncomingCarrySensitivity.lean` works with every finite coefficient block
whose entries are in 0 through 18. Symmetry, positive outer coefficients,
and overflow-clock agreement are not assumed. The only imported project
source is the unchanged `continuation/LychrelDigitSums.lean`.

Let `carryWith q c i` be the incoming carry at column i after starting
with carry c, and let `outputWith q c i` be its emitted decimal digit.
The new recurrences are proved equal to the existing ordinary decimal
`carry` and `output` when c=0. A value theorem proves that the finite
output including its terminal carry evaluates to `value(q)+c`.

For I_i equal to 1 exactly when every coefficient strictly before i is 9,
the module proves, using integer differences,

    carryWith(q,1,i) - carryWith(q,0,i) = I_i
    outputWith(q,1,i) - outputWith(q,0,i) = I_i - 10 I_(i+1).

Both identities extend to an arbitrary binary incoming carry c by
multiplying the right side by c. The first identity includes the final
boundary i=L. The output identity applies to every actual column i<L.

## Exact finite run and terminal case

Every finite block is proved to have a maximal initial 9-run of some
length ell in 0 through L. For initial carries 0 versus 1, the emitted
digit difference is -9 before ell, +1 at ell if ell<L, and 0 after ell.
The terminal carries differ by 1 exactly when ell=L. In that all-9 case,
the whole low output is explicitly proved to change from 9s to 0s, with
terminal carry changing from 0 to 1. Empty blocks are included.

Key declarations are `carry_difference`, `output_difference`, their
`_bit` versions, `initialNineRun_exists`, `output_difference_run`,
`terminal_difference_run`, and `all_nine_normalization`.

## Direct use at an actual seam

For an actual coefficient word q, let a be a block start and let
W(i)=q(a+i). The module proves that restarting at this offset with
the actual incoming carry `carry(q,a)` reproduces the original carry
and output recurrences exactly.

In particular, `actual_block_outgoing_run` proves the following for
every actual block of length L with initial 9-run ell and every i<L:

    carry(q,a+i+1) - carry(W,i+1)
      = carry(q,a)    if i<ell,
      = 0             otherwise.

Thus the difference between actual and isolated outgoing carries is
supported exactly on the initial 9-run when the actual incoming carry
is 1, and is zero everywhere when it is 0. The companion
`actual_block_output_defect` proves the exact actual-minus-isolated digit
formula. These are statements about the existing normalization of the
actual finite word, not hypotheses postulating a symbolic carry pattern.

This provides the local coefficient support needed by the constructive
branch's seam polynomial K. The full concatenated polynomial identity,
reflection law, collision reset, and an infinite safe orbit are not
formalized by this module.

## Reproduction and retained development

From the project root run:

    python main_existence_attempt/renewal_pass/lean/incoming_carry/check.py /workspace/scratch/fe6abe1df721/lean-runtime/lean

The checker freshly rebuilds the decimal dependency and new module,
then audits every new theorem transitively. Only `propext`,
`Classical.choice`, and `Quot.sound` are allowed. It rejects placeholders,
custom axioms, and `native_decide`; compares source hashes before and
after compilation; and writes `verification.json` only on complete PASS.

All development source snapshots and compiler output are retained in
`development_checks/`. Initial proof-script fixes concerned the explicit
classical decision for the finite-prefix indicator, namespaced integer
simplification lemmas, a branch with fewer remaining conditionals, and
normalization of natural-number addition in the shift proof. No numerical
search or rejected counterexample was used in proving the results.

The earlier finalized overlap-gate and prefix-obstruction modules and
their evidence are unchanged.

Fresh Lean 4.19.0 compilation and all 28 theorem audits completed with
PASS. The dependency compiled in 51.73 seconds, the new module in 0.88
seconds, and the generated audit in 0.65 seconds. Only the three standard
axioms listed above occur. The checked source SHA-256 is
`52850d75999a8fdad298e2e9da638965472ab6507f88630bf428698576ac631f`.
