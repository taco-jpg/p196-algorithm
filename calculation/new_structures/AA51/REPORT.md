# AA51 report: base-transfer variant 1

**Status: PARTIAL (3/4 requested bases structurally compared; 0/1 decimal transfer lemmas closed).**  
**Label: UNDECIDED.** This report is not a decimal Lychrel proof and contains no finite-horizon claim.

## Exact missing lemma sought

A decimal carry/seam regeneration lemma: a finite state σ encoding the rooted W9/U3 boundary and all relevant carry/phase information, plus a positive-increment macro transition σ → σ' whose seam states form a proved finite cycle, while the W9 defect is restored exactly after each macro. For T*, this must realize 120 genuine decimal reverse-and-add steps with (q) fixed, (kmapsto k+5), and the seam/centre/phase restored (or a proved closed moving-seam family), uniformly for all sufficiently large independent q,k.

## What transfers from bases 2, 4, and 8

The published base-2 construction is a four-step symbolic recurrence. The pairword/run-length state has four phase types; exact carry identities map the designated phase back to the same family with the run parameter incremented. Intermediate phase forms are explicitly tracked and guarded against palindromes. This is stronger than observing many numerical iterations: the repeated-run parameter is an inductive invariant, and each boundary's carry behavior is part of the proof.

The classification paper reports that this construction generalizes to bases that are powers of two, including bases 4 and 8. The transferable abstraction is therefore not a literal digit string or a fixed neutral band; it is a finite phase-indexed template family with a proved symbolic transition at its moving boundaries. Sources: [ProofWiki's base-2 proof](https://proofwiki.org/wiki/Non-Palindromes_in_Base_2_by_Reverse-and-Add-Process), [OEIS A058042](https://oeis.org/A058042), and [Search for and classification of Lychrel numbers](https://cocalc.com/share/download/00ae14310fa0520ec7b59482b0807d8082d2c891/ReverseAndAddPDF.pdf).

## Comparison with decimal T*

T* has a different required invariant. Its 120-step macro adds five U copies but must leave the W9 exponent unchanged and restore the rooted exterior, seam, centre and phase. The supplied swarm state says one-epoch seams exist, but the second epoch loses about 21–23 W9 columns and changes the seam (including the observed J[1] transition 5 to 9). Thus the known decimal seam map is not yet a closed transition on a finite set of states with exact replenishment.

The useful lesson from the power-of-two cases is to promote the *entire phase-indexed seam and carry signature* to the state, rather than treating J alone as the state or demanding a fixed J prematurely. This is a research direction, not yet a lemma: no finite decimal state transition has been extracted or verified here, and the base-9 absorbing-band mechanism has not yet been inspected at the transition-table level.

## What was and was not done

- Registered route BASE-TRANSFER-1 in issue #475.
- Added TARGET.md, NOTES.md, and IDEAS.md under calculation/new_structures/AA51/.
- Fetched AGENTS.md and the opening portion of docs/FOCUS_SWARM.md. GitHub API reads then returned rate-limit 403, so the required last 40 FEED lines, historical pages 18–25, OPEN_PROBLEMS.md and FORMATS.md could not be independently inspected in this run.
- No independent big-integer replay or Lean check was performed; no claim is made that the decimal target survives even one full macro.
- No result belongs in results/ and no ALERT is warranted.

## Next decisive test

Recover the base-9 transition table and encode its absorbing-band boundary signature. Then compare that signature against a decimal phase-indexed seam signature, allowing a finite cycle of seam states rather than a fixed seam. A result counts only if the resulting transition proves uniform all-width regeneration and the intermediate states are non-palindromic.