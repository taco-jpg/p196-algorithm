# Q09: Exact carry-column symmetry centralizer

**PAPER PROOF (all radices b >= 2).** This classifies *universal columnwise* automorphisms of the coefficient-to-digit/carry normalizer, not arbitrary context-dependent symmetries, and is NOT a decimal Lychrel certificate.

Let A={0,...,2b-2}, D={0,...,b-1}, C={0,1}, and T_b(p,c)=((p+c)%b, floor((p+c)/b)).
Let a:A->A, d:D->D, k:C->C be bijections satisfying, for EVERY p in A and c in C,

    T_b(a(p),k(c))=( d(first(T_b(p,c))), k(second(T_b(p,c))) ).

**Theorem:** exactly two triples exist:
1. identity a(p)=p, d(r)=r, k(c)=c;
2. complement a(p)=2b-2-p, d(r)=b-1-r, k(c)=1-c.

**Exhaustiveness.** k is either identity or the flip. With k=id, use inputs (p,c)=(r,0),(r,1) for every 0<=r<=b-2. Both original outputs have carry 0, so a(r)=d(r), a(r)+1=d(r+1). Thus d(r+1)-d(r)=1. Bijectivity forces d(r)=r. The identity for (p,0) now uniquely fixes a(p)=p, including p>=b.

With k(c)=1-c, the same two inputs originally have carry zero, hence the transformed carry is one: a(r)+1=d(r)+b and a(r)=d(r+1)+b. Thus d(r+1)-d(r)=-1. Bijectivity forces d(r)=b-1-r. Substituting into (p,0) uniquely determines a(p)=2b-2-p (for p<b and p>=b separately). Direct substitution checks both triples for all p,c. QED.

**Exact all-length consequence.** For any P=(p_0,...,p_{n-1}) with each p_i in A, and either incoming carry c, normalize from low to high. Complementing EVERY p_i and flipping the incoming carry transforms EVERY output digit y_i into b-1-y_i and the final carry into its complement, by induction on n. Conversely, no other fixed letterwise relabeling and carry-state bijection can have this *universal* intertwining property.

**Physical-root necessary condition.** In ordinary radix-b reverse-and-add the carry entering the least significant pair column is always ZERO. The unique nonidentity local automorphism requires that carry to be ONE in its complemented copy. Therefore complement is not a commuting symmetry of the physical rooted reverse-and-add map. Any all-time template certificate whose cycle closure identifies two phases through such a nontrivial columnwise relabeling must provide an explicit carry-inverting boundary junction, verify its input/output port states, and show that junction regenerates on every positive-growth cycle. Quotienting by complement without this repair is unsound. This is a necessary condition only: an all-time regenerative decimal junction is still UNDECIDED.

**Whole-string centralizer within the stated elementary classes.** For a single fixed digit permutation pi acting on ALL canonical positive decimal strings while preserving length, pi(0)=0 is necessary (otherwise some nonzero leading digit maps to zero). If pi commutes with F(n)=n+rev_10(n), the one-digit input 5 gives 2*pi(5)=10*pi(1), so pi(1)=1 and pi(5)=5; inputs 1,2,4,3,6,7,8,9 then fix all other digits. For S=rev_10 after pi, one-digit inputs 1,2,4 force pi(1)=1, pi(2)=2, pi(4)=4, pi(8)=8, but input 5 requires 2*pi(5)=pi(1)=1: impossible. This excludes all nonidentity global zero-preserving digit-permutation symmetries, with or without reversal.

Reversal alone satisfies F(rev_10(n))=F(n) when 10 does NOT divide n, but does not commute: F(rev_10(19))=110 while rev_10(F(19))=11. Similarly multiplication by 10^k (k>=1) fails at n=1: F(10^k)=10^k+1, versus 10^k F(1)=2*10^k. Fixed additive shifts F(n+c)=F(n)+c would require rev(n+c)=rev(n) for every sufficiently large n; choose an n for which n,n+c have equal length and nonzero units and use injectivity of reversal there, forcing c=0. Nine's complement is not a global length-preserving canonical operation; even where defined it fails on n=5: F(4)=8, whereas complement_2(F(5)=10)=89.

Swapping the two digits within any chosen mirrored input pair leaves its *one-step* F value unchanged: the sum depends only on pair coefficients p_i=x_i+x_{n-1-i}. These are one-step F-fiber symmetries, not commuting symmetries of iterates, and folding to pairwords is already used elsewhere in this repository. A new decimal proof must supply the periodic carry-port repair, not another quotient by these fibers.

**Missing lemma for an all-time decimal result:** construct and verify a canonical base-10 finite growing edge cycle carrying a complementary carry-inverter boundary from one phase back to itself, for every symbolic band length m>=m0, with every phase nonpalindromic. No such cycle is exhibited here.
