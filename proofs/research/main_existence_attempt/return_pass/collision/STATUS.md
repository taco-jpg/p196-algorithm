# Arbitrary-motif collision coordinates and the first failed return

No closed recurrent family, all-time palindrome-avoidance proof, or finite
decimal Lychrel witness was obtained. The positive result is an exact
variable-time **zero-gap collision identity**, valid after the inherited
18 reservoirs have died. It uses arbitrary finite motifs over all nineteen
pair-sum coefficients. A length argument then excludes its most immediate
parameter-changing return. Other later or rescaled returns remain open.

All words below are low-to-high symmetric digit-pair sums. Reverse-and-add
is continued even when a component, or a whole integer, is palindromic;
palindrome avoidance is a separate obligation.

## 1. An exact arbitrary-word separation law

Let A and B be nonempty symmetric words over 0,...,18, each with positive
end coefficients. Let a=|A|, b=|B|, and n>=1. Normalize each word using
ordinary decimal carries starting at zero:

    normal(A) = (d_A,h),     normal(B) = (d_B,k),

where d_A and d_B retain their input lengths and h,k are the final carries.
Define E_A=d_A followed by a final 1 if h=1, and define

| h | k | E_B | delta |
|---|---|---|---:|
| 0 | 0 | d_B | 0 |
| 0 | 1 | 0 · d_B · 1 | 1 |
| 1 | 0 or 1 | d_B · k | 1 |

Set A'=E_A+reverse(E_A) and B'=E_B+reverse(E_B), where addition here is
coefficientwise, and delta=max(h,k). Then exactly

    G(A · 0^n · B · 0^n · A)
      = A' · 0^(n-delta) · B' · 0^(n-delta) · A'.          (1)

There are no restrictions on internal motif alphabets, periods, or run
lengths. Both new motifs again have positive end coefficients. In fact,
if the first coefficient x of B is below 9, k=0 and its new end is 2x
or x; if x>9, k=1 and the new end is 1 or x-9; and x=9 gives a positive
end in every case. The same argument applies to A'. Thus the zero gaps
remain the exact gaps between these three motifs, without hidden zero
prefixes or a trimming convention.

Proof of (1): zero gaps reset carries. If h=k=0, the actual output digits
are

    d_A · 0^n · d_B · 0^n · d_A.

If h=0,k=1, they are equivalently

    d_A · 0^(n-1) · (0 · d_B · 1) · 0^(n-1) · d_A.

If h=1, they are

    (d_A · 1) · 0^(n-1) · (d_B · k)
                    · 0^(n-1) · (d_A · 1).

Reflecting each of these literal digit concatenations proves (1). It also
proves the exact safety test: the next whole integer is a palindrome if
and only if **both** E_A and E_B are palindromes. A palindrome in the
outer component alone is allowed. This statement is valid even at n=1,
when the new gaps disappear.

## 2. A finite variable-time collision for every gap parameter

Start with the earlier reservoir family, now written

    A_0 = 9^2 · 18^5 · 9^2,
    B_0(M) = 9^2 · 18^M · 9^2,
    S_(M,N) = A_0 · 0^N · B_0(M) · 0^N · A_0.

Iterate the arbitrary-word law on (A_t,B_t), and put

    K_0=0,       K_(t+1)=K_t+delta_t,
    H_0=0,       H_(t+1)=H_t+h_t.

Here A_t is exactly the ordinary pair-sum orbit of the finite seed
999999900; B_t(M) is the companion driven by its overflow clock. The
motifs and K depend on M and t, but not on N. Their lengths are exactly

    |A_t| = 9+H_t,
    |B_t(M)| = M+4+2K_t-H_t.

Let

    tau_M(N) = min { t : K_t=N }.

This time exists for every finite positive N. Indeed, K_t>=H_t. The
ordinary outer integer strictly increases, so its digit length, and
hence H_t, cannot remain bounded. Also K increases only by zero or one.
For every t<=tau_M(N), repeated application of (1) gives

    G^t(S_(M,N)) =
        A_t · 0^(N-K_t) · B_t(M) · 0^(N-K_t) · A_t,

and in particular the exact variable-time collision identity

    G^tau_M(N)(S_(M,N)) = A_tau · B_tau(M) · A_tau.        (2)

Equation (2) does not leave an infinite spacer or a reservoir assumed to
survive forever. The two finite zero gaps have actually vanished.

For M=8, the inherited central 18 run dies at time 14. The 18 runs
regenerated in the outer components die at time 42, where K_42=22.
Consequently every N>=23 has its zero-gap collision **after both kinds
of inherited 18 reservoir have disappeared**. These death times and
K_42 are exact finite arithmetic calculations, and (1) makes them
independent of N while the gaps remain.

