# Agent N08: exact palindrome preimages of regular folded pairword languages

## The gap closed (PAPER PROOF; every length, not a horizon)

N08's earlier folded-regular certificate `AgentN08FoldedRegular` used the
sufficient safety condition that every pairword contain an odd coefficient.
This discards genuinely non-palindromic normalized successors with *only even*
coefficients. This report replaces the guard with an **exact** finite-state
condition, with no odd-coefficient restriction.

Let b>=2. Let P=(p_0,...,p_(n-1)) be a symmetric coefficient word with
0<=p_i<=2b-2 and p_i=p_(n-1-i), written least-significant first, whose
middle coefficient is even if n is odd. The canonical integer represented
by P is val_b(P)=sum p_i b^i. When P is a valid pairword of a positive
integer N, val_b(P)=N+rev_b(N), exactly.

Fold P as (h,z), where h is the list of floor(n/2) coefficients from the
outer end inwards, and z=None for even n or the centre coefficient for
odd n. The folded input alphabet is finite.

**Theorem 1 (regular palindrome preimage).** The set of valid folds
(h,z) for which val_b(P) has palindromic *normalized digits* is a regular
language, for each fixed integer b>=2, including both choices of n parity
and the possible extra overflow digit.

Proof: Use a nondeterministic digit-normalization transducer with state
(a,u,v): lower carry a, upper carry *leaving* the current outer column u,
and previous upper normalized digit v (sentinel -1 before the first column).
Initially (0,gamma,-1), gamma in {0,1}. When reading symmetric coefficient
p, guess the carry c entering the upper copy of p and require
floor((p+c)/b)=u. Put l=(p+a) mod b, a'=floor((p+a)/b),
r=(p+c) mod b. Update to (a',c,r). For gamma=0, require l=r,
since these are mirrored normalized digits. For gamma=1, require
l=1 for the first pair (extra most-significant overflow digit), and
l=v at every subsequent pair (upper partner shifted by one).

At an even-length terminal require a=u. With gamma=1 the last upper
normalized digit is the central output digit, requiring no equality.
At an odd-length terminal with centre coefficient z, require z even
and floor((z+a)/b)=u, and define mid=(z+a) mod b. With gamma=0,
mid is the central digit (no further equality); with gamma=1 require
mid=v, or mid=1 when the input had length one. These conditions are
exactly ordinary base-b normalization in both directions. Carries
belong to {0,1} because p<=2b-2. Therefore finitely many states
recognize precisely the palindrome-output preimage. Finite languages
are closed under product/intersection with any source DFA; emptiness
is ordinary finite graph reachability. QED.

**Theorem 2 (strengthened all-time certificate criterion).**
Let L_0,...,L_(q-1) be folded-regular languages of valid pairwords, and
choose a positive non-palindromic decimal integer N_0 with
P(N_0) in L_0. If the two exact folded normalization transducers give
T_(b,0)(L_i) union T_(b,1)(L_i) subset L_(i+1 mod q) for each i,
and every L_i has *empty intersection* with the palindrome-output
preimage of Theorem 1, then all iterates N_t are non-palindromic.
Indeed P(N_t) in L_(t mod q) by inclusion, so N_(t+1)=val_b(P(N_t))
is non-palindromic by the exact guard. Induction handles arbitrarily
many cycles. This criterion is strictly weaker than the original
odd-pair guard, because it directly tests normalised output digits.

## Strict decimal witness, exact for ALL m>=1 (not an orbit certificate)

Take the palindrome coefficient word
P_m=[2,4,12] ++ [0]^m ++ [12,4,2], m>=1.
The digit carry identities give the *exact* normalized digit list,
least-significant first,
  digits(val_10(P_m)) = [2,4,2,1] ++ [0]^(m-1) ++ [2,5,2].
Thus the first and last normalized digits both equal 2, while the
next outer pair is 4 versus 5. The output is non-palindromic for
EVERY m>=1; a test that only inspects the outer digits would miss it.
All pair coefficients are even, so the previous N08 odd-pair criterion
fails on every P_m.

A genuine source integer for every m is
  N_m = 2*10^(m+5) + 4*10^(m+4) + 6*10^(m+3) + 600.
Its pairword is exactly P_m, so the displayed identity describes a
real decimal reverse-and-add step. The source and successor are
nonpalindromic, but **no later iterate is certified** by this family.

The regular fold-language for all m is recognized by the four-symbol
path 2,4,12 followed by any number of zeroes: terminal centre 0 is
allowed immediately; even-length terminal None requires >=1 zero.
The product with the finite palindrome-normalization transducer is
empty for both overflow branches: for gamma=0 the palindrome-equality
constraint fails at the second outer pair; gamma=1 fails at the first.
This is an *unbounded-length finite computation*.

## Machine-checked computation and independent controls

Run:
  python3 calculation/new_structures/agent-N08/exact_palindrome_guard.py

The script constructs the exact product automaton; checks its emptiness
for the entire decimal regular family, and finds a positive witness in
the comparison palindrome family [2]++[0]^m++[2]. It compares the finite
palindrome-preimage algorithm with independent ordinary digit arithmetic
on 34,993 valid singleton folds (bases 2,3,4,10,13 and n<=6) including
the single-digit gamma=1 corner case. Additional ordinary integer checks
of N_m are sanity controls, **not** the justification of the all-m fact.
The all-m fact follows from Theorem 1 and the displayed carry identity.

## The remaining single missing lemma

Find a nonempty **decimal** cycle of folded-regular languages L_i
satisfying BOTH the exact successor-language inclusions and the new
palindrome-output guard, with a valid starting integer. In concrete
period-8 lattice terms this is a finite-state recurrent *carry/interface
repair* that closes the centre after each clock without spending a
finite defect budget. The theorem here eliminates the unnecessary
odd-pair guard but does not prove the existence of such a recurrent
decimal repair. No Lychrel number, seed 196 result, or Lean proof is
claimed, and no finite-horizon orbit is asserted.
