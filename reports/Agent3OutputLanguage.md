# All-window physical output-language asymmetry for decimal rec2

**PAPER PROOF (finite-state certificate).** For the base-10 rec2 period-8/spatial-period-48 bulk, the overflow-0 local map is surjective on *all finite physically admissible parity/carry blocks*, when the cyclic source period may be any sufficiently large multiple of 48. The overflow-1 map is not: it forbids the eleven-symbol block `(7,1)^5,7` although the target is physically admissible. This is an exact unbounded-spatial-window lemma, not a bounded-width centre exclusion, an all-time decimal orbit, or a 196 claim.

## Physical state and map

A physical pairword coefficient is `P_j` in `0..18`. Its ascending/descending carries `a_j,d_j` are in `{0,1}` and obey

    a_(j+1) = floor((P_j+a_j)/10),  d_(j-1) = floor((P_j+d_j)/10).

The 76 states `(P_j,a_j,d_j)` form a directed graph `G` with 1444 edges; label each state `ell=(P_j mod 2)+2*a_j+4*d_j` in `0..7`. A finite label block is *physically admissible* if it labels a path in `G`. For an input edge `(p,a,d)->(q,A,D)`, the exact output coefficient is

    g=0: y = 2q+A+D-10*(floor((q+A)/10)+floor((q+D)/10));
    g=1: y = p+q+A+d-10*(floor((q+A)/10)+floor((p+d)/10)).

These are simply sums of the two schoolbook-normalized output digits, with the one-position reflection shift at overflow 1. The output product graph `H_g` has 1444 input edges times four output carry pairs = 5776 vertices and exactly 109744 edges. A vertex is `(input-edge,alpha,delta)`, labeled `(y mod2)+2*alpha+4*delta`. The transition to `(next-input-edge,beta,Delta)` requires concatenated input edges and

    beta=floor((y+alpha)/10),  delta=floor((y_next+Delta)/10).

Thus every genuine interior reverse-and-add image is a path in `H_g`. Conversely a closed `H_g` walk gives a cyclic physical source/output pair. The independent checker computes `y` using two literal decimal digit residues rather than the primary's bulk formula, and validates 2000 random physical 48-cycles as ordinary 386-/387-digit reverse-and-add steps.

## Overflow 0: exact forward simulation for all block lengths

The SCC containing vertex 1563 of `H_0` has 3116 vertices and a self-loop at 1563. Its hub source coefficient is 5 and its output coefficient is 10, so both input and output carry fixed points are forced and correspond to ordinary digit normalization. Let `C` be this SCC and define

    R0 = {(s,h) in G x C : label_G(s)=label_H(h)}.
    R1 = {(s,h) in R0 : for every edge s->t in G, some h->k in H_0 has (t,k) in R0}.

Exhaustive integer enumeration gives `|R0|=29600`, `|R1|=14924`, and every one of the 76 states of `G` is the first coordinate of an `R1` pair. Crucially, independently checked *for every* `(s,h) in R1` and *every* target edge `s->t`, there is an output edge `h->k` with `(t,k) in R1`. Thus `R1` is a total forward simulation. Induction lifts any target physical path of any finite length into `C`. Strong connectivity closes the lifted path through hub 1563, and the hub self-loop pads the source period to a multiple of 48. The forcing coefficient at the hub makes the closed carry solution physical. Repeating the band between canonical decimal ends realizes the target block in a genuine ordinary reverse-and-add output sufficiently far from both ends. This proves **all finite lengths**, not just the seven-cell rank result.

The deterministic witness is an exact physical 48-cycle whose `g=0` output begins with eleven alternating target labels `7,1,7,1,7,1,7,1,7,1,7`. The independent checker verifies it as an ordinary 386-digit decimal step, including the actual output carries.

## Overflow 1: an exact physically admissible forbidden block

Take `w=(7,1)^5,7`, length 11. Starting from all 5776 vertices of `H_1` labeled 7, propagate only successors labeled alternately 1 and 7. The exact nonzero-state counts after each prefix are

    722, 191, 133, 99, 81, 79, 71, 57, 36, 10, 0.

The last set is empty, even without restricting to a recurrent SCC. Thus no physical `g=1` bulk output, at *any* spatial length, contains this eleven-symbol block. This target is not an artificial independent-carry word: the physical 48-cycle `P=(1,11)^24` has ascending and descending carry bits `(1,0)^24` and therefore precisely the repeated labels `(7,1)^24`. The ten-symbol prefix is sharp for this pattern: the committed separate 48-cycle witness has a genuine `g=1` image starting with `(7,1)^5`, independently normalized from an ordinary 386-digit decimal input to a 387-digit output. Reversing the starting parity gives the same state-count sequence.

## Reproduction and limitations

From the repository root:

    sh calculation/decimal_frontier/lattice_kinks/agent3_output_language/run_checks.sh

The primary enumerates all physical states/edges, constructs `R1`, checks every simulation edge, checks the forbidden-word automaton, generates two 48-cell cyclic witnesses, and pins their combined text file to SHA256 `ac5a2193fbcbcd5ef03cef2cd9a57185f5f570dd96b5bd55566559c801f457a8`. The independent Python checker enumerates all 76x76 candidate physical edges and computes the output from actual decimal digit residues, independently reconstructs the simulation and forbidden-word counts, validates both witnesses by literal schoolbook normalization, runs 1000 genuine decimal steps for each overflow class, and replays all eight published 406-digit rec2 phase controls with deliberately wrong-overflow negatives. Local `run_checks.sh` passed. The full repository `tools/verify.py --changed` and Lean checks are not claimed because the local shell cannot resolve GitHub and no checkout/toolchain is available.

**Exact limitation:** The theorem distinguishes the two physical *bulk factor languages*, not the complete rooted temporal centre transfer. It does not force the forbidden block to appear in any proposed rec2 centre, and therefore does not exclude a centre of any width or establish an infinite decimal nonpalindromic orbit. Its role is to replace finite-window parity-rank evidence by an all-window output-language criterion that future centre repair constructions must respect.
