# N08: a folded regular-language reverse-and-add certificate

## New certificate format (PAPER PROOF)

Fix an integer radix b>=2. For an n-digit integer N write its digits least
significant first as d_0,...,d_(n-1), and let its symmetric *pair word*
P(N) have coefficients p_i=d_i+d_(n-1-i) in 0,...,2b-2.
This word is a palindrome. Put V_b(P)=sum_i p_i b^i. One ordinary
reverse-and-add step is exactly N'=V_b(P(N)).

Encode any symmetric pair word by its *fold* (u,z), where
u=(p_0,...,p_(floor(n/2)-1)) runs outside-to-centre, and z=None
for even n, otherwise z=p_(n//2). This representation is a word over
0,...,2b-2 terminated with E(None) or E(z), hence can be accepted
by a standard DFA. For a valid initial integer odd n requires even z.

For gamma in {0,1} the following finite transducer T_(b,gamma) maps
folded P to folded P(N') *exactly* whenever the arithmetic overflow is
gamma. Its state is (a,z,h): the incoming low-end carry a, the carry
leaving the upper outside boundary z, and the upper digit h produced at
the previous outer pair (or sentinel -1). Initial state (0,gamma,-1).

On reading symmetric input coefficient p, guess the carry c entering
the upper copy of p. All carries are in {0,1}. Require
    floor((p+c)/b)=z.
Compute
    low=(p+a) mod b, a'=floor((p+a)/b),
    high=(p+c) mod b.
Emit low+high when gamma=0; when gamma=1 emit low+1 for the FIRST
pair, or low+h for every subsequent pair. Update (a',c,high).
The gamma=1 displacement is necessary because the overflow creates
one extra leading digit and shifts every upper partner by one place.

At the terminal E(None), require a=z. Emit E(None) when gamma=0
or E(2h) when gamma=1. At E(pmid), require
floor((pmid+a)/b)=z, put mid=(pmid+a) mod b, and emit E(2mid)
when gamma=0 or the extra ordinary pair symbol (mid+h) then E(None)
when gamma=1. There are finitely many states and at most one output
symbol beyond input length. Every successful path is a valid
normalisation, and for a given valid P exactly one of the two
gamma-transducers has a successful path, with one resulting word.

**Soundness theorem.** Let L_0,...,L_(r-1) be regular languages of
folded pair words over b>=2, with (i) at least one valid seed N whose
folded pairword is in L_0; (ii) for all phase i, and both gamma=0,1,
every successful output of T_(b,gamma) on L_i belongs to
L_((i+1) mod r); and (iii) every accepted word has an ODD pair
coefficient. Then N,N+rev(N),... contains no palindromes. Indeed,
P(N_{t+1}) belongs to the next language by the exact transducer and
induction; a palindromic N_t would have P(N_t)=2 d_i at every
position, contradicting (iii). No growth assumption is needed:
reverse-and-add strictly increases every positive integer.

**Finite checker.** DFA-image inclusion is determined by reachability
in the product (source DFA, transducer state, target DFA), where the
target DFA has a rejecting sink; check accepting source terminals
against the target terminal after the optional extra symbol.
Checking both gamma branches is essential. An odd-pair guard is
itself regular, hence DFA inclusion tests can also establish it.
All state spaces are finite independent of the word length.
A Lean sketch: induct on normalisation positions to prove the carry
relation; prove terminal correctness for both parities/gamma; define
reachable-product closure by finite graph search; prove its soundness
by induction on source word length; conclude via ordinary orbit
induction. This report claims PAPER PROOF, not LEAN-VERIFIED.

## Constructive positive control (COMPUTED + PAPER PROOF argument)

Base 2, seed N=22, P_0=11211. Its first successor is
P_1=210012. For k>=1 define full symmetric pair words
    A_k=2 1^k 00 1^k 2,
    B_k=10 1^(k-1) 202 1^(k-1) 01,
    C_k=2 1^k 020 1^k 2,
    D_k=10 1^(k-1) 2112 1^(k-1) 01.
Each is folded-regular, and the computed product graphs establish
A_k -> B_k (gamma1), B_k -> C_k (gamma0),
C_k -> D_k (gamma1), D_k -> A_(k+1) (gamma0)
**for every integer k>=1**, not merely a bounded replay.
Every phase contains a digit-1 pair coefficient, so no palindrome
can arise. The product checker visits 7,8,7,10 states, respectively;
wrong-gamma branches each have no accepted terminal. The separate
Python-bigint script checks the exact regular-language phase at
20,000 ordinary reverse-add integer steps, reaching 10,006 bits.

## Decimal exploratory test (COMPUTED, not a certificate)

A separate C++ implementation uses only ordinary decimal digits.
Seed 196 survives all 20,000 checked states, final length 8,211.
Pairwords containing an odd coefficient occur at 19,998 states;
the only failures of the odd guard occur at steps 1 and 7.
The measured overflow count is 8,208; no palindrome encountered.
These finite observations do NOT imply 196 is Lychrel and are not
an exclusion of any candidate family. The next search should infer a
**carry-coupled DFA invariant with a transient entry prefix**, not
force a naive single-letter parity guard onto the entire orbit.

## Reproduction

    sh calculation/new_structures/agent-N08/run.sh

The transducer script checks 3,230 fully enumerated palindromic words
across bases 2,3,4,10,13 and 20,000 seeded random cases (bases 2..40,
lengths 2..180) against its independent ordinary digit normalizer,
including rejection of the incorrect gamma. The regular product
checker exhausts all reachable finite states. The bigint and C++
scripts do not import the transducer. Neither the repo-wide
verify.py gate nor Lean were run in the tool environment; Git DNS
prevents obtaining the repository checkout.
