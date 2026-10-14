# Continuation with finite residue defects

No parameterized all-time safe family or finite decimal Lychrel witness was
obtained. The calculation allows the wall parameter to change and does not
discard states when their residue budgets differ from 18.

Let Q_m=V_m reverse(V_m), as in the preceding constructive report, and let
q_t(m)=G^t(Q_m). For a proposed positive integer modulus D define

    B_t,D(j) = sum(q_t(m)[i] : i == j mod D),
    E_t,D(j) = B_t,D(j)-18,
    A_t,D = sum_j |E_t,D(j)|.

The defect E is a necessary correction to any balanced Delta_D wall.
Its support and absolute charge quantify a finite-defect proposal without
requiring the correction to be zero. Increasing D is explicitly allowed.

## The small defect does not form a closed menu

The exact affine calculation covers every m>=256, through 128 updates. It
contains no sampled integer orbit used as a proof. At C=6m+3, the defects
immediately after the known delayed repair are:

| time | nonzero E(j) |
|---|---|
| 12 | E(1)=E(2)=1; E(4)=E(C-1)=-1 |
| 13 | E(1)=E(2)=2; E(4)=E(C-1)=-2 |
| 14 | E(0)=E(3)=-1; E(1)=E(2)=23; E(4)=E(C-1)=-4 |

Thus the four unit errors double, then acquire a new carry event and two
extra sites. At time 15 the defect occupies twelve sites and has absolute
charge 120. This defeats the proposed four-site repair packet directly;
it is not a claim that every larger finite defect alphabet is impossible.

Changing D cannot improve the following charge minima. These are global
minima over **every positive integer D**, separately for every m>=256:

| time | minimum A_t,D | unique minimizing D | support there |
|---|---:|---|---:|
| 11 | 58 | 6m+3 | 5 |
| 12 | 4 | 6m+3 | 4 |
| 13 | 8 | 6m+3 | 4 |
| 14 | 56 | 6m+3 | 6 |
| 15 | 120 | 6m+3 | 12 |
| 16 | 80 | 6m+3 | 10 |
| 32 | 104 | 6m+3 | 22 |
| 64 | 274 | 6m+3 | 38 |
| 128 | 514 | 6m+3 | 76 |

Why the minimization is exhaustive: the total q mass is 18(6m+c_t), so

    A_t,D >= |sum q_t - 18D| = 18 |D-(6m+c_t)|.

An explicit charge upper bound from D=6m+3 restricts every improving D
to a finite interval. Each member of that necessary interval is folded
symbolically, including all parameter-dependent lengths. Values outside
the interval lose by the displayed inequality. This also covers choices
D depending arbitrarily on m: pointwise they must lie in the same finite
set of offsets from 6m.

No exact q-family identity q_b(m)=q_a(m+r), for any integer r, occurs among
the 129 symbolic phases. No nonzero defect-budget profile repeats by such
a parameter shift either. The zero-budget phases 0 through 8 and 10 are
the already known balanced interval and delayed repair. These finite-time
facts do not prove that defect charge diverges forever or exclude every
larger menu of defect types.

## Why a fixed-time growing affine cycle cannot retain these long bands

Here is a structural obstruction beyond the finite calculation. It applies
to the proposed family with its long 18 bands, not to all decimal orbits.

Consider a maximal q=18 interval of length M, with neighboring coefficients
different from 18. At a nonoverflow step, each strict interior column has
both incoming carries equal to one and stays 18. The two endpoint columns
are 17 or 18, except that a length-one interval can disappear. If an
adjacent outside coefficient becomes 18, that coefficient must have been
8 with incoming carry one from each side. It therefore sends carry zero
into the old interval, forcing that old endpoint to become 17. Consequently
the surviving descendant cannot extend into, or join, an outside 18 run.
Its length is M, M-1, or M-2, when positive.

At overflow, the M-1 positions combining two neighboring old 18 columns
are exactly 18. A boundary position combines one old 18 with a neighboring
x!=18. For it to equal 18, both component digits would have to be 9.
The digit from x, entered from the 18 side, equals 9 only if x=8; but 8
sends carry zero into the 18 column, making its digit 8. This contradiction
excludes both boundary positions. Thus the descendant has exactly M-1
symbols, and is again separated from every outside 18 run. Physical outer
endpoints after overflow have pair sum at most 10 and cannot extend it.

Therefore a surviving long 18 run never expands or merges; it loses at
least one position per overflow and at most two per step.

Suppose an affine run family R_m has r>0 unbounded maximal 18 runs, all
with positive slopes, and a fixed-time identity

    G^p(R_m) = R_(m+g),       g>0,

holds for every sufficiently large m. Choose m large enough that all r
old long runs survive the p steps. They have r distinct long descendants.
The target has exactly r long 18 runs, so those descendants must be all
of them. Their total length cannot exceed its old value (and decreases
at each overflow), whereas increasing m by g increases the total length
by g times the positive sum of their slopes. Contradiction.

The same argument applies after following a finite menu of bounded-time
phases around one complete cycle. It is insensitive to a relabeling of C
or a bounded collection of defect symbols. In Q_m itself, the first update
already creates two maximal 18 runs of length 2m-1. A fixed-time return
to the original Q family, which has no 18 coefficient, is impossible for
the simpler reason that those runs survive for sufficiently large m.

A growing return must therefore destroy at least one old long run before
re-entering the same affine phase. Because at most two positions disappear
per step, that requires a return time at least half the length of the
shortest old long 18 run, hence proportional to m. A variable-time
collision and regeneration could still evade this obstruction. No such
regeneration equation was found. The observed defect support and run types
grow through the currently derived collision approach, so they do not
provide the required bounded finite phase description.

## Independent verification and scope

`symbolic_defects.py` uses the existing exact affine-run carry operations.
`optimal_defect_charge.py` performs the exhaustive modulus minimization.
`independent_polynomial_check.py` does not use either run normalizer or
residue folder. It instead checks the carry-polynomial equations

    h=0: Q' = 2Q + (x-10)C + (x^-1-10)C*,
    h=1: Q' = (1+x)Q + (x-10)C + (1-10x)C*,

as formal finite sums whose exponents are affine functions of m. It checks
all 128 transitions and 5,046 residue-budget families for every m>=256.
Reduction modulo x^D-1, together with equality of total coefficient sums,
independently verifies the residue budgets. No finite sample establishes
an all-parameter equality. The separate local column controls in
`long_run_check.py` supplement the arbitrary-length proof above.

These are exact symbolic calculations and a written obstruction proof,
not Lean formalizations. The lower parameters m<256 are outside this
symbolic horizon claim; no finite witness is claimed at any parameter.
