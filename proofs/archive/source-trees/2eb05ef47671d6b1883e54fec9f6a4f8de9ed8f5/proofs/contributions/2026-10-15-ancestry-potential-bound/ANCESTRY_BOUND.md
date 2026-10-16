# A sharper time bound for one absorbing-run ancestry

This combines two existing results; it does not supply a new persistence
mechanism. It improves the external bound of `5 ell` for the lifetime of
one maximal run of zero or eighteen coefficients.

Start an actual positive decimal reverse-and-add orbit with a maximal run
of symbol zero or eighteen of positive length `ell`. Follow its natural
descendant in the sense of the external absorbing-core theorem. Let `O_t`
be the number of overflowing additions in the first `t` steps, and let
`p_t` be the exterior pair coefficient at time `t`. Define the existing
outer potential by

| Exterior coefficient | Potential psi |
| --- | ---: |
| 1 | 4 |
| 2 | 3 |
| 3, 4, 5 | 2 |
| 6, 7, 8, 9, 10 | 1 |
| 11 through 18 | 0 |

**Claim.** If this ancestry is still nonempty at time `t`, then

\[
t+\psi(p_t)\le 4(\ell-1)+\psi(p_0).
\]

Consequently it is extinct by time

\[
4\ell-3+\psi(p_0)\le 4\ell+1.
\]

The external exact ancestry theorem states that a surviving descendant
cannot expand or merge with newly born runs, and that every overflow
decreases its length by at least one. If it survives at time `t`, it
therefore has `O_t <= ell-1`. The existing actual outer-step inequality is

\[
\psi(p_{j+1})+1\le\psi(p_j)+4\gamma_j,
\]

where `gamma_j` is the actual overflow bit. Summing through the first `t`
steps gives `t+psi(p_t) <= psi(p_0)+4 O_t`. Substitution proves the claim.
The potential is nonnegative, so survival at the integer time
`4(ell-1)+psi(p_0)+1` is impossible. This is the displayed extinction
bound. Since `ell >= 1`, this time is positive even when `psi(p_0)=0`.

For example, initial exterior at least eleven gives extinction by
`4 ell-3`; initial exterior one gives the uniform bound `4 ell+1`.
The uniform bound agrees with `5 ell` at `ell=1` and improves it for
every `ell>=2`. No claim is made that the new bound is optimal.

The argument applies from any later orbit state by restarting time and
using that state's run length and exterior potential. It follows one
ancestry only. Newly born runs can persist after it disappears; the
statement neither eliminates all zero/eighteen coefficients nor implies
that a palindrome is reached. The ordinary mathematical map may be
continued after any palindrome.

## Provenance and evidence scope

The exact ancestry and no-merging theorem is in external commit
`d528a5f96773cba3f3aee88d006ff60dc946581c`, at
`proofs/research/main_existence_attempt/continuation_pass/seam_persistence/followup_absorbing_core/ABSORBING_CORE.md`.
Its `5 ell` estimate used a coarser five-step overflow guarantee. The
stronger potential was already available in the project and is also
used by that checkpoint's variable-return theorem.

The original formal dependency
`proofs/research/continuation/LychrelDigitSums.lean` defines
`DecimalWidthGrowth.lowerPotential` and proves
`DecimalWidthGrowth.lower_potential_step`. The latter is exactly the
one-step inequality above after replacing the width increase by its
overflow bit. `width_lower_potential` records its telescoped width
consequence. This addendum is a written corollary of those established
results, not a new Lean formalization of the ancestry construction.
No additional search or numerical extrapolation is used.
