# Agent N02: constructive regular-centre backward refinement at all lengths

**Label: COMPUTED** (exact finite automaton computations through six steps); **PAPER PROOF** of the language preimage construction. Neither establishes a base-10 Lychrel orbit. This report extends `AgentN02RegularCentreFormat.md`, not another fixed-centre width exclusion.

## Precise construction

Fix base 10, the first p8/m20 rec0 rooted lattice exterior from tracked `calculation/decimal_frontier/lattice_formats/p8_scc.txt`, and its first **39** pair coefficients `B_t` at each temporal phase t=0..7. The forced overflow schedule is `gamma=10101010`; because `B_t[0]` alternates 17 and 8, the overflow is independent of all central digits. For parity `e in {0,1}`, define the regular language `U[t,e]` of **every** physically admissible palindromic pair halfword with prefix `B_t` and unrestricted remaining centre, including centre-evenness when the total length is odd. Every such word has an odd coefficient in its fixed prefix, so no corresponding number is a palindrome.

For a target DFA L and fixed parity e and overflow gamma, the exact **preimage NFA** of the lower-half reverse-add map has states `(low_carry, high_carry, previous_high_digit, target_DFA_state, first_symbol)`. There are at most 2x2x10x|Q|x2 ordinary labelled states plus a terminal state. Its pair-letter transitions use the original two-sided carry equations from the preceding report, and its final acceptance/centre transition exactly enforces the middle carry meeting. Taking the reachable subset construction yields a DFA for **all source lengths**, not merely sources below a bound. The NFA state and final-state proof gives `w in Pre_gamma(L)` iff the ordinary base-10 successor of the physical pairword w has overflow gamma and its halfword lies in L. Hence regular languages are effectively closed under this preimage, with no spatial-width restriction.

Iterate `S[t,e,0]=U[t,e]` and

`S[t,e,k+1] = U[t,e] intersection Pre_(gamma[t],e)(S[(t+1) mod 8, (e+gamma[t]) mod 2, k])`.

Thus `S[t,e,k]` is the **exact language of all centred decimal pairwords of arbitrary length** whose first k reverse-add steps preserve the prescribed rooted exterior and nonpalindromicity. This statement is a PAPER PROOF by induction, conditional only on the already specified rooted exterior data; the implemented automata are complete and checked with actual base-10 numbers. The precise data and tested scope are `calculation/new_structures/agent-N02/preimage_depth6.json`.

## Exact completed computation

For each k=0..6, all 16 `S[t,e,k]` were determinized, intersected with the physical prefix language, and minimized. No source-word length bound was imposed; the subset construction has a 20,000-state safety cap and the intersection 80,000 states, **neither cap reached for the completed six levels**. Full 16-language per-depth minimized DFA sizes and shortest lengths are tracked in JSON. The largest automata by depth:

| k | max minimized states | shortest accepted halfword lengths (across 16 classes) |
|---|---:|---|
| 0 | 43 | 39–40 |
| 1 | 43 | 39–40 |
| 2 | 47 | 39–40 |
| 3 | 66 | 39–40 |
| 4 | 231 | 39–40 |
| 5 | 878 | 39–40 |
| 6 | 3558 | 39–40 |

All 16 depth-6 DFAs have a reachable accepting cycle, so **each accepts infinitely many word lengths**. The automata admit unbounded centre complexity, though this particular check does not establish nonperiodicity of individual accepted words. This is a positive growing-centre construction for every tested finite horizon, not a periodic certificate. DFA state growth, rather than absence of admissible centre words, currently blocks direct finite-state fixed-point induction.

## Independent validation

`python3 calculation/new_structures/agent-N02/preimage_check.py` runs three independent controls:

1. **18,480 random predecessor membership checks** for bases fixed at 10, all four parity/overflow modes and three independently specified target languages. Every NFA-determinized preimage answer agrees with direct integer place-value evaluation, independent of the transducer used to build the automaton.
2. **96 literal decimal digit-list replay steps**: for each of 16 phase/parity languages at depth 6, reconstruct a positive number realizing its shortest pairword, then run six ordinary digit-list `N + reverse(N)` updates. Every phase matches the expected overflow and all 39 exterior pair coefficients on every step; initial numbers at each step are nonpalindromic.
3. **16 unboundedness checks** for the exact depth-6 deterministic machines: all have an accepting cycle reachable from their start state (all return true), independently of any sampled length.

`python3 calculation/new_structures/agent-N02/regular_preimage.py 6` recomputes all seven depth tables. Depth 7 was not completed in this result; no claim of stabilization, all-k survival for a *fixed* seed, or a decimal certificate is made. For the known base-9 all-length **positive** certificate control, run the separate `base9_control.py` from the preceding commit.

## Constructive next step

The 16 independent automata could be quotiented by their **carry-history residual languages**, not rebuilt by full subset determinization, to seek a finite phase-cycle fixed point. Alternatively an automatic substitution should provide a finite description of the growing refinement tower even when DFA state counts grow with depth. The exact `S[t,e,k]` automata supply testable target languages for either construction and, through accepting cycles, centre words of arbitrary length at every completed k.

No Lean files were changed. The container does not include a GitHub clone, so full `tools/verify.py --changed` was unavailable; all local Python reproduction commands above completed.