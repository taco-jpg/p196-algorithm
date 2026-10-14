# Collision pass: exact regeneration, missing return

No finite decimal Lychrel witness, all-time safe family, or proof for 196
was obtained. The positive result is a new exact two-parameter collision
and mass-regeneration gate. Its later return remains unproved. These
identities have exact arithmetic checks, not Lean formalizations.

All q words are ordered from the low decimal end. G is the ordinary
reverse-and-add update on symmetric digit-pair sums. A superscript is a
run length. Every displayed parameter is finite.

## 1. A twelve-step compression identity

For every integer M >= 6, put

    Q_M = 9^2 · 18^M · 9^2.

Then exactly

    G^12(Q_M) = 9^7 · 18^(M-5) · 9^7.

The twelve overflow flags are

    1,1,0,0,0,0,1,0,1,0,1,0.

Both words have q mass 18M+36. The identity moves mass into the outer
neutral bands; it does not itself increase digit sum. Every intermediate
ordinary integer is nonpalindromic. A central 18 run survives throughout,
and the checker also directly exhibits an unequal mirrored output-digit
interval at every transition.

The tempting immediate repetition fails exactly. For every M >= 6 let

    W = (8,17,7,12,13,9,9,5,6,11,1,10).

The next twelve-step calculation is

    G^12(9^7 · 18^M · 9^7) = W · 18^(M-5) · reverse(W).

Its outer coefficient is 8, so it is not another three-run word of the
form 9^K · 18^L · 9^K. This excludes only this immediate twelve-step
iteration, not a later variable-time return.

At the exhausted edge M=5, the literal canonical seed 999999900 reaches
q=9^14 at step 12 and the palindrome 99999999999999 at step 13. Thus
reservoir exhaustion cannot simply be declared safe.

## 2. Exact collision followed by genuine mass regeneration

For independent integers M >= 8 and N >= 7 define

    S_(M,N) =
      9^2 · 18^5 · 9^2 · 0^N · 9^2 · 18^M
          · 9^2 · 0^N · 9^2 · 18^5 · 9^2.

The two short outer 18 reservoirs disappear in exactly twelve steps:

    G^12(S_(M,N)) =
      9^14 · 0^(N-5) · 9^7 · 18^(M-5)
           · 9^7 · 0^(N-5) · 9^14.

The thirteenth step has no overflow and creates two new 18 reservoirs:

    R_(M,N) := G^13(S_(M,N)) =
      18^14 · 0^(N-6) · 1 · 9^7 · 17 · 18^(M-7)
            · 17 · 9^7 · 1 · 0^(N-6) · 18^14.

The q masses are

    S_(M,N) and its step-12 state: 18M+288,
    R_(M,N):                       18M+540.

The ordinary digit sum therefore increases by exactly 126 at the
regeneration step. The two newly created maximal 18 runs each have
length 14; they replace old outer runs of length 5 after a genuine
collision. The surviving central reservoir protects the entire segment.
The identities cover every independent M,N in the stated domain, not
only pairs sampled from a line or a finite box.

This is a positive collision component. It is not a return to S or R
with increasing parameters. In particular, fixed-time reuse cannot be
inferred by treating the surviving long central 18 run as replenished.
From phase R_(M,N), a return to either displayed phase with a new
central parameter M'>M must first destroy the inherited central run,
by the previous long-run nonexpansion lemma. Its length at phase R is
M-7, and no update removes more than two inherited positions. Such a
return needs at least ceil((M-7)/2) further steps before that destruction.

## 3. Exact verification

`orthant_runs.py` represents a length as

    c + a*k + b*l,    k,l >= 0 independently.

Every used run-order comparison is certified by nonnegative coefficients.
A parameter-dependent ordering raises an error. `reservoir_gate.py`
derives all displayed states and clocks without expanding parameterized
words. It also normalizes actual output digits and exhibits a
positive-length interval on which mirrored output digits differ, giving
all-parameter safety through the stated finite segments.

`independent_gate_check.py` checks all 37 transitions by sparse carry
polynomials. It imports neither the normalizer nor its run alignment.
If C records outgoing carries and D includes the possible overflow digit,
it verifies D=Q+(x-10)C, followed by exact polynomial reflection. Affine
exponents are compared algebraically. This independent check uses no
parameter samples for the identities.

There are also 3,538 independent literal-integer transition controls,
including odd/even central lengths, both independent parameters, and
larger values. The exhausted-reservoir palindrome is checked directly.
The C++ discovery engine also passes 106,301 literal decimal transitions
from 6,507 valid q words in `check_rle_search.cpp`; its result is saved in
`check_rle_search.json`.

Run the exact checks with

    python reservoir_gate.py
    python independent_gate_check.py

## 4. Completed discovery searches and precise limits

The C++ searches use exact integer run lengths and decimal carries.
They stop on a palindrome output or at the explicit horizon. No horizon
or absence of a match is promoted to an all-time impossibility theorem.

| Search | Scope | Result |
|---|---|---|
| One uniform band with two boundary symbols | All 6,498 words a·x^256·b·b·x^256·a, a=1..18 and x,b=0..18; 160 steps | 585,096 transitions; no repeated RLE digit skeleton |
| One additional outer boundary symbol | All 123,462 corresponding words a·z·x^256·b·b·x^256·z·a; 240 steps | 20,905,129 transitions; four two-occurrence skeleton matches, all the twelve-step identity or its next phase; no three-occurrence translation |
| Smaller uniform bands through collisions | All 6,498 words each at M=8 and M=16; horizons 256 and 320 | 912,101 and 1,161,500 transitions; no repeated skeleton |
| Three-band returns | K=1..128, central 18 length 10,000; horizon 24K+128 | 214,528 transitions; the only return to 9^K'·18^M'·9^K' is K=2 at time 12 |
| Multiple alternating reservoirs | M=256, 1,709 distinct words; and M=32, 1,617 distinct words; up to nine symmetric domains, horizon 400 | 668,872 and 632,072 transitions; all skeleton matches are phases 0→12 or 1→13; no repeated translation cycle |
| Regeneration family S/R | Every M=8..64 and N=7..64, starting at exact phase R, through absolute time 16(M+N)+64 | 3,950,670 transitions; no return to S or R, and no later word using only coefficients 0,9,18 after inherited-center death |

The precise multiple-reservoir width alphabets are in the JSON summaries.
The wider 240-step scan originally logged only three-occurrence matches;
the separate 64-step rerun saved all four two-occurrence records in
`wide64_candidates.jsonl`, agreeing with the full scan's total count.

In the focused S/R search, every inherited central 18 run was destroyed,
at absolute times between 14 and 107. Every run later produced another
central coefficient 18, but these finite events did not yield either
parameterized gate form. No tested S/R orbit produced a palindrome within
its horizon. None of these finite observations establishes an infinite
nonpalindromic orbit.

The unresolved positive obligation is an exact variable-time return,
possibly with more phases or parameters, that both rebuilds the usable
reservoir structure and certifies safety throughout each collision phase.
The present files supply the collision and genuine mass increase but
do not supply that return.
