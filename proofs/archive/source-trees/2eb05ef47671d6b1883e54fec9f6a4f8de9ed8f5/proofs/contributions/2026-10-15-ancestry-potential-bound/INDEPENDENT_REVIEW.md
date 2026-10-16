# Independent review of the ancestry time bound

**PASS**, independent gate-review stream, 2026-10-15. I read the complete addendum, the exact external absorbing-core note, and the original formal potential definition and one-step theorem.

Reviewed SHA-256 pins:

- `ANCESTRY_BOUND.md`: `cf3d64bfe77474542aa9bb010ba1be500e0d4950ab5e1b0e63d331b71ae25492`.
- `sources.json`: `af05fc76effb5554116755b95ae0d2f208e14a14bf1e73ba558d3c727c9dded8`.
- External `ABSORBING_CORE.md`: `c301936575fe275ac11e22ad56be2654da7ff4317ec36b3061af9524b0cec910`.
- Original `LychrelDigitSums.lean`: `ca5f46523b7cff02c00918b6466a97963087b499fb5f184232b8b3d806dc0b57`.

Both dependency byte counts and Git blob hashes also match `sources.json`.

The external no-expansion/no-merging result gives `O_t<=ell-1` whenever the identified ancestry survives. Summing `lower_potential_step` gives `t+psi(p_t)<=4O_t+psi(p_0)` after cancelling the initial width. Substitution and nonnegativity exclude survival at integer time `4ell-3+psi(p_0)`. The potential table matches the original definition and is bounded by four, so the uniform bound is `4ell+1`; it equals `5ell` at `ell=1` and is strictly smaller for `ell>=2`. The endpoint `ell=1, psi(p_0)=0` correctly gives extinction by time one.

The addendum cites the one-step inequality for the retained terminal potential and describes `width_lower_potential` only as its width consequence. Restarting from a later state uses that state's length and potential. The claim concerns one tracked ancestry, permits new births elsewhere, and makes no whole-orbit extinction or palindrome-attainment assertion. This is a written corollary; no new computation or Lean compilation is claimed or needed.
