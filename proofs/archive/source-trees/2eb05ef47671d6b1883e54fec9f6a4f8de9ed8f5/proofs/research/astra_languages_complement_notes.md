# Correlated complementary blocks and the loss of a marked defect

Status: no safe closed nonempty language and no decimal Lychrel witness.
This branch establishes exact all-length carry identities, explores a
context-free correlation rather than an uncorrelated tile abstraction, and
gives kernel-checked counterexamples to the resulting marked-defect idea.
No novelty claim is made.

## 1. A genuinely correlated language

Write `kappa(x)=18-x`, extended letterwise. For a nonempty word U of length m
over 0,...,18, define the folded word

    A(U) = ( U ++ kappa(reverse(U)) ; no center ).

Its full symmetric q word has length 4m. With s=2m it satisfies

    q[i+s] = 18-q[i]   for 0 <= i < s.

The requirement U[0]>0 gives a valid positive decimal realization. The
language remembers an arbitrarily long reverse-complement copy; its matching
relation is not supplied by independent sets of allowed local tiles. It is
recognized by a stack pushing U and checking its complementary reverse.

A(U) is a palindrome predecessor exactly when U is entirely 9. Indeed,
every matched pair has sum18, so both members are <=9 exactly when both are9.
The exceptional bad pattern with outer11 cannot occur, because the matched
7 would also have to be0 or11.

This is a safe nonempty correlated language after removing the all-nine
word. It is **not closed** under the exact update.

## 2. Exact carry-complement identity

For C(q,a)=(q+a)//10 and D(q,a)=(q+a)%10, if q+r=18 and a+b=1, then

    C(q,a)+C(r,b)=1,     D(q,a)+D(r,b)=9.

Their total input is19, so exactly one column carries and the output digits
sum9. If the incoming carries are instead both0, a pair of neutral9
symbols leaves both carries0 and produces digit sum18. The first non-nine
complementary pair repairs this mismatch: its carries sum1 and its digits
sum8. All later complementary columns then have the ordinary sum9.

These identities, and induction through any finite number of columns,
are proved in `astra_languages_complement.lean`. In particular, when a
half-complementary word has carry1 at its halfway point, every pair of
half-shifted output digits sums9 and its final overflow is0.

## 3. Complete first-step relation for A(U)

Assume U is not all9, and let k be the first index with U[k]!=9.

If U[k]<9, the halfway carry is1 and the final carry is0. Therefore the
output digits have complementary halves, and taking mirrored sums shows
that G(A(U)) is again an A word of the same size. In particular, this covers
every U[0] in1,...,8, and also the outer9 case whose first non-nine symbol is
low. The complete folded reverse-complement correlation is preserved.

If U[0]=9+x is high, so 1<=x<=9 and k=0, the halfway carry is0 and the
final carry is1. The exact output has the form

    B(x,V) = ( [x] ++ V ++ [9] ++ kappa(reverse(V)) ; 18-2x ),
    |V|=m-1.

Proof: write the first-half output digits as e[0],...,e[s-1]. The second
half is their digitwise complement except its first digit: the paired digit
sum there is8 rather than9. Hence for 1<=i<s,

    q'[i] = 9 + e[i] - e[s-i],
    q'[i]+q'[s-i] =18,
    q'[m]=9.

The outer q' symbol is e[0]+1=x and its center is2*(9-x). This proves the
displayed B form without any length bound.

The remaining case is a neutral prefix of positive length k followed by a
high symbol. Put

    epsilon[i] = 9 if i<k, -1 if i=k, and0 if i>k.

The second digit half satisfies e[i+s]=9-e[i]+epsilon[i]. Consequently

    q'[0]=10,     center(q')=18,
    q'[i]+q'[s-i]=18+epsilon[i]+epsilon[s-i]  (1<=i<s).

Thus the overflow image retains an exact linked strip of pair sums27,17,
and18. The strip length is precisely the original neutral-prefix length.
In this case the output is safe because its center is18. The formula makes
explicit why the carry state at both ends of a neutral run must be retained.

## 4. Safety of B and an exact annihilation criterion

