# N27: exact carry/overflow contract for a moving saturated central band

## Scope
**PAPER PROOF (one-step transfer, arbitrary base b>=2, with stated conditions). COMPUTED (five real decimal orbit intervals and exhaustive arithmetic controls).** This isolates a two-bit *front contract* that turns an observed decimal moving band into a precise, independently verifiable local mechanism. Neither a full certificate nor a universal persistence theorem for the carry lock is claimed.

## Local symbolic front format and exact theorem
Use least-significant-first palindromic pair coefficients in 0..2(b-1). Fix any integer base b>=2, let M=2(b-1), let L be a finite list whose final coefficient is not M (or L empty), and let q>=3. Set C=L ++ M^q ++ reverse(L). Choose an incoming carry e1 in {0,1}; normalize C from e1 by ordinary base-b carries to obtain digit list D and e2. Choose gamma in {0,1}; define the raw next centre by the exact standard reverse-add template operation:
gamma=0: Cnext_i = D_i + D_{|D|-1-i}.
gamma=1: Cnext = (D ++ [(b-1)(1-e2)]) + ([(b-1)(1-e2)] ++ reverse(D)), coefficient-wise.
Let c be the outgoing carry after normalizing L from e1. Let qnext be the length of the maximal central contiguous M-run in Cnext. Then exactly:
qnext = q - gamma - 2*(1-gamma)*(1-c).
This is nonnegative because q>=3. Removal of matching boundary neutral coefficients b-1 in Cnext does not change this central M-run, so the theorem also holds for the canonical neutral-band centre.
This is a closed one-step format: the only variable length q is updated by an explicit affine integer offset determined by two carry bits. Together with the existing exact exterior/neutral-gap edge condition, its transition can be used inside a finite checked template search. No recurrence-cycle closure is asserted.

## Paper proof
Normalize the prefix L, leaving carry c. The central M^q block normalizes to the digit string (b-1)^q if c=1, or (b-2) ++ (b-1)^(q-1) if c=0; in both cases its outgoing carry is 1. Normalizing the mirror suffix reverse(L) then starts with carry 1. For gamma=0, mirroring the normalized block aligns it with itself: when c=1, all q positions pair to M; when c=0, its two boundary positions pair (b-2)+(b-1)=M-1 and the q-2 central positions pair to M. For gamma=1 the shift by one position gives exactly q-1 central aligned (b-1)+(b-1)=M pairs in either case. Because L's terminal coefficient is not M, the immediately adjacent output coefficient cannot extend this maximal central run: obtaining M on both sides would require both normalized boundary digits b-1; the only possible nonmaximal terminal input is b-2 with incoming carry1, which exits with carry0 and cannot also satisfy the needed c=1 boundary case. In the c=0, gamma=0 case, a possible exterior M is separated from the central run by a boundary coefficient M-1. The formula follows by cases. Neutral b-1 trimming at the far ends cannot affect the centre since M>b-1.

## Decimal antiphase synchronization (computed)
For B0=[12,9], C0=[6]++9^m++[6], outer neutral gap g0=12000 and m=3000 (or g0=10000 for m=40,80,200,500), apply genuine ordinary decimal reverse-and-add. For every transition with an identified central 18 run q>=3 in the precollision region, calculate c by normalizing the literal lower prefix L of the central 18 plateau, and gamma by the actual decimal length change. The observed relation is c+gamma=1 on every checked transition. The first result's ordinary digit-list engine recomputes the entire integer and entire pairword at each time, so this is not a centre-only simulator.

| Initial m | Checked antiphase transitions | c=0,gamma=1 | c=1,gamma=0 | Other |
| ---: | ---: | ---: | ---: | ---: |
| 40 | 89 | 37 | 52 | 0 |
| 80 | 182 | 77 | 105 | 0 |
| 200 | 473 | 197 | 276 | 0 |
| 500 | 1181 | 497 | 684 | 0 |
| 3000 | 7251 | 2997 | 4254 | 0 |

Thus the symbolic theorem reduces on these trajectories to qnext=q-gamma. For m=3000 this is a striking 7251-step exact correlation between a near-centre carry and the global leading overflow; it is a computed carry lock, not an asserted algebraic law of all decimal seeds. At the subsequent front collision (t=7256) the maximal central run is zero, and this single-species formula no longer supplies a positive-length invariant.

## Reproduce and direction
Run sh calculation/new_structures/agent-N27/run_guard.sh from repo root (C++17 and Python3 only). guard_replay.cpp includes the earlier committed N27 replay.cpp, independently validates every full integer pairword, checks the local front equation, and asserts the observed antiphase condition on five explicit finite intervals. guard_generic.py exhaustively tests 255816 arbitrary-base single-edge cases in bases 2..20, q=3..8, L length 0..2 and all incoming carry/overflow bits. guard_expected.json lists the exact histograms and proof scope.
**Search redirection:** because this single M-plateau contracts under overflow, a genuine infinite decimal certificate should investigate a *multi-species absorbing-band handoff* that can create fresh saturated domains or feed an independent new band, rather than attempting to make this same plateau grow with a fixed core boundary. No all-width exclusion or Lychrel claim follows.
