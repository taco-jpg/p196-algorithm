# Decimal Lychrel existence: where things stand (2026-11-10)

A self-contained status report for a reader who starts from zero. **Nothing here proves that a decimal Lychrel number
exists, and nothing is claimed about 196.** Labels: LEAN-VERIFIED / COMPUTED / PAPER PROOF / UNDECIDED. Each item
says where it lives: *[main]* = already on `main` before this report; *[round NN]* = computed in rounds 12-14
(2026-11-05 .. 2026-11-11), code, logs and reports under `calculation/decimal_frontier/roundNN/` (see the README
there); the `results/` note named in each item states the exact claim and scope. Updated 2026-11-11.

## 0. The problem

Reverse-and-add: n -> n + rev(n) (rev reverses the decimal digits). n is a *Lychrel number* if its orbit never
contains a palindrome. 196 is the smallest decimal candidate. In bases 2, 4, 8, 9, 11, 13, 16, 17, 20, 26, 32 Lychrel
numbers are proved to exist, with Lean proofs. **In base 10 not a single Lychrel number is known.** The aim is one
finite, checkable *certificate* that some decimal number is Lychrel (not necessarily 196).

## 1. Basic objects (digits least significant first)

1. **Pair word.** For the digit word x_0 ... x_{L-1} of n, the uncarried sum n + rev(n) has entries
   P_i = x_i + x_{L-1-i} in 0..18. P is a palindrome, so half of it (the *folded* pair word) carries all information.
   One step = normalise P with carries, read off the new digits, form the next pair word.
2. **Two carry streams.** In the folded picture every column sees an upward carry (from the low end) and a carry from
   its mirror position. This coupling is what makes the dynamics non-trivial.
3. **Overflow.** When the top carry creates a new digit the length grows by 1 (gamma = 1, else 0); the fold point moves
   by half a column (*frame shift*). The *clock* of a structure is its overflow sequence g in {0,1}^p.
4. **Certificate.** A template, e.g. `number = B ++ band(W, l) ++ C ++ mirror`, such that after one or more steps the
   number has the same shape with a longer band (l grows) and one of finitely many phases. A finite closed cycle of
   such edges, checked once, holds for every band length, so the orbit is non-palindromic for all time.
   Sound checkers in Lean (for every base):
   - neutral-band format: `Agent120.Neutral.cycleOK` with `lychrel_of_cycle`; Python mirror
     `calculation/neutral_band_search.py` (its selftest re-accepts the eight known certificates, bases 2, 4, 8, 16, 32,
     11, 17, 26);
   - lattice-band format: `lcycleOK` with `lychrel_of_lcycle` (`lean/P196/LatticeBand`); base-9 instance |W| = 4,
     |B| = 61, overflow word 1100011000, 10 edges, LEAN-VERIFIED (`reports/REPORT_LATTICE_BAND.md`);
   - `CertificateToLychrel`: any return certificate accepted by the checker yields a Lychrel number.

## 2. The two known mechanisms in base 10

**A. Neutral band.** Exterior B + a run of 9s (a *9-wire*, it only passes carries) + centre C. B evolves on its own and
sends two bit streams (carry e, overflow gamma) to the centre, which sees nothing else. Certificate = a B-cycle and a
C-cycle with the same streams.
- Decimal exteriors, periods <= 24 *[main, COMPUTED]*: only p = 11 (g = 11100010000, e = 10100110011, |B| = 29) and
  p = 12 (g = 100010001000, three streams, |B| = 52-53). Base 10 needs Sigma gamma >= 4 per cycle (all known
  certificates of other bases have 2).
- Centres *[main, COMPUTED + PAPER PROOF reduction, `results/NeutralBandNoCapAllPeriods.md`]*: for every exterior the
  census found (overflow periods <= 32), no centre of any width or time period sits on the 9-wire, and no converter
  caps the streams. The neutral-band route is closed inside the census. Not covered: capped dense clocks such as
  (01)^12, (01)^16, 00001110001100010000111000110001.

**B. Lattice / absorbing band.** The band is a space-time periodic lattice W (time period = clock period, space period
m); absorbing = both incoming carries give the same outgoing carry. A self-mirror lattice with m | S needs no centre
(bases 9 and 13, LEAN-VERIFIED). Base 10 *[main, COMPUTED]*: no reachable self-mirror lattice with m | S for any
period <= 24 that the automaton decides (such lattices exist as orbits, reachability is the obstruction). So a decimal
lattice needs a periodic *centre* ("kink") between the lattice and its mirror: task K1.
Decimal lattices: clock 10101010 (period 8): the big strongly connected component (SCC) of the interface graph, every
closed walk a lattice, basic ones rec0 (m = 20), rec1, rec2 (m = 48); clock (0001)^3 (p = 12): lattice p12m9 (m = 9);
clock 1000 (d = 12): left tail W0 (m = 9) and 9-wires.

