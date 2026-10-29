# Agent N29: exact algebraic (geometric-series) word certificates

**PAPER PROOF** (soundness theorem for a proposed new format). **COMPUTED** (base-10 positive finite-edge control and deliberate counterchecks). No infinite base-10 certificate found or claimed.

## Word format, new distinction from spatial lattice checks
Let b>=2 be fixed; a template `T(q)` is an **arbitrary ordered concatenation** of literal base-b words and repetitions `w^(a*q+c)`, with integer `a>=0`, signed integer `c`, parameter `q>=q0>=0`. Require all counts nonnegative, the first digit of the resulting word nonzero **for every q in the domain**, and nonempty templates. There is no symmetry requirement, centre, fixed spatial period, carry itinerary, or bounded defect. Different repetitions may have independent slopes a. The parameter is shared but affine widths can differ. End-of-cycle parameter substitution is `q -> q+gain`, with `gain>=0`.

Set `X=b^q`. The length-m repeated word w (numeric value v) with repeat count `k=a*q+c` has

`val_b(w^k) = v*(b^(m*c)*X^(m*a)-1)/(b^m-1).`

If `F` is the value of the already read prefix and `G` the next segment value of length `k*m`, then appending the segment maps `F -> F*b^(m*c)*X^(m*a)+G`. Hence `val_b(T(q))` is a rational-coefficient polynomial `F_T(X) in Q[X]` with explicitly computable coefficients, despite arbitrarily long repetitions. Reverse the entire segment order and each segment's word, yielding `T^R` and `F_(T^R)(X)`. Leading zeros in this reversed string do not alter its integer value.

## Finite certificate criterion (proof)
Let T0,...,T(p-1) satisfy the domain conditions and `gain>=0`, and let `T_p(q)=T_0(q+gain)`. Suppose for every 0<=i<p,

`F_(T_i)(X)+F_(T_i^R)(X)=F_(T_(i+1))(X)`

as **identical rational polynomials**, and every T_i(q) is nonpalindromic for all integer q>=q0. Then **for every** q>=q0 the base-b orbit from T0(q) never reaches a palindrome. Proof: substitute X=b^q to get each exact real integer reverse-add edge; after p steps the parameter advances by gain, remaining >=q0. Induct over macrocycles. This can be turned into a Lean checker using Q-polynomial equality, string semantics for `w^(a*q+c)`, and one geometric-series lemma; **no Lean proof was produced**.

## Fully decidable all-q nonpalindrome check (proof)
Form `D(X)=F_T(X)-F_(T^R)(X)`. If D is identically zero, every T(q) is palindromic, so reject. Otherwise multiply by the lcm of its coefficient denominators, factor out `X^k` at the smallest nonzero exponent, leaving an integer polynomial `P(X)` with constant coefficient `c0 != 0`. If T(q) is palindromic, `P(b^q)=0`. Since b^q is a positive **integer root** of P, the elementary constant-term divisibility lemma gives `b^q | c0`, hence `b^q <= abs(c0)`. So it is enough to check the finite set `q0 <= q <= floor(log_b(abs(c0)))` exactly; if there are no such q, nonpalindromicity is automatic. This is a complete arithmetic decision procedure within the format, not sampling or a numerical root bound.

## Base-10 constructive control
For every q>=3 the following six words are a **five-edge positive chain** (not a closing cycle):

`T0=12 9^q 34`,

`T1=569 9^(q-2) 855`,

`T2=1128 9^(q-2) 820`,

`T3=1418 9^(q-3) 8031`,

`T4=2727 9^(q-3) 6172`,

`T5=5444 9^(q-3) 3444`.

All five reverse-add transitions are exact identities in Q[X]. None of these six words is a palindrome for any q>=3, established by the integer-root test. The source also runs genuine base-10 integer controls q=3,4,5,12,1000 and checks two deliberate failures: corrupt T2's last digit and assert that a false q+1 cycle is rejected.

Reproduce with `python3 calculation/new_structures/agent-N29/geometric_checker.py`; the program uses only the Python standard library. `geometric_control.json` stores the control sequence and exact checker output.

## Constructive next direction
Use the polynomial identity checker as a backend for synthesis: unknown literal boundary digits and repetition slopes lead to **coefficient constraints** rather than exponentially large integer words. Seek non-palindromic closing cycles first with two unequal affine bands and freely moving packet boundaries, then with alternating 0/9 bands and terminal q-growth. Unlike the previous bounded-centre exclusions, this tests the *possibility* of a new centre-free algebraic orbit. Whether a decimal closing cycle exists is **UNDECIDED**.
