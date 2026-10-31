# Open problems (maintained by the owner; status 2026-10-28)

Goal: a reverse-and-add orbit in base 10 that never reaches a palindrome. The proof method is a *certificate*: a
finite cycle of template-to-template steps, checked once and sound for every length (`lychrel_of_cycle`,
`lychrel_of_lcycle`). Certificates exist, with Lean proofs, in bases 2, 4, 8, 9, 11, 13, 16, 17, 20, 26, 32. **Base 10 has none.**

Labels: LEAN-VERIFIED / COMPUTED / PAPER PROOF / UNDECIDED. Every item below is UNDECIDED unless stated.

## What is already known (do not redo)

- Neutral-band format (`Agent120.Neutral.cycleOK`): the exterior B evolves alone and sends two bit streams (carry, overflow)
  to the centre C. Decimal single-band exteriors exist only for periods 11 and 12 (up to period 24, COMPUTED); no centre
  exists for p11 with 1 or 2 laps or p12 with 2 laps, at any length (COMPUTED, `cauto_fast`). See
  `calculation/neutral_band/README.md`. Further unreviewed claims about this route (centre width, overflow count) sit in
  128 closed pull requests, kept as tags `archive/2026-10-28/*`; treat them as unverified.
- Absorbing / lattice format (`lean/P196/AbsorbingBand`, `lean/P196/LatticeBand`, `reports/REPORT_LATTICE_BAND.md`): needs no
  centre when the lattice is self-mirror and m divides S. Found and Lean-verified in bases 9 and 13. In bases 5..31 and
  overflow period <= 12 nothing else exists (COMPUTED). Decimal: no reachable self-mirror lattice with m | S for any period
  up to 24 that the automaton decides (self-mirror lattices exist as cyclic row-map orbits, reachability is the obstruction); capped streams are dense words such as (10)^8, (1000)^6, 101010100101010100.
- Decimal period-8 exterior (g = 10101010) has lattice SCCs of period 20 and 48 (S = 4), p = 12 has m = 9 (S = 3). These are
  periodic exteriors that **need a periodic centre ("kink")**. Exhaustive search finds none of half-width <= 5 (p=8, p=12)
  and <= 7 (neutral p=11, p=12). Wider centres UNDECIDED. Code: `calculation/decimal_frontier/lattice_kinks`.
- Prefix method: 5,808 of 9,000 four-digit palindrome prefixes excluded in Lean. It cannot prove existence; ignore it.

## Tasks (claim one in issue #474 before starting)

- **K1 Centre existence for the period-8 lattices (the main difficulty).** Decide whether a time-periodic centre exists
  between the period-8 exterior lattices and their mirror, for half-width 8, 9, 10, ... Needs a smarter search than the
  current DFS (cost x10 per width): SAT/SMT, transfer-matrix / automaton on the centre column, or symbolic reasoning.
  Output: a certificate (then replay with big integers >= 20,000 steps and Lean-check) or an exact no-go for the
  stated widths.
- **K2 Wall-speed argument.** Prove or refute: the defect front between lattice and mirror advances at most c positions per
  step, so a centre of bounded width can never close. A proof for all widths would kill the period-8 route; a counterexample
  is a centre. Use the lifetime tables of the kink search as data. Output: PAPER PROOF with every table value checked.
- **E1 Exterior census beyond p = 24.** Position automaton (`calculation/decimal_frontier/lattice_formats/code/bauto*`):
  remove the 127-bit state key (it skipped 560 streams), rerun p <= 24, then p = 25..32. Output: the list of exterior
  cycles, all primitive, each replayed with big integers; DECIDED / CAPPED per stream.
- **E2 Capped dense streams.** (10)^8, (1000)^6, (10)^12, 101010100101010100 and the other capped words: decide them
  (backward cone, symmetry reduction, better pruning).
- **F1 New formats.** Templates with two or more bands, or a periodic band with a quasi-periodic centre, that cover the
  decimal data. Output: a format with a soundness theorem in Lean and a base where it finds a certificate (a control),
  then the decimal search in it.
- **F2 Families.** A parametric certificate for infinitely many bases (the bases 9 and 13 certificates, or the known power-of-
  two ones) with a Lean proof for all parameters. Bases 7, 19, 22, 25 have none for overflow period <= 12 (COMPUTED).
- **V1 Independent check of a claimed certificate** when one appears (task for the second agent, not before).

Nothing in this file is a claim that base 10 has or has no certificate.
