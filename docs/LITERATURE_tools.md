# T02: literature tools for the decimal repair interface

**Scope, 2026-10-28.** This is a focused literature-to-tool transfer, not a claimed base-10 Lychrel number. Code is in calculation/new_structures/T02/port_contract.py and the scoped result is results/T02FullBandPortCriterion.md. Finite-horizon survival is deliberately not used as evidence of an infinite orbit.

## What needs proving

For the rooted decimal period-8, spatial-period-20 exterior in calculation/new_structures/agent-N10/phase.json, a word has palindromic pair coefficients B_t W_t^k C_t reverse(W_t^k) reverse(B_t), with k symbolic. The missing **all-time** lemma is a physically realizable, closed seam/centre transition that never spends the band budget and excludes every palindrome. Existing finite gliders lose the guard. A practical proof requires an exact transition relation for all k, a safe phase-indexed inductive language, and a *canonical decimal seed* in that language.

## Carry automata and Walnut-style predicates

Walnut decides first-order properties of automatic sequences by constructing finite automata [R1,R2]. A direct same-direction zipped numeral encoding cannot synchronously recognize arbitrary digit reversal; intersecting the graph of reversal with the diagonal would recognize the nonregular palindrome language. Do not call a long numerical test a Walnut proof. Instead fold a numeral outside-to-centre: a letter is the mirrored digit pair or its pair sum; carry states (low incoming, upper outgoing), parity, overflow and the previous high normalized digit make one reverse-add step a finite-state relation. This precise encoding is already established by AgentN07FoldedRegularSafety and AgentN07TwoTrackStrictSafety; T02 does NOT claim to invent it. The new task is *synthesizing* a regular invariant satisfying exact inclusion L_t R subset L_(t+1), with phase-specific boundary ports.

## Synthesize rather than hand-guess invariants

Esparza, Raskin and Welzel-Mohr [R3] construct bounded-clause inductive regular invariants from above rather than merely enumerating reachable prefixes. For reverse-add, start from a language of physically safe pairwords, refine by exact predecessor inclusion and preserve the seam carry and a nonpalindrome witness as distinct predicates. Their length-preserving complexity bounds cannot be imported unchanged: encode the zero/one-length growth via an end marker or prove a finite rational-transduction extension first.

Habermehl and Vojnar's regular-language inference [R4], and abstract regular model checking [R5], suggest learning candidate phase DFAs from interface traces, then counterexample-guided refinement using the *unabstracted* two-ended carry product. A learned DFA is only a conjecture until a finite graph emptiness test proves exact closure for every word length. In particular do not merge carries 0 and 1 at the band/centre seam: this test shows they can have opposite full-band survival effects.

## Semigroup and transducer acceleration

Legay and Wolper [R6] analyze transducer-iteration acceleration. Start with **spatial** acceleration: compute the exact map induced by one whole 20-letter W_t band on sets of carry-product states, and find a fixed set or finite cycle. This proves universal k by induction without asking for 10,000 increasingly wide samples. Only attempt **temporal** acceleration after the repaired centre relation is proved and includes a nondecreasing band-count counter. A periodic moving window with a shrinking guard is not temporal recurrence.

## Gliders, substitution, semilinear guards

Glider collision taxonomies [R7] suggest representing a repair event by a finite carry-port contract: incoming phase/carry/position, outgoing phase/carry/position, and signed band credit. The known decimal 88-step moving front retreats; a genuine repair requires a verified collision/re-emission producing outward credit. Substitution-tiling self-similarity [R8] suggests a commuting macrocell diagram with a checked two-ended carry collar at *every scale*. The repo's Thue-Morse space-time tiles cover finitely many temporal layers at every spatial height; they do not give a complete temporal macrocycle. Presburger or semilinear one-counter calculations can validate nonnegative prefix credit over an already sound finite edge cycle; a positive abstract counter cycle without its rooted ordinary-decimal realization is spurious.