For 1<=x<=9, B(x,V) is bad exactly when

    x>=5 and every symbol of V is9.

The outer symbol is at most9, ruling out the exceptional outer11 pattern;
the center is at most9 exactly when x>=5; each complementary pair inside V
is entirely low exactly when it is9,9.

There is a useful explicit form when A(U) has no symbol9. Define

    r(u)=u-9*[u>=10].

At an overflow every non-neutral symbol fixes its outgoing carry, and exact
column addition gives q'[i]=r(q[i])+r(q[i-1]) for interior positions. Thus

    V[i-1] = r(U[i])+r(U[i-1])   (1<=i<m).

An arbitrary-length family is annihilated in one step: take U to alternate
17,10,17,10,..., truncated at any positive length m. Its reduced values
alternate8,1, so

    G(A(U)) = B(8, 9^(m-1)),

which is bad. The source has arbitrarily long, exactly matched non-neutral
blocks; their correlation alone does not stop cancellation at overflow.

## 5. Why marking one surviving defect does not close the language

The first candidate strengthening was to mark an adjacency with
r(U[i])+r(U[i-1])!=9, so that the next overflowing image would contain a
non-nine V symbol. But non-overflow steps can erase that marked defect:

    (2,3,15,16; -)
    -> (4,7,11,14; -)
    -> (8,15,3,10; -)
    -> (17,10,8,1; -)
    -> (8,9,9,9; 2),

and the final word is bad. Initially the reduced adjacency sum is2+3=5;
just before overflow it is8+1=9. Every row before overflow still has the
exact complementary-block relation. A literal numeric realization is

    23997600 -> 24677532 -> 48255174 -> 95410458
             -> 180811917 -> 899929998,

where the last integer is a palindrome.

There is also an exact internal transition for the B family: if1<=x<=4,
then G(B(x,V)) is B(x',V') with x' in {2x,2x+1}. The central high column
sets carry1; the complementary blocks transmit opposite carries, giving
the displayed new root and center relation. This holds at every width.
Nevertheless a marked V symbol different from9 can disappear in this
branch too:

    B(3,(4)) = (3,4,9,14;12)
      -> (6,9,9,9;6) = B(6,(9)),

which is bad. Its literal numeric orbit is

    349965000 -> 350534943 -> 699969996.

Both full-word q traces and their low-only terminal property are checked
by Lean's kernel. Thus no safe closed language containing either explicit
seed exists, even if it keeps these complete spatial correlations.

## 6. Verification and precise remaining obligation

`astra_languages_complement_check.py` reconstructs positive decimal integers,
performs literal decimal reversal and addition, and independently compares
the resulting q words against a small-column implementation. It checks:

- 6,858 admissible A words with |U|<=3;
- 3,237 non-overflow A transitions;
- 3,429 high-outer A-to-B transitions;
- 189 neutral-prefix overflow strip identities;
- 3,087 reduced-adjacency identities with no neutral symbol;
- 28,960 small-root B transitions with |V|<=3;
- the arbitrary-length annihilating family at m=1,...,12 as controls.

These finite checks validate implementations. The all-length statements
above follow from the carry-complement calculation, not from extrapolation.

The Lean file proves the general local and half-word carry identities and
both concrete counterexamples. The full A/B language-level identities and
the neutral-prefix strip formula are algebraic proofs in these notes, not
claimed as fully formalized Lean theorems. Axiom audits use only propext,
Classical.choice, and Quot.sound; the concrete counterexamples use only
propext and Quot.sound. There is no sorry or native_decide.

The outstanding positive obligation is a finite grammar or another exact
description of a nonempty subset with a *renewable* defect: every accepted
word must be valid and safe, and every exact image must still have an
accepted defect certificate. Such a certificate must handle all three
effects established here: cancellation of a marked adjacency under the
non-overflow branch, disappearance of a marked B symbol, and the linked
neutral-prefix mismatch strip. The A/B relations alone do not provide it.

Reproduce with:

    python3 astra_languages_complement_check.py
    ../lean-runtime/lean astra_languages_complement.lean