## 3. What is excluded

1. **Tool: window relaxation, all periods at once** (PAPER PROOF; r12g, r13b, round 14). Keep the bottom K cells of a
   centre above the frame, everything higher free (free carry, free top digit): a finite graph R_K. A state is
   *accepting* if its bottom cell is off the lattice. Cyc_acc(K) = states on closed walks through an accepting state;
   projection lemma Cyc_acc(K) <= Cyc_acc(K-1) x {0..18}. Theorem A: if Cyc_acc(K0) is empty and the exact fold map
   F_K has no periodic orbit inside Cyc_acc(K) for K < K0, the lattice has no centre of any time period and any depth
   in that phase orbit. Positive control: the 8 Lean-verified neutral certificates reappear as exact orbits.
2. **p11 / p12 9-wires and the clock-1000 tail W0** *[per-tail closures: main; completeness: round 14,
   `P11P12PeriodicLeftPartsNoCentre`]*: on clocks 00001110001 (d = 11) and (1000)^3 (d = 12) every d-periodic rooted
   history ends in a 9-wire or in W0 = p12m9, and the all-period closure dies at K = 6 on each of them (C++ and plain
   Python agree): no d-periodic left part carries an eventually periodic centre. *[main]* p12m9 has no bounded-width
   centre; *[round 13, `P12M9SlowFrameDepth6`]* boundaries with drift 0 < d <= 1/8 cannot reach depth 7 (drift 0 open).
3. **Centres of the period-8 lattices (K1).**
   - *[main]* rec1 centres |C| <= 16 and p8 fixed centres <= 12 excluded.
   - *[round 13, `P8FixedPeriodCentresAnyDepth`]* no centre of period 80 for rec0, rec1, none of period 192 for rec2,
     any depth.
   - *[round 12, `P8CentreDepthBound`]* no centre of depth <= 23 on rec0, rec1 and of depth <= 27 on rec2, any period.
   - *[round 12, `P8FixedCentrePeriods160to576`]* no fixed-centre return at periods 160..480 (rec0, rec1, |C| <= 12-13)
     and 384, 576 (rec2, |C| <= 11-12).
   - *[round 14, `P8SccLatticesNoCentreAllPeriods`]* big-SCC lattices with cycle length 61..159: 55 of the 83 classes
     are closed for all periods (K0 = 16..39); no exact orbit anywhere; 28 classes budget-limited (UNDECIDED). Family
     closure (all of the big SCC except rec2 at once): no centre of exact depth <= 21; K = 22 exceeded 75 GB.
   - *[round 14, r14b, no results note]* K1 for all periods: no centre found; rec0 orbit 0 still has accepting states at
     K = 19 (8 of 80 phases): UNDECIDED. Lemma H (healing offsets +-5 at g = 0, +-9 at g = 1, PAPER PROOF). r14b's
     band-anchored closures disagree with an independent main-session program (cause not found): UNDECIDED.
   - *[round 12, `T12NoTemplateReturn`, PAPER PROOF + COMPUTED SAT]* the T12 route (P(q,k) = B0 W0^q J U^k C mirror)
     has no template return Phi^(120m) P(q,k) = P(q,k+5m) for any m, q, J, C (k >= 90m+10).
4. **Infinite closed L-histories (ICH) on dense overflow clocks (task E2).** For a clock word of period L: is there an
   L-periodic column structure (interface I = forward carry c, digit below xb, allowed backward carries A) that
   extends upward forever? Above a fixed interface J, a *tower* is a chain J -> J1 -> J2 ... of L-periodic interfaces,
   each arrow a closed L-column; a tower dies (finite) or contains a cycle (an ICH, a positive lead). Theorem B (r13c,
   PAPER PROOF) reduces each word to finitely many towers.
   - *[round 13, `BirthTowersT16T55`]* (00010010111)^5 (T = 55): no ICH (1,240,956 towers, deepest 345); every closed
     16-history of (01)^8 is 8-periodic.
   - *[round 14, `IchTowersT24T32T40T56`]* clock 01: every ICH of period 24 (max level 3309), 32 (16 heavy towers,
     max 17714, tree DFS only) and 40 (max 1670) is 8-periodic. Root-14 word, T = 56: no ICH (last tower dies at 742,
     one method). Clock 0001 at L = 60: tower N60_1 dies at 464, N60_2 still running.
     *[main]* (01)^12 has no exterior and no uniform band at T = 24.
