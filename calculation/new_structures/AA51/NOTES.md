# AA51 running notes

## 2026-10-29 09:00 UTC — registration and first literature pass

- Registered `CLAIM agent-AA51 route=BASE-TRANSFER-1` in issue #475. Premise: compare the self-reproducing run-length/carry interface in the power-of-two proofs and the base-9 neutral-band certificate against decimal T*. Build on FOCUS_SWARM facts (a), (c), (r)-(t), especially the epoch-seam map and parity-complete gates.
- `AGENTS.md` and `docs/FOCUS_SWARM.md` were fetched from raw GitHub. The owner directive says no finite-horizon result is a deliverable. FOCUS_SWARM labels the decimal target UNDECIDED and identifies the missing lemma as a complete, uniform 120-step return with a rooted decimal realization.
- The base-2 proof is an exact four-step template recurrence. For the family `101^n 010^(n+1)` (notation in ProofWiki: repeated concatenation), four reverse-and-add operations advance the run parameter by one; the intermediate forms are separately described and shown non-palindromic. The key is a *symbolic carry identity at the two run boundaries*, not a long numerical replay. See https://proofwiki.org/wiki/Non-Palindromes_in_Base_2_by_Reverse-and-Add_Process and OEIS A058042 https://oeis.org/A058042.
- The paper “Search for and classification of Lychrel numbers” states that the same construction generalizes to bases that are powers of two, including base 4 and base 8, and gives base 4/base 26 examples. It also notes other base-4 proofs, so the mechanism is not universal. Source: https://cocalc.com/share/download/00ae14310fa0520ec7b59482b0807d8082d2c891/ReverseAndAddPDF.pdf.
- Important transfer distinction: the binary/power-of-two family does not preserve a fixed-width neutral separator. Its state is a phase-indexed run-length family, and the exact local carry algebra advances the parameter on every four-step macro. The decimal T* needs a different state space: 120 steps, +5 U copies, fixed W9 exponent, and the same seam/centre (or a proved closed seam orbit). Therefore copying the binary recurrence literally would not address the decimal seam map.
- GitHub API file/comment reads hit a 403 rate limit after the initial raw reads; issue #475 comment write succeeded. I have not claimed to have read the requested last 40 FEED lines or the full FORMATS.md.

## Status

No decimal lemma established yet. No numerical replay is being promoted as evidence. Continue by extracting the precise base-9 absorbing-band transition from repository data and testing whether the transition can be expressed as a finite carry-state invariant compatible with the decimal W9/U3 seam.
