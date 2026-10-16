# Primary-source audit and one constructive transfer lead

Date: 2026-10-13. Research task: finite decimal Lychrel existence. No decimal
existence proof was obtained or found in the sources inspected. This is a
bounded literature search, not an exhaustive bibliographic assertion.

## 1. Decisions useful to the current work

1. Do not cite the 2024 probabilistic paper as a proof of the usual conjecture.
2. The exact-length modular saturation argument has substantial earlier
   special cases; avoid a novelty claim for the coprime-modulus case.
3. The full all-moduli exact-length support characterization was not found
   explicitly in the checked primary literature. This does not establish
   novelty, and support existence is weaker than equidistribution.
4. The constructive transfer worth retaining is an exact **multivariate
   run-length Presburger certificate**, allowing a union of parameter regions
   and switching branches. This extends the archived single-parameter affine
   ray search. A finite seed and closed safe region have not been found.

## 2. Audited decimal proof claims

### Rostand S. Kuitche, 2024

*Lychrel Numbers in Base 10: A Probabilistic Approach*, Advances in Pure
Mathematics 14, 667-694, DOI 10.4236/apm.2024.148037.

Primary PDF:
https://www.scirp.org/pdf/apm2024148_45302477.pdf

Web retrieval references: turn85view2, turn86view5; HTML turn86view1.

Section 3.3, printed pp. 678-680, replaces the ordinary definition with a
probability threshold below 10^-330, justified by floating-point underflow.
That cannot establish probability zero or a deterministic orbit's
nontermination. Independently, the derivation of Theorem 4 bounds eventual
first-hit probability by one later first-hit probability. Eventual hitting is
a union over times, so its probability is at least each constituent event's
probability, not at most. The uniform-random numeral estimate for a specified
length is also applied to a deterministic orbit without a proved sampling
law. The numerical limit about 0.414 is based on replacing orbit frequencies
with ambient frequencies. The conclusion is therefore not a proof under the
standard finite-integer definition.

### Ait abida, Sghiar, Sghiar, and Sghiar, 2017

*Brisure De Symetrie Et Nombres De Lychrel*, IOSR-JCE 19(1), 91-94,
DOI 10.9790/0661-1901019194.

Primary PDF:
https://www.iosrjournals.org/iosr-jce/papers/Vol19-issue1/Version-1/M1901019194.pdf

Web retrieval reference: turn91view0.

The proof of Theorem 1 infers eventual reversal symmetry from a physical
force-cancellation analogy. No implication from cancellation to an orbit
hitting a palindrome is proved. More directly, Corollary 1 asserts eventual
palindromicity for every element of the enlarged domain containing N, while
Corollary 2 asserts a nonterminating orbit in N under the same map. Its
justification for the latter is that deleting certain reverse strings breaks
equilibrium. Deleting unused states does not alter any iteration starting in
N because the stated reverse-add map already maps the enlarged domain into N.
Those assertions cannot supply a consistent proof of decimal existence.

### Prior-audit sources, rechecked for status

Ando's February 2026 primary repository expressly describes its result as
conditional and leaves digit non-degeneracy unproved:
https://github.com/nkc-daiki/196-carry-asymmetry
(turn80view1).

Its one-step pair-sum criterion is already in this project's archive. The
archived `continuation_literature_findings.md` also gives a counterexample to
the paper's marginal non-degeneracy-to-joint-independence inference. No new
positive bridge was obtained by reusing that result.

Brown's constructive notes are genuine sources for patterned solutions in
other bases and finite decimal quasi-cycles, but do not give finite decimal
closure:
https://www.mathpages.com/home/kmath312/kmath312.htm (turn85view0),
https://www.mathpages.com/home/kmath602/kmath602.htm (turn85view1).
Their fixed inner/outer periodic construction is already covered by the
archive's searches, so it is not the new lead selected below.

## 3. Exact-length modular saturation: prior-art boundary

### Banks-Hart-Sakata (2004)

*Almost All Palindromes Are Composite*, Mathematical Research Letters 11,
853-868; arXiv:math/0405056.

Primary source: https://arxiv.org/pdf/math/0405056

Retrievals: turn96view1, turn99view2 (Proposition 4.2, PDF p. 9).