5. **Uniform bands on left ends** *[main, COMPUTED under premise (B), now a PAPER PROOF for 9-wire streams]*: no
   periodic left end with combined period T <= 32 carries a uniform absorbing band, except the 9-wire streams of
   (24, 01) and (32, 01).
6. **Band census and band centres** *[round 13, `BandCensusS8ErosionGA`, `BandCentresClock1000T24`]*: 265 / 284 / 161
   bands of word length <= 8 for clocks 1000 / 10 / p11. Band centres DO exist: bands (11,8,5) with C = (13,2,13) and
   (13,10,7) with C = (5,16,5) of clock 1000 grow V^m C rev(V)^m -> V^(m+1) C rev(V)^(m+1) every 24 steps; among
   bands with T <= 400, 73 / 113 / 58 carry exact centre orbits. The obstruction is the junction: no census band with
   T | d has a rooted d-periodic left end (d = 8, 11, 12). "Band + centre" exists; "left end -> band" is missing.
7. **Exterior census** *[main: periods <= 24 (560 streams skipped by a 127-bit key) and 33..40; round 12,
   `ExteriorPeriods41to56`: 41..56, open words listed there; `ExteriorUniquenessP9P11m`: clock (0001)^9 carries only
   N12, clocks p11^m (m <= 5) only p11]*.
8. **Not worth redoing.** Prefix exclusions (5,808 of 9,000 four-digit prefixes are excluded in Lean, but they can never
   prove existence); finite-horizon replays; more exclusions for their own sake.

## 4. What is still open (this is the problem to solve)

1. **K1 remainder.** rec0, rec1 centres of depth >= 24 and rec2 of depth >= 28 at periods other than 80 / 192; the
   28 budget-limited big-SCC classes;
   lattices of cycle length > 160 beyond depth 21. Computation grows fast here: a structural theorem, an invariant or
   a transfer-matrix argument is needed, not a bigger run.
2. **K2 wall speed.** Prove or refute: the defect front between lattice and mirror moves at most c cells per step, so a
   bounded centre never closes. A proof kills the period-8 route; a counterexample is a centre.
3. **Remaining towers and words on dense clocks** (E2): clock 01 at T = 48 (heavy towers not run); clock 001010101 at
   L = 54 (tower CAP54a) and clock 0001 at L = 60 (tower N60_2), both running; the open exterior words of
   `ExteriorPeriods41to56` (p34, (01)^20 as an exterior question, N12^4, (01)^24, (01)^28, ...). A tower with a cycle
   gives a new periodic structure: a positive lead.
4. **Band centres beyond the scan**: timed-out bands (121 / 145 / 51 for clocks 1000 / 10 / p11) and all bands with
   T > 400. Even then the left-end junction is missing (3.6).
5. **New formats (F1), the most promising direction.** The decimal pieces exist (left ends: p11 / p12 9-wires, W0;
   period-8 lattices; bands with centres) but do not fit together periodically. A format with a non-time-periodic
   junction is needed: a moving wall (left end + wire + wall moving relative to the fold + band + centre + mirror; an
   exploratory SAT scan at K = 24 with small wall periods, the W9 tails of clock 1000 and p11 against all census bands,
   found 0 solutions in 16,570 decided instances, 151 timeouts; not a census, nothing claimed), two or more bands, or a periodic band with a
   quasi-periodic centre. Prove soundness in Lean, recover a known certificate in another base (control), then search
   base 10. Known facts for the moving wall: the first off-wire cell is >= 10 when the wire stream bit is 0 and <= 8
   when it is 1; the wall can move only at g = 0 steps, with value 14 or 4. Read the existing moving-seam work first
   (`results/X45MovingSeamPhaseLock.md`, `R08MovingSeamShield.md`, `Z45*`, `AgentN01*`, `N09*`).
6. **Exterior census E1** beyond the covered periods (and the 560 skipped streams at p <= 24): every new exterior
   is a new neutral-band or lattice candidate.
7. **F2 families**: a parametric certificate for infinitely many bases, Lean-proved for all parameters. Not decimal by
   itself, but it may show the structure base 10 lacks. Bases 7, 19, 22, 25 have none for overflow period <= 12.

## 5. What a certificate must come with

The full edge data; acceptance by the Python mirror; a big-integer replay as a sanity check; `cycleOK 10` /
`lcycleOK 10` closed by `decide` in Lean without `sorry`, custom axioms or `native_decide`; an independent second
check (V1). A certificate proves that *some* decimal Lychrel number exists; it says nothing about 196.