Some exact collision values for M=8 are:

| N | tau_8(N) | length A_tau | length B_tau |
|---:|---:|---:|---:|
| 7 | 14 | 15 | 20 |
| 16 | 30 | 22 | 31 |
| 23 | 44 | 29 | 38 |
| 24 | 46 | 30 | 39 |
| 32 | 60 | 36 | 49 |
| 64 | 123 | 64 | 85 |
| 128 | 245 | 117 | 160 |
| 240 | 482 | 208 | 293 |

The full nineteen-symbol motifs, without a guessed periodic reduction,
are saved in `motif_collision.json`.

## 3. The zero-gap boundary changes the recurrence

For a word W, write normal_c(W) for normalization with incoming carry c.
At the collision state C=A·B·A, the exact next digit word is obtained by

    (X,c_1) = normal_0(A),
    (Y,c_2) = normal_c_1(B),
    (Z,gamma) = normal_c_2(A),
    D = X · Y · Z, followed by 1 if gamma=1.

Then G(C)=D+reverse(D). The seams now pass carries; they no longer reset
them through a zero digit. This is the exact boundary law implemented by
`collision_step`, with both incoming-carry variants allowed.

There is an all-word obstruction to simply continuing the companion
motifs. If delta=0, then h=k=0, the seams transmit zero, and exactly

    G(A·B·A) = A'·B'·A'.

If delta=1, the independent target A'·B'·A' has length

    2a+b+2+h,

whereas the actual next q word has length 2a+b+gamma. Hence

    |A'·B'·A'| - |G(A·B·A)| = 2+h-gamma >= 1.            (3)

Thus the proposed next phase is impossible, for **every** choice of
arbitrary motifs at an active seam step. The actual final carry gamma
must not be silently replaced by h. For example A=9^2 and B=18 have
h=0, k=1, gamma=1; the actual next q is (10,9,8,8,9,10), while the
independent target is (18,18,1,16,1,18,18). The deficit is one there.

This also excludes a natural variable-time, parameter-changing return.
Define C_(M,N)=A_tau_M(N) · B_tau_M(N)(M) · A_tau_M(N). Between
tau_M(N) and tau_M(N+1), all but the last companion step have delta=0.
The actual orbit agrees through those quiet steps. The final delta=1
step fails by (3). Therefore, for all finite admissible M,N,

    G^[tau_M(N+1)-tau_M(N)](C_(M,N)) != C_(M,N+1).        (4)

For M=8,N=32 the collision is at time 60, the next parameter's collision
is at time 63, and the candidate target is two digits too long after the
three actual updates. This is a genuine post-reservoir-exhaustion failed
return with unrestricted motif coefficients, not another S/R-form test.
Equations (3)--(4) exclude this specific continuation and clock. They do
not exclude later returns, different rescaling maps, or a seam-defect
alphabet that is closed under the coupled boundary law.

## 4. Finite realizability, safety scope, and verification

Every q word generated from the displayed S family is finite and symmetric, with coefficients in
0,...,18, positive end coefficients, and an even center coefficient when
its length is odd. These conditions supply an ordinary positive decimal
realization: on each mirrored pair use low digit max(0,q_i-9) and high
digit min(9,q_i), and at an odd center use q_i/2. Subsequent q identities
are identities of the actual ordinary reverse-and-add orbit.

Through time 512 the independent outer component's only palindrome
output is at time 13. The M=8 companion is not palindromic then (its
q word has coefficients 1 and 17). Thus (1) certifies safety for every
S_(8,N) through min(tau_8(N),512). The computation gives K_512=254,
so all first collisions with 7<=N<=254 lie in this certified finite
horizon. No assertion is made about simultaneous component palindromes
beyond time 512, or about continued safety after the seams interact.

Run

    python -B motif_collision.py

The checker uses 5,648 independent literal-integer controls for the
separated law and another 5,648 for the zero-gap law. They include every
positive constant two-column A, every positive even one-column B, gaps
1..4, and 5,000 deterministic longer motif pairs. It also checks selected
S_(8,N) trajectories by literal integer reversal through their collisions
and verifies their failed adjacent-parameter returns. The all-word proof
is the digit-concatenation argument above; random tests are implementation
controls, not the proof.

The exact remaining constructive obligation is to close the **coupled**
seam dynamics into a finite or morphically specified growing family and
prove palindrome avoidance throughout every repeated collision phase.
The current A_t,B_t words grow without a proved finite motif substitution.
Equations (1)--(2) reach the collision, while (3)--(4) show precisely why
the immediate independent-motif return does not close it. Neither finite
realizability alone nor arbitrarily large finite gaps establishes an
infinite safe orbit from one finite integer.