Let P_L be base-g palindromes with precisely L digits. Proposition 4.2 states
that for q>=2, gcd(q,g(g^2-1))=1 and L>=10+2q^2 log q,

    | #{n in P_L : n == a mod q} - #P_L/q |
       < (#P_L/q) exp(-L/(2q^2))

for every residue a. In particular, all residue classes contain a palindrome
of **each** length above that threshold. For g=10 this covers gcd(q,990)=1.
Exact-length existence in that range is established prior art, not merely
an inference from infinitely many palindromes in an arithmetic progression.

### Sylvain Col (2009)

*Palindromes dans les progressions arithmetiques*, Acta Arithmetica 137,
1-41, DOI 10.4064/aa137-1-1.

Primary PDF:
https://www.impan.pl/shop/en/publication/transaction/download/product/83451

Retrievals: turn99view0, turn100view3.

Theorem 1 strengthens the uniform distribution range but retains
gcd(q,g^3-g)=1. Its elementary method uses the mirrored-place-weight identity

    g Phi_N(k+1) - Phi_N(k) = (g^2-1) g^k,
    Phi_N(k) = g^(N-k)+g^k.

The fixed-length pseudopalindrome analysis is developed in Section 3.
This source does not state the desired arbitrary-modulus support theorem.

### Onphaeng et al. (2024)

*Exact Formulas for the Number of Palindromes in Certain Arithmetic
Progressions*, Journal of Integer Sequences 27, Article 24.4.8.

Primary PDF:
https://cs.uwaterloo.ca/journals/JIS/VOL27/Phunphayap/phun7.pdf

Retrievals: turn99view1, turn101view0, turn101view1, turn101view3.

Theorems 7 and 9 count palindromes up to a specified bound for b==0 or 1 mod q.
Differences of such counts give exact-length special cases. Section 4 leaves
distribution for b not congruent to -1,0,1 modulo q, with
gcd(b(b^2-1),q)>1, as an open question. This is a question about distribution,
not evidence that the weaker eventual support theorem is new. General
products and prime powers involving 2,3,5,11 are not covered as one explicit
support theorem by these sources.

I did not locate an explicit earlier statement of the proposed full-modulus
odd/even exact-length saturation result or its consequence excluding a safe
invariant based only on value congruences and digit length. The conclusion
should be labeled an independently derived lemma unless a broader novelty
search is performed. The modular agent owns the derivation and validation.

## 4. Selected constructive transfer: multivariate run domains

### Primary inspiration and its limit

Johann Thiel, *On RATS Sequences in General Bases*, Integers 14 (2014), A50:
https://math.colgate.edu/~integers/o50/o50.pdf
(turn93view0, turn94view1).

The proof of Theorem 4.3 constructs growing digit blocks by deriving and
solving a system for their independent multiplicities, rather than guessing
one numerical orbit. RATS includes sorting; neither its divergent examples
nor its existence theorem transfer to ordinary reverse-add. The transferable
method is solving exact count relations with a large free block parameter.
Below is a sorting-free extension of that method to the project's exact q
coordinate, with multiple independent count parameters and branch domains.

### Exact piecewise-affine run theorem

Fix a finite symbol list s=(s_1,...,s_r), 0<=s_i<=18, with adjacent symbols
different. Consider the q word

    Q(n) = s_1^n_1 ... s_r^n_r, n_i>=1.

Restrict to symmetric words with positive outer q and even middle q when
the width is odd. Then the exact q update G is representable by a finite
partition of the integer n-domain into regions given by linear integer
equalities/inequalities, on each of which:

* the output run symbol list is fixed;
* every output run length is an integer affine function of n;
* at most 4r+1 output runs occur before adjacent equal runs are merged.

Proof. Carry through each constant input run is independent of its positive
length. A q=9 run transmits its entering carry; every other q resets it at
its first digit. Thus that run emits at most two constant digit pieces:
one first digit of length 1 and one stable digit of length n_i-1. Include
the final leading carry if present. There are at most 2r+1 pieces, whose
boundaries are integer affine in n. Reflected boundaries are affine too.
Partition the n-domain by their finite possible orders, including equality.
On each region, the overlay of the digit word and its reversal consists of
at most 2(2r+1)-1=4r+1 constant-sum intervals. Interval lengths are differences
of affine boundaries. Remove zero intervals and merge adjacent equal ones.
All decisions have linear guards. This proves the statement for every
finite length, without sample extrapolation.

### Fully worked decimal branch

For independent integers a,b>=1, superscripts denoting repetition,

    Q(a,b) = 16^a 2^b 16^a,
    D(Q)   = 6 7^(a-1) 3 2^(b-1) 6 7^(a-1) 1,
    G(Q)   = 7 14^(a-1) 9 4^(b-1) 9 14^(a-1) 7.

The displayed D is least-significant digit first. Its ends are 6 and 1,
so the numerical reverse-add output is nonpalindromic for all a,b>=1.
All Q(a,b) are realizable decimal pair-sum words because their symbols are
even and their outside sum is positive. The formula was independently
checked for all 10,000 pairs 1<=a,b<=100; the preceding run-carry calculation
is the arbitrary-parameter proof. This family is an algebraic control, not
a claimed persistent candidate.

### Concrete certificate target

Choose a finite catalogue of q run symbol lists s_lambda. To each associate
a Presburger-definable domain D_lambda of its independent positive lengths
(e.g. a finite union of integer polyhedra with parity conditions). Compile
every exact G branch by the theorem. Verify:

1. At least one domain contains a canonical realizable integer q word.
2. Every admitted symbol list avoids the two exact next-palindrome patterns.
3. Every guarded branch maps its admitted domain into the union of admitted
   output domains.

For a fixed proposed catalogue and fixed domains, these obligations are
decidable Presburger sentences. A positive result yields an actual finite
seed: realize any admitted Q, perform its first reverse-add, and induct on
closure. No period, common growth vector, or fixed affine ray is required.
Strict growth of positive integer reverse-add makes an additional growth
condition unnecessary.

This changes the archived one-parameter condition

    G^p(Q_k) = Q_(k+1)

to a finite union of count regions, allowing switches between branches and
interacting run lengths. It also allows constraints such as a>=b, which
need not define a regular language of folded q words, so it is not simply
the existing DFA synthesis in another notation.

Missing work: no closed safe run-domain catalogue was synthesized, and no
finite seed is certified. There is no claim that bounded run structure can
capture a decimal Lychrel orbit. The new item is the exact compiler theorem
and a concrete larger certificate class, not a result on decimal existence
or a claim of publication-level novelty.

## 5. Citation handoff

The parent must reopen any primary URL it cites. The relevant web reference
IDs above belong to this research task and were provided for retrieval
convenience. No third-party commentary is needed for the substantive claims.
