# Y16: 72/144-step mod-9 obstruction for a stationary period-3 kink crystal

**PAPER PROOF (general charge conservation / all spatial widths); COMPUTED (18 phases x 3 cuts); NOT a decimal Lychrel certificate.**

## Exact scope
Fix the alternating decimal overflow clock gamma_t=1 for even t, 0 for odd t. At a spatial cut of the *time-cyclic* position automaton of period P (P=72 or 144), let L_t be the upward carry entering the next coefficient, H_t the downward carry leaving toward the preceding coefficient, and Y_t the previous upper output digit (used only when gamma_t=1). A stationary-periodic bridge is a finite path of these time-cyclic cut states from the canonical root to a bulk spatial-period-3 ring on the exact X23 recurrent 18-phase orbit. No fixed bound on bridge width is imposed. We do **not** allow a translating or widening interface that fails to return to its own coefficient at a fixed spatial site after P steps.

## All-width conservation lemma
For a column with coefficient x_t, successor x_{t+1}, and next spatial cut (L'_t,H'_t,Y'_t), the exact decimal carry equations are:

* gamma_t=0: x_{t+1} = 2x_t+L_t+H'_t -10(L'_t+H_t).
* gamma_t=1: x_{t+1} = x_t+L_t+Y_t -10 L'_t, and Y'_t=x_t+H'_t -10 H_t.

Let lambda_t=2^(-t) mod 9. Since 6 divides P, 2^P=1 mod 9, so lambda_{t-1}=2 lambda_t including the temporal wrap. Multiply the gamma=0 equation by lambda_t; at gamma=1, multiply both equations by lambda_t and add. Reduce 10 to 1 modulo 9 and sum over all t. The coefficient x_t telescopes to zero by the lambda recurrence, leaving

`Q(S') - Q(S) = 0 (mod 9)`, where `Q(S)=sum_t lambda_t (L_t-H_t+gamma_t Y_t) mod 9`.

This identity holds at **every** spatial edge, hence for a finite bridge of arbitrary width. The canonical decimal root has L_t=0, H_t=gamma_t, Y_t=1, so Q(root)=0 term by term.

## Charge of the X23 ring
The X23 ring starts with (8,6,8), then enters an exact 18-phase ring after 12 steps, at row (4,14,4) with gamma_0=1. At each time the ascending and descending cyclic carry is unique because each 3-site row is non-neutral. Define cyclic output digits d^+ and d^- from each carry; the next row is `r'[j]=d^+[j]+d^-[(j-gamma)%3]`.

The complete 18-row exact enumeration verifies this transition, its minimal period, and the time-cyclic column equations. For all three spatial cuts and all 18 temporal phase shifts, the length-18 charge is 3 when gamma_0=1 and 6 when gamma_0=0. Lambda has period 6, hence charges repeat additively: at P=72 (four laps), Q=3 or 6; at P=144 (eight laps), Q=6 or 3; at P=216 (twelve laps), Q=0. The first two values are nonzero for every phase. Therefore an exact 72- or 144-step stationary rooted bridge cannot terminate in the recurrent m3 crystal because Q(root)=0 differs from Q(ring). This contradiction is independent of bridge length, choice of intermediate coefficients and SAT search width.

Reproduce with `python3 calculation/new_structures/agent-Y16/kink_charge.py`: checks 18 temporal phases, three cuts, all 72/144/216 coefficient equations, the root charge and both X23 ring clocks. As a separate model check, builds two canonical *ordinary decimal integers* with p8 B/W exteriors and m3 interior, evolves them using Python arbitrary-precision integer reversal and addition, independently evolves whole pairwords by coefficient normalization, compares both words at each of 145 times, and checks protected interior ring phases; no horizon claim is made from this replay.

## Redirection and limitations
The exact m3 stationary repair cycle of period 72 or 144, including all microscopic junction widths, is **impossible**. Since 216 has zero charge, the shortest unrestricted same-clock superperiod not blocked by this invariant is 216, beyond the requested period-200 search. The X23 spatial-period-6 temporal-period-96 ring has zero charge at all six cuts and remains a viable target for a separate exact junction SAT search (not a proof of its existence). Moving, spatially translating, phase-resetting and growing interfaces are not ruled out, because fixed-position time closure fails there; neither is any decimal Lychrel orbit.