# Exterior charge and quantized gains for complementary-band returns

**Status: written proofs, internally checked by Agent #2; not yet a Lean theorem about ordinary reverse-and-add. No cycle, Lychrel witness, or proof about 196 is supplied.**

Dependency: the exact complementary-band quotient in
`../2026-10-15-complementary-bulk-quotient/METHOD_AND_PROOF.md`, sections 2--6,
read at integration head `a71d6e79b009da691e2d97057f83e108a3fcff4f`.
The width-growth bound is already established in `../../research/exist_count_notes.txt`
and `DecimalWidthGrowth` in the existing formalization. The new follow-up here
applies a modular exterior charge to the returned-interface problem. No claim
of literature novelty, independent human review, or a new width-growth theorem
is made.

## 1. An autonomous exterior factor

Retain the source notation `Q(c;B,A,C;g,h)`, least-significant-first words,
`d=18-c`, and the actual overflow bit `gamma`. Put

    k = 1 if c >= 10, else 0
    t = c - 9*k
    c_next = 2*t.

Normalize `B` with incoming carry zero, obtaining `(D,e)`. Normalize
`reverse(B)` with incoming carry `k`, obtaining `(R,gamma)`. Set
`u=c+e-10*k`. The untrimmed exterior is exactly

    B_raw = (D ++ [u]) + (reverse(R) ++ [t])       if gamma=0,
    B_raw = (D ++ [u]) + ([1] ++ reverse(R))       if gamma=1.

Here `+` is coordinatewise addition. Strip the maximal suffix of `c_next`
from `B_raw`, obtaining `B_next`.

**Factor lemma.** The next exterior state `(c_next,B_next)` and overflow
are functions of `(c,B)` alone. They do not depend on `A`, `C`, `g`, or `h`,
provided the source lies in the original quotient domain `g,h>=2`.

This is a direct consequence of the actual carry resets and the two displayed
formulas. In particular, a complete acyclicity certificate on bounded exterior
states excludes returned full interfaces with that exterior bound, regardless
of the sizes or contents of the two inner blocks. Exiting a bound does not
exclude a later return through larger exterior states.

## 2. A single-band identity used only to prove the charge law

Let `b=length(B)`, `b_next=length(B_next)`. For any even `m>=2`, consider

    W = B ++ [c]*m ++ reverse(B).

This is a canonical pair word. Normalize its integer value, then take the
pair word of the resulting ordinary digits. The same exterior formulas give

    G(W) = B_next ++ [c_next]*m_next ++ reverse(B_next),
    m_next = m + gamma + 2*b - 2*b_next.

**Proof.** Before suffix trimming, the two end transients leave `m-2` copies
of `c_next` without overflow, or `m-1` with overflow. Each trimmed suffix
coefficient from either end adds two copies to the core. If `u_B` is the
stripped suffix length, `b_next=b+1-u_B`, giving the displayed formula.
`m_next>=0` follows from `m>=2` and `b_next<=b+1`. The even source core avoids
any odd-center issue even when `c` is odd; the target phase is always even.
This identity does not assert that these single-band sources are safe.

## 3. The exterior charge law modulo nine

Define the integer charge

    E(c,B) = sum(B) - length(B)*c.

For every exterior transition,

    E(c_next,B_next) == 2*E(c,B) - gamma*c   (mod 9).       (1)

**Proof.** Normalizing any coefficient word preserves its coefficient sum
modulo nine. Taking the pair word of the normalized digits doubles that sum.
Apply this to the single-band identity in section 2:

    2*sum(B_next) + (m+gamma+2*b-2*b_next)*c_next
        == 2*(2*sum(B)+m*c)                  (mod 9).

Substitute `c_next==2*c (mod 9)` and cancel the core and exterior-length terms:

    2*E_next + gamma*c_next == 4*E           (mod 9).

Two is invertible modulo nine, so (1) follows. This proof covers arbitrary
finite exteriors, including the empty exterior. Trimming introduces no
unjustified bound or periodicity assumption.