## Concrete Walnut-style all-length decision test: the p8/m20 full-band port

T02's exact two-ended finite-state product consumes the committed eight B_t (length 39) and W_t (length 20) sequences. Its state stores low carry, upper-side carry, preceding high normalized digit, mismatch count and age of the last mismatch. The two carry equations for pair sum x are

    l' = floor((x+l)/10),     r = floor((x+r')/10).

The low output digit is (x+l) mod 10, the upper output digit is (x+r') mod 10. When overflow gamma=0 their sum is the target pair; when gamma=1 the target uses the *previous* upper digit, except the first pair uses 1. Starting from l=0, r=gamma, the finite product processes B_t and then W_t. **For every phase its complete two-state boundary set after one W_t is exactly equal to that after two W_t blocks.** Induction gives the classification for every k>=1, for arbitrary physically realizable palindromic C, including both centre parities. Let u_t be the genuine carry at the upper-side W/C junction, c_(n-h) with h=39+20k.

| Phase t | gamma_t | Carries u_t preserving the entire next B_(t+1) W_(t+1)^k prefix |
|---|---:|---|
| 0 | 1 | 0 or 1 |
| 1 | 0 | 1 |
| 2 | 1 | 0 or 1 |
| 3 | 0 | 1 |
| 4 | 1 | 0 or 1 |
| 5 | 0 | 0 |
| 6 | 1 | 0 or 1 |
| 7 | 0 | 0 |

This is an **if and only if** all-width one-step carry-port criterion, not merely a sufficient worst-case erosion bound. The forbidden carry causes *exactly one* output mismatch, in the final coefficient of the full protected prefix. Thus the exact zero-loss interface demand for successive phase transitions is u_1=u_3=1 and u_5=u_7=0. The initial B/W prefixes already have odd pair coefficients, so full-band preservation plus dynamic realization of the port for all phases would preserve a nonpalindrome witness.

The code independently reconstructs canonical decimal integers, applies actual arbitrary-precision Python integer reverse-and-add, and compares 5,600 one-step outputs at widths k=1,2,3,5,8 and randomly varied palindromic centres. Both seam carry classes occur in every phase. These finite real-integer tests validate implementation; the universal-k claim rests **only** on the two-state transfer fixed-point proof. Reproduce with python3 calculation/new_structures/T02/port_contract.py.

**Exact unresolved lemma:** produce a nonempty, canonical-integer-rooted centre-language cycle that enforces u_1=u_3=1 and u_5=u_7=0 at *every* eight-phase repetition (or a certified alternative collision that restores a lost full W block), while maintaining k>=1. No such cycle has been found in T02. A nonzero positive-gain repaired cycle plus all-phase nonpalindrome guards, not another long trajectory, is required for an ALERT.

## References

- [R1] Baranwal, Decision Algorithms for Ostrowski-Automatic Sequences (2020), https://uwspace.uwaterloo.ca/items/9b25240e-3e35-4074-8bcf-08a9d7e7c048
- [R2] Walnut theorem prover, https://github.com/Walnut-Theorem-Prover/Walnut
- [R3] Esparza, Raskin, Welzel-Mohr, Regular Model Checking Upside-Down, https://arxiv.org/abs/2205.03060
- [R4] Habermehl and Vojnar, Regular Model Checking Using Inference of Regular Languages, https://doi.org/10.1016/j.entcs.2005.01.044
- [R5] Rogalewicz et al., Abstract Regular (Tree) Model Checking, https://www.fit.vut.cz/research/result/c91492/
- [R6] Legay and Wolper, On (Omega-)Regular Model Checking, https://arxiv.org/abs/0809.2214
- [R7] Glider collision analysis, https://doi.org/10.1142/S0129183111016348
- [R8] Walton and Whittaker, Self-similarity and limit spaces of substitution tiling semigroups, https://doi.org/10.4171/ggd/807
