# Maximal growth forces a specific boundary clock

Research notes. No decimal Lychrel number is established. No claim of novelty is made.

## Exact projective map

Let n have L decimal digits, m=n+rev(n), and let h be the change in digit length, either 0 or 1. Let c_i be the carry entering column i in the least-significant-first addition, with c_0=0, and put

    K = sum_{i=1}^L c_i 10^(L-i),
    x=n/10^L, y=rev(n)/10^L, kappa=K/10^L.

Then the normalized pair after one step is exactly

    x'=(x+y)/10^h,
    y'=x+y-(99/10)kappa.

This follows from rev(m)=m-99K/10 when h=0, and rev(m)=10m-99K when h=1. The carry coordinate kappa is a finite decimal whose digits are 0 or 1; it remains coupled to the digits of n. Treating it as independent would discard the decisive constraint. A trapping region has not been found.

## A finite potential controls expansion

Write a for the sum of the outermost mirrored digits, so 1<=a<=18. The exact possibilities for the next a and the overflow h are:

    1<=a<=8: a'=2a or 2a+1, h=0;
    a=9: (a',h)=(18,0) or (10,1);
    10<=a<=18: a'=a-9, h=1.

Define psi on a=1,...,18 by

    [0,0,0,1,0,1,1,1,2,1,1,1,2,1,2,2,2,3].

Every allowed edge satisfies

    2h-1 <= psi(a)-psi(a').

Consequently, for H(t)=L(T^t(n))-L(n),

    2H(t) <= t+psi(a_0)-psi(a_t) <= t+3.

The only cycles attaining mean overflow 1/2 in this graph are 8->17->8 and 9->18->9.

More strongly, suppose the digit-growth deficit t-2H(t) is bounded above. Each edge has nonnegative integer slack

    s_t=psi(a_t)-psi(a_{t+1})-(2h_t-1).

The partial sums satisfy

    sum_{j<t} s_j=psi(a_0)-psi(a_t)+t-2H(t).

These sums are bounded, so only finitely many s_t are positive. Eventually the orbit follows only zero-slack edges. The zero-slack graph has just the two cyclic strongly connected components above; a one-way path can connect the first to the second, but an infinite path must eventually stay in one component.

## The 9/18 clock is impossible indefinitely

The outer-two-pair quotient eliminates the 9/18 component. Let b be the second mirrored digit sum and u in {0,1} the incoming carry from deeper inside at the second most significant column. Set

    l=floor(a/10), r=floor((b+u)/10), h=floor((a+r)/10).

For h=0,

    a'=a mod10+(a+r) mod10,
    b'=(b+l) mod10+(b+u) mod10.

For h=1,

    a'=a mod10+1,
    b'=(b+l) mod10+(a+r) mod10.

These are exact for length at least two. Allowing both u values can only enlarge the set of genuine trajectories.

For a=9 followed by 18, one must have b<=9. To continue 9->18->9->18, the initial b must be 0 or 4: the intermediate b at a=18 must be 0 or 9, as follows directly from the displayed formulas. After the first two steps, however, b is 8 or 9. Neither can be 0 or 4, so a second overlapping three-edge block cannot occur. Thus five consecutive alternating transitions are impossible. The maximum is four; the abstract initial state (a,b)=(9,4) achieves this.

Therefore every actual reverse-and-add orbit with bounded maximal-growth deficit must eventually obey

    a_t=8,17,8,17,...

(up to a phase shift). This is a necessary condition, not a constructed orbit. Such a permanent clock would itself ensure nonpalindromic steps: at the a=8 phase the next a=17 requires an interior carry, while at the a=17 phase the exceptional 0/11 palindrome predecessor is impossible. The missing issue is a finite seed maintaining this clock.

This condition is relevant to a one-decimal-digit-per-binary-digit embedding of the known binary 22 orbit: that orbit gains two digits per four steps, so a length-preserving embedding with bounded overhead would necessarily maintain the decimal 8/17 clock eventually.

## Why a permanently protected 18-core does not work

Consider a symmetric q-word P 18^m reverse(P), where the last digit of P is not 18 and m>0. The maximal central run has length m. At an overflow step its new length is exactly m-1. At a no-overflow step it is either m or max(0,m-2). This follows by inspecting the columns on the two edges of the run; the interior outputs remain 18, and the new boundary output at an overflow is strictly below 18.

Hence an initially finite, unchanging central 18-core cannot survive indefinitely. There are infinitely many overflow steps on every positive orbit: n strictly increases at each reverse-and-add step and so is unbounded. This rules out this particular protected-core construction, not a variable core, a regenerating core, or a Lychrel number.

The accompanying Python script verifies the finite potential inequalities, checks 32,485 core transitions, and exhausts the 38-state 9/18 two-pair abstraction. Its checks support the implementation; the arguments above explain the unrestricted claims. These notes have not been formalized in Lean.

## Follow-up: changing the base4 encoding clock

The centered encoder of base4 digits is E(d)=d+3. Source annuli with mirrored sum3 therefore become decimal annuli with mirrored sum9. This cannot escape the previously investigated neutral-annulus construction. Encoding mirrored annuli with opposite orientations instead gives mirrored sum6 or12; these alternate under the uniform bulk rule. This is a different candidate.

A fixed six-step family with the q-core growing by two would change its q-digit sum by12. Since decimal reversal preserves digit sum modulo9 and 2^6=1 modulo9, that fixed return is impossible. A three-phase eighteen-step return growing the core by six passes this necessary check: the sum changes by36 or72, both divisible by9.

Preserving the source base4 overflow clock 001 is nevertheless impossible in decimal. At the outer-pair level it permits only the periodic clocks

    2,5,11   or   3,6,12.

The first has no live state in the exact width-two prefix graph. The second forces the second-pair clock2,4,9; its width-three graph has no live states. The alternative six-step outer clock1,3,7,14,5,10 is also eliminated at width two. These are exact finite abstractions with arbitrary incoming interior carry, so the exclusions do not depend on a bound on total digit length.

I therefore enumerated all58 cyclic outer-q walks of period18 containing six overflows, without preserving the source clock. Four survived the width-three prefix graph and three survived width four. Their overflow segment lengths (ending at each overflow) are:

    [5,2,2,3,2,4]
    [4,1,4,1,4,4]
    [4,1,4,4,1,4].

Each was tested against q-core6 and q-core12 return templates. All six width-eight templates were UNSAT. At width16, the two templates for the first clock were UNSAT; the other four timed out and are recorded as UNKNOWN. These are bounded-template results, not general impossibility claims.

Next, I switched to the exact backward spatial carry graph instead of increasing the prefix bound. The target was an actual digit core3 or6 whose digits alternate3,6 under addition, with identical incoming and outgoing carry streams at each time phase. The target's spatial self-loop was checked before exploring predecessors.

For segment lengths[4,1,4,1,4,4], the backward graph closed completely at14,464 states for each core phase, without reaching the required exterior. For[4,1,4,4,1,4], it closed at14,400 states for each core phase, also without reaching the exterior. These completed exclusions apply to the stated digit-interface ansatz, allowing arbitrary interface width.

For[5,2,2,3,2,4], the extended searches reached111,489 states for core3 and101,332 for core6 before their eight-second limits. Both remain INCOMPLETE. Neither found an exterior path. This is the remaining concrete candidate class from this bounded investigation; no candidate seed was found.

The prefix-update implementation was also compared against full reverse-addition on2,880 randomly generated numeral/prefix cases. The prefix rule is an exact digit-column identity; the check is implementation validation.

## Reproduction and dependencies

Python3 is sufficient for the finite graph and core checks:

    python3 novel_projective_core.py
    python3 novel_projective_clock.py
    python3 novel_projective_period18_clocks.py

`novel_projective_period18_clocks.py` generates the width-two/three/four clock results, pruning each clock when its live set becomes empty.

The SMT searches require the Python z3-solver package:

    python3 novel_projective_base4.py
    python3 novel_projective_base4_irregular.py

The irregular search reads `novel_projective_period18_clocks.json`, retaining the three clocks whose final recorded prefix check is live.

The backward graph script uses the existing exact spatial graph modules `continuation_theory_multigrowth.py` and `continuation_theory_graph.py`:

    python3 novel_projective_base4_backward.py

The extended first-clock results are stored in `novel_projective_base4_backward_clock0_extended.json`. Reproduce them with `backwards(10,[5,2,2,3,2,4],target_for(periods,d),maxstates=300000,seconds=8)` for d=3 and6. Runtime-limited state counts can vary between machines.

None of these computations establishes a decimal Lychrel number. None of this follow-up has been added to the Lean formalization.