More generally, along `p` transitions with `H=sum(gamma_i)`, iteration gives

    E_p == 2^p*E_0 - 2^(p-1)*c_0*H         (mod 9), p>=1. (2)

The identity uses `c_i==2^i*c_0 (mod 9)`. Formula (2) is useful also for the
`6,12` phase family; one must not divide its phases by three modulo nine.

## 4. Overflow quantization on the six-phase family

Assume `c` belongs to `{2,4,8,16,14,10}`. These phases are units modulo nine.
Define

    J(c,B) = 2*c^(-1)*E(c,B)                in Z/9Z.

Equation (1) and `c_next==2*c` give

    J_next = J - gamma                     in Z/9Z.       (3)

Consequently a nonempty closed exterior walk has `9 | H`.
It also has `H>0`: without any overflow the positive actual exterior
coefficient evolves as `a_next=2*a+e`, with `e` a carry bit, and strictly
increases. It cannot return to its initial value. Thus every such exterior
return has at least nine overflows.

For a closed **full** quotient walk, let `Delta_g,Delta_h` be the signed
accumulated gap increments. The source's exact physical-width identity gives

    2*(Delta_g+Delta_h) = H.                              (4)

So `H` is even. Together with (3),

    18 | H,     H>=18,     Delta_g+Delta_h>=9.             (5)

This assertion does not assume coordinatewise nonnegative gains. Such gains
are an additional requirement for the persistent-cycle construction.

## 5. Each gap gain is itself a multiple of nine

For every closed full quotient walk in the six-phase family,

    9 | Delta_g,     9 | Delta_h.                         (6)

**Proof.** Its length `p` is divisible by six because its phase returns. Hence
`2^p==1 (mod 9)`. Choose finite initial gaps large enough to realize the
entire finite walk; the exact quotient formulas guarantee that this is
possible, even when some edge increments are negative. The coefficient sum
of a pair word doubles modulo nine on each actual step. At the returned
interface the only sum change is

    2*c*Delta_g + 2*(18-c)*Delta_h
        == 2*c*(Delta_g-Delta_h)            (mod 9).

It must vanish. Since `2*c` is invertible, `Delta_g==Delta_h (mod 9)`.
Equations (4)--(5) also imply `Delta_g+Delta_h==0 (mod 9)`.
Adding and subtracting these congruences proves (6).

In particular, if a qualifying nonnegative-gain return has the smallest
allowed overflow count `H=18`, its only possible gain pairs are `(9,0)`
and `(0,9)`. This is a necessary condition, not an existence assertion.

## 6. A lower bound on the return length

The pre-existing outer-growth potential, telescoped around a returned
exterior coefficient, gives `2*H<=p`. Combining this with (5),

    p>=36                                                (7)

for every nonempty closed full six-phase quotient walk. A closed exterior
walk alone has the weaker necessary bound `p>=18`.

For an independent small arithmetic check of the growth inequality, define

    a:    1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18
    rho:  3 2 2 1 1 1 1 1 1  2  0  0  0  0  0  0  0  0.

For every `a in 1..18` and incoming carry `e in {0,1}`, put
`gamma=(a+e)//10` and

    a_next=2*a+e        if gamma=0,
    a_next=(a%10)+1    if gamma=1.

The 36 cases satisfy `2*gamma-1<=rho(a_next)-rho(a)`. Telescoping on a
closed walk proves the required bound. This alternate certificate reuses
an already-known upper growth rate; it is not a new all-time theorem.

## 7. Exact scope and remaining work

These arguments restrict the quotient's possible returns. They neither
supply a returned interface nor exclude long cycles with large exteriors.
They apply to the six-phase family specifically where stated; the `6,12`
family retains only the undivided charge law (1)--(2) and other general
necessary conditions. They do not show whether the ordinary orbit of 196
enters any such returned family. Every claim of persistent safety still
requires the source's actual-map domain and coordinatewise gain conditions.

Finite controls and bounded exterior searches are reported separately.
No finite experiment is substituted for any of the all-length proofs above.
