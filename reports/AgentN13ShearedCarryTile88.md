# Agent N13: a two-ended 88-phase carry-cut macro-tile in base 10

Labels: **COMPUTED** for the fully enumerated finite arithmetic experiment; **PAPER PROOF** for the elementary conditional local-carry lemma below; **UNDECIDED** for whether the boundary contract can be closed for all time. No infinite decimal Lychrel certificate or Lean theorem is claimed.

## Decimals, coordinates, and the prior constructive data

Use the same two 10400-digit decimal seeds of `AgentN13DecimalShearedFront22` and `AgentN13ShearedDigitGlider88`. Both are generated self-contained from phase-zero 39-position rooted exterior and 20-position periodic lattice (`PATH` and `CYC` embedded in the C++ and Python sources). Seed A is unperturbed; seed B has the last 100 lower-half pair coefficients replaced by `(7*j+11)%19` and reflected to the other half. For every time t, `f(t)` is their first differing lower-half paired-coefficient position. Both are independently iterated with literal base-ten `N -> N+reverse(N)`.

Write `d_t[j]` for the decimal digit at least-significant-first index j and `P_t[j]=d_t[j]+d_t[n_t-1-j]`. Carry input is `c_t[0]=0`, `c_t[j+1] = [P_t[j]+c_t[j]>=10]`. This is the actual normalization carry during the next reverse-and-add step, not an independent local automaton introduced by assumption.

At each time t define the four carry positions for the paired strip `f(t)+[-100,74]`, using `n=n_t`:

* Low incoming gate `L_in = c_t[f(t)-100]`.
* Low outgoing gate `L_out = c_t[f(t)+75]`.
* High incoming gate `H_in = c_t[n-1-(f(t)+74)]` (carry moving toward higher absolute digit indices).
* High outgoing gate `H_out = c_t[n-(f(t)-100)]`.

Compute each gate for BOTH Seed A and Seed B, thus eight bits at every time. The *high* carry is not generally the same on the two orbits because it has traversed the differing central region. This matters: a one-sided exterior carry pattern alone does not close a two-sided digit window.

## New computed temporal contract

For every integer t=1000..20000, calculate all eight gate bits from a full decimal carry scan and compare them against the corresponding gate at t-88. **All eight agree in each of the 19,001 comparisons**, for a total of **152,008** checked bit equalities and zero violations. Independently verify that the window front moves `f(t)=f(t-88)-20`, its two digit arrays gain 44 digits, and the complete digit-window source and target coincide as shown in the preceding `AgentN13ShearedDigitGlider88` result.

The measured phase-0..87 eight-bit gate table is committed as `calculation/new_structures/agent-N13/carry88.csv`. Gate column order: `lowA, lowB, highA, highB, lowEndA, lowEndB, highEndA, highEndB`; the phase origin is time t=1000. In exactly **49 out of 88 phases** the high incoming bits of orbit A and B differ. Therefore the contract is nontrivial: an internal perturbation affects the high-side carry schedule, yet its whole moving boundary state is 88-periodic in the finite test. The low incoming bits are equal between orbits, consistent with their common outer prefix.

The primary C++17 checker performs full ordinary base-ten digit-list iteration through step 20000, recomputes carries from scratch and compares all eight bits to a ring of 88 previous states. The independent Python script constructs both starting integers from pair coefficients and uses native arbitrary-precision `int` reverse-and-add through step 2000. It independently rebuilds the carry state from the decimal representation, checks 8*1001=8008 carry equalities on t=1000..2000 and produces its own 88-row phase table. Both table outputs are byte-identical to `carry88.csv`. No C++ step function or external seed data is imported into the Python checker.

Reproduce in any checkout of the repository:

```sh
bash calculation/new_structures/agent-N13/carry_tile_run.sh
```

The runner compiles `carry_tile.cpp`, asserts the full 20,000-step primary tally, runs `carry_tile_independent.py`, compares the two 88-row outputs byte-for-byte, and compares both to the committed `carry88.csv`. Success is printed only as `AGENT_N13_88_PHASE_CARRY_TILE_REPLAY_PASS`.

## Conditional two-ended carry-cut lemma (PAPER PROOF)

**Lemma.** Fix a base b and two digit configurations X and Y of equal length n. Suppose that for a pair of reflected blocks with lower indices in a..b0 and upper indices in n-1-b0..n-1-a: (i) corresponding digit pairs of X and Y are equal in both blocks, (ii) their carry inputs at lower block index a agree, and (iii) their carry inputs at upper block index n-1-b0 agree. Then the output digits obtained by ONE full reverse-and-add operation agree positionwise on both corresponding blocks, and the two outgoing carry states at positions b0+1 and n-a are equal. The assertion holds independently of every digit outside the blocks, conditional on the two incoming carry equalities.

**Proof.** For each source block, the normalized output digit at position i is `(X[i]+X[n-1-i]+c[i]) mod b` and next carry is `floor((X[i]+X[n-1-i]+c[i])/b)`. For i increasing from the block's left endpoint, the two input digit pairs and incoming carry coincide. Induction on i therefore gives identical output digit and next carry throughout the block, including at its right endpoint. Repeat the same induction on the reflected high block. Since the high block's incoming carry is supplied explicitly, the arbitrary uninspected centre has no influence on this conditional statement. QED.

This lemma is a precise finite local transition rule for **two-ended carry gates**, unlike a rule that retains only pair sums and neglects high-side carries. It is a possible building block for a finite-state glider certificate whose time/space translated edges close under genuine carry-boundary contracts.

## Remaining obstruction and next search direction

The computations DO NOT show that the eight gates will continue to self-generate with this schedule after step 20000, nor that the paired strip survives indefinitely without reaching the exterior. At the observed velocity the defect still moves outward. To prove a decimal Lychrel orbit, one needs a *closed* macro-tile whose outside carries follow from a finite periodic source and an inward / replenishing interface that sustains the exterior without bounded spatial exhaustion. Precisely those exterior-source and opposite-moving front contracts are the next constructive targets. No negative existence conclusion is drawn from their current absence.
